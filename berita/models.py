"""
Models untuk aplikasi Berita
Berisi model untuk berita, kategori, dan tag
"""

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User


class KategoriBerita(models.Model):
    """
    Model untuk kategori berita
    """
    nama = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    deskripsi = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text='Class icon Bootstrap, contoh: bi-newspaper')
    warna = models.CharField(max_length=20, default='primary', help_text='Class warna Bootstrap')
    
    class Meta:
        verbose_name = 'Kategori Berita'
        verbose_name_plural = 'Kategori Berita'
        ordering = ['nama']
    
    def __str__(self):
        return self.nama
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nama)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('berita:kategori_detail', kwargs={'slug': self.slug})


class TagBerita(models.Model):
    """
    Model untuk tag berita
    Inovasi: Tag cloud dengan popularitas
    """
    nama = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)
    
    class Meta:
        verbose_name = 'Tag Berita'
        verbose_name_plural = 'Tag Berita'
        ordering = ['nama']
    
    def __str__(self):
        return self.nama
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nama)
        super().save(*args, **kwargs)
    
    def get_berita_count(self):
        """Menghitung jumlah berita dengan tag ini"""
        return self.berita_set.filter(is_published=True).count()


class Berita(models.Model):
    """
    Model utama untuk berita
    """
    JENIS_CHOICES = [
        ('berita', 'Berita'),
        ('informasi', 'Informasi'),
        ('pengumuman', 'Pengumuman'),
        ('agenda', 'Agenda'),
    ]
    
    judul = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True, max_length=350)
    jenis = models.CharField(max_length=20, choices=JENIS_CHOICES, default='berita')
    kategori = models.ForeignKey(KategoriBerita, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(TagBerita, blank=True)
    
    # Konten
    ringkasan = models.TextField(blank=True, help_text='Ringkasan singkat untuk preview')
    konten = models.TextField(help_text='Konten lengkap berita (mendukung HTML)')
    
    # Media
    gambar_utama = models.ImageField(upload_to='berita/', blank=True)
    gambar_alt = models.CharField(max_length=200, blank=True, help_text='Alt text untuk gambar')
    video_url = models.URLField(blank=True, help_text='URL video YouTube (opsional)')
    
    # Untuk agenda/event
    tanggal_event = models.DateTimeField(blank=True, null=True, help_text='Untuk jenis Agenda')
    lokasi_event = models.CharField(max_length=200, blank=True)
    
    # Meta
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_published = models.BooleanField(default=False, verbose_name='Dipublikasikan')
    is_featured = models.BooleanField(default=False, verbose_name='Berita Unggulan')
    is_pinned = models.BooleanField(default=False, verbose_name='Pin di Atas')
    
    # Statistik
    view_count = models.IntegerField(default=0, verbose_name='Jumlah Dilihat')
    share_count = models.IntegerField(default=0, verbose_name='Jumlah Dibagikan')
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Berita'
        verbose_name_plural = 'Berita'
        ordering = ['-is_pinned', '-published_at']
    
    def __str__(self):
        return self.judul
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.judul)[:300]
            slug = base_slug
            counter = 1
            while Berita.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        
        # Set published_at saat pertama kali dipublish
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('berita:detail', kwargs={'slug': self.slug})
    
    def get_ringkasan(self):
        """Mengembalikan ringkasan atau potongan konten"""
        if self.ringkasan:
            return self.ringkasan
        # Potong konten jika tidak ada ringkasan
        import re
        clean = re.compile('<.*?>')
        text = re.sub(clean, '', self.konten)
        return text[:200] + '...' if len(text) > 200 else text
    
    def increment_view(self):
        """Tambah jumlah view"""
        self.view_count += 1
        self.save(update_fields=['view_count'])
    
    def get_related_berita(self, limit=4):
        """Mendapatkan berita terkait berdasarkan kategori atau tag"""
        related = Berita.objects.filter(
            is_published=True
        ).exclude(pk=self.pk)
        
        if self.kategori:
            related = related.filter(kategori=self.kategori)
        
        return related[:limit]


class GaleriBerita(models.Model):
    """
    Model untuk galeri gambar dalam berita
    Inovasi: Multiple images per berita
    """
    berita = models.ForeignKey(Berita, on_delete=models.CASCADE, related_name='galeri')
    gambar = models.ImageField(upload_to='berita/galeri/')
    caption = models.CharField(max_length=200, blank=True)
    urutan = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Galeri Berita'
        verbose_name_plural = 'Galeri Berita'
        ordering = ['urutan']
    
    def __str__(self):
        return f'Galeri {self.berita.judul[:30]}'


class KomentarBerita(models.Model):
    """
    Model untuk komentar berita
    Inovasi: Sistem komentar dengan moderasi
    """
    berita = models.ForeignKey(Berita, on_delete=models.CASCADE, related_name='komentar')
    nama = models.CharField(max_length=100)
    email = models.EmailField()
    komentar = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    is_approved = models.BooleanField(default=False, verbose_name='Disetujui')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Komentar Berita'
        verbose_name_plural = 'Komentar Berita'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.nama} - {self.berita.judul[:30]}'
