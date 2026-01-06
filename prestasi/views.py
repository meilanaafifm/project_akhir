"""
Views untuk aplikasi Prestasi
"""

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q

from .models import Prestasi


class PrestasiListView(ListView):
    """View untuk daftar prestasi"""
    model = Prestasi
    template_name = 'prestasi/prestasi_list.html'
    context_object_name = 'prestasi_list'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Prestasi.objects.filter(is_published=True)
        
        tingkat = self.request.GET.get('tingkat')
        if tingkat:
            queryset = queryset.filter(tingkat=tingkat)
        
        tahun = self.request.GET.get('tahun')
        if tahun:
            queryset = queryset.filter(tanggal__year=tahun)
        
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(
                Q(judul__icontains=search) |
                Q(deskripsi__icontains=search) |
                Q(nama_peserta__icontains=search)
            )
        
        return queryset.order_by('-tanggal')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tingkat_list'] = Prestasi.TINGKAT_CHOICES
        context['tahun_list'] = Prestasi.objects.filter(is_published=True).dates('tanggal', 'year', order='DESC')
        context['selected_tingkat'] = self.request.GET.get('tingkat', '')
        context['selected_tahun'] = self.request.GET.get('tahun', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context


class PrestasiDetailView(DetailView):
    """View untuk detail prestasi"""
    model = Prestasi
    template_name = 'prestasi/prestasi_detail.html'
    context_object_name = 'prestasi'
    slug_field = 'slug'
    
    def get_queryset(self):
        return Prestasi.objects.filter(is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prestasi = self.object
        
        context['prestasi_terkait'] = Prestasi.objects.filter(
            is_published=True, tingkat=prestasi.tingkat
        ).exclude(pk=prestasi.pk)[:4]
        
        return context
