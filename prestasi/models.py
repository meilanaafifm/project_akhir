"""
Models untuk aplikasi Prestasi
Berisi model untuk prestasi mahasiswa dan dosen
"""

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class KategoriPrestasi(models.Model):
    """
    Model untuk kategori prestasi
    """
    nama = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text='Class icon Bootstrap')
    warna = models.CharField(max_length=20, default='warning')
    
    class Meta:
        verbose_name = 'Kategori Prestasi'
        verbose_name_plural = 'Kategori Prestasi'
        ordering = ['nama']
    
    def __str__(self):
        return self.nama
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nama)
        super().save(*args, **kwargs)


class Prestasi(models.Model):
    """
    Model utama untuk prestasi
    """
    TINGKAT_CHOICES = [
        ('internasional', 'Internasional'),
        ('nasional', 'Nasional'),
        ('regional', 'Regional'),
        ('provinsi', 'Provinsi'),
        ('universitas', 'Universitas'),
    ]
    
    PERINGKAT_CHOICES = [
        ('juara_1', 'Juara 1 / Gold Medal'),
        ('juara_2', 'Juara 2 / Silver Medal'),
        ('juara_3', 'Juara 3 / Bronze Medal'),
        ('harapan_1', 'Harapan 1'),
        ('harapan_2', 'Harapan 2'),
        ('harapan_3', 'Harapan 3'),
        ('finalis', 'Finalis'),
        ('nominee', 'Nominee'),
        ('special_award', 'Special Award'),
        ('best_paper', 'Best Paper'),
        ('lainnya', 'Lainnya'),
    ]
    
    JENIS_CHOICES = [
        ('mahasiswa', 'Prestasi Mahasiswa'),
        ('dosen', 'Prestasi Dosen'),
        ('prodi', 'Prestasi Program Studi'),
    ]
    
    judul = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True, max_length=350)
    kategori = models.ForeignKey(KategoriPrestasi, on_delete=models.SET_NULL, null=True, blank=True)
    jenis = models.CharField(max_length=20, choices=JENIS_CHOICES, default='mahasiswa')
    tingkat = models.CharField(max_length=20, choices=TINGKAT_CHOICES)
    peringkat = models.CharField(max_length=20, choices=PERINGKAT_CHOICES)
    
    # Detail
    deskripsi = models.TextField()
    nama_kompetisi = models.CharField(max_length=300, verbose_name='Nama Kompetisi/Event')
    penyelenggara = models.CharField(max_length=200)
    lokasi = models.CharField(max_length=200, blank=True)
    tanggal = models.DateField()
    
    # Peraih
    nama_peraih = models.TextField(help_text='Nama peraih prestasi, pisahkan dengan enter jika lebih dari satu')
    foto_peraih = models.ImageField(upload_to='prestasi/', blank=True)
    
    # Media
    gambar = models.ImageField(upload_to='prestasi/', blank=True)
    video_url = models.URLField(blank=True)
    link_berita = models.URLField(blank=True, help_text='Link ke berita terkait')
    
    # Meta
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, verbose_name='Tampilkan di Homepage')
    view_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Prestasi'
        verbose_name_plural = 'Prestasi'
        ordering = ['-tanggal', '-created_at']
    
    def __str__(self):
        return self.judul
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.judul)[:300]
            slug = base_slug
            counter = 1
            while Prestasi.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('prestasi:detail', kwargs={'slug': self.slug})
    
    def get_nama_peraih_list(self):
        """Mengembalikan daftar nama peraih"""
        return [n.strip() for n in self.nama_peraih.split('\n') if n.strip()]
    
    def get_peringkat_badge_class(self):
        """Mengembalikan class CSS untuk badge peringkat"""
        badge_map = {
            'juara_1': 'bg-warning text-dark',
            'juara_2': 'bg-secondary',
            'juara_3': 'bg-bronze',
            'special_award': 'bg-info',
            'best_paper': 'bg-success',
        }
        return badge_map.get(self.peringkat, 'bg-primary')
