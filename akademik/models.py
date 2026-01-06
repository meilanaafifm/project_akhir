"""
Models untuk aplikasi Akademik
Berisi model untuk dosen, kurikulum, mata kuliah, jadwal, dan riset grup
"""

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Dosen(models.Model):
    """
    Model untuk data dosen
    """
    JABATAN_CHOICES = [
        ('guru_besar', 'Guru Besar'),
        ('lektor_kepala', 'Lektor Kepala'),
        ('lektor', 'Lektor'),
        ('asisten_ahli', 'Asisten Ahli'),
        ('tenaga_pengajar', 'Tenaga Pengajar'),
    ]
    
    # Data pribadi
    nama = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    nip = models.CharField(max_length=50, blank=True, verbose_name='NIP/NIDN')
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    foto = models.ImageField(upload_to='dosen/', blank=True)
    
    # Data akademik
    jabatan_fungsional = models.CharField(max_length=50, choices=JABATAN_CHOICES, blank=True)
    gelar_depan = models.CharField(max_length=50, blank=True)
    gelar_belakang = models.CharField(max_length=100, blank=True)
    bidang_keahlian = models.CharField(max_length=200, blank=True)
    
    # Pendidikan
    pendidikan_s1 = models.CharField(max_length=200, blank=True, verbose_name='Pendidikan S1')
    pendidikan_s2 = models.CharField(max_length=200, blank=True, verbose_name='Pendidikan S2')
    pendidikan_s3 = models.CharField(max_length=200, blank=True, verbose_name='Pendidikan S3')
    
    # Biodata
    bio = models.TextField(blank=True, verbose_name='Biografi')
    research_interest = models.TextField(blank=True, verbose_name='Minat Penelitian')
    
    # Link
    google_scholar = models.URLField(blank=True, verbose_name='Google Scholar')
    scopus = models.URLField(blank=True, verbose_name='Scopus')
    sinta = models.URLField(blank=True, verbose_name='SINTA')
    orcid = models.URLField(blank=True, verbose_name='ORCID')
    website = models.URLField(blank=True, verbose_name='Website Pribadi')
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    is_kaprodi = models.BooleanField(default=False, verbose_name='Ketua Prodi')
    urutan = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Dosen'
        verbose_name_plural = 'Dosen'
        ordering = ['-is_kaprodi', 'urutan', 'nama']
    
    def __str__(self):
        return self.get_full_name()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nama)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('akademik:dosen_detail', kwargs={'slug': self.slug})
    
    def get_full_name(self):
        """Mengembalikan nama lengkap dengan gelar"""
        parts = []
        if self.gelar_depan:
            parts.append(self.gelar_depan)
        parts.append(self.nama)
        if self.gelar_belakang:
            parts.append(self.gelar_belakang)
        return ' '.join(parts)


class RisetGrup(models.Model):
    """
    Model untuk riset grup
    """
    nama = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    deskripsi = models.TextField()
    fokus_riset = models.TextField(blank=True, help_text='Pisahkan setiap fokus dengan enter baru')
    gambar = models.ImageField(upload_to='riset/', blank=True)
    ketua = models.ForeignKey(Dosen, on_delete=models.SET_NULL, null=True, 
                              related_name='ketua_riset_grup')
    anggota = models.ManyToManyField(Dosen, blank=True, related_name='riset_grup')
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Riset Grup'
        verbose_name_plural = 'Riset Grup'
        ordering = ['nama']
    
    def __str__(self):
        return self.nama
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nama)
        super().save(*args, **kwargs)
    
    def get_fokus_list(self):
        """Mengembalikan daftar fokus riset sebagai list"""
        if not self.fokus_riset:
            return []
        return [f.strip() for f in self.fokus_riset.split('\n') if f.strip()]


