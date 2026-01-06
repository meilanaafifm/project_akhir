"""
URL configuration untuk akademik app
"""

from django.urls import path
from . import views

app_name = 'akademik'

urlpatterns = [
    # Dosen
    path('dosen/', views.DosenListView.as_view(), name='dosen_list'),
    path('dosen/<slug:slug>/', views.DosenDetailView.as_view(), name='dosen_detail'),
    
    # Kurikulum
    path('kurikulum/', views.KurikulumView.as_view(), name='kurikulum'),
    path('matakuliah/<slug:slug>/', views.MataKuliahDetailView.as_view(), name='matakuliah_detail'),
    
    # Jadwal
    path('jadwal/', views.JadwalView.as_view(), name='jadwal'),
    
    # Riset Grup
    path('riset-grup/', views.RisetGrupView.as_view(), name='riset_grup'),
    
    # Publikasi
    path('publikasi/', views.PublikasiView.as_view(), name='publikasi'),
    
    # Fasilitas
    path('fasilitas/', views.FasilitasView.as_view(), name='fasilitas'),
]
