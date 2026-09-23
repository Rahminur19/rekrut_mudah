# Entity Relationship Diagram (ERD) & Database Specification
## Rekrut Mudah: Platform Rekrutmen Vokasi, Magang & Kerja Terpadu

---

## 1. Diagram Relasi Entitas (Mermaid ERD)

```mermaid
erDiagram
    User ||--o| UserProfile : "has profile (Seeker/PKL)"
    User ||--o| CompanyProfile : "owns company (Recruiter)"
    CompanyProfile ||--o{ CompanyGalleryPhoto : "showcases photos"
    CompanyProfile ||--o{ JobListing : "publishes"
    JobCategory ||--o{ JobListing : "categorizes"
    JobListing }o--o{ Major : "targets (jurusan SMK)"
    User ||--o{ JobBookmark : "saves wishlist"
    JobListing ||--o{ JobBookmark : "is bookmarked by"
    JobListing ||--o{ JobDiscussion : "has discussions"
    User ||--o{ JobDiscussion : "posts questions/replies"
    
    JobListing ||--o{ Application : "receives"
    User ||--o{ Application : "submits"
    Application ||--o{ ApplicationStatusHistory : "tracks timeline"
    User ||--o{ ApplicationStatusHistory : "status changed by"

    User ||--o{ Conversation : "initiates as applicant"
    CompanyProfile ||--o{ Conversation : "participates as company"
    JobListing ||--o{ Conversation : "inquires regarding"
    Conversation ||--o{ ChatMessage : "contains messages"
    User ||--o{ ChatMessage : "sends"

    User {
        UUID id PK
        string email UK
        string username
        string role "SEEKER | RECRUITER | ADMIN"
        string phone_number
        boolean is_verified
        datetime created_at
    }

    UserProfile {
        UUID id PK
        UUID user_id FK
        string candidate_type "JOB_SEEKER | INTERN | PKL_STUDENT"
        string headline
        text bio
        string education_level "SMK | SMA | D3 | D4_S1"
        string institution_name
        string major_name
        string expected_internship_duration
        file resume_file
        file recommendation_letter_file "Surat Pengantar PKL"
        string portfolio_url
        string city
        string province
    }

    CompanyProfile {
        UUID id PK
        UUID user_id FK
        string company_name
        string slug UK
        string industry
        string company_size
        text description
        image logo
        image banner_image
        string banner_url
        string website_url
        text address
        string city
        string province
        boolean is_verified
        decimal rating "1.0 - 5.0 Bintang"
        int review_count "Jumlah Ulasan"
        boolean accepts_pkl
        boolean accepts_internship
    }

    CompanyGalleryPhoto {
        UUID id PK
        UUID company_id FK
        image photo
        string photo_url
        string caption
        datetime created_at
    }

    JobCategory {
        int id PK
        string name
        string slug UK
        string icon_name
    }

    Major {
        int id PK
        string name
        string level "SMK | D3_S1 | SEMUA"
    }

    JobListing {
        UUID id PK
        UUID company_id FK
        UUID created_by_id FK
        int category_id FK
        string title
        string slug UK
        string opportunity_type "JOB | INTERNSHIP | PKL"
        string employment_type "FULL_TIME | PART_TIME | CONTRACT | INTERNSHIP"
        string workplace_type "ONSITE | HYBRID | REMOTE"
        string city
        string province
        text description
        text requirements
        text benefits_and_allowance
        decimal min_salary
        decimal max_salary
        boolean is_salary_disclosed
        string duration
        boolean requires_pkl_letter
        date application_deadline
        string status "PUBLISHED | DRAFT | CLOSED"
        int view_count
        datetime created_at
    }

    Application {
        UUID id PK
        UUID job_listing_id FK
        UUID applicant_id FK
        string status "SUBMITTED | REVIEWED | INTERVIEW | ACCEPTED | REJECTED | WITHDRAWN"
        text cover_letter
        file resume_snapshot
        file pkl_letter_snapshot
        datetime interview_datetime "Jadwal Wawancara HRD"
        string interview_location "Lokasi / Link Meet"
        text interview_notes "Instruksi Persyaratan HRD"
        datetime applied_at
        datetime updated_at
    }

    ApplicationStatusHistory {
        UUID id PK
        UUID application_id FK
        string from_status
        string to_status
        text notes
        UUID changed_by_id FK
        datetime created_at
    }

    Conversation {
        UUID id PK
        UUID applicant_id FK "User (Seeker)"
        UUID company_id FK "CompanyProfile"
        UUID job_listing_id FK "JobListing (Optional)"
        datetime last_message_at
        datetime created_at
    }

    ChatMessage {
        UUID id PK
        UUID conversation_id FK
        UUID sender_id FK "User"
        text message
        file file_attachment
        boolean is_read
        datetime created_at
    }
```

---

## 2. Rincian Kamus Data (Data Dictionary)

### 2.1 Modul Akun & Profil (`apps/accounts`)

