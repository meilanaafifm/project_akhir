"""
URL configuration untuk chatbot app
"""

from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('widget/', views.chat_widget, name='widget'),
    path('api/send/', views.chat_send, name='send'),
    path('api/feedback/', views.chat_feedback, name='feedback'),
    path('api/history/<str:session_id>/', views.chat_history, name='history'),
]
