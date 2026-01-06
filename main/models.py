"""
Models untuk aplikasi Main
Berisi model untuk konfigurasi website, profil prodi, kemitraan, dan statistik
"""

from django.db import models
from django.utils import timezone


class SiteSettings(models.Model):
    """
    Model untuk menyimpan pengaturan website
    Menggunakan Singleton pattern - hanya 1 instance
    """
    site_name = models.CharField(max_length=200, default='Program Studi Teknik Informatika')
    site_tagline = models.CharField(max_length=500, default='Membangun Generasi Digital Indonesia')
    site_description = models.TextField(blank=True)
    university_name = models.CharField(max_length=200, default='Universitas Muhammadiyah Surakarta')
    faculty_name = models.CharField(max_length=200, default='Fakultas Keguruan dan Ilmu Pendidikan')
    
    # Informasi kontak
    address = models.TextField(default='Jl. A. Yani, Mendungan, Pabelan, Kec. Kartasura, Kabupaten Sukoharjo, Jawa Tengah 57162')
    phone = models.CharField(max_length=20, default='(0271) 717417')
    email = models.EmailField(default='pti@ums.ac.id')
    
    # Social media
    instagram = models.URLField(blank=True, default='https://instagram.com/ptiums')
    youtube = models.URLField(blank=True, default='https://youtube.com/@ptiums')
    twitter = models.URLField(blank=True, default='https://twitter.com/ptiums')
    tiktok = models.URLField(blank=True, default='https://tiktok.com/@ptiums')
    
    # Logo dan gambar
    logo = models.ImageField(upload_to='site/', blank=True)
    favicon = models.ImageField(upload_to='site/', blank=True)
    hero_image = models.ImageField(upload_to='site/', blank=True)
    
    # Meta SEO
    meta_keywords = models.TextField(blank=True, help_text='Keywords untuk SEO, pisahkan dengan koma')
    
    # Statistik
    jumlah_mahasiswa_aktif = models.IntegerField(default=0)
    jumlah_alumni = models.IntegerField(default=0)
    jumlah_dosen = models.IntegerField(default=0)
    jumlah_hak_cipta = models.IntegerField(default=0)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Pengaturan Website'
        verbose_name_plural = 'Pengaturan Website'
    
    def __str__(self):
        return self.site_name
    
    def save(self, *args, **kwargs):
        # Singleton pattern - pastikan hanya ada 1 instance
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """Mendapatkan instance settings, buat jika belum ada"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class ProfilProdi(models.Model):
    """
    Model untuk menyimpan profil program studi
    """
    visi = models.TextField(verbose_name='Visi')
    misi = models.TextField(verbose_name='Misi', help_text='Pisahkan setiap poin misi dengan enter baru')
    tujuan = models.TextField(verbose_name='Tujuan', blank=True)
    sejarah = models.TextField(verbose_name='Sejarah', blank=True)
    
    # Ketua Prodi
    nama_kaprodi = models.CharField(max_length=200, verbose_name='Nama Ketua Prodi')
    foto_kaprodi = models.ImageField(upload_to='profil/', blank=True, verbose_name='Foto Kaprodi')
    gelar_kaprodi = models.CharField(max_length=100, blank=True, verbose_name='Gelar')
    sambutan_kaprodi = models.TextField(blank=True, verbose_name='Sambutan Kaprodi')
    
    # Akreditasi
    akreditasi = models.CharField(max_length=10, default='A', verbose_name='Akreditasi')
    nomor_sk_akreditasi = models.CharField(max_length=100, blank=True, verbose_name='Nomor SK Akreditasi')
    tanggal_akreditasi = models.DateField(blank=True, null=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Profil Program Studi'
        verbose_name_plural = 'Profil Program Studi'
    
    def __str__(self):
        return f'Profil Prodi - {self.nama_kaprodi}'
    
    def get_misi_list(self):
        """Mengembalikan daftar misi sebagai list"""
        return [m.strip() for m in self.misi.split('\n') if m.strip()]
    
    def get_tujuan_list(self):
        """Mengembalikan daftar tujuan sebagai list"""
        return [t.strip() for t in self.tujuan.split('\n') if t.strip()]


class Kemitraan(models.Model):
    """
    Model untuk menyimpan informasi kemitraan/partnership
    """
    nama = models.CharField(max_length=200, verbose_name='Nama Mitra')
    logo = models.ImageField(upload_to='kemitraan/', verbose_name='Logo Mitra')
    deskripsi = models.TextField(blank=True, verbose_name='Deskripsi Kerjasama')
    website = models.URLField(blank=True)
    jenis_kerjasama = models.CharField(max_length=100, blank=True, verbose_name='Jenis Kerjasama')
    tanggal_mulai = models.DateField(blank=True, null=True)
    tanggal_berakhir = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    urutan = models.IntegerField(default=0, verbose_name='Urutan Tampil')
    
    class Meta:
        verbose_name = 'Kemitraan'
        verbose_name_plural = 'Kemitraan'
        ordering = ['urutan', 'nama']
    
    def __str__(self):
        return self.nama


class PesanKontak(models.Model):
    """
    Model untuk menyimpan pesan dari form kontak
    """
    STATUS_CHOICES = [
        ('baru', 'Baru'),
        ('dibaca', 'Sudah Dibaca'),
        ('dibalas', 'Sudah Dibalas'),
    ]
    
    nama = models.CharField(max_length=100)
    email = models.EmailField()
    subjek = models.CharField(max_length=200)
    pesan = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='baru')
    created_at = models.DateTimeField(auto_now_add=True)
    replied_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Pesan Kontak'
        verbose_name_plural = 'Pesan Kontak'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.subjek} - {self.nama}'


class Slider(models.Model):
    """
    Model untuk slider/carousel di homepage
    """
    judul = models.CharField(max_length=200)
    subjudul = models.CharField(max_length=500, blank=True)
    gambar = models.ImageField(upload_to='slider/')
    link = models.URLField(blank=True, help_text='URL tujuan saat slider diklik')
    urutan = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Slider'
        verbose_name_plural = 'Slider'
        ordering = ['urutan']
    
    def __str__(self):
        return self.judul


class FAQ(models.Model):
    """
    Model untuk Frequently Asked Questions
    Inovasi: FAQ interaktif dengan pencarian
    """
    KATEGORI_CHOICES = [
        ('akademik', 'Akademik'),
        ('pendaftaran', 'Pendaftaran'),
        ('beasiswa', 'Beasiswa'),
        ('fasilitas', 'Fasilitas'),
        ('karir', 'Karir'),
        ('lainnya', 'Lainnya'),
    ]
    
    pertanyaan = models.CharField(max_length=500)
    jawaban = models.TextField()
    kategori = models.CharField(max_length=20, choices=KATEGORI_CHOICES, default='lainnya')
    urutan = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0, verbose_name='Jumlah Dilihat')
    helpful_count = models.IntegerField(default=0, verbose_name='Jumlah Terbantu')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'
        ordering = ['kategori', 'urutan']
    
    def __str__(self):
        return self.pertanyaan[:50]


class Testimonial(models.Model):
    """
    Model untuk testimonial alumni/mahasiswa
    Inovasi: Testimonial dengan video
    """
    TIPE_CHOICES = [
        ('alumni', 'Alumni'),
        ('mahasiswa', 'Mahasiswa'),
        ('dosen', 'Dosen'),
        ('mitra', 'Mitra'),
    ]
    
    nama = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='testimonial/', blank=True)
    tipe = models.CharField(max_length=20, choices=TIPE_CHOICES, default='alumni')
    angkatan = models.CharField(max_length=10, blank=True, help_text='Tahun angkatan, contoh: 2020')
    pekerjaan = models.CharField(max_length=200, blank=True, help_text='Pekerjaan saat ini')
    perusahaan = models.CharField(max_length=200, blank=True)
    testimoni = models.TextField()
    video_url = models.URLField(blank=True, help_text='Link video YouTube (opsional)')
    rating = models.IntegerField(default=5, help_text='Rating 1-5')
    is_featured = models.BooleanField(default=False, verbose_name='Tampilkan di Homepage')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonial'
        ordering = ['-is_featured', '-created_at']
    
    def __str__(self):
        return f'{self.nama} - {self.tipe}'


class VisitorLog(models.Model):
    """
    Model untuk tracking pengunjung
    Inovasi: Analytics sederhana
    """
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    page_url = models.URLField()
    referrer = models.URLField(blank=True)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    device_type = models.CharField(max_length=50, blank=True)  # desktop, mobile, tablet
    browser = models.CharField(max_length=100, blank=True)
    visited_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Log Pengunjung'
        verbose_name_plural = 'Log Pengunjung'
        ordering = ['-visited_at']
    
    def __str__(self):
        return f'{self.ip_address} - {self.visited_at}'
