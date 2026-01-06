# 🎓 Website Program Studi dengan Django

Website Program Studi yang dibangun menggunakan Django Framework dengan berbagai inovasi modern.

## 📋 Fitur Utama

### 1. **Homepage Interaktif**
- Hero section dengan slider
- Statistik program studi
- Berita terbaru
- Prestasi mahasiswa
- Testimonial

### 2. **Modul Berita**
- Kategorisasi berita
- Tag sistem
- Galeri foto per berita
- Sistem komentar
- Sharing ke social media

### 3. **Modul Akademik**
- Profil dosen lengkap
- Kurikulum per tahun
- Jadwal kuliah
- Publikasi ilmiah
- Grup riset
- Fasilitas

### 4. **Modul Prestasi**
- Filter berdasarkan tingkat (Internasional, Nasional, Regional)
- Peringkat (Juara 1, 2, 3, dst)
- Sertifikat dan dokumentasi

### 5. **Modul Karya Mahasiswa**
- Showcase project mahasiswa
- Filter berdasarkan teknologi
- Sistem like
- Link demo & GitHub

### 6. **🤖 AI Chatbot (INOVASI UTAMA)**
- Chatbot berbasis knowledge base
- Quick reply buttons
- Typing indicator
- Session tracking
- Feedback system

### 7. **Fitur Tambahan**
- Live search
- FAQ dengan rating
- Form kontak
- Newsletter
- Responsive design

## 🛠️ Teknologi yang Digunakan

- **Backend**: Django 4.2
- **Frontend**: Bootstrap 5.3, CSS Custom
- **Database**: SQLite (development) / PostgreSQL (production)
- **Icons**: Bootstrap Icons
- **Animations**: AOS (Animate on Scroll)
- **Font**: Plus Jakarta Sans

## 📁 Struktur Folder

```
prodi_website/
├── prodi_website/          # Project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── main/                   # Main app
│   ├── models.py           # SiteSettings, ProfilProdi, FAQ, dll
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── berita/                 # Berita/News app
│   ├── models.py           # Berita, Kategori, Tag, Komentar
│   ├── views.py
│   └── admin.py
├── akademik/               # Akademik app
│   ├── models.py           # Dosen, Kurikulum, MataKuliah
│   ├── views.py
│   └── admin.py
├── prestasi/               # Prestasi app
│   ├── models.py           # Prestasi, Kategori
│   ├── views.py
│   └── admin.py
├── karya/                  # Karya Mahasiswa app
│   ├── models.py           # Karya, Teknologi
│   ├── views.py
│   └── admin.py
├── chatbot/                # Chatbot app (INOVASI)
│   ├── models.py           # Knowledge, Session, Message
│   ├── views.py
│   └── chatbot.py          # AI Logic
├── templates/              # HTML Templates
├── static/                 # CSS, JS, Images
└── media/                  # User uploaded files
```

## 🚀 Cara Menjalankan

### 1. Clone & Setup Virtual Environment

```bash
cd prodi_website
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Database

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Buat Superuser

```bash
python manage.py createsuperuser
```

### 5. Jalankan Server

```bash
python manage.py runserver
```

### 6. Akses Website

- Website: http://127.0.0.1:8000
- Admin: http://127.0.0.1:8000/admin

## 📝 Penjelasan Inovasi

### 1. AI Chatbot
Chatbot menggunakan algoritma NLP sederhana dengan:
- **Keyword Matching**: Mencari kata kunci dalam knowledge base
- **Similarity Score**: Menghitung kecocokan dengan pertanyaan
- **Quick Replies**: Saran pertanyaan otomatis
- **Session Tracking**: Menyimpan riwayat percakapan
- **Feedback System**: User dapat memberikan rating jawaban

```python
# Contoh algoritma chatbot (chatbot/chatbot.py)
class SimpleChatbot:
    def get_response(self, message):
        # Preprocessing
        words = self.preprocess(message)
        
        # Find best match in knowledge base
        best_match = None
        best_score = 0
        
        for knowledge in ChatbotKnowledge.objects.all():
            score = self.calculate_similarity(words, knowledge.keywords)
            if score > best_score:
                best_score = score
                best_match = knowledge
        
        return best_match.answer if best_score > 0.3 else default_response
```

### 2. Live Search
Pencarian real-time tanpa reload halaman menggunakan JavaScript fetch API.

### 3. Visitor Analytics
Tracking pengunjung dengan:
- IP Address hashing
- User Agent
- Page views
- Session duration

### 4. Like System
Sistem like untuk karya mahasiswa dengan proteksi duplikasi berdasarkan session/cookies.

### 5. Dynamic FAQ
FAQ dengan:
- Kategori
- Search
- Rating helpful/not helpful
- Auto-suggest dari chatbot

## 🔧 Konfigurasi

### Environment Variables (opsional)
Buat file `.env` di root folder:

```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
```

### Static Files (Production)
```bash
python manage.py collectstatic
```

## 📱 Responsive Design

Website sudah responsive untuk berbagai ukuran layar:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (< 768px)

## 🎨 Customization

### Mengubah Warna Theme
Edit file `static/css/style.css`:

```css
:root {
    --primary-color: #2563eb;
    --primary-dark: #1d4ed8;
    /* Ubah warna sesuai keinginan */
}
```

### Mengubah Logo
Upload logo melalui Admin Panel:
- Settings > Site Settings > Logo

## 📚 Dokumentasi API

### Chatbot API
```
POST /chatbot/send/
Content-Type: application/json

{
    "message": "Apa syarat pendaftaran?"
}

Response:
{
    "response": "Syarat pendaftaran adalah...",
    "quick_replies": ["Biaya kuliah", "Jadwal pendaftaran"]
}
```

### Like Karya API
```
POST /karya/{slug}/like/

Response:
{
    "status": "liked",
    "like_count": 42
}
```

## 👨‍💻 Pengembang

Dibuat untuk Tugas Akhir Pemrograman Web

## 📄 Lisensi

MIT License
