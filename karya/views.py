"""
Views untuk aplikasi Karya Mahasiswa - Compatible with Vercel
"""

from django.views.generic import TemplateView
import os

IS_VERCEL = os.environ.get('VERCEL', False)


class KaryaListView(TemplateView):
    template_name = 'karya/karya_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['karya_list'] = []
        context['kategori_list'] = []
        context['tahun_list'] = []
        
        if not IS_VERCEL:
            try:
                from .models import KaryaMahasiswa, KategoriKarya
                context['karya_list'] = list(KaryaMahasiswa.objects.filter(is_published=True).order_by('-created_at'))
                context['kategori_list'] = list(KategoriKarya.objects.all())
                context['tahun_list'] = list(KaryaMahasiswa.objects.filter(is_published=True).dates('created_at', 'year', order='DESC'))
            except Exception:
                pass
        return context


class KaryaDetailView(TemplateView):
    template_name = 'karya/karya_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['karya'] = None
        context['karya_terkait'] = []
        
        if not IS_VERCEL:
            try:
                from .models import KaryaMahasiswa
                slug = self.kwargs.get('slug')
                karya = KaryaMahasiswa.objects.filter(slug=slug, is_published=True).first()
                if karya:
                    karya.views_count += 1
                    karya.save()
                    context['karya'] = karya
                    context['karya_terkait'] = list(KaryaMahasiswa.objects.filter(
                        is_published=True, kategori=karya.kategori
                    ).exclude(pk=karya.pk)[:4])
            except Exception:
                pass
        return context
