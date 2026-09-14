# Rekrut Mudah 🇮🇩
> **Portal Lowongan Kerja, Magang Mahasiswa, dan Penempatan Siswa PKL SMK / Vokasi**  
> Dibangun dengan **DATH Stack** (Django + Alpine.js + Tailwind CSS + HTMX) berbasis **Google Material Design 3 (M3)** dengan paradigma **Modern Monolith / HTML-over-the-Wire**.

---

## 🌟 Fitur Utama

1. **3 Pilar Peluang Karir**:
   - 🎓 **Praktik Kerja Lapangan (PKL SMK & Vokasi)**: Kategori khusus untuk siswa SMK dan politeknik, lengkap dengan pemilihan kompetensi keahlian/jurusan (RPL, TKJ, Otomotif, AKL, OTKP), filter durasi (3 bulan, 6 bulan), dan pengunggahan **Surat Pengantar PKL Sekolah**.
   - 💼 **Magang Mahasiswa (Internship)**: Magang bersertifikat dan magang berbayar dengan transparansi uang saku / benefit.
   - 🏢 **Lowongan Kerja (Full-Time / Part-Time / Remote)**: Posisi profesional dan fresh graduate dengan filter gaji dan sistem kerja (Onsite, Hybrid, Remote).
2. **HTML-over-the-Wire dengan HTMX 2.x**:
   - **Live Search & Filter**: Pencarian kata kunci lowongan debounced (300ms) tanpa reload seluruh halaman.
   - **One-Click Apply Modal**: Pop-up dialog lamaran kerja instan yang memuat form on-demand dan mengirim dokumen via HTMX multipart form.
   - **Instant Status Update di ATS**: Perekrut dapat mengubah tahapan seleksi kandidat langsung dari dropdown tabel tanpa refresh.
3. **Micro-Interactions dengan Alpine.js 3.x**:
   - Dropdown user menu, navigation drawer mobile, dialog modal transitions, dan toast notification store.
4. **Google Material Design 3 (M3)**:
   - Dynamic color system (Primary, Secondary, Tertiary untuk PKL, Surface containers, Outlines).
   - Elevation system berbasis surface tint levels 0 hingga 4.
   - Komponen M3 asli: Top App Bar, Assist/Filter Chips, Cards, Badges, Modals, dan Snackbars.
5. **Autentikasi Multi-Role & RBAC**:
   - **Pelamar / Siswa PKL**: Dashboard pemantauan lamaran, upload CV & Surat Pengantar PKL.
   - **Perusahaan / Perekrut**: Dashboard posting lowongan dan ATS (Applicant Tracking System) untuk screening pelamar.
   - **Superadmin**: Panel manajemen Django Admin.

---

## 🚀 Panduan Menjalankan Aplikasi (Quickstart)

### 1. Masuk ke Direktori Proyek
```bash
cd C:\Users\ACER\.gemini\antigravity\scratch\rekrut_mudah
```

### 2. Pasang Dependensi Python
```bash
pip install -r requirements.txt
```
*(Atau menggunakan virtualenv: `python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt`)*

### 3. Jalankan Migrasi Basis Data
```bash
python manage.py makemigrations accounts jobs applications
python manage.py migrate
```

### 4. Isi Data Contoh (Seed Data Otomatis)
Jalankan script untuk menginjeksi kategori, jurusan SMK, akun demo, lowongan, dan lamaran masuk:
```bash
python seed_data.py
```

### 5. Jalankan Server Pengembangan
```bash
python manage.py runserver
```
Buka browser Anda di: **`http://127.0.0.1:8000/`**

---

## 👥 Akun Demo untuk Pengujian Cepat

Semua akun demo di-generate otomatis oleh `seed_data.py` dengan kata sandi bawaan:

| Peran Akun | Alamat Email | Kata Sandi | Deskripsi |
| :--- | :--- | :--- | :--- |
| **Siswa PKL SMK** | `ahmad.smk@rekrut.id` | `password123` | Siswa SMKN 1 Jakarta (RPL), telah melamar posisi PKL Frontend. |
| **Pencari Kerja** | `budi@rekrut.id` | `password123` | Pelamar fresh graduate developer. |
| **Perekrut / HRD** | `hrd@nusantara.tech` | `password123` | HRD PT Nusantara Teknologi Mandiri (Akses ATS & Kelola Lowongan). |
| **Perekrut Otomotif** | `karir@wahanaotomotif.co.id` | `password123` | HRD PT Wahana Otomotif Nusantara (Lowongan PKL Otomotif). |
| **Superadmin** | `admin@rekrut.id` | `admin123` | Akses penuh Django Admin di `/admin/`. |

---

## 📂 Struktur Direktori Proyek

```
rekrut_mudah/
├── manage.py                  # CLI Django
├── requirements.txt           # Dependensi Python
├── seed_data.py               # Otomasi pengisian data awal
├── rekrut_mudah/              # Pengaturan Core Django
│   ├── settings.py            # Konfigurasi M3 static, auth model, HTMX middleware
│   ├── urls.py                # Routing aplikasi
│   ├── wsgi.py & asgi.py
├── apps/
│   ├── accounts/              # User model (UUID), UserProfile, CompanyProfile, Auth
│   ├── jobs/                  # JobListing, Category, Major SMK, Live Filter HTMX
│   └── applications/          # Lamaran, ATS Recruiter, Status History, Apply Modal
├── templates/
│   ├── base.html              # Shell M3, TopBar, CDN Tailwind, Alpine, HTMX
│   ├── components/            # navbar, footer, job_card, chips, modal
│   ├── accounts/              # login, register, profile_seeker, profile_company
│   ├── jobs/                  # job_list, job_detail, job_form, recruiter_jobs
│   └── applications/          # my_applications, recruiter_ats, partials
└── static/
    ├── css/m3.css             # Material Design 3 Design Tokens & Elevation
    └── js/main.js             # Alpine client notification store
```

---

## 📑 Dokumen Perancangan Arsitektur

Dokumen lengkap perancangan sistem tersimpan di:
- **Product Requirements Document (PRD)**: `PRD.md`
- **Database Specification & ERD**: `ERD.md`
- **System Architecture (DATH & M3)**: `ARCHITECTURE.md`
- **Rencana Implementasi**: `implementation_plan.md`
