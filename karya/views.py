"""
Views untuk aplikasi Karya
"""

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.db.models import Q, Count

from .models import KaryaMahasiswa, KategoriKarya, Teknologi


class KaryaListView(ListView):
    """
    View untuk daftar karya mahasiswa
    Inovasi: Gallery dengan filter dan sort
    """
    model = KaryaMahasiswa
    template_name = 'karya/karya_list.html'
    context_object_name = 'karya_list'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = KaryaMahasiswa.objects.filter(is_published=True)
        
        # Filter berdasarkan jenis
        jenis = self.request.GET.get('jenis')
        if jenis:
            queryset = queryset.filter(jenis=jenis)
        
        # Filter berdasarkan kategori
        kategori = self.request.GET.get('kategori')
        if kategori:
            queryset = queryset.filter(kategori__slug=kategori)
        
        # Filter berdasarkan teknologi
        teknologi = self.request.GET.get('teknologi')
        if teknologi:
            queryset = queryset.filter(teknologi__slug=teknologi)
        
        # Filter berdasarkan tahun
        tahun = self.request.GET.get('tahun')
        if tahun:
            queryset = queryset.filter(tahun=tahun)
        
        # Pencarian
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(
                Q(judul__icontains=search) |
                Q(nama_pembuat__icontains=search) |
                Q(deskripsi__icontains=search)
            )
        
        # Sorting
        sort = self.request.GET.get('sort', '-created_at')
        if sort == 'popular':
            queryset = queryset.order_by('-view_count')
        elif sort == 'liked':
            queryset = queryset.order_by('-like_count')
        elif sort == 'oldest':
            queryset = queryset.order_by('created_at')
        else:
            queryset = queryset.order_by('-created_at')
        
        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Kategori
        context['kategori_list'] = KategoriKarya.objects.annotate(
            karya_count=Count('karyamahasiswa', filter=Q(karyamahasiswa__is_published=True))
        )
        
        # Teknologi populer
        context['teknologi_list'] = Teknologi.objects.annotate(
            karya_count=Count('karyamahasiswa', filter=Q(karyamahasiswa__is_published=True))
        ).filter(karya_count__gt=0).order_by('-karya_count')[:15]
        
        # Tahun
        context['tahun_list'] = KaryaMahasiswa.objects.filter(
            is_published=True
        ).values_list('tahun', flat=True).distinct().order_by('-tahun')
        
        # Choices
        context['jenis_choices'] = KaryaMahasiswa.JENIS_CHOICES
        
        # Selected filters
        context['selected_jenis'] = self.request.GET.get('jenis', '')
        context['selected_kategori'] = self.request.GET.get('kategori', '')
        context['selected_teknologi'] = self.request.GET.get('teknologi', '')
        context['selected_tahun'] = self.request.GET.get('tahun', '')
        context['selected_sort'] = self.request.GET.get('sort', '')
        context['search_query'] = self.request.GET.get('q', '')
        
        # Karya unggulan
        context['featured_list'] = KaryaMahasiswa.objects.filter(
            is_published=True, is_featured=True
        )[:3]
        
        return context


class KaryaDetailView(DetailView):
    """
    View untuk detail karya
    """
    model = KaryaMahasiswa
    template_name = 'karya/karya_detail.html'
    context_object_name = 'karya'
    
    def get_queryset(self):
        return KaryaMahasiswa.objects.filter(is_published=True)
    
    def get_object(self):
        obj = super().get_object()
        obj.view_count += 1
        obj.save(update_fields=['view_count'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Karya terkait (berdasarkan kategori atau teknologi)
        related = KaryaMahasiswa.objects.filter(
            is_published=True
        ).exclude(pk=self.object.pk)
        
        if self.object.kategori:
            related = related.filter(kategori=self.object.kategori)
        
        context['related_list'] = related[:4]
        
        return context


def like_karya(request, slug):
    """
    AJAX view untuk like karya
    Inovasi: Like/vote system
    """
    if request.method == 'POST':
        try:
            karya = KaryaMahasiswa.objects.get(slug=slug, is_published=True)
            
            # Check if already liked (using session)
            liked_karya = request.session.get('liked_karya', [])
            
            if karya.pk not in liked_karya:
                karya.like_count += 1
                karya.save(update_fields=['like_count'])
                liked_karya.append(karya.pk)
                request.session['liked_karya'] = liked_karya
                status = 'liked'
            else:
                status = 'already_liked'
            
            return JsonResponse({
                'status': status,
                'like_count': karya.like_count
            })
        except KaryaMahasiswa.DoesNotExist:
            return JsonResponse({'status': 'error'}, status=404)
    return JsonResponse({'status': 'error'}, status=400)
