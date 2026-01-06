"""
Views untuk aplikasi Berita - Compatible with Vercel
"""

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
import os

IS_VERCEL = os.environ.get('VERCEL', False)


class BeritaListView(TemplateView):
    template_name = 'berita/berita_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['berita_list'] = []
        context['kategori_list'] = []
        context['tag_list'] = []
        context['berita_populer'] = []
        context['jenis_list'] = []
        
        if not IS_VERCEL:
            try:
                from .models import Berita, KategoriBerita, TagBerita
                context['berita_list'] = list(Berita.objects.filter(is_published=True).order_by('-published_at')[:9])
                context['kategori_list'] = list(KategoriBerita.objects.all())
                context['tag_list'] = list(TagBerita.objects.all()[:20])
                context['berita_populer'] = list(Berita.objects.filter(is_published=True).order_by('-views_count')[:5])
                context['jenis_list'] = Berita.JENIS_CHOICES
            except Exception:
                pass
        return context


class BeritaDetailView(TemplateView):
    template_name = 'berita/berita_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['berita'] = None
        context['berita_terkait'] = []
        context['komentar_list'] = []
        
        if not IS_VERCEL:
            try:
                from .models import Berita
                slug = self.kwargs.get('slug')
                berita = Berita.objects.filter(slug=slug, is_published=True).first()
                if berita:
                    berita.views_count += 1
                    berita.save()
                    context['berita'] = berita
                    context['berita_terkait'] = list(Berita.objects.filter(
                        is_published=True, kategori=berita.kategori
                    ).exclude(pk=berita.pk)[:4])
                    context['komentar_list'] = list(berita.komentar.filter(is_approved=True))
            except Exception:
                pass
        return context


def berita_komentar(request, pk):
    """Handle komentar berita"""
    return JsonResponse({'status': 'success'})
