"""
Views untuk aplikasi Main
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .models import (
    SiteSettings, ProfilProdi, Kemitraan, PesanKontak,
    Slider, FAQ, Testimonial
)
from berita.models import Berita
from prestasi.models import Prestasi
from akademik.models import Dosen
from karya.models import KaryaMahasiswa


class HomeView(TemplateView):
    """View untuk halaman utama"""
    template_name = 'main/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sliders'] = Slider.objects.filter(is_active=True)[:5]
        
        try:
            context['profil'] = ProfilProdi.objects.first()
        except:
            context['profil'] = None
        
        context['berita_list'] = Berita.objects.filter(is_published=True).order_by('-published_at')[:6]
        context['prestasi_list'] = Prestasi.objects.filter(is_published=True).order_by('-tanggal')[:8]
        context['karya_list'] = KaryaMahasiswa.objects.filter(is_published=True).order_by('-created_at')[:6]
        context['kemitraan_list'] = Kemitraan.objects.filter(is_active=True)[:10]
        context['testimonial_list'] = Testimonial.objects.filter(is_active=True, is_featured=True)[:4]
        context['faq_list'] = FAQ.objects.filter(is_active=True).order_by('-view_count')[:5]
        
        return context


class TentangKamiView(TemplateView):
    """View untuk halaman Tentang Kami"""
    template_name = 'main/tentang_kami.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['profil'] = ProfilProdi.objects.first()
        except:
            context['profil'] = None
        context['dosen_list'] = Dosen.objects.filter(is_active=True)[:6]
        return context


class VisiMisiView(TemplateView):
    """View untuk halaman Visi Misi"""
    template_name = 'main/visi_misi.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['profil'] = ProfilProdi.objects.first()
        except:
            context['profil'] = None
        return context


class FAQListView(ListView):
    """View untuk halaman FAQ"""
    model = FAQ
    template_name = 'main/faq.html'
    context_object_name = 'faq_list'
    
    def get_queryset(self):
        queryset = FAQ.objects.filter(is_active=True)
        kategori = self.request.GET.get('kategori')
        if kategori:
            queryset = queryset.filter(kategori=kategori)
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(
                Q(pertanyaan__icontains=search) | Q(jawaban__icontains=search)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kategori_list'] = FAQ.KATEGORI_CHOICES
        context['selected_kategori'] = self.request.GET.get('kategori', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context


def faq_helpful(request, pk):
    """AJAX view untuk menandai FAQ sebagai helpful"""
    if request.method == 'POST':
        try:
            faq = FAQ.objects.get(pk=pk)
            faq.helpful_count += 1
            faq.save()
            return JsonResponse({'status': 'success', 'helpful_count': faq.helpful_count})
        except FAQ.DoesNotExist:
            return JsonResponse({'status': 'error'}, status=404)
    return JsonResponse({'status': 'error'}, status=400)


class KontakView(TemplateView):
    """View untuk halaman Kontak"""
    template_name = 'main/kontak.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['profil'] = ProfilProdi.objects.first()
        except:
            context['profil'] = None
        return context
    
    def post(self, request, *args, **kwargs):
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        subjek = request.POST.get('subjek')
        pesan = request.POST.get('pesan')
        
        if nama and email and subjek and pesan:
            PesanKontak.objects.create(
                nama=nama, email=email, subjek=subjek, pesan=pesan
            )
            messages.success(request, 'Pesan Anda telah terkirim!')
            return redirect('main:kontak')
        else:
            messages.error(request, 'Mohon lengkapi semua field.')
        return self.get(request, *args, **kwargs)


class KemitraanListView(ListView):
    """View untuk daftar kemitraan"""
    model = Kemitraan
    template_name = 'main/kemitraan.html'
    context_object_name = 'kemitraan_list'
    
    def get_queryset(self):
        return Kemitraan.objects.filter(is_active=True)


class TestimonialListView(ListView):
    """View untuk daftar testimonial"""
    model = Testimonial
    template_name = 'main/testimonial.html'
    context_object_name = 'testimonial_list'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Testimonial.objects.filter(is_active=True)
        tipe = self.request.GET.get('tipe')
        if tipe:
            queryset = queryset.filter(tipe=tipe)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipe_list'] = Testimonial.TIPE_CHOICES
        context['selected_tipe'] = self.request.GET.get('tipe', '')
        return context


def search_view(request):
    """View untuk pencarian global"""
    query = request.GET.get('q', '')
    results = {
        'berita': [], 'prestasi': [], 'karya': [], 'faq': [], 'dosen': [],
    }
    
    if query and len(query) >= 3:
        results['berita'] = Berita.objects.filter(
            Q(judul__icontains=query) | Q(konten__icontains=query), is_published=True
        )[:5]
        results['prestasi'] = Prestasi.objects.filter(
            Q(judul__icontains=query) | Q(deskripsi__icontains=query), is_published=True
        )[:5]
        results['karya'] = KaryaMahasiswa.objects.filter(
            Q(judul__icontains=query) | Q(deskripsi__icontains=query), is_published=True
        )[:5]
        results['faq'] = FAQ.objects.filter(
            Q(pertanyaan__icontains=query) | Q(jawaban__icontains=query), is_active=True
        )[:5]
        results['dosen'] = Dosen.objects.filter(
            Q(nama__icontains=query) | Q(bidang_keahlian__icontains=query), is_active=True
        )[:5]
    
    total = sum(len(v) for v in results.values())
    
    return render(request, 'main/search_results.html', {
        'query': query, 'results': results, 'total': total,
    })


def live_search(request):
    """AJAX view untuk live search"""
    query = request.GET.get('q', '')
    suggestions = []
    
    if query and len(query) >= 2:
        berita = Berita.objects.filter(judul__icontains=query, is_published=True).values_list('judul', flat=True)[:3]
        suggestions.extend([{'text': b, 'type': 'Berita'} for b in berita])
        
        prestasi = Prestasi.objects.filter(judul__icontains=query, is_published=True).values_list('judul', flat=True)[:3]
        suggestions.extend([{'text': p, 'type': 'Prestasi'} for p in prestasi])
        
        dosen = Dosen.objects.filter(nama__icontains=query, is_active=True).values_list('nama', flat=True)[:3]
        suggestions.extend([{'text': d, 'type': 'Dosen'} for d in dosen])
    
    return JsonResponse({'suggestions': suggestions[:10]})