#### Tabel: `accounts_user`
- `id`: Primary Key (UUID v4), menjamin keunikan identitas tanpa mengekspos ID berurutan.
- `email`: Email unik untuk autentikasi sistem.
- `role`: Tipe akun: `SEEKER` (Pelamar / Siswa PKL), `RECRUITER` (Perusahaan), `ADMIN`.
- `phone_number`: Nomor telepon/WhatsApp aktif untuk keperluan koordinasi cepat.
- `is_verified`: Status verifikasi email/dokumen resmi.

#### Tabel: `accounts_userprofile`
- `user_id`: One-to-One ke `accounts_user`.
- `candidate_type`: Menentukan segmentasi kandidat (`JOB_SEEKER`, `INTERN`, `PKL_STUDENT`).
- `education_level`: `SMK`, `SMA`, `D3`, `D4_S1`.
- `institution_name`: Nama institusi asal (contoh: SMKN 1 Jakarta, Politeknik Negeri Jakarta).
- `major_name`: Jurusan (contoh: Rekayasa Perangkat Lunak, Akuntansi).
- `recommendation_letter_file`: Surat Pengantar PKL dari sekolah (wajib untuk siswa SMK yang melamar PKL resmi).

#### Tabel: `accounts_companyprofile`
- `company_name`: Nama resmi badan usaha atau perusahaan mitra.
- `slug`: Slug URL ramah SEO (contoh: `pt-nusantara-teknologi-mandiri`).
- `logo` & `banner_image`: Identitas visual perusahaan.
- `accepts_pkl`: Boolean flag apakah perusahaan membuka program PKL untuk siswa SMK.
- `accepts_internship`: Boolean flag untuk magang mahasiswa.

#### Tabel: `accounts_companygalleryphoto`
- `company_id`: Foreign Key ke `CompanyProfile` (Cascade).
- `photo` / `photo_url`: Gambar foto fasilitas, ruang praktik, atau lab komputer.
- `caption`: Keterangan foto (contoh: "Lab Komputer & Coding Peserta PKL").

---

### 2.2 Modul Lowongan & Kategori (`apps/jobs`)

#### Tabel: `jobs_jobcategory`
- Menyediakan pengelompokan industri (Teknologi, Otomotif, Akuntansi, Desain, Perhotelan, dll.) dilengkapi icon Material Symbols.

#### Tabel: `jobs_major`
- Master data kompetensi keahlian/jurusan sekolah kejuruan (RPL, TKJ, OTKP, AKL, TKRO, dll.).

#### Tabel: `jobs_joblisting`
- `opportunity_type`: Penanda tipe lowongan (`PKL`, `INTERNSHIP`, `JOB`).
- `duration`: Khusus program PKL/Magang (contoh: "3 Bulan", "6 Bulan").
- `requires_pkl_letter`: Memvalidasi syarat Surat Pengantar PKL dari sekolah.
- `target_majors`: Relasi Many-to-Many ke `jobs_major` untuk mencocokkan kualifikasi siswa.

---

### 2.3 Modul Lamaran & ATS (`apps/applications`)

#### Tabel: `applications_application`
- Relasi antara Pelamar (`User`) dan Lowongan (`JobListing`).
- Constraint: `UniqueConstraint(fields=['job_listing', 'applicant'])` mencegah spam ganda.
- `resume_snapshot` & `pkl_letter_snapshot`: Menyimpan berkas saat melamar sehingga aman meskipun profil pengguna diperbarui di kemudian hari.

#### Tabel: `applications_applicationstatushistory`
- Catatan audit jejak tahapan seleksi: perubahan dari status awal ke status baru beserta catatan HR.

---

### 2.4 Modul Chat Interaktif (`apps/chat`)

#### Tabel: `chat_conversation`
- `applicant_id`: Foreign Key ke `User` (Pelamar).
- `company_id`: Foreign Key ke `CompanyProfile` (Perusahaan).
- `job_listing_id`: Foreign Key ke `JobListing` (Opsional, menautkan diskusi dengan lowongan spesifik).
- `last_message_at`: Timestamp pesan terakhir untuk pengurutan percakapan teratas di Inbox.
- Constraint: `UniqueConstraint(fields=['applicant', 'company', 'job_listing'])` untuk mencegah duplikasi thread percakapan dengan topik yang sama.

#### Tabel: `chat_chatmessage`
- `conversation_id`: Foreign Key ke `Conversation` (Cascade).
- `sender_id`: Foreign Key ke `User` (Pengirim pesan).
- `message`: Isi teks pesan pertanyaan atau jawaban.
- `is_read`: Status apakah pesan sudah dibaca oleh lawan bicara.
- `created_at`: Waktu kirim pesan (ISO timestamp).

---

## 3. Strategi Indexing & Integritas Basis Data
1. **Pencarian Cepat**:
   - Index pada `JobListing(status, opportunity_type, city)`.
   - Index pada `Conversation(applicant, company, last_message_at)`.
   - Index pada `ChatMessage(conversation, created_at)`.
2. **Keamanan Penghapusan Data**:
   - Penghapusan akun pelamar tidak menghapus riwayat audit lamaran yang telah masuk (`on_delete=models.SET_NULL` pada `created_by` / `changed_by`).
   - Obrolan chat dilindungi hak akses sehingga hanya partisipan percakapan (`applicant` atau HRD pemilik `company`) yang berhak membaca atau mengirim pesan.
