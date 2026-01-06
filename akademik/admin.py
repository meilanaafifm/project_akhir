"""
Admin configuration untuk akademik app
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Dosen, RisetGrup, Kurikulum, MataKuliah,
    JadwalKuliah, Publikasi, Fasilitas
)


@admin.register(Dosen)
class DosenAdmin(admin.ModelAdmin):
    """Admin untuk dosen"""
    
    list_display = ('get_full_name', 'foto_preview', 'jabatan_fungsional', 
                   'bidang_keahlian', 'is_kaprodi', 'is_active')
    list_filter = ('jabatan_fungsional', 'is_active', 'is_kaprodi')
    search_fields = ('nama', 'nip', 'bidang_keahlian')
    prepopulated_fields = {'slug': ('nama',)}
    list_editable = ('is_active',)
    
    fieldsets = (
        ('Data Pribadi', {
            'fields': ('nama', 'slug', 'nip', 'email', 'phone', 'foto')
        }),
        ('Data Akademik', {
            'fields': ('jabatan_fungsional', 'gelar_depan', 'gelar_belakang', 'bidang_keahlian')
        }),
        ('Pendidikan', {
            'fields': ('pendidikan_s1', 'pendidikan_s2', 'pendidikan_s3'),
            'classes': ('collapse',)
        }),
        ('Biodata', {
            'fields': ('bio', 'research_interest'),
            'classes': ('collapse',)
        }),
        ('Link Profil', {
            'fields': ('google_scholar', 'scopus', 'sinta', 'orcid', 'website'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active', 'is_kaprodi', 'urutan')
        }),
    )
    
    def foto_preview(self, obj):
        if obj.foto:
            return format_html('<img src="{}" width="40" height="40" style="border-radius: 50%; object-fit: cover;" />', obj.foto.url)
        return '-'
    foto_preview.short_description = 'Foto'


@admin.register(RisetGrup)
class RisetGrupAdmin(admin.ModelAdmin):
    """Admin untuk riset grup"""
    
    list_display = ('nama', 'ketua', 'is_active')
    prepopulated_fields = {'slug': ('nama',)}
    filter_horizontal = ('anggota',)


class MataKuliahInline(admin.TabularInline):
    """Inline untuk mata kuliah dalam kurikulum"""
    model = MataKuliah
    extra = 1
    fields = ('kode', 'nama', 'semester', 'sks_teori', 'sks_praktik', 'jenis')


@admin.register(Kurikulum)
class KurikulumAdmin(admin.ModelAdmin):
    """Admin untuk kurikulum"""
    
    list_display = ('nama', 'tahun', 'is_active')
    list_filter = ('is_active',)
    inlines = [MataKuliahInline]


@admin.register(MataKuliah)
class MataKuliahAdmin(admin.ModelAdmin):
    """Admin untuk mata kuliah"""
    
    list_display = ('kode', 'nama', 'kurikulum', 'semester', 'total_sks', 'jenis')
    list_filter = ('kurikulum', 'semester', 'jenis')
    search_fields = ('kode', 'nama')
    filter_horizontal = ('prasyarat', 'dosen_pengampu')


@admin.register(JadwalKuliah)
class JadwalKuliahAdmin(admin.ModelAdmin):
    """Admin untuk jadwal kuliah"""
    
    list_display = ('mata_kuliah', 'kelas', 'hari', 'jam_mulai', 'jam_selesai', 
                   'ruangan', 'dosen', 'is_active')
    list_filter = ('semester_aktif', 'hari', 'is_active')
    search_fields = ('mata_kuliah__nama', 'mata_kuliah__kode')
    list_editable = ('is_active',)


@admin.register(Publikasi)
class PublikasiAdmin(admin.ModelAdmin):
    """Admin untuk publikasi"""
    
    list_display = ('judul_short', 'jenis', 'tahun', 'is_indexed')
    list_filter = ('jenis', 'tahun', 'is_indexed')
    search_fields = ('judul', 'penulis_text')
    filter_horizontal = ('penulis',)
    
    def judul_short(self, obj):
        return obj.judul[:60] + '...' if len(obj.judul) > 60 else obj.judul
    judul_short.short_description = 'Judul'


@admin.register(Fasilitas)
class FasilitasAdmin(admin.ModelAdmin):
    """Admin untuk fasilitas"""
    
    list_display = ('nama', 'gambar_preview', 'lokasi', 'urutan', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('urutan', 'is_active')
    
    def gambar_preview(self, obj):
        if obj.gambar:
            return format_html('<img src="{}" width="80" height="50" style="object-fit: cover;" />', obj.gambar.url)
        return '-'
    gambar_preview.short_description = 'Gambar'
