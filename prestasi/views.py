"""
Views untuk aplikasi Prestasi
"""

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q, Count

from .models import Prestasi, KategoriPrestasi


class PrestasiListView(ListView):
    """
    View untuk daftar prestasi
    """
    model = Prestasi
    template_name = 'prestasi/prestasi_list.html'
    context_object_name = 'prestasi_list'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Prestasi.objects.filter(is_published=True)
        
        # Filter berdasarkan jenis
        jenis = self.request.GET.get('jenis')
        if jenis:
            queryset = queryset.filter(jenis=jenis)
        
        # Filter berdasarkan tingkat
        tingkat = self.request.GET.get('tingkat')
        if tingkat:
            queryset = queryset.filter(tingkat=tingkat)
        
        # Filter berdasarkan kategori
        kategori = self.request.GET.get('kategori')
        if kategori:
            queryset = queryset.filter(kategori__slug=kategori)
        
        # Filter berdasarkan tahun
        tahun = self.request.GET.get('tahun')
        if tahun:
            queryset = queryset.filter(tanggal__year=tahun)
        
        # Pencarian
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(
                Q(judul__icontains=search) |
                Q(nama_peraih__icontains=search) |
                Q(nama_kompetisi__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Kategori
        context['kategori_list'] = KategoriPrestasi.objects.annotate(
            prestasi_count=Count('prestasi', filter=Q(prestasi__is_published=True))
        )
        
        # Tahun
        context['tahun_list'] = Prestasi.objects.filter(
            is_published=True
        ).dates('tanggal', 'year').values_list('tanggal__year', flat=True).distinct()
        
        # Choices
        context['jenis_choices'] = Prestasi.JENIS_CHOICES
        context['tingkat_choices'] = Prestasi.TINGKAT_CHOICES
        
        # Selected filters
        context['selected_jenis'] = self.request.GET.get('jenis', '')
        context['selected_tingkat'] = self.request.GET.get('tingkat', '')
        context['selected_kategori'] = self.request.GET.get('kategori', '')
        context['selected_tahun'] = self.request.GET.get('tahun', '')
        context['search_query'] = self.request.GET.get('q', '')
        
        # Statistik
        context['total_prestasi'] = Prestasi.objects.filter(is_published=True).count()
        context['prestasi_internasional'] = Prestasi.objects.filter(
            is_published=True, tingkat='internasional'
        ).count()
        context['prestasi_nasional'] = Prestasi.objects.filter(
            is_published=True, tingkat='nasional'
        ).count()
        
        return context


class PrestasiDetailView(DetailView):
    """
    View untuk detail prestasi
    """
    model = Prestasi
    template_name = 'prestasi/prestasi_detail.html'
    context_object_name = 'prestasi'
    
    def get_queryset(self):
        return Prestasi.objects.filter(is_published=True)
    
    def get_object(self):
        obj = super().get_object()
        obj.view_count += 1
        obj.save(update_fields=['view_count'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Prestasi terkait
        context['related_list'] = Prestasi.objects.filter(
            is_published=True
        ).exclude(pk=self.object.pk)[:4]
        
        return context