class Kurikulum(models.Model):
    """
    Model untuk kurikulum
    """
    nama = models.CharField(max_length=200, verbose_name='Nama Kurikulum')
    tahun = models.CharField(max_length=10, verbose_name='Tahun Kurikulum')
    deskripsi = models.TextField(blank=True)
    file_kurikulum = models.FileField(upload_to='kurikulum/', blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Kurikulum Aktif')
    
    class Meta:
        verbose_name = 'Kurikulum'
        verbose_name_plural = 'Kurikulum'
        ordering = ['-tahun']
    
    def __str__(self):
        return f'{self.nama} ({self.tahun})'


class MataKuliah(models.Model):
    """
    Model untuk mata kuliah
    """
    SEMESTER_CHOICES = [
        (1, 'Semester 1'),
        (2, 'Semester 2'),
        (3, 'Semester 3'),
        (4, 'Semester 4'),
        (5, 'Semester 5'),
        (6, 'Semester 6'),
        (7, 'Semester 7'),
        (8, 'Semester 8'),
    ]
    
    JENIS_CHOICES = [
        ('wajib', 'Wajib'),
        ('pilihan', 'Pilihan'),
        ('praktikum', 'Praktikum'),
    ]
    
    kurikulum = models.ForeignKey(Kurikulum, on_delete=models.CASCADE, related_name='mata_kuliah')
    kode = models.CharField(max_length=20, verbose_name='Kode MK')
    nama = models.CharField(max_length=200, verbose_name='Nama Mata Kuliah')
    semester = models.IntegerField(choices=SEMESTER_CHOICES)
    sks_teori = models.IntegerField(default=0, verbose_name='SKS Teori')
    sks_praktik = models.IntegerField(default=0, verbose_name='SKS Praktik')
    jenis = models.CharField(max_length=20, choices=JENIS_CHOICES, default='wajib')
    deskripsi = models.TextField(blank=True)
    capaian_pembelajaran = models.TextField(blank=True, verbose_name='Capaian Pembelajaran')
    prasyarat = models.ManyToManyField('self', blank=True, symmetrical=False, 
                                       related_name='prasyarat_untuk')
    dosen_pengampu = models.ManyToManyField(Dosen, blank=True, related_name='mata_kuliah_diampu')
    
    class Meta:
        verbose_name = 'Mata Kuliah'
        verbose_name_plural = 'Mata Kuliah'
        ordering = ['semester', 'kode']
        unique_together = ['kurikulum', 'kode']
    
    def __str__(self):
        return f'{self.kode} - {self.nama}'
    
    @property
    def total_sks(self):
        return self.sks_teori + self.sks_praktik


class JadwalKuliah(models.Model):
    """
    Model untuk jadwal kuliah
    Inovasi: Jadwal interaktif dengan filter
    """
    HARI_CHOICES = [
        ('senin', 'Senin'),
        ('selasa', 'Selasa'),
        ('rabu', 'Rabu'),
        ('kamis', 'Kamis'),
        ('jumat', 'Jumat'),
        ('sabtu', 'Sabtu'),
    ]
    
    mata_kuliah = models.ForeignKey(MataKuliah, on_delete=models.CASCADE, 
                                    related_name='jadwal')
    semester_aktif = models.CharField(max_length=20, verbose_name='Semester Aktif',
                                     help_text='Contoh: Gasal 2025/2026')
    kelas = models.CharField(max_length=10)
    hari = models.CharField(max_length=10, choices=HARI_CHOICES)
    jam_mulai = models.TimeField()
    jam_selesai = models.TimeField()
    ruangan = models.CharField(max_length=50)
    dosen = models.ForeignKey(Dosen, on_delete=models.SET_NULL, null=True, blank=True)
    kapasitas = models.IntegerField(default=40)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Jadwal Kuliah'
        verbose_name_plural = 'Jadwal Kuliah'
        ordering = ['hari', 'jam_mulai']
    
    def __str__(self):
        return f'{self.mata_kuliah.kode} - {self.kelas} ({self.hari})'


class Publikasi(models.Model):
    """
    Model untuk publikasi dosen
    Inovasi: Database publikasi terintegrasi
    """
    JENIS_CHOICES = [
        ('jurnal_intl', 'Jurnal Internasional'),
        ('jurnal_nas', 'Jurnal Nasional'),
        ('konferensi_intl', 'Konferensi Internasional'),
        ('konferensi_nas', 'Konferensi Nasional'),
        ('buku', 'Buku'),
        ('book_chapter', 'Book Chapter'),
        ('hki', 'Hak Kekayaan Intelektual'),
    ]
    
    judul = models.CharField(max_length=500)
    penulis = models.ManyToManyField(Dosen, related_name='publikasi')
    penulis_text = models.TextField(help_text='Nama penulis lengkap, pisahkan dengan koma')
    jenis = models.CharField(max_length=20, choices=JENIS_CHOICES)
    nama_jurnal = models.CharField(max_length=300, blank=True, 
                                   verbose_name='Nama Jurnal/Prosiding')
    tahun = models.IntegerField()
    volume = models.CharField(max_length=20, blank=True)
    issue = models.CharField(max_length=20, blank=True)
    halaman = models.CharField(max_length=20, blank=True)
    doi = models.CharField(max_length=200, blank=True, verbose_name='DOI')
    url = models.URLField(blank=True)
    abstrak = models.TextField(blank=True)
    is_indexed = models.BooleanField(default=False, verbose_name='Terindeks Scopus/WoS')
    
    class Meta:
        verbose_name = 'Publikasi'
        verbose_name_plural = 'Publikasi'
        ordering = ['-tahun', 'judul']
    
    def __str__(self):
        return f'{self.judul[:50]} ({self.tahun})'


class Fasilitas(models.Model):
    """
    Model untuk fasilitas prodi
    """
    nama = models.CharField(max_length=200)
    deskripsi = models.TextField()
    gambar = models.ImageField(upload_to='fasilitas/')
    kapasitas = models.CharField(max_length=50, blank=True)
    lokasi = models.CharField(max_length=200, blank=True)
    urutan = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Fasilitas'
        verbose_name_plural = 'Fasilitas'
        ordering = ['urutan']
    
    def __str__(self):
        return self.nama
