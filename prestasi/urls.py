"""
URL configuration untuk prestasi app
"""

from django.urls import path
from . import views

app_name = 'prestasi'

urlpatterns = [
    path('', views.PrestasiListView.as_view(), name='list'),
    path('<slug:slug>/', views.PrestasiDetailView.as_view(), name='detail'),
]
