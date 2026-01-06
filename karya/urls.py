"""
URL configuration untuk karya app
"""

from django.urls import path
from . import views

app_name = 'karya'

urlpatterns = [
    path('', views.KaryaListView.as_view(), name='list'),
    path('<slug:slug>/', views.KaryaDetailView.as_view(), name='detail'),
    path('<slug:slug>/like/', views.like_karya, name='like'),
]
