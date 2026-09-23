# Product Requirements Document (PRD)
## Rekrut Mudah: Platform Rekrutmen Vokasi, Magang & Kerja Terpadu

---

| Dokumen | Spesifikasi Kebutuhan Produk (PRD) |
| :--- | :--- |
| **Nama Proyek** | Rekrut Mudah |
| **Versi** | 1.0.0 (Tahap Rilis MVP Plus) |
| **Status** | Approved & Ready for Implementation |
| **Tech Stack** | DATH Stack (Django 5 + Alpine.js 3 + Tailwind CSS + HTMX 2) |
| **Desain Sistem** | Google Material Design 3 (M3) |
| **Arsitektur** | Modern Monolith / HTML-over-the-Wire |

---

## 1. Latar Belakang & Pernyataan Masalah

### 1.1 Permasalahan di Lapangan
1. **Siswa SMK / Vokasi Kesulitan Mencari Tempat PKL**:
   - Siswa SMK seringkali mencari tempat Praktik Kerja Lapangan (PKL) secara konvensional, mendatangi kantor satu per satu tanpa kejelasan apakah perusahaan tersebut menerima jurusan mereka (RPL, TKJ, AKL, OTKP, Otomotif, dll.).
   - Banyak lowongan magang di portal umum hanya ditujukan untuk mahasiswa tingkat akhir universitas, bukan untuk siswa usia sekolah kejuruan yang memerlukan persuratan resmi (Surat Pengantar PKL dari sekolah).
2. **Pencari Kerja Umum & Fresh Graduate Butuh Transparansi**:
   - Minimnya informasi mengenai fasilitas, transparansi uang saku/gaji, lingkungan kerja, dan budaya perusahaan.
3. **Perekrut / HRD Kesulitan Menyaring Talenta Vokasi & Berkomunikasi**:
   - HRD sering kali kewalahan mengelola berkas lamaran PKL dan kerja melalui email yang tidak terorganisir.
   - Tidak ada kanal komunikasi langsung (*in-app messaging*) untuk menanyakan kejelasan kualifikasi pelamar sebelum tahap wawancara formal.

### 1.2 Solusi "Rekrut Mudah"
Platform rekrutmen berbasis web modern yang didesain secara spesifik untuk memfasilitasi 3 pilar:
1. **Penempatan PKL SMK & Vokasi**: Dilengkapi filter kompetensi keahlian/jurusan, durasi penempatan (3/6/12 bulan), dan pengunggahan berkas resmi Surat Pengantar Sekolah.
2. **Magang Mahasiswa (Internship)**: Magang bersertifikat dan berbayar untuk perguruan tinggi.
3. **Lowongan Kerja Profesional & Fresh Graduate**: Peluang karir penuh waktu (Full-time), paruh waktu (Part-time), kontrak, dan kerja remote.
4. **Fitur Chat Interaktif Pelamar ↔ HRD**: Komunikasi langsung di dalam platform untuk menanyakan lowongan dan mendiskusikan kualifikasi.
5. **Transparansi Profil Perusahaan**: Menampilkan foto fasilitas kantor, lab praktik PKL, daftar fasilitas (uang saku, makan siang, sertifikat, mentoring 1-on-1), dan status verifikasi resmi industri.

---

## 2. Target Persona Pengguna

| Persona | Profil & Karakteristik | Kebutuhan Utama |
| :--- | :--- | :--- |
| **1. Siswa SMK (PKL Seeker)** | Siswa usia 16-18 tahun (misal: Ahmad, Jurusan RPL SMKN 1 Jakarta). Cepat, praktis, menggunakan smartphone atau laptop sekolah. | Menemukan tempat PKL yang menerima jurusannya, mengunggah surat pengantar sekolah, dan chat HRD untuk memastikan kuota. |
| **2. Mahasiswa / Job Seeker Dewasa** | Mahasiswa tingkat akhir atau fresh graduate (misal: Budi, S1 Sistem Informasi). | Mencari pekerjaan full-time atau magang dengan rincian benefit jelas, melamar via CV instan, memantau status seleksi. |
| **3. Perekrut / HRD Perusahaan** | HR Manager atau Talent Acquisition (misal: Ibu Dewi Lestari, PT Nusantara Teknologi Mandiri). | Membuka lowongan dengan kriteria spesifik, mengelola ATS (Applicant Tracking System), meninjau berkas, dan membalas chat calon pelamar. |
| **4. Administrator Sistem** | Pengelola platform untuk verifikasi perusahaan, manajemen kategori, dan kurasi jurusan. | Akses Django Admin untuk moderasi konten dan validasi kredibilitas perusahaan. |

