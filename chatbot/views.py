"""
Views untuk aplikasi Chatbot - Compatible with Vercel
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os

IS_VERCEL = os.environ.get('VERCEL', False)


def chatbot_widget(request):
    """Render chatbot widget"""
    return render(request, 'chatbot/widget.html')


@csrf_exempt
def chatbot_response(request):
    """Handle chatbot messages"""
    if request.method == 'POST':
        message = request.POST.get('message', '')
        
        # Simple response for demo
        responses = {
            'halo': 'Halo! Selamat datang di Program Studi Teknik Informatika. Ada yang bisa saya bantu?',
            'pendaftaran': 'Untuk informasi pendaftaran, silakan kunjungi halaman PMB atau hubungi bagian admisi.',
            'akreditasi': 'Program Studi kami terakreditasi A oleh BAN-PT.',
            'biaya': 'Informasi biaya kuliah dapat dilihat di website resmi universitas atau hubungi bagian keuangan.',
            'kurikulum': 'Kurikulum kami berbasis KKNI dan disesuaikan dengan kebutuhan industri.',
        }
        
        # Find matching response
        response = 'Terima kasih atas pertanyaannya. Untuk informasi lebih lanjut, silakan hubungi kami melalui halaman Kontak.'
        for key, val in responses.items():
            if key in message.lower():
                response = val
                break
        
        return JsonResponse({
            'status': 'success',
            'response': response
        })
    
    return JsonResponse({'status': 'error'}, status=400)
