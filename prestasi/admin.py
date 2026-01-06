"""
Admin configuration untuk prestasi app
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Prestasi, KategoriPrestasi


@admin.register(KategoriPrestasi)
class KategoriPrestasiAdmin(admin.ModelAdmin):
    """Admin untuk kategori prestasi"""
    list_display = ('nama', 'slug', 'warna', 'icon')
    prepopulated_fields = {'slug': ('nama',)}


@admin.register(Prestasi)
class PrestasiAdmin(admin.ModelAdmin):
    """Admin untuk prestasi"""
    
    list_display = ('judul', 'jenis', 'tingkat', 'peringkat', 'gambar_preview',
                   'tanggal', 'is_published', 'is_featured')
    list_filter = ('jenis', 'tingkat', 'peringkat', 'kategori', 'is_published', 'is_featured')
    search_fields = ('judul', 'nama_peraih', 'nama_kompetisi')
    prepopulated_fields = {'slug': ('judul',)}
    date_hierarchy = 'tanggal'
    list_editable = ('is_published', 'is_featured')
    
    fieldsets = (
        ('Informasi Dasar', {
            'fields': ('judul', 'slug', 'kategori', 'jenis')
        }),
        ('Detail Prestasi', {
            'fields': ('tingkat', 'peringkat', 'nama_kompetisi', 'penyelenggara', 
                      'lokasi', 'tanggal')
        }),
        ('Peraih', {
            'fields': ('nama_peraih', 'foto_peraih')
        }),
        ('Deskripsi', {
            'fields': ('deskripsi',)
        }),
        ('Media', {
            'fields': ('gambar', 'video_url', 'link_berita'),
            'classes': ('collapse',)
        }),
        ('Publikasi', {
            'fields': ('is_published', 'is_featured')
        }),
    )
    
    def gambar_preview(self, obj):
        if obj.gambar:
            return format_html('<img src="{}" width="80" height="50" style="object-fit: cover;" />', obj.gambar.url)
        return '-'
    gambar_preview.short_description = 'Gambar'
