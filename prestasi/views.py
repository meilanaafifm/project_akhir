"""
Views untuk aplikasi Prestasi - Compatible with Vercel
"""

from django.views.generic import TemplateView
import os

IS_VERCEL = os.environ.get('VERCEL', False)


class PrestasiListView(TemplateView):
    template_name = 'prestasi/prestasi_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prestasi_list'] = []
        context['tingkat_list'] = []
        context['tahun_list'] = []
        
        if not IS_VERCEL:
            try:
                from .models import Prestasi
                context['prestasi_list'] = list(Prestasi.objects.filter(is_published=True).order_by('-tanggal'))
                context['tingkat_list'] = Prestasi.TINGKAT_CHOICES
                context['tahun_list'] = list(Prestasi.objects.filter(is_published=True).dates('tanggal', 'year', order='DESC'))
            except Exception:
                pass
        return context


class PrestasiDetailView(TemplateView):
    template_name = 'prestasi/prestasi_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prestasi'] = None
        context['prestasi_terkait'] = []
        
        if not IS_VERCEL:
            try:
                from .models import Prestasi
                slug = self.kwargs.get('slug')
                prestasi = Prestasi.objects.filter(slug=slug, is_published=True).first()
                if prestasi:
                    context['prestasi'] = prestasi
                    context['prestasi_terkait'] = list(Prestasi.objects.filter(
                        is_published=True, tingkat=prestasi.tingkat
                    ).exclude(pk=prestasi.pk)[:4])
            except Exception:
                pass
        return context
