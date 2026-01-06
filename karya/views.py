"""
Views untuk aplikasi Karya Mahasiswa
"""

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.db.models import Q

from .models import KaryaMahasiswa, KategoriKarya


class KaryaListView(ListView):
    """View untuk daftar karya mahasiswa"""
    model = KaryaMahasiswa
    template_name = 'karya/karya_list.html'
    context_object_name = 'karya_list'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = KaryaMahasiswa.objects.filter(is_published=True)
        
        kategori = self.request.GET.get('kategori')
        if kategori:
            queryset = queryset.filter(kategori__slug=kategori)
        
        tahun = self.request.GET.get('tahun')
        if tahun:
            queryset = queryset.filter(created_at__year=tahun)
        
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(
                Q(judul__icontains=search) |
                Q(deskripsi__icontains=search) |
                Q(nama_mahasiswa__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kategori_list'] = KategoriKarya.objects.all()
        context['tahun_list'] = KaryaMahasiswa.objects.filter(is_published=True).dates('created_at', 'year', order='DESC')
        context['selected_kategori'] = self.request.GET.get('kategori', '')
        context['selected_tahun'] = self.request.GET.get('tahun', '')
        context['search_query'] = self.request.GET.get('q', '')
        context['karya_populer'] = KaryaMahasiswa.objects.filter(is_published=True).order_by('-views_count')[:5]
        return context


class KaryaDetailView(DetailView):
    """View untuk detail karya mahasiswa"""
    model = KaryaMahasiswa
    template_name = 'karya/karya_detail.html'
    context_object_name = 'karya'
    slug_field = 'slug'
    
    def get_queryset(self):
        return KaryaMahasiswa.objects.filter(is_published=True)
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        karya = self.object
        
        context['karya_terkait'] = KaryaMahasiswa.objects.filter(
            is_published=True, kategori=karya.kategori
        ).exclude(pk=karya.pk)[:4]
        
        return context


def karya_like(request, pk):
    """AJAX view untuk like karya"""
    if request.method == 'POST':
        try:
            karya = KaryaMahasiswa.objects.get(pk=pk)
            karya.likes_count += 1
            karya.save()
            return JsonResponse({'status': 'success', 'likes_count': karya.likes_count})
        except KaryaMahasiswa.DoesNotExist:
            return JsonResponse({'status': 'error'}, status=404)
    return JsonResponse({'status': 'error'}, status=400)
