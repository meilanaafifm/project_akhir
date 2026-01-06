"""
URL configuration untuk chatbot app
"""

from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('widget/', views.chatbot_widget, name='widget'),
    path('api/send/', views.chatbot_response, name='send'),
]