---

## 3. Kebutuhan Fungsional (Functional Requirements)

### FR-01: Autentikasi & Manajemen Pengguna Multi-Role
- Pengguna dapat mendaftar dengan peran: **Pelamar / Siswa PKL** atau **Perusahaan / HRD**.
- Autentikasi berbasis Email / Username + Password standar dengan sistem login Django Auth yang aman.
- Siswa/Pelamar dapat melengkapi profil: Jenis Kandidat (Siswa PKL, Mahasiswa, Job Seeker), Nama Sekolah/Universitas, Jurusan/Kompetensi, Resume (PDF), dan Surat Pengantar PKL Sekolah (PDF).
- Perusahaan dapat melengkapi: Nama PT, Logo, Foto Banner Gedung/Kantor, Deskripsi, Skala Tim, Alamat, Website, Rating/Ulasan, dan Kebijakan Penerimaan PKL.

### FR-02: Eksplorasi Lowongan & Live Filter (HTMX)
- Daftar lowongan dengan pencarian kata kunci (*search-as-you-type* dengan debouncing 300ms via HTMX).
- Filter multivariabel instan:
  - Tipe Kesempatan: `Semua`, `PKL SMK & Vokasi`, `Magang Mahasiswa`, `Lowongan Kerja`.
  - Sistem Kerja: `Onsite`, `Hybrid`, `Remote`.
  - Jurusan / Kompetensi Keahlian SMK.
- Kartu lowongan bergaya Material Design 3 dengan badge pembeda warna yang jelas serta **Status Bintang Reputasi Perusahaan**.
- Fitur simpan lowongan (*Bookmark / Wishlist*) dengan HTMX toggle tanpa refresh.

### FR-03: Rincian Lowongan & Galeri Perusahaan
- Tampilan detail lowongan dengan banner hero perusahaan, info gaji/uang saku, persyaratan, dan fasilitas/benefit.
- Indikator Status Bintang Perusahaan (*Rating Score* dan jumlah ulasan nyata).
- Galeri foto lingkungan kerja, ruang lab komputer/praktik industri untuk memberikan gambaran nyata tempat PKL.
- Diskusi publik / Q&A seputar lowongan dengan dukungan balasan resmi dari perusahaan.

### FR-04: Alur Pengajuan Lamaran & Pemantauan Jadwal Wawancara
- Tombol *"Lamar Sekarang"* memicu modal dialog interaktif (HTMX) tanpa reload halaman.
- Pelamar dapat memilih berkas CV/Surat PKL yang sudah tersimpan di profil atau mengunggah berkas baru.
- Catatan pengantar singkat (cover letter opsional).
- Pencegahan lamaran ganda (Unique constraint per user-job).
- Halaman *"Lamaran Saya"* untuk memantau status secara *real-time*: `Terkirim`, `Ditinjau`, `Wawancara`, `Diterima`, `Ditolak`.
- **Kartu Jadwal Wawancara & Kunjungan Perusahaan**: Jika pelamar masuk ke tahap wawancara, sistem menampilkan kartu jadwal khusus berisi: Tanggal & Waktu, Lokasi/Tautan Pertemuan, serta Catatan Persyaratan khusus dari HRD.

### FR-05: Sistem Chat Langsung (Pelamar ↔ HRD)
- Tombol *"💬 Tanya HRD / Chat Perusahaan"* tersedia di:
  1. Halaman Rincian Lowongan (otomatis menautkan konteks posisi yang ditanyakan).
  2. Halaman Profil Perusahaan.
