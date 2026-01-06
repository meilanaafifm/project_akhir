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
    path('matakuliah/<str:kode>/', views.MataKuliahDetailView.as_view(), name='matakuliah_detail'),
    
    # Jadwal
    path('jadwal/', views.JadwalKuliahView.as_view(), name='jadwal'),
    path('api/jadwal/', views.jadwal_api, name='jadwal_api'),
    
    # Riset Grup
    path('riset-grup/', views.RisetGrupListView.as_view(), name='riset_grup'),
    
    # Publikasi
    path('publikasi/', views.PublikasiListView.as_view(), name='publikasi'),
    
    # Fasilitas
    path('fasilitas/', views.FasilitasListView.as_view(), name='fasilitas'),
]
