"""
URL configuration untuk main app
"""

from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    # Homepage
    path('', views.HomeView.as_view(), name='home'),
    
    # Tentang Kami
    path('tentang-kami/', views.TentangKamiView.as_view(), name='tentang_kami'),
    path('visi-misi/', views.VisiMisiView.as_view(), name='visi_misi'),
    
    # FAQ
    path('faq/', views.FAQListView.as_view(), name='faq'),
    path('faq/<int:pk>/helpful/', views.faq_helpful, name='faq_helpful'),
    
    # Kontak
    path('kontak/', views.KontakView.as_view(), name='kontak'),
    
    # Kemitraan
    path('kemitraan/', views.KemitraanListView.as_view(), name='kemitraan'),
    
    # Testimonial
    path('testimonial/', views.TestimonialListView.as_view(), name='testimonial'),
    
    # Search
    path('search/', views.search_view, name='search'),
    path('api/live-search/', views.live_search, name='live_search'),
]
