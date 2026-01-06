"""
Admin configuration untuk main app
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SiteSettings, ProfilProdi, Kemitraan, PesanKontak,
    Slider, FAQ, Testimonial, VisitorLog
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Admin untuk pengaturan website"""
    
    fieldsets = (
        ('Informasi Dasar', {
            'fields': ('site_name', 'site_tagline', 'site_description', 
                      'university_name', 'faculty_name')
        }),
        ('Kontak', {
            'fields': ('address', 'phone', 'email')
        }),
        ('Media Sosial', {
            'fields': ('instagram', 'youtube', 'twitter', 'tiktok'),
            'classes': ('collapse',)
        }),
        ('Logo & Gambar', {
            'fields': ('logo', 'favicon', 'hero_image'),
            'classes': ('collapse',)
        }),
        ('SEO', {
            'fields': ('meta_keywords',),
            'classes': ('collapse',)
        }),
        ('Statistik', {
            'fields': ('jumlah_mahasiswa_aktif', 'jumlah_alumni', 
                      'jumlah_dosen', 'jumlah_hak_cipta')
        }),
    )
    
    def has_add_permission(self, request):
        # Hanya boleh ada 1 instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ProfilProdi)
class ProfilProdiAdmin(admin.ModelAdmin):
    """Admin untuk profil program studi"""
    
    fieldsets = (
        ('Visi & Misi', {
            'fields': ('visi', 'misi', 'tujuan', 'sejarah')
        }),
        ('Ketua Prodi', {
            'fields': ('nama_kaprodi', 'gelar_kaprodi', 'foto_kaprodi', 'sambutan_kaprodi')
        }),
        ('Akreditasi', {
            'fields': ('akreditasi', 'nomor_sk_akreditasi', 'tanggal_akreditasi')
        }),
    )
    
    def has_add_permission(self, request):
        return not ProfilProdi.objects.exists()


@admin.register(Kemitraan)
class KemitraanAdmin(admin.ModelAdmin):
    """Admin untuk kemitraan"""
    
    list_display = ('nama', 'jenis_kerjasama', 'logo_preview', 'is_active', 'urutan')
    list_filter = ('is_active', 'jenis_kerjasama')
    search_fields = ('nama', 'deskripsi')
    list_editable = ('is_active', 'urutan')
    ordering = ('urutan', 'nama')
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: contain;" />', obj.logo.url)
        return '-'
    logo_preview.short_description = 'Logo'


@admin.register(PesanKontak)
class PesanKontakAdmin(admin.ModelAdmin):
    """Admin untuk pesan kontak"""
    
    list_display = ('subjek', 'nama', 'email', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('nama', 'email', 'subjek', 'pesan')
    readonly_fields = ('nama', 'email', 'subjek', 'pesan', 'created_at')
    list_editable = ('status',)
    date_hierarchy = 'created_at'
    
    def has_add_permission(self, request):
        return False


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    """Admin untuk slider"""
    
    list_display = ('judul', 'gambar_preview', 'urutan', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('urutan', 'is_active')
    ordering = ('urutan',)
    
    def gambar_preview(self, obj):
        if obj.gambar:
            return format_html('<img src="{}" width="100" height="50" style="object-fit: cover;" />', obj.gambar.url)
        return '-'
    gambar_preview.short_description = 'Preview'


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    """Admin untuk FAQ"""
    
    list_display = ('pertanyaan_short', 'kategori', 'view_count', 'helpful_count', 'is_active')
    list_filter = ('kategori', 'is_active')
    search_fields = ('pertanyaan', 'jawaban')
    list_editable = ('is_active',)
    ordering = ('kategori', 'urutan')
    
    def pertanyaan_short(self, obj):
        return obj.pertanyaan[:50] + '...' if len(obj.pertanyaan) > 50 else obj.pertanyaan
    pertanyaan_short.short_description = 'Pertanyaan'


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    """Admin untuk testimonial"""
    
    list_display = ('nama', 'tipe', 'foto_preview', 'rating', 'is_featured', 'is_active')
    list_filter = ('tipe', 'is_featured', 'is_active')
    search_fields = ('nama', 'testimoni')
    list_editable = ('is_featured', 'is_active')
    
    def foto_preview(self, obj):
        if obj.foto:
            return format_html('<img src="{}" width="40" height="40" style="border-radius: 50%; object-fit: cover;" />', obj.foto.url)
        return '-'
    foto_preview.short_description = 'Foto'


@admin.register(VisitorLog)
class VisitorLogAdmin(admin.ModelAdmin):
    """Admin untuk log pengunjung"""
    
    list_display = ('ip_address', 'page_url', 'device_type', 'browser', 'visited_at')
    list_filter = ('device_type', 'browser', 'visited_at')
    search_fields = ('ip_address', 'page_url')
    date_hierarchy = 'visited_at'
    readonly_fields = ('ip_address', 'user_agent', 'page_url', 'referrer', 'country', 'city', 'device_type', 'browser', 'visited_at')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
