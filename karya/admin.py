"""
Admin configuration untuk karya app
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import KaryaMahasiswa, KategoriKarya, Teknologi


@admin.register(KategoriKarya)
class KategoriKaryaAdmin(admin.ModelAdmin):
    """Admin untuk kategori karya"""
    list_display = ('nama', 'slug', 'icon')
    prepopulated_fields = {'slug': ('nama',)}


@admin.register(Teknologi)
class TeknologiAdmin(admin.ModelAdmin):
    """Admin untuk teknologi"""
    list_display = ('nama', 'slug', 'icon')
    prepopulated_fields = {'slug': ('nama',)}
    search_fields = ('nama',)


@admin.register(KaryaMahasiswa)
class KaryaMahasiswaAdmin(admin.ModelAdmin):
    """Admin untuk karya mahasiswa"""
    
    list_display = ('judul', 'nama_pembuat', 'jenis', 'gambar_preview', 
                   'tahun', 'view_count', 'like_count', 'is_published', 'is_featured')
    list_filter = ('jenis', 'kategori', 'tahun', 'is_published', 'is_featured')
    search_fields = ('judul', 'nama_pembuat', 'deskripsi')
    prepopulated_fields = {'slug': ('judul',)}
    filter_horizontal = ('teknologi',)
    list_editable = ('is_published', 'is_featured')
    
    fieldsets = (
        ('Informasi Dasar', {
            'fields': ('judul', 'slug', 'kategori', 'jenis', 'teknologi', 'tahun')
        }),
        ('Pembuat', {
            'fields': ('nama_pembuat', 'nim_pembuat', 'angkatan', 'foto_pembuat', 
                      'nama_pembimbing')
        }),
        ('Deskripsi', {
            'fields': ('deskripsi', 'fitur')
        }),
        ('Media', {
            'fields': ('gambar_utama', 'gambar_2', 'gambar_3', 'video_demo')
        }),
        ('Link', {
            'fields': ('link_demo', 'link_github', 'link_playstore', 'link_download'),
            'classes': ('collapse',)
        }),
        ('Publikasi', {
            'fields': ('is_published', 'is_featured')
        }),
        ('Statistik', {
            'fields': ('view_count', 'like_count'),
            'classes': ('collapse',)
        }),
    )
    
    def gambar_preview(self, obj):
        if obj.gambar_utama:
            return format_html('<img src="{}" width="80" height="50" style="object-fit: cover;" />', obj.gambar_utama.url)
        return '-'
    gambar_preview.short_description = 'Gambar'
