"""
Models untuk aplikasi Karya Mahasiswa
Berisi model untuk showcase karya mahasiswa
"""

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class KategoriKarya(models.Model):
    """
    Model untuk kategori karya
    """
    nama = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=50, blank=True)
    deskripsi = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Kategori Karya'
        verbose_name_plural = 'Kategori Karya'
        ordering = ['nama']
    
    def __str__(self):
        return self.nama
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nama)
        super().save(*args, **kwargs)


class Teknologi(models.Model):
    """
    Model untuk teknologi yang digunakan
    Inovasi: Tag teknologi untuk filter
    """
    nama = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text='Class icon atau URL')
    
    class Meta:
        verbose_name = 'Teknologi'
        verbose_name_plural = 'Teknologi'
        ordering = ['nama']
    
    def __str__(self):
        return self.nama
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nama)
        super().save(*args, **kwargs)


class KaryaMahasiswa(models.Model):
    """
    Model utama untuk karya mahasiswa
    Inovasi: Portfolio showcase dengan demo link
    """
    JENIS_CHOICES = [
        ('skripsi', 'Skripsi'),
        ('proyek', 'Proyek Akhir'),
        ('penelitian', 'Penelitian'),
        ('aplikasi', 'Aplikasi'),
        ('game', 'Game'),
        ('website', 'Website'),
        ('multimedia', 'Multimedia'),
        ('iot', 'IoT'),
        ('ai_ml', 'AI/Machine Learning'),
        ('vr_ar', 'VR/AR'),
        ('lainnya', 'Lainnya'),
    ]
    
    judul = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True, max_length=350)
    kategori = models.ForeignKey(KategoriKarya, on_delete=models.SET_NULL, null=True, blank=True)
    jenis = models.CharField(max_length=20, choices=JENIS_CHOICES, default='proyek')
    teknologi = models.ManyToManyField(Teknologi, blank=True)
    
    # Pembuat
    nama_pembuat = models.CharField(max_length=200)
    nim_pembuat = models.CharField(max_length=20, blank=True, verbose_name='NIM')
    angkatan = models.CharField(max_length=10, blank=True)
    foto_pembuat = models.ImageField(upload_to='karya/pembuat/', blank=True)
    
    # Pembimbing
    nama_pembimbing = models.CharField(max_length=200, blank=True)
    
    # Deskripsi
    deskripsi = models.TextField()
    fitur = models.TextField(blank=True, help_text='Fitur utama, pisahkan dengan enter')
    
    # Media
    gambar_utama = models.ImageField(upload_to='karya/')
    gambar_2 = models.ImageField(upload_to='karya/', blank=True)
    gambar_3 = models.ImageField(upload_to='karya/', blank=True)
    video_demo = models.URLField(blank=True, help_text='URL video demo (YouTube)')
    
    # Link
    link_demo = models.URLField(blank=True, help_text='Link ke demo/live preview')
    link_github = models.URLField(blank=True, help_text='Link GitHub repository')
    link_playstore = models.URLField(blank=True, help_text='Link Play Store')
    link_download = models.URLField(blank=True, help_text='Link download')
    
    # Meta
    tahun = models.IntegerField(verbose_name='Tahun Pembuatan')
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, verbose_name='Karya Unggulan')
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Karya Mahasiswa'
        verbose_name_plural = 'Karya Mahasiswa'
        ordering = ['-is_featured', '-tahun', '-created_at']
    
    def __str__(self):
        return f'{self.judul} - {self.nama_pembuat}'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.judul)[:300]
            slug = base_slug
            counter = 1
            while KaryaMahasiswa.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('karya:detail', kwargs={'slug': self.slug})
    
    def get_fitur_list(self):
        """Mengembalikan daftar fitur"""
        return [f.strip() for f in self.fitur.split('\n') if f.strip()]
    
    def get_gambar_list(self):
        """Mengembalikan daftar gambar"""
        images = [self.gambar_utama]
        if self.gambar_2:
            images.append(self.gambar_2)
        if self.gambar_3:
            images.append(self.gambar_3)
        return images