- Antarmuka Chat Inbox bergaya Google Material Design 3:
  - Daftar percakapan aktif dengan avatar, nama lawan bicara, judul lowongan, cuplikan pesan terakhir, dan timestamp.
  - Jendela obrolan dengan *chat bubbles* M3 (Primary Container untuk pengirim, Surface High untuk lawan bicara).
  - Pengiriman pesan instan via HTMX `hx-post` (pesan langsung ditambahkan di akhir stream tanpa kedip).
  - Live polling background setiap 4 detik (`hx-get`) untuk mengambil pesan masuk baru secara mulus.
  - Auto-scroll ke posisi pesan terbawah menggunakan Alpine.js.

### FR-06: Profil Perusahaan Publik, Status Bintang & Pemilihan Posisi
- Direktori Perusahaan Mitra (`/accounts/companies/`) menampilkan daftar seluruh mitra terverifikasi.
- **Status Bintang Perusahaan**: Menampilkan reputasi bintang (1.0 s/d 5.0) berdasarkan keunggulan perusahaan dan ulasan peserta PKL/karyawan.
- Halaman Profil Detail Perusahaan (`/accounts/companies/<slug>/`):
  - Banner gedung/kantor resolusi tinggi dan logo perusahaan ber-badge terverifikasi.
  - Rating bintang perusahaan dan ulasan keunggulan industri.
  - Rincian profil: industri, skala karyawan, visi misi, fasilitas PKL, alamat fisik.
  - Galeri foto interaktif suasana kerja dengan modal lightbox.
  - Tab seluruh lowongan aktif dari perusahaan tersebut.
  - **Tombol Lamar ke Perusahaan dengan Pilihan Posisi**: Membuka modal pendaftaran di mana pelamar dapat memilih lowongan/posisi yang ingin dilamar dari dropdown daftar posisi aktif di perusahaan tersebut.
  - Tombol aksi *"💬 Hubungi HRD"*.

### FR-07: Dashboard Perekrut / ATS & Penjadwalan Wawancara
- Dashboard posting, edit, dan penutupan lowongan.
- Tabel pelamar masuk dengan filter lowongan dan filter status.
- Pembaruan status kandidat instan melalui dropdown tabel via HTMX inline swap.
- **Fitur Pengaturan Jadwal Wawancara (HRD)**:
  - HRD dapat mengatur Tanggal, Jam, Lokasi Fisik / Tautan Online, dan Catatan Instruksi Khusus yang otomatis terkirim dan tampil di dashboard pelamar.
- Unduh langsung CV dan Surat Pengantar PKL kandidat dalam format PDF.

---

## 4. Kebutuhan Non-Fungsional (Non-Functional Requirements)

1. **Performa & Ringan**:
   - Menggunakan pendekatan **HTML-over-the-Wire**: payload jaringan berupa potongan HTML bersih berukuran kecil (1-5 KB), bukan bundle JSON + JS raksasa.
   - Waktu respon halaman di localhost < 100ms.
2. **Desain Sistem & Responsivitas**:
   - Menerapkan **Google Material Design 3**: bentuk sudut rounded-3xl, tonal elevation (`surface-container`), palet warna terstandar M3 (Primary, Secondary, Tertiary, Outline).
   - Sepenuhnya responsif: optimal dibuka di smartphone (viewport 360px), tablet, hingga layar desktop lebar.
3. **Keandalan & Zero-Config**:
   - Menggunakan SQLite3 dan sistem file lokal untuk kemudahan instalasi sekali klik (*plug-and-play*).
   - Pustaka CSS/JS frontend dimuat melalui CDN berperforma tinggi dengan *caching*.
4. **Keamanan**:
   - Proteksi CSRF di seluruh request POST HTMX melalui header global `X-CSRFToken`.
   - Validasi kepemilikan data (Role-Based Access Control) di tingkat decorator view Django.

---

## 5. Indikator Keberhasilan (Success Metrics)
- Pengguna dapat menavigasi, mencari lowongan, melihat profil perusahaan dengan galeri, mengirim lamaran, dan berbalas chat dengan HRD secara mulus tanpa kegagalan atau full-page freeze.
- Waktu yang dibutuhkan pelamar untuk mengajukan lamaran PKL < 1 menit.
