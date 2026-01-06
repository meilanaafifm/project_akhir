"""
Views untuk aplikasi Chatbot
INOVASI: AI Chatbot dengan NLP sederhana
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
import json
import re
import uuid

from .models import ChatbotKnowledge, ChatSession, ChatMessage, ChatbotFeedback, QuickReply


class SimpleChatbot:
    """
    Chatbot dengan algoritma matching sederhana
    """
    
    def __init__(self):
        self.knowledge_base = list(ChatbotKnowledge.objects.filter(is_active=True))
    
    def preprocess(self, text):
        """Membersihkan dan memproses teks input"""
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        return text
    
    def tokenize(self, text):
        """Memecah teks menjadi kata-kata"""
        return text.split()
    
    def calculate_similarity(self, user_input, knowledge):
        """Menghitung skor kecocokan"""
        processed_input = self.preprocess(user_input)
        input_tokens = set(self.tokenize(processed_input))
        
        score = 0
        
        # Cek kecocokan dengan kata kunci
        kata_kunci = knowledge.get_kata_kunci_list()
        for keyword in kata_kunci:
            if keyword in processed_input:
                score += 3  # Bonus jika kata kunci ditemukan
            for token in input_tokens:
                if keyword in token or token in keyword:
                    score += 1
        
        # Cek kecocokan dengan pertanyaan
        pertanyaan_tokens = set(self.tokenize(self.preprocess(knowledge.pertanyaan)))
        common_tokens = input_tokens.intersection(pertanyaan_tokens)
        score += len(common_tokens) * 2
        
        # Bonus prioritas
        score += knowledge.prioritas * 0.5
        
        return score
    
    def get_response(self, user_input):
        """Mendapatkan respons terbaik untuk input user"""
        if not self.knowledge_base:
            return self.get_default_response(), None, 0
        
        best_match = None
        best_score = 0
        
        for knowledge in self.knowledge_base:
            score = self.calculate_similarity(user_input, knowledge)
            if score > best_score:
                best_score = score
                best_match = knowledge
        
        # Threshold untuk jawaban
        if best_score >= 2 and best_match:
            response = best_match.jawaban
            if best_match.link_terkait:
                response += f'\n\n📎 Link terkait: {best_match.link_terkait}'
            confidence = min(best_score / 10, 1.0)
            return response, best_match, confidence
        
        return self.get_default_response(), None, 0
    
    def get_default_response(self):
        """Respons default jika tidak ada kecocokan"""
        return (
            "Maaf, saya belum bisa menjawab pertanyaan tersebut. 😊\n\n"
            "Silakan coba pertanyaan lain atau hubungi kami melalui:\n"
            "📧 Email: pti@ums.ac.id\n"
            "📞 Telepon: (0271) 717417\n\n"
            "Anda juga bisa mengunjungi halaman FAQ untuk informasi lebih lanjut."
        )


def chat_widget(request):
    """
    View untuk menampilkan widget chatbot
    """
    quick_replies = QuickReply.objects.filter(is_active=True)
    return render(request, 'chatbot/widget.html', {
        'quick_replies': quick_replies,
    })


@csrf_exempt
@require_POST
def chat_send(request):
    """
    API untuk mengirim pesan dan mendapatkan respons
    """
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', '')
        
        if not user_message:
            return JsonResponse({'error': 'Pesan kosong'}, status=400)
        
        # Buat atau ambil session
        if not session_id:
            session_id = str(uuid.uuid4())
        
        session, created = ChatSession.objects.get_or_create(
            session_id=session_id,
            defaults={
                'ip_address': request.META.get('REMOTE_ADDR')
            }
        )
        
        # Simpan pesan user
        user_msg = ChatMessage.objects.create(
            session=session,
            sender='user',
            message=user_message
        )
        
        # Dapatkan respons dari chatbot
        chatbot = SimpleChatbot()
        bot_response, matched_knowledge, confidence = chatbot.get_response(user_message)
        
        # Simpan respons bot
        bot_msg = ChatMessage.objects.create(
            session=session,
            sender='bot',
            message=bot_response,
            matched_knowledge=matched_knowledge,
            confidence_score=confidence
        )
        
        # Update last activity
        session.last_activity = timezone.now()
        session.save()
        
        return JsonResponse({
            'status': 'success',
            'session_id': session_id,
            'response': bot_response,
            'message_id': bot_msg.id,
            'confidence': confidence,
        })
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_POST
def chat_feedback(request):
    """
    API untuk memberikan feedback pada respons chatbot
    """
    try:
        data = json.loads(request.body)
        message_id = data.get('message_id')
        rating = data.get('rating')
        komentar = data.get('komentar', '')
        
        if not message_id or not rating:
            return JsonResponse({'error': 'Data tidak lengkap'}, status=400)
        
        message = ChatMessage.objects.get(pk=message_id, sender='bot')
        
        ChatbotFeedback.objects.create(
            message=message,
            rating=rating,
            komentar=komentar
        )
        
        return JsonResponse({'status': 'success'})
    
    except ChatMessage.DoesNotExist:
        return JsonResponse({'error': 'Pesan tidak ditemukan'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def chat_history(request, session_id):
    """
    API untuk mendapatkan riwayat chat
    """
    try:
        session = ChatSession.objects.get(session_id=session_id)
        messages = session.messages.all().values(
            'id', 'sender', 'message', 'timestamp'
        )
        return JsonResponse({
            'status': 'success',
            'messages': list(messages)
        })
    except ChatSession.DoesNotExist:
        return JsonResponse({'error': 'Session tidak ditemukan'}, status=404)
