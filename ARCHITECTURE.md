# System Architecture & Technical Specification
## Rekrut Mudah: Modern Monolith dengan DATH Stack & Material Design 3

---

## 1. Ikhtisar Arsitektur: Modern Monolith & HTML-over-the-Wire

Aplikasi **Rekrut Mudah** dirancang menggunakan paradigma **Modern Monolith / HTML-over-the-Wire**. Berbeda dengan arsitektur SPA (Single Page Application) tradisional yang memisahkan backend REST/GraphQL dan frontend React/Vue dengan ribuan dependensi `node_modules`, DATH Stack menggabungkan kesederhanaan monolitik Django dengan reaktivitas tinggi:

```
+-------------------------------------------------------------------------------+
|                                    BROWSER                                    |
|                                                                               |
|  +-------------------------------------------------------------------------+  |
|  |             Tailwind CSS + Material Design 3 Design Tokens              |  |
|  +-------------------------------------------------------------------------+  |
|                                                                               |
|  +---------------------------+             +-------------------------------+  |
|  |         Alpine.js         |             |             HTMX              |  |
|  |  (Local UI State, Modals, |             |   (HTML-over-the-Wire Ajax,   |  |
|  |  Dropdowns, Auto-Scroll)  |             |  Live Search, Chat Streaming) |  |
|  +---------------------------+             +-------------------------------+  |
+------------------------------------------------------------|------------------+
                                                             | HTTP GET / POST
                                                             | (Payload: Partial HTML)
+------------------------------------------------------------v------------------+
|                                DJANGO 5 SERVER                                |
|                                                                               |
|  [HtmxMiddleware] -> Memeriksa header request.htmx                            |
|                                                                               |
|  +---------------------+  +--------------------+  +------------------------+  |
|  |    apps.accounts    |  |     apps.jobs      |  |       apps.chat        |  |
|  | (Auth, Profiles,    |  | (Listings, Filter, |  |  (In-App Messaging,   |  |
|  |  Company Gallery)   |  |  Majors, Bookmark) |  |   Polling, Real-time)  |  |
|  +---------------------+  +--------------------+  +------------------------+  |
|                                                                               |
|  +-------------------------------------------------------------------------+  |
|  |                      Django ORM + SQLite3 Database                      |  |
|  +-------------------------------------------------------------------------+  |
+-------------------------------------------------------------------------------+
```

### Keunggulan DATH Stack:
1. **Zero Client-Side Build Step**: Tidak membutuhkan proses kompilasi bundler Node.js (Webpack / Vite) yang rumit saat runtime. Aplikasi berjalan seketika saat di-clone.
2. **Server-Rendered Security**: Seluruh aturan bisnis, hak akses (RBAC), dan otorisasi terpusat di Python/Django.
3. **Bandwidth Efisien**: Hanya potongan HTML yang berubah yang dikirimkan melalui jaringan (misal: balon pesan chat baru atau baris status pelamar ATS).
4. **Single Source of Truth**: Template HTML Django menjadi satu-satunya definisi UI, menghindari duplikasi DTO atau validasi skema frontend/backend ganda.

---

## 2. Pola Interaksi HTML-over-the-Wire

### 2.1 Live Filter Lowongan (Debounced Search)
```html
<input type="text"
       name="q"
       placeholder="Cari lowongan atau posisi..."
       hx-get="{% url 'jobs:job_list' %}"
       hx-trigger="keyup changed delay:300ms, search"
       hx-target="#job-listings-container"
       hx-include="#filter-form"
       hx-indicator="#loading-spinner">
```
- Pengguna mengetik kata kunci.
- HTMX menunda request selama 300 milidetik (*debounce*).
- Django menerima request dengan `request.htmx == True`, merender partial template `job_cards_partial.html`, dan menyuntikkannya ke dalam `#job-listings-container` tanpa me-refresh halaman.

### 2.2 Sistem Chatting & Live Polling
```html
<!-- Form Kirim Pesan (Instant Append) -->
<form hx-post="{% url 'chat:send_message' conversation.id %}"
      hx-target="#chat-messages-container"
      hx-swap="beforeend"
      @htmx:after-request="$el.reset(); $nextTick(() => scrollToBottom())">
    <input type="text" name="message" required autocomplete="off" />
    <button type="submit">Kirim</button>
</form>

<!-- Polling Otomatis Pesan Masuk -->
<div id="chat-messages-container"
     hx-get="{% url 'chat:poll_messages' conversation.id %}"
     hx-trigger="every 3s"
     hx-swap="innerHTML">
     <!-- Pesan-pesan dirender di sini -->
</div>
```
- Saat pengguna mengirim pesan, request dikirim via HTMX. Server menyimpan pesan dan mengembalikan potongan HTML balon pesan baru.
- Balon langsung disisipkan di posisi paling akhir (`beforeend`).
- Polling ringan setiap 3 detik menyinkronkan pesan masuk baru dari lawan bicara secara otomatis.

---

## 3. Sistem Desain: Google Material Design 3 (M3)

Aplikasi dibangun sepenuhnya dengan mengikuti spesifikasi token warna, elevasi, dan radius dari **Google Material Design 3**:

### 3.1 Peran Warna (Color Roles)
- **Primary (`#00639B`)**: Warna dominan untuk tombol aksi utama, navigasi aktif, dan ikon utama.
- **Primary Container (`#CEE5FF`)** & **On-Primary Container (`#001D33`)**: Digunakan untuk balon pesan chat pengirim, badge sorotan, dan kartu terfokus.
- **Secondary (`#51606F`)**: Elemen pendukung, filter chip sekunder.
- **Tertiary (`#6B5778`)** & **Tertiary Container (`#F3DAFF`)**: **Warna khusus untuk pilar PKL SMK & Vokasi**, membedakannya secara visual dari lowongan kerja umum.
- **Surface Container (`#ECEDF4`)**: Warna latar belakang kartu dengan kontras halus tanpa bayangan hitam tajam (*tonal elevation*).
- **Outline Variant (`#C2C7CF`)**: Garis tepi halus pada input form dan kartu lowongan.

### 3.2 Tipografi & Komponen
- **Font**: *Plus Jakarta Sans* dipadukan dengan *Google Material Symbols Outlined*.
- **Border Radius**: Bentuk sudut membulat modern (`rounded-3xl` untuk kartu, `rounded-full` untuk chip dan tombol pill).
- **Elevation**: Transisi elevasi permukaan menggunakan `surface-container-low` hingga `surface-container-high`.

---

## 4. Keamanan & Role-Based Access Control (RBAC)

1. **Proteksi CSRF**:
   - Header global disuntikkan pada setiap request HTMX:
     ```html
     <body hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'>
     ```
2. **Dekorator Hak Akses**:
   - `@login_required`: Memastikan pelamar atau recruiter telah terautentikasi.
   - Pengecekan peran khusus:
     - Hanya akun ber-role `RECRUITER` yang dapat mengakses form pembukaan lowongan dan tabel ATS.
     - Hanya akun ber-role `SEEKER` yang dapat mengajukan lamaran ke lowongan.
     - Akses ruang obrolan obrolan (`Conversation`) diverifikasi: `request.user == conversation.applicant` ATAU `request.user == conversation.company.user`. Pengguna lain yang mencoba mengakses URL UUID akan mendapatkan respon `403 Forbidden`.
