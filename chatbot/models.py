"""
Models untuk aplikasi Chatbot
INOVASI UTAMA: AI Chatbot untuk menjawab pertanyaan pengunjung
"""

from django.db import models
import json


class ChatbotKnowledge(models.Model):
    """
    Model untuk knowledge base chatbot
    """
    KATEGORI_CHOICES = [
        ('pendaftaran', 'Pendaftaran'),
        ('akademik', 'Akademik'),
        ('kurikulum', 'Kurikulum'),
        ('fasilitas', 'Fasilitas'),
        ('beasiswa', 'Beasiswa'),
        ('karir', 'Karir'),
        ('kontak', 'Kontak'),
        ('umum', 'Umum'),
    ]
    
    kategori = models.CharField(max_length=20, choices=KATEGORI_CHOICES)
    pertanyaan = models.TextField(help_text='Pertanyaan atau kata kunci yang mungkin diajukan')
    kata_kunci = models.TextField(help_text='Kata kunci terkait, pisahkan dengan koma')
    jawaban = models.TextField()
    link_terkait = models.URLField(blank=True, help_text='Link ke halaman terkait')
    prioritas = models.IntegerField(default=0, help_text='Semakin tinggi, semakin diprioritaskan')
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Knowledge Base'
        verbose_name_plural = 'Knowledge Base'
        ordering = ['-prioritas', 'kategori']
    
    def __str__(self):
        return f'{self.kategori}: {self.pertanyaan[:50]}'
    
    def get_kata_kunci_list(self):
        """Mengembalikan daftar kata kunci"""
        return [k.strip().lower() for k in self.kata_kunci.split(',') if k.strip()]


class ChatSession(models.Model):
    """
    Model untuk menyimpan sesi chat
    """
    session_id = models.CharField(max_length=100, unique=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Sesi Chat'
        verbose_name_plural = 'Sesi Chat'
        ordering = ['-started_at']
    
    def __str__(self):
        return f'Session {self.session_id[:8]}...'


class ChatMessage(models.Model):
    """
    Model untuk menyimpan pesan chat
    """
    SENDER_CHOICES = [
        ('user', 'User'),
        ('bot', 'Bot'),
    ]
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Untuk analisis
    matched_knowledge = models.ForeignKey(
        ChatbotKnowledge, on_delete=models.SET_NULL, 
        null=True, blank=True, related_name='matched_messages'
    )
    confidence_score = models.FloatField(default=0.0)
    
    class Meta:
        verbose_name = 'Pesan Chat'
        verbose_name_plural = 'Pesan Chat'
        ordering = ['timestamp']
    
    def __str__(self):
        return f'{self.sender}: {self.message[:50]}'


class ChatbotFeedback(models.Model):
    """
    Model untuk feedback chatbot
    INOVASI: Sistem feedback untuk meningkatkan akurasi
    """
    RATING_CHOICES = [
        (1, 'Tidak Membantu'),
        (2, 'Kurang Membantu'),
        (3, 'Cukup Membantu'),
        (4, 'Membantu'),
        (5, 'Sangat Membantu'),
    ]
    
    message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE, related_name='feedback')
    rating = models.IntegerField(choices=RATING_CHOICES)
    komentar = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Feedback Chatbot'
        verbose_name_plural = 'Feedback Chatbot'
    
    def __str__(self):
        return f'Rating {self.rating} untuk {self.message}'


class QuickReply(models.Model):
    """
    Model untuk quick reply suggestions
    """
    teks = models.CharField(max_length=100)
    urutan = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Quick Reply'
        verbose_name_plural = 'Quick Reply'
        ordering = ['urutan']
    
    def __str__(self):
        return self.teks
