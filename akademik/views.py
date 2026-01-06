"""
Views untuk aplikasi Akademik
"""

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q

from .models import Dosen, MataKuliah, Fasilitas, JadwalKuliah, RisetGrup, Publikasi


class DosenListView(ListView):
    """View untuk daftar dosen"""
    model = Dosen
    template_name = 'akademik/dosen_list.html'
    context_object_name = 'dosen_list'
    
    def get_queryset(self):
        queryset = Dosen.objects.filter(is_active=True)
        
        jabatan = self.request.GET.get('jabatan')
        if jabatan:
            queryset = queryset.filter(jabatan_fungsional=jabatan)
        
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(
                Q(nama__icontains=search) |
                Q(bidang_keahlian__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jabatan_list'] = Dosen.JABATAN_CHOICES
        context['selected_jabatan'] = self.request.GET.get('jabatan', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context


class DosenDetailView(DetailView):
    """View untuk detail dosen"""
    model = Dosen
    template_name = 'akademik/dosen_detail.html'
    context_object_name = 'dosen'
    slug_field = 'slug'
    
    def get_queryset(self):
        return Dosen.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dosen = self.object
        context['publikasi_list'] = Publikasi.objects.filter(penulis__icontains=dosen.nama)[:10]
        context['matakuliah_list'] = MataKuliah.objects.filter(dosen_pengampu=dosen)
        return context


class KurikulumView(TemplateView):
    """View untuk halaman kurikulum"""
    template_name = 'akademik/kurikulum.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['semester_list'] = range(1, 9)
        context['matakuliah_list'] = MataKuliah.objects.filter(is_active=True).order_by('semester', 'nama')
        
        semester = self.request.GET.get('semester')
        if semester:
            context['matakuliah_list'] = context['matakuliah_list'].filter(semester=semester)
            context['selected_semester'] = int(semester)
        else:
            context['selected_semester'] = None
        
        return context


class MataKuliahDetailView(DetailView):
    """View untuk detail mata kuliah"""
    model = MataKuliah
    template_name = 'akademik/matakuliah_detail.html'
    context_object_name = 'matakuliah'
    slug_field = 'slug'
    
    def get_queryset(self):
        return MataKuliah.objects.filter(is_active=True)


class FasilitasView(ListView):
    """View untuk halaman fasilitas"""
    model = Fasilitas
    template_name = 'akademik/fasilitas.html'
    context_object_name = 'fasilitas_list'
    
    def get_queryset(self):
        return Fasilitas.objects.filter(is_active=True)


class JadwalView(TemplateView):
    """View untuk halaman jadwal kuliah"""
    template_name = 'akademik/jadwal.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jadwal_list'] = JadwalKuliah.objects.filter(is_active=True).order_by('hari', 'jam_mulai')
        context['hari_list'] = JadwalKuliah.HARI_CHOICES
        
        hari = self.request.GET.get('hari')
        if hari:
            context['jadwal_list'] = context['jadwal_list'].filter(hari=hari)
            context['selected_hari'] = hari
        else:
            context['selected_hari'] = None
        
        return context


class RisetGrupView(ListView):
    """View untuk halaman riset grup"""
    model = RisetGrup
    template_name = 'akademik/riset_grup.html'
    context_object_name = 'riset_list'
    
    def get_queryset(self):
        return RisetGrup.objects.filter(is_active=True)


class PublikasiView(ListView):
    """View untuk halaman publikasi"""
    model = Publikasi
    template_name = 'akademik/publikasi.html'
    context_object_name = 'publikasi_list'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Publikasi.objects.all().order_by('-tahun')
        
        tahun = self.request.GET.get('tahun')
        if tahun:
            queryset = queryset.filter(tahun=tahun)
        
        jenis = self.request.GET.get('jenis')
        if jenis:
            queryset = queryset.filter(jenis=jenis)
        
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(
                Q(judul__icontains=search) |
                Q(penulis__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tahun_list'] = Publikasi.objects.values_list('tahun', flat=True).distinct().order_by('-tahun')
        context['jenis_list'] = Publikasi.JENIS_CHOICES
        context['selected_tahun'] = self.request.GET.get('tahun', '')
        context['selected_jenis'] = self.request.GET.get('jenis', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context
