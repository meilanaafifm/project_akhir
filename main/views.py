"""
Views untuk aplikasi Main - Compatible with Vercel (no database)
"""

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib import messages
import os

# Check if running on Vercel
IS_VERCEL = os.environ.get('VERCEL', False)


class HomeView(TemplateView):
    """Homepage"""
    template_name = 'main/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_demo'] = IS_VERCEL
        context['sliders'] = []
        context['profil'] = None
        context['berita_list'] = []
        context['prestasi_list'] = []
        context['karya_list'] = []
        context['kemitraan_list'] = []
        context['testimonial_list'] = []
        context['faq_list'] = []
        
        if not IS_VERCEL:
            try:
                from .models import Slider, ProfilProdi, Kemitraan, FAQ, Testimonial
                from berita.models import Berita
                from prestasi.models import Prestasi
                from karya.models import KaryaMahasiswa
                
                context['sliders'] = list(Slider.objects.filter(is_active=True)[:5])
                context['profil'] = ProfilProdi.objects.first()
                context['berita_list'] = list(Berita.objects.filter(is_published=True).order_by('-published_at')[:6])
                context['prestasi_list'] = list(Prestasi.objects.filter(is_published=True).order_by('-tanggal')[:8])
                context['karya_list'] = list(KaryaMahasiswa.objects.filter(is_published=True).order_by('-created_at')[:6])
                context['kemitraan_list'] = list(Kemitraan.objects.filter(is_active=True)[:10])
                context['testimonial_list'] = list(Testimonial.objects.filter(is_active=True, is_featured=True)[:4])
                context['faq_list'] = list(FAQ.objects.filter(is_active=True).order_by('-view_count')[:5])
            except Exception:
                pass
        return context


class TentangKamiView(TemplateView):
    template_name = 'main/tentang_kami.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profil'] = None
        context['dosen_list'] = []
        if not IS_VERCEL:
            try:
                from .models import ProfilProdi
                from akademik.models import Dosen
                context['profil'] = ProfilProdi.objects.first()
                context['dosen_list'] = list(Dosen.objects.filter(is_active=True)[:6])
            except Exception:
                pass
        return context


class VisiMisiView(TemplateView):
    template_name = 'main/visi_misi.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profil'] = None
        if not IS_VERCEL:
            try:
                from .models import ProfilProdi
                context['profil'] = ProfilProdi.objects.first()
            except Exception:
                pass
        return context


class FAQListView(TemplateView):
    template_name = 'main/faq.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faq_list'] = []
        context['kategori_list'] = []
        context['selected_kategori'] = ''
        context['search_query'] = ''
        if not IS_VERCEL:
            try:
                from .models import FAQ
                context['faq_list'] = list(FAQ.objects.filter(is_active=True))
                context['kategori_list'] = FAQ.KATEGORI_CHOICES
            except Exception:
                pass
        return context


class KontakView(TemplateView):
    template_name = 'main/kontak.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profil'] = None
        if not IS_VERCEL:
            try:
                from .models import ProfilProdi
                context['profil'] = ProfilProdi.objects.first()
            except Exception:
                pass
        return context
    
    def post(self, request, *args, **kwargs):
        messages.success(request, 'Pesan Anda telah terkirim!')
        return redirect('main:kontak')


class KemitraanListView(TemplateView):
    template_name = 'main/kemitraan.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kemitraan_list'] = []
        if not IS_VERCEL:
            try:
                from .models import Kemitraan
                context['kemitraan_list'] = list(Kemitraan.objects.filter(is_active=True))
            except Exception:
                pass
        return context


class TestimonialListView(TemplateView):
    template_name = 'main/testimonial.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testimonial_list'] = []
        context['tipe_list'] = []
        context['selected_tipe'] = ''
        if not IS_VERCEL:
            try:
                from .models import Testimonial
                context['testimonial_list'] = list(Testimonial.objects.filter(is_active=True))
                context['tipe_list'] = Testimonial.TIPE_CHOICES
            except Exception:
                pass
        return context


def search_view(request):
    """Search view"""
    query = request.GET.get('q', '')
    results = {'berita': [], 'prestasi': [], 'karya': [], 'faq': [], 'dosen': []}
    total = 0
    
    if not IS_VERCEL and query and len(query) >= 3:
        try:
            from django.db.models import Q
            from berita.models import Berita
            from prestasi.models import Prestasi
            from karya.models import KaryaMahasiswa
            from akademik.models import Dosen
            from .models import FAQ
            
            results['berita'] = list(Berita.objects.filter(
                Q(judul__icontains=query) | Q(konten__icontains=query), is_published=True
            )[:5])
            results['prestasi'] = list(Prestasi.objects.filter(
                Q(judul__icontains=query) | Q(deskripsi__icontains=query), is_published=True
            )[:5])
            results['karya'] = list(KaryaMahasiswa.objects.filter(
                Q(judul__icontains=query) | Q(deskripsi__icontains=query), is_published=True
            )[:5])
            results['faq'] = list(FAQ.objects.filter(
                Q(pertanyaan__icontains=query) | Q(jawaban__icontains=query), is_active=True
            )[:5])
            results['dosen'] = list(Dosen.objects.filter(
                Q(nama__icontains=query) | Q(bidang_keahlian__icontains=query), is_active=True
            )[:5])
            total = sum(len(v) for v in results.values())
        except Exception:
            pass
    
    return render(request, 'main/search_results.html', {
        'query': query, 'results': results, 'total': total
    })


def faq_helpful(request, pk):
    """AJAX view untuk FAQ helpful"""
    if not IS_VERCEL and request.method == 'POST':
        try:
            from .models import FAQ
            faq = FAQ.objects.get(pk=pk)
            faq.helpful_count += 1
            faq.save()
            return JsonResponse({'status': 'success', 'helpful_count': faq.helpful_count})
        except Exception:
            pass
    return JsonResponse({'status': 'success', 'helpful_count': 0})


def live_search(request):
    """AJAX view untuk live search"""
    query = request.GET.get('q', '')
    suggestions = []
    
    if not IS_VERCEL and query and len(query) >= 2:
        try:
            from berita.models import Berita
            from prestasi.models import Prestasi
            from akademik.models import Dosen
            
            berita = Berita.objects.filter(judul__icontains=query, is_published=True).values_list('judul', flat=True)[:3]
            suggestions.extend([{'text': b, 'type': 'Berita'} for b in berita])
            
            prestasi = Prestasi.objects.filter(judul__icontains=query, is_published=True).values_list('judul', flat=True)[:3]
            suggestions.extend([{'text': p, 'type': 'Prestasi'} for p in prestasi])
            
            dosen = Dosen.objects.filter(nama__icontains=query, is_active=True).values_list('nama', flat=True)[:3]
            suggestions.extend([{'text': d, 'type': 'Dosen'} for d in dosen])
        except Exception:
            pass
    
    return JsonResponse({'suggestions': suggestions[:10]})
