"""
Views untuk aplikasi Akademik
"""

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.http import JsonResponse
from django.db.models import Q, Sum

from .models import (
    Dosen, RisetGrup, Kurikulum, MataKuliah, 
    JadwalKuliah, Publikasi, Fasilitas
)


class DosenListView(ListView):
    """
    View untuk daftar dosen
    """
    model = Dosen
    template_name = 'akademik/dosen_list.html'
    context_object_name = 'dosen_list'
    
    def get_queryset(self):
        queryset = Dosen.objects.filter(is_active=True)
        
        # Filter berdasarkan jabatan
        jabatan = self.request.GET.get('jabatan')
        if jabatan:
            queryset = queryset.filter(jabatan_fungsional=jabatan)
        
        # Pencarian
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(
                Q(nama__icontains=search) |
                Q(bidang_keahlian__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jabatan_choices'] = Dosen.JABATAN_CHOICES
        context['selected_jabatan'] = self.request.GET.get('jabatan', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context


class DosenDetailView(DetailView):
    """
    View untuk detail dosen
    """
    model = Dosen
    template_name = 'akademik/dosen_detail.html'
    context_object_name = 'dosen'
    
    def get_queryset(self):
        return Dosen.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Publikasi dosen
        context['publikasi_list'] = self.object.publikasi.all()[:10]
        
        # Mata kuliah yang diampu
        context['matakuliah_list'] = self.object.mata_kuliah_diampu.all()
        
        # Riset grup
        context['riset_grup_list'] = self.object.riset_grup.all()
        
        return context


class KurikulumView(TemplateView):
    """
    View untuk halaman kurikulum
    Inovasi: Tampilan kurikulum interaktif per semester
    """
    template_name = 'akademik/kurikulum.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Ambil kurikulum aktif
        try:
            kurikulum = Kurikulum.objects.get(is_active=True)
        except Kurikulum.DoesNotExist:
            kurikulum = Kurikulum.objects.first()
        
        context['kurikulum'] = kurikulum
        
        if kurikulum:
            # Kelompokkan mata kuliah per semester
            mata_kuliah_per_semester = {}
            for semester in range(1, 9):
                mk_list = kurikulum.mata_kuliah.filter(semester=semester)
                if mk_list.exists():
                    total_sks = sum(mk.total_sks for mk in mk_list)
                    mata_kuliah_per_semester[semester] = {
                        'list': mk_list,
                        'total_sks': total_sks,
                    }
            
            context['mata_kuliah_per_semester'] = mata_kuliah_per_semester
            
            # Total SKS keseluruhan
            context['total_sks'] = sum(
                data['total_sks'] for data in mata_kuliah_per_semester.values()
            )
        
        return context


class MataKuliahDetailView(DetailView):
    """
    View untuk detail mata kuliah
    """
    model = MataKuliah
    template_name = 'akademik/matakuliah_detail.html'
    context_object_name = 'matakuliah'
    
    def get_object(self):
        return get_object_or_404(
            MataKuliah,
            kurikulum__is_active=True,
            kode=self.kwargs['kode']
        )


class JadwalKuliahView(TemplateView):
    """
    View untuk jadwal kuliah
    Inovasi: Jadwal interaktif dengan filter hari dan dosen
    """
    template_name = 'akademik/jadwal.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Ambil semester aktif (dari jadwal terakhir)
        jadwal_terbaru = JadwalKuliah.objects.filter(is_active=True).first()
        semester_aktif = jadwal_terbaru.semester_aktif if jadwal_terbaru else ''
        
        # Filter
        hari = self.request.GET.get('hari', '')
        dosen_id = self.request.GET.get('dosen', '')
        
        jadwal = JadwalKuliah.objects.filter(is_active=True)
        
        if hari:
            jadwal = jadwal.filter(hari=hari)
        if dosen_id:
            jadwal = jadwal.filter(dosen_id=dosen_id)
        
        # Kelompokkan jadwal per hari
        jadwal_per_hari = {}
        for h, label in JadwalKuliah.HARI_CHOICES:
            jadwal_hari = jadwal.filter(hari=h)
            if jadwal_hari.exists():
                jadwal_per_hari[h] = {
                    'label': label,
                    'jadwal': jadwal_hari,
                }
        
        context['jadwal_per_hari'] = jadwal_per_hari
        context['semester_aktif'] = semester_aktif
        context['hari_choices'] = JadwalKuliah.HARI_CHOICES
        context['dosen_list'] = Dosen.objects.filter(is_active=True)
        context['selected_hari'] = hari
        context['selected_dosen'] = dosen_id
        
        return context


def jadwal_api(request):
    """
    API untuk mendapatkan jadwal dalam format JSON
    Inovasi: API untuk integrasi kalender
    """
    jadwal = JadwalKuliah.objects.filter(is_active=True)
    
    hari = request.GET.get('hari')
    if hari:
        jadwal = jadwal.filter(hari=hari)
    
    data = []
    for j in jadwal:
        data.append({
            'id': j.id,
            'matakuliah': j.mata_kuliah.nama,
            'kode': j.mata_kuliah.kode,
            'kelas': j.kelas,
            'hari': j.hari,
            'jam_mulai': j.jam_mulai.strftime('%H:%M'),
            'jam_selesai': j.jam_selesai.strftime('%H:%M'),
            'ruangan': j.ruangan,
            'dosen': j.dosen.get_full_name() if j.dosen else '-',
        })
    
    return JsonResponse({'jadwal': data})


class RisetGrupListView(ListView):
    """
    View untuk daftar riset grup
    """
    model = RisetGrup
    template_name = 'akademik/riset_grup.html'
    context_object_name = 'riset_grup_list'
    
    def get_queryset(self):
        return RisetGrup.objects.filter(is_active=True)


class PublikasiListView(ListView):
    """
    View untuk daftar publikasi
    Inovasi: Database publikasi dengan filter
    """
    model = Publikasi
    template_name = 'akademik/publikasi.html'
    context_object_name = 'publikasi_list'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Publikasi.objects.all()
        
        # Filter berdasarkan jenis
        jenis = self.request.GET.get('jenis')
        if jenis:
            queryset = queryset.filter(jenis=jenis)
        
        # Filter berdasarkan tahun
        tahun = self.request.GET.get('tahun')
        if tahun:
            queryset = queryset.filter(tahun=tahun)
        
        # Filter indexed only
        indexed = self.request.GET.get('indexed')
        if indexed:
            queryset = queryset.filter(is_indexed=True)
        
        # Pencarian
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(
                Q(judul__icontains=search) |
                Q(penulis_text__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jenis_choices'] = Publikasi.JENIS_CHOICES
        context['tahun_list'] = Publikasi.objects.values_list(
            'tahun', flat=True
        ).distinct().order_by('-tahun')
        context['selected_jenis'] = self.request.GET.get('jenis', '')
        context['selected_tahun'] = self.request.GET.get('tahun', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context


class FasilitasListView(ListView):
    """
    View untuk daftar fasilitas
    """
    model = Fasilitas
    template_name = 'akademik/fasilitas.html'
    context_object_name = 'fasilitas_list'
    
    def get_queryset(self):
        return Fasilitas.objects.filter(is_active=True)
