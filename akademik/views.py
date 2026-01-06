"""
Views untuk aplikasi Akademik - Compatible with Vercel
"""

from django.shortcuts import render
from django.views.generic import TemplateView
import os

IS_VERCEL = os.environ.get('VERCEL', False)


class DosenListView(TemplateView):
    template_name = 'akademik/dosen_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dosen_list'] = []
        if not IS_VERCEL:
            try:
                from .models import Dosen
                context['dosen_list'] = list(Dosen.objects.filter(is_active=True))
            except Exception:
                pass
        return context


class DosenDetailView(TemplateView):
    template_name = 'akademik/dosen_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dosen'] = None
        if not IS_VERCEL:
            try:
                from .models import Dosen
                slug = self.kwargs.get('slug')
                context['dosen'] = Dosen.objects.filter(slug=slug, is_active=True).first()
            except Exception:
                pass
        return context


class KurikulumView(TemplateView):
    template_name = 'akademik/kurikulum.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['semester_list'] = []
        context['matakuliah_list'] = []
        if not IS_VERCEL:
            try:
                from .models import MataKuliah
                context['matakuliah_list'] = list(MataKuliah.objects.filter(is_active=True).order_by('semester', 'nama'))
                context['semester_list'] = list(range(1, 9))
            except Exception:
                pass
        return context


class MataKuliahDetailView(TemplateView):
    template_name = 'akademik/matakuliah_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['matakuliah'] = None
        if not IS_VERCEL:
            try:
                from .models import MataKuliah
                slug = self.kwargs.get('slug')
                context['matakuliah'] = MataKuliah.objects.filter(slug=slug, is_active=True).first()
            except Exception:
                pass
        return context


class FasilitasView(TemplateView):
    template_name = 'akademik/fasilitas.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fasilitas_list'] = []
        if not IS_VERCEL:
            try:
                from .models import Fasilitas
                context['fasilitas_list'] = list(Fasilitas.objects.filter(is_active=True))
            except Exception:
                pass
        return context


class JadwalView(TemplateView):
    template_name = 'akademik/jadwal.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jadwal_list'] = []
        if not IS_VERCEL:
            try:
                from .models import JadwalKuliah
                context['jadwal_list'] = list(JadwalKuliah.objects.filter(is_active=True))
            except Exception:
                pass
        return context


class RisetGrupView(TemplateView):
    template_name = 'akademik/riset_grup.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['riset_list'] = []
        if not IS_VERCEL:
            try:
                from .models import RisetGrup
                context['riset_list'] = list(RisetGrup.objects.filter(is_active=True))
            except Exception:
                pass
        return context


class PublikasiView(TemplateView):
    template_name = 'akademik/publikasi.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publikasi_list'] = []
        if not IS_VERCEL:
            try:
                from .models import Publikasi
                context['publikasi_list'] = list(Publikasi.objects.all().order_by('-tahun'))
            except Exception:
                pass
        return context
