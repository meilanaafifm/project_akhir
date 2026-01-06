"""
Views untuk aplikasi Chatbot
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import ChatbotKnowledge, ChatMessage


def chatbot_widget(request):
    """Render chatbot widget"""
    return render(request, 'chatbot/widget.html')


@csrf_exempt
def chatbot_response(request):
    """Handle chatbot messages"""
    if request.method == 'POST':
        message = request.POST.get('message', '').lower().strip()
        
        # Cari response dari database
        response_text = None
        
        # Cek keyword match
        try:
            responses = ChatbotKnowledge.objects.filter(is_active=True).order_by('-prioritas')
            for resp in responses:
                keywords = [k.strip().lower() for k in resp.kata_kunci.split(',')]
                for keyword in keywords:
                    if keyword in message:
                        response_text = resp.jawaban
                        break
                if response_text:
                    break
        except:
            pass
        
        # Default response jika tidak ada match
        if not response_text:
            response_text = 'Terima kasih atas pertanyaannya. Untuk informasi lebih lanjut, silakan hubungi kami melalui halaman Kontak atau email ke prodi@universitas.ac.id'
        
        return JsonResponse({
            'status': 'success',
            'response': response_text
        })
    
    return JsonResponse({'status': 'error'}, status=400)
