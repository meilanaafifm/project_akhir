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
    """
    View untuk daftar berita
    """
    model = Berita
    template_name = 'berita/berita_list.html'
    context_object_name = 'berita_list'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = Berita.objects.filter(is_published=True)
        
        # Filter berdasarkan jenis
        jenis = self.request.GET.get('jenis')
        if jenis:
            queryset = queryset.filter(jenis=jenis)
        
        # Filter berdasarkan kategori
        kategori = self.request.GET.get('kategori')
        if kategori:
            queryset = queryset.filter(kategori__slug=kategori)
        
        # Filter berdasarkan tag
        tag = self.request.GET.get('tag')
        if tag:
            queryset = queryset.filter(tags__slug=tag)
        
        # Pencarian
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(
                Q(judul__icontains=search) |
                Q(konten__icontains=search) |
                Q(ringkasan__icontains=search)
            )
        
        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Kategori untuk sidebar
        context['kategori_list'] = KategoriBerita.objects.annotate(
            berita_count=Count('berita', filter=Q(berita__is_published=True))
        )
        
        # Tag populer
        context['tag_list'] = TagBerita.objects.annotate(
            berita_count=Count('berita', filter=Q(berita__is_published=True))
        ).filter(berita_count__gt=0).order_by('-berita_count')[:15]
        
        # Berita unggulan
        context['featured_list'] = Berita.objects.filter(
            is_published=True, is_featured=True
        )[:3]
        
        # Berita terpopuler
        context['popular_list'] = Berita.objects.filter(
            is_published=True
        ).order_by('-view_count')[:5]
        
        # Filter aktif
        context['selected_jenis'] = self.request.GET.get('jenis', '')
        context['selected_kategori'] = self.request.GET.get('kategori', '')
        context['selected_tag'] = self.request.GET.get('tag', '')
        context['search_query'] = self.request.GET.get('q', '')
        
        context['jenis_choices'] = Berita.JENIS_CHOICES
        
        return context


class BeritaDetailView(DetailView):
    """
    View untuk detail berita
    """
    model = Berita
    template_name = 'berita/berita_detail.html'
    context_object_name = 'berita'
    
    def get_queryset(self):
        return Berita.objects.filter(is_published=True)
    
    def get_object(self):
        obj = super().get_object()
        # Increment view count
        obj.increment_view()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Berita terkait
        context['related_list'] = self.object.get_related_berita()
        
        # Komentar yang sudah disetujui
        context['komentar_list'] = self.object.komentar.filter(
            is_approved=True, parent=None
        )
        
        # Galeri
        context['galeri_list'] = self.object.galeri.all()
        
        # Berita sebelum dan sesudah
        context['prev_berita'] = Berita.objects.filter(
            is_published=True, published_at__lt=self.object.published_at
        ).order_by('-published_at').first()
        
        context['next_berita'] = Berita.objects.filter(
            is_published=True, published_at__gt=self.object.published_at
        ).order_by('published_at').first()
        
        return context
    
    def post(self, request, *args, **kwargs):
        """Handle komentar baru"""
        self.object = self.get_object()
        
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        komentar = request.POST.get('komentar')
        parent_id = request.POST.get('parent_id')
        
        if nama and email and komentar:
            parent = None
            if parent_id:
                try:
                    parent = KomentarBerita.objects.get(pk=parent_id)
                except:
                    pass
            
            KomentarBerita.objects.create(
                berita=self.object,
                nama=nama,
                email=email,
                komentar=komentar,
                parent=parent
            )
            messages.success(request, 'Komentar Anda sedang menunggu moderasi.')
            return redirect(self.object.get_absolute_url())
        
        messages.error(request, 'Mohon lengkapi semua field.')
        return self.get(request, *args, **kwargs)


class KategoriDetailView(ListView):
    """
    View untuk berita berdasarkan kategori
    """
    model = Berita
    template_name = 'berita/kategori_detail.html'
    context_object_name = 'berita_list'
    paginate_by = 9
    
    def get_queryset(self):
        self.kategori = get_object_or_404(KategoriBerita, slug=self.kwargs['slug'])
        return Berita.objects.filter(
            is_published=True, kategori=self.kategori
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kategori'] = self.kategori
        return context


class TagDetailView(ListView):
    """
    View untuk berita berdasarkan tag
    """
    model = Berita
    template_name = 'berita/tag_detail.html'
    context_object_name = 'berita_list'
    paginate_by = 9
    
    def get_queryset(self):
        self.tag = get_object_or_404(TagBerita, slug=self.kwargs['slug'])
        return Berita.objects.filter(
            is_published=True, tags=self.tag
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


def share_berita(request, slug):
    """
    AJAX view untuk tracking share berita
    """
    if request.method == 'POST':
        try:
            berita = Berita.objects.get(slug=slug, is_published=True)
            berita.share_count += 1
            berita.save(update_fields=['share_count'])
            return JsonResponse({
                'status': 'success',
                'share_count': berita.share_count
            })
        except Berita.DoesNotExist:
            return JsonResponse({'status': 'error'}, status=404)
    return JsonResponse({'status': 'error'}, status=400)


def agenda_list(request):
    """
    View untuk daftar agenda/event
    """
    from django.utils import timezone
    
    # Agenda mendatang
    upcoming = Berita.objects.filter(
        is_published=True,
        jenis='agenda',
        tanggal_event__gte=timezone.now()
    ).order_by('tanggal_event')
    
    # Agenda yang sudah lewat
    past = Berita.objects.filter(
        is_published=True,
        jenis='agenda',
        tanggal_event__lt=timezone.now()
    ).order_by('-tanggal_event')[:10]
    
    return render(request, 'berita/agenda_list.html', {
        'upcoming_list': upcoming,
        'past_list': past,
    })
