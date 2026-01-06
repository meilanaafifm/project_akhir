"""
Views untuk aplikasi Karya Mahasiswa
"""

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.db.models import Q

from .models import KaryaMahasiswa, KategoriKarya, Teknologi


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
            queryset = queryset.filter(tahun=tahun)
        
        jenis = self.request.GET.get('jenis')
        if jenis:
            queryset = queryset.filter(jenis=jenis)
        
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(
                Q(judul__icontains=search) |
                Q(deskripsi__icontains=search) |
                Q(nama_pembuat__icontains=search)
            )
        
        sort = self.request.GET.get('sort')
        if sort == 'popular':
            queryset = queryset.order_by('-view_count')
        elif sort == 'liked':
            queryset = queryset.order_by('-like_count')
        elif sort == 'oldest':
            queryset = queryset.order_by('created_at')
        else:
            queryset = queryset.order_by('-created_at')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kategori_list'] = KategoriKarya.objects.all()
        context['tahun_list'] = KaryaMahasiswa.objects.filter(is_published=True).values_list('tahun', flat=True).distinct().order_by('-tahun')
        context['teknologi_list'] = Teknologi.objects.all()
        context['jenis_choices'] = KaryaMahasiswa.JENIS_CHOICES
        context['selected_kategori'] = self.request.GET.get('kategori', '')
        context['selected_tahun'] = self.request.GET.get('tahun', '')
        context['selected_jenis'] = self.request.GET.get('jenis', '')
        context['selected_sort'] = self.request.GET.get('sort', '')
        context['search_query'] = self.request.GET.get('q', '')
        context['karya_populer'] = KaryaMahasiswa.objects.filter(is_published=True).order_by('-view_count')[:5]
        context['featured_list'] = KaryaMahasiswa.objects.filter(is_published=True, is_featured=True)[:3]
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
        obj.view_count += 1
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
            karya.like_count += 1
            karya.save()
            return JsonResponse({'status': 'success', 'likes_count': karya.like_count})
        except KaryaMahasiswa.DoesNotExist:
            return JsonResponse({'status': 'error'}, status=404)
    return JsonResponse({'status': 'error'}, status=400)
