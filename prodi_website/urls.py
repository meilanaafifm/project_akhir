"""
URL configuration for prodi_website project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),
    
    # Main app (homepage, about, contact, dll)
    path('', include('main.urls')),
    
    # Berita dan informasi
    path('berita/', include('berita.urls')),
    
    # Akademik (kurikulum, dosen, jadwal)
    path('akademik/', include('akademik.urls')),
    
    # Prestasi
    path('prestasi/', include('prestasi.urls')),
    
    # Karya mahasiswa
    path('karya/', include('karya.urls')),
    
    # Chatbot AI - Inovasi
    path('chatbot/', include('chatbot.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Customize admin site
admin.site.site_header = 'Admin Panel - Program Studi Teknik Informatika'
admin.site.site_title = 'PTI Admin'
admin.site.index_title = 'Selamat Datang di Panel Administrasi'
