"""
Admin configuration untuk chatbot app
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import ChatbotKnowledge, ChatSession, ChatMessage, ChatbotFeedback, QuickReply


@admin.register(ChatbotKnowledge)
class ChatbotKnowledgeAdmin(admin.ModelAdmin):
    """Admin untuk knowledge base chatbot"""
    
    list_display = ('pertanyaan_short', 'kategori', 'prioritas', 'is_active')
    list_filter = ('kategori', 'is_active')
    search_fields = ('pertanyaan', 'kata_kunci', 'jawaban')
    list_editable = ('prioritas', 'is_active')
    
    fieldsets = (
        ('Pertanyaan', {
            'fields': ('kategori', 'pertanyaan', 'kata_kunci')
        }),
        ('Jawaban', {
            'fields': ('jawaban', 'link_terkait')
        }),
        ('Pengaturan', {
            'fields': ('prioritas', 'is_active')
        }),
    )
    
    def pertanyaan_short(self, obj):
        return obj.pertanyaan[:60] + '...' if len(obj.pertanyaan) > 60 else obj.pertanyaan
    pertanyaan_short.short_description = 'Pertanyaan'


class ChatMessageInline(admin.TabularInline):
    """Inline untuk pesan dalam sesi"""
    model = ChatMessage
    extra = 0
    readonly_fields = ('sender', 'message', 'timestamp', 'confidence_score')
    can_delete = False


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    """Admin untuk sesi chat"""
    
    list_display = ('session_id_short', 'ip_address', 'message_count', 'started_at', 'last_activity')
    list_filter = ('started_at',)
    search_fields = ('session_id', 'ip_address')
    readonly_fields = ('session_id', 'ip_address', 'started_at', 'last_activity')
    date_hierarchy = 'started_at'
    
    inlines = [ChatMessageInline]
    
    def session_id_short(self, obj):
        return obj.session_id[:8] + '...'
    session_id_short.short_description = 'Session ID'
    
    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Jumlah Pesan'
    
    def has_add_permission(self, request):
        return False


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    """Admin untuk pesan chat"""
    
    list_display = ('message_short', 'sender', 'session', 'confidence_score', 'timestamp')
    list_filter = ('sender', 'timestamp')
    search_fields = ('message',)
    readonly_fields = ('session', 'sender', 'message', 'timestamp', 'matched_knowledge', 'confidence_score')
    date_hierarchy = 'timestamp'
    
    def message_short(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_short.short_description = 'Pesan'
    
    def has_add_permission(self, request):
        return False


@admin.register(ChatbotFeedback)
class ChatbotFeedbackAdmin(admin.ModelAdmin):
    """Admin untuk feedback chatbot"""
    
    list_display = ('message_short', 'rating', 'komentar_short', 'created_at')
    list_filter = ('rating', 'created_at')
    readonly_fields = ('message', 'rating', 'komentar', 'created_at')
    
    def message_short(self, obj):
        return obj.message.message[:30] + '...'
    message_short.short_description = 'Pesan'
    
    def komentar_short(self, obj):
        return obj.komentar[:30] + '...' if len(obj.komentar) > 30 else obj.komentar
    komentar_short.short_description = 'Komentar'
    
    def has_add_permission(self, request):
        return False


@admin.register(QuickReply)
class QuickReplyAdmin(admin.ModelAdmin):
    """Admin untuk quick reply"""
    
    list_display = ('teks', 'urutan', 'is_active')
    list_editable = ('urutan', 'is_active')
    ordering = ('urutan',)
