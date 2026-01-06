"""
Admin configuration untuk berita app
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Berita, KategoriBerita, TagBerita, GaleriBerita, KomentarBerita


class GaleriBeritaInline(admin.TabularInline):
    """Inline untuk galeri berita"""
    model = GaleriBerita
    extra = 1
    fields = ('gambar', 'caption', 'urutan')


@admin.register(KategoriBerita)
class KategoriBeritaAdmin(admin.ModelAdmin):
    """Admin untuk kategori berita"""
    list_display = ('nama', 'slug', 'warna', 'icon')
    prepopulated_fields = {'slug': ('nama',)}
    search_fields = ('nama',)


@admin.register(TagBerita)
class TagBeritaAdmin(admin.ModelAdmin):
    """Admin untuk tag berita"""
    list_display = ('nama', 'slug', 'get_berita_count')
    prepopulated_fields = {'slug': ('nama',)}
    search_fields = ('nama',)
    
    def get_berita_count(self, obj):
        return obj.get_berita_count()
    get_berita_count.short_description = 'Jumlah Berita'


@admin.register(Berita)
class BeritaAdmin(admin.ModelAdmin):
    """Admin untuk berita"""
    
    list_display = ('judul', 'jenis', 'kategori', 'gambar_preview', 
                   'is_published', 'is_featured', 'view_count', 'published_at')
    list_filter = ('jenis', 'kategori', 'is_published', 'is_featured', 'is_pinned')
    search_fields = ('judul', 'konten', 'ringkasan')
    prepopulated_fields = {'slug': ('judul',)}
    filter_horizontal = ('tags',)
    date_hierarchy = 'published_at'
    list_editable = ('is_published', 'is_featured')
    
    inlines = [GaleriBeritaInline]
    
    fieldsets = (
        ('Informasi Dasar', {
            'fields': ('judul', 'slug', 'jenis', 'kategori', 'tags')
        }),
        ('Konten', {
            'fields': ('ringkasan', 'konten')
        }),
        ('Media', {
            'fields': ('gambar_utama', 'gambar_alt', 'video_url'),
            'classes': ('collapse',)
        }),
        ('Agenda/Event', {
            'fields': ('tanggal_event', 'lokasi_event'),
            'classes': ('collapse',),
            'description': 'Isi bagian ini jika jenis berita adalah Agenda'
        }),
        ('Publikasi', {
            'fields': ('author', 'is_published', 'is_featured', 'is_pinned', 'published_at')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Statistik', {
            'fields': ('view_count', 'share_count'),
            'classes': ('collapse',)
        }),
    )
    
    def gambar_preview(self, obj):
        if obj.gambar_utama:
            return format_html('<img src="{}" width="80" height="50" style="object-fit: cover;" />', obj.gambar_utama.url)
        return '-'
    gambar_preview.short_description = 'Preview'
    
    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(KomentarBerita)
class KomentarBeritaAdmin(admin.ModelAdmin):
    """Admin untuk komentar berita"""
    
    list_display = ('nama', 'berita_title', 'email', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('nama', 'email', 'komentar')
    list_editable = ('is_approved',)
    readonly_fields = ('berita', 'nama', 'email', 'komentar', 'parent', 'created_at')
    
    def berita_title(self, obj):
        return obj.berita.judul[:50]
    berita_title.short_description = 'Berita'
    
    def has_add_permission(self, request):
        return False
