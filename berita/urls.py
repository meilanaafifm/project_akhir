"""
URL configuration untuk berita app
"""

from django.urls import path
from . import views

app_name = 'berita'

urlpatterns = [
    # Daftar berita
    path('', views.BeritaListView.as_view(), name='list'),
    
    # Agenda
    path('agenda/', views.agenda_list, name='agenda'),
    
    # Kategori
    path('kategori/<slug:slug>/', views.KategoriDetailView.as_view(), name='kategori_detail'),
    
    # Tag
    path('tag/<slug:slug>/', views.TagDetailView.as_view(), name='tag_detail'),
    
    # Detail berita
    path('<slug:slug>/', views.BeritaDetailView.as_view(), name='detail'),
    
    # Share tracking
    path('<slug:slug>/share/', views.share_berita, name='share'),
]
