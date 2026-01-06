"""
Views untuk aplikasi Berita
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator

from .models import Berita, KategoriBerita, TagBerita, KomentarBerita


class BeritaListView(ListView):
    """View untuk daftar berita"""
    model = Berita
    template_name = 'berita/berita_list.html'
    context_object_name = 'berita_list'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = Berita.objects.filter(is_published=True)
        
        jenis = self.request.GET.get('jenis')
        if jenis:
            queryset = queryset.filter(jenis=jenis)
        
        kategori = self.request.GET.get('kategori')
        if kategori:
            queryset = queryset.filter(kategori__slug=kategori)
        
        tag = self.request.GET.get('tag')
        if tag:
            queryset = queryset.filter(tags__slug=tag)
        
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(
                Q(judul__icontains=search) |
                Q(konten__icontains=search) |
                Q(ringkasan__icontains=search)
            )
        
        return queryset.distinct().order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kategori_list'] = KategoriBerita.objects.annotate(
            berita_count=Count('berita', filter=Q(berita__is_published=True))
        )
        context['tag_list'] = TagBerita.objects.all()[:20]
        context['berita_populer'] = Berita.objects.filter(is_published=True).order_by('-view_count')[:5]
        context['jenis_choices'] = Berita.JENIS_CHOICES
        context['selected_jenis'] = self.request.GET.get('jenis', '')
        context['selected_kategori'] = self.request.GET.get('kategori', '')
        context['search_query'] = self.request.GET.get('q', '')
        context['featured_list'] = Berita.objects.filter(is_published=True, is_featured=True)[:3]
        return context


class BeritaDetailView(DetailView):
    """View untuk detail berita"""
    model = Berita
    template_name = 'berita/berita_detail.html'
    context_object_name = 'berita'
    slug_field = 'slug'
    
    def get_queryset(self):
        return Berita.objects.filter(is_published=True)
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.view_count += 1
        obj.save()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        berita = self.object
        
        context['berita_terkait'] = Berita.objects.filter(
            is_published=True, kategori=berita.kategori
        ).exclude(pk=berita.pk)[:4]
        
        context['komentar_list'] = berita.komentar.filter(is_approved=True)
        return context


class KategoriDetailView(ListView):
    """View untuk berita berdasarkan kategori"""
    model = Berita
    template_name = 'berita/berita_list.html'
    context_object_name = 'berita_list'
    paginate_by = 9
    
    def get_queryset(self):
        self.kategori = get_object_or_404(KategoriBerita, slug=self.kwargs['slug'])
        return Berita.objects.filter(is_published=True, kategori=self.kategori).order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kategori'] = self.kategori
        context['kategori_list'] = KategoriBerita.objects.all()
        return context


class TagDetailView(ListView):
    """View untuk berita berdasarkan tag"""
    model = Berita
    template_name = 'berita/berita_list.html'
    context_object_name = 'berita_list'
    paginate_by = 9
    
    def get_queryset(self):
        self.tag = get_object_or_404(TagBerita, slug=self.kwargs['slug'])
        return Berita.objects.filter(is_published=True, tags=self.tag).order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        context['tag_list'] = TagBerita.objects.all()
        return context


def agenda_list(request):
    """View untuk daftar agenda"""
    agenda = Berita.objects.filter(is_published=True, jenis='agenda').order_by('-published_at')
    return render(request, 'berita/berita_list.html', {
        'berita_list': agenda,
        'is_agenda': True,
    })


def share_berita(request, slug):
    """Track share count"""
    berita = get_object_or_404(Berita, slug=slug, is_published=True)
    berita.share_count += 1
    berita.save()
    return JsonResponse({'status': 'success', 'share_count': berita.share_count})


def berita_komentar(request, pk):
    """Handle komentar berita"""
    if request.method == 'POST':
        berita = get_object_or_404(Berita, pk=pk, is_published=True)
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        komentar = request.POST.get('komentar')
        
        if nama and email and komentar:
            KomentarBerita.objects.create(
                berita=berita, nama=nama, email=email, komentar=komentar
            )
            messages.success(request, 'Komentar Anda telah dikirim dan menunggu moderasi.')
        else:
            messages.error(request, 'Mohon lengkapi semua field.')
        
        return redirect('berita:detail', slug=berita.slug)
    
    return redirect('berita:list')
