import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rekrut_mudah.settings')
django.setup()

from apps.accounts.models import User, UserProfile, CompanyProfile, CompanyGalleryPhoto
from apps.jobs.models import JobCategory, Major, JobListing
from apps.applications.models import Application, ApplicationStatusHistory
from apps.chat.models import Conversation, ChatMessage

def run_seed():
    print("[*] Mulai seeding data awal Rekrut Mudah...")

    # 1. Kategori Lowongan
    categories_data = [
        ('Teknologi Informasi & Software', 'teknologi-informasi', 'terminal'),
        ('Otomotif & Manufaktur', 'otomotif-manufaktur', 'precision_manufacturing'),
        ('Akuntansi & Keuangan', 'akuntansi-keuangan', 'account_balance'),
        ('Desain Grafis & Multimedia', 'desain-multimedia', 'palette'),
        ('Administrasi Perkantoran', 'administrasi-perkantoran', 'business_center'),
        ('Pemasaran & Digital Marketing', 'pemasaran-digital', 'campaign'),
        ('Perhotelan & Kuliner', 'perhotelan-kuliner', 'hotel'),
    ]
    categories = {}
    for name, slug, icon in categories_data:
        cat, _ = JobCategory.objects.get_or_create(slug=slug, defaults={'name': name, 'icon_name': icon})
        categories[slug] = cat
    print("[OK] Kategori lowongan siap.")

    # 2. Kompetensi Keahlian / Jurusan SMK & Vokasi
    majors_data = [
        ('Rekayasa Perangkat Lunak (RPL)', 'SMK'),
        ('Teknik Komputer dan Jaringan (TKJ)', 'SMK'),
        ('Desain Komunikasi Visual (DKV) / Animasi', 'SMK'),
        ('Akuntansi dan Keuangan Lembaga (AKL)', 'SMK'),
        ('Otomatisasi & Tata Kelola Perkantoran (OTKP)', 'SMK'),
        ('Teknik Kendaraan Ringan Otomotif (TKRO)', 'SMK'),
        ('Tata Boga & Perhotelan', 'SMK'),
        ('Teknik Mekatronika & Elektronika', 'SMK'),
        ('Sistem Informasi', 'D3_S1'),
        ('Teknik Informatika', 'D3_S1'),
    ]
    majors = {}
    for name, level in majors_data:
        m, _ = Major.objects.get_or_create(name=name, defaults={'level': level})
        majors[name] = m
    print("[OK] Daftar jurusan SMK & Vokasi siap.")

    # 3. Akun Superadmin
    admin_user, _ = User.objects.get_or_create(
        email='admin@rekrut.id',
        defaults={
            'username': 'admin',
            'first_name': 'Administrator',
            'role': 'ADMIN',
            'is_staff': True,
            'is_superuser': True,
            'is_verified': True
        }
    )
    admin_user.set_password('admin123')
    admin_user.save()

    # 4. Akun Pelamar Demo (Siswa PKL & Fresh Graduate)
    ahmad_user, _ = User.objects.get_or_create(
        email='ahmad.smk@rekrut.id',
        defaults={
            'username': 'ahmad_fauzi',
            'first_name': 'Ahmad Fauzi',
            'role': 'SEEKER',
            'phone_number': '085711223344',
            'is_verified': True
        }
    )
    ahmad_user.set_password('password123')
    ahmad_user.save()

    UserProfile.objects.get_or_create(
        user=ahmad_user,
        defaults={
            'candidate_type': 'PKL_STUDENT',
            'headline': 'Siswa Kelas XI SMK Rekayasa Perangkat Lunak | Siap PKL 3-6 Bulan',
            'bio': 'Siswa aktif SMKN 1 Jakarta jurusan RPL dengan ketertarikan tinggi pada frontend web development (Tailwind, HTML, JavaScript dasar). Memiliki motivasi belajar tinggi dan disiplin.',
            'education_level': 'SMK',
            'institution_name': 'SMKN 1 Jakarta',
            'major_name': 'Rekayasa Perangkat Lunak (RPL)',
            'expected_internship_duration': '3_BULAN',
            'city': 'Jakarta Pusat',
            'province': 'DKI Jakarta',
            'portfolio_url': 'https://github.com/ahmad-fauzi-smk'
        }
    )

    budi_user, _ = User.objects.get_or_create(
        email='budi@rekrut.id',
        defaults={
            'username': 'budi_santoso',
            'first_name': 'Budi Santoso',
            'role': 'SEEKER',
            'phone_number': '087812345678',
            'is_verified': True
        }
    )
    budi_user.set_password('password123')
    budi_user.save()

    UserProfile.objects.get_or_create(
        user=budi_user,
        defaults={
            'candidate_type': 'JOB_SEEKER',
            'headline': 'Fresh Graduate S1 Sistem Informasi | Junior Fullstack Web Developer',
            'bio': 'Lulusan baru berorientasi solusi dengan pengalaman proyek capstone web modern Django dan React.',
            'education_level': 'D4_S1',
            'institution_name': 'Universitas Indonesia',
            'major_name': 'Sistem Informasi',
            'city': 'Depok',
            'province': 'Jawa Barat',
            'portfolio_url': 'https://budisantoso.dev'
        }
    )
    print("[OK] Akun pelamar demo siap.")

    # 5. Daftar Perusahaan Lengkap & Berbeda (Setiap Perusahaan Punya Logo & Foto Unik)
    companies_info = [
        {
            'key': 'comp_1',
            'email': 'hrd@nusantara.tech',
            'username': 'nusantara_hr',
            'first_name': 'Dewi Lestari (HRD)',
            'company_name': 'PT Nusantara Teknologi Mandiri',
            'slug': 'pt-nusantara-teknologi-mandiri',
            'industry': 'Teknologi Informasi & Software',
            'company_size': '51-200',
            'description': 'Perusahaan pengembang solusi enterprise cloud, SaaS platform modern, dan edukasi digital. Kami secara aktif membuka program PKL terstruktur dengan mentor teknis senior.',
            'logo_url': '/static/images/companies/logos/pt-nusantara-teknologi-mandiri.svg',
            'banner_url': 'https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1200&q=80',
            'website_url': 'https://nusantaratech.id',
            'address': 'Gedung Cyber 2 Lantai 14, Jl. HR Rasuna Said, Kuningan',
            'city': 'Jakarta Selatan',
            'province': 'DKI Jakarta',
            'rating': 5.0,
            'review_count': 48,
            'accepts_pkl': True,
            'accepts_internship': True,
            'gallery': [
                ('https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=800&q=80', 'Lab Komputer & Ruang Coding Peserta PKL'),
                ('https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=800&q=80', 'Sesi Mentoring 1-on-1 dengan Senior Software Engineer'),
                ('https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=800&q=80', 'Ruang Diskusi Proyek & Standup Meeting Harian'),
            ]
        },
        {
            'key': 'comp_2',
            'email': 'karir@wahanaotomotif.co.id',
            'username': 'wahana_hr',
            'first_name': 'Bambang Soediro (HRD)',
            'company_name': 'PT Wahana Otomotif Nusantara',
            'slug': 'pt-wahana-otomotif-nusantara',
            'industry': 'Otomotif & Manufaktur Komponen',
            'company_size': '201+',
            'description': 'Jaringan bengkel resmi mobil modern dan distributor sparepart terkemuka. Menjadi mitra resmi 30+ SMK Vokasi bidang Teknik Kendaraan Ringan dengan bengkel standar ISO.',
            'logo_url': '/static/images/companies/logos/pt-wahana-otomotif-nusantara.svg',
            'banner_url': 'https://images.unsplash.com/photo-1619642751034-765dfdf7c58e?auto=format&fit=crop&w=1200&q=80',
            'website_url': 'https://wahanaotomotif.co.id',
            'address': 'Kawasan Industri KIIC Lot C-4, Telukjambe Timur',
            'city': 'Karawang',
            'province': 'Jawa Barat',
            'rating': 4.8,
            'review_count': 35,
            'accepts_pkl': True,
            'accepts_internship': False,
            'gallery': [
                ('https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=800&q=80', 'Bengkel Resmi & Area Servis Kendaraan Berstandar ISO'),
                ('https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=800&q=80', 'Peralatan Diagnostik Komputer & Scanner Injeksi PKL'),
            ]
        },
        {
            'key': 'comp_3',
            'email': 'studio@karyamandiri.id',
            'username': 'mandiri_studio',
            'first_name': 'Rian Pratama (Creative Lead)',
            'company_name': 'Studio Animasi & Desain Kreatif Mandiri',
            'slug': 'studio-animasi-desain-kreatif-mandiri',
            'industry': 'Desain Grafis & Multimedia',
            'company_size': '11-50',
            'description': 'Studio produksi animasi 2D/3D, motion graphics, ilustrasi komersial, dan branding digital. Sangat terbuka membina siswa SMK DKV dan animasi untuk portofolio industri nyata.',
            'logo_url': '/static/images/companies/logos/studio-animasi-desain-kreatif-mandiri.svg',
            'banner_url': 'https://images.unsplash.com/photo-1542744094-3a31f272c490?auto=format&fit=crop&w=1200&q=80',
            'website_url': 'https://karyamandiri.id',
            'address': 'Komp. Ruko Dago Asri No. 18, Jl. Ir. H. Juanda',
            'city': 'Bandung',
            'province': 'Jawa Barat',
            'rating': 4.9,
            'review_count': 29,
            'accepts_pkl': True,
            'accepts_internship': True,
            'gallery': [
                ('https://images.unsplash.com/photo-1600132806370-bf17e65e942f?auto=format&fit=crop&w=800&q=80', 'Studio Gambar Digital & Pen Tablet Siswa DKV'),
                ('https://images.unsplash.com/photo-1513542789411-b6a5d4f31634?auto=format&fit=crop&w=800&q=80', 'Ruang Editing Video & Render Farm Animasi'),
            ]
        },
        {
            'key': 'comp_4',
            'email': 'recruiter@cybernetwork.asia',
            'username': 'cna_hr',
            'first_name': 'Ferry Handoko (IT Ops)',
            'company_name': 'PT Cyber Network Asia',
            'slug': 'pt-cyber-network-asia',
            'industry': 'Teknologi Informasi & Software',
            'company_size': '51-200',
            'description': 'Penyedia infrastruktur jaringan telekomunikasi, data center, dan cloud security. Menyediakan pelatihan teknis langsung instalasi rack server dan routing bagi siswa TKJ.',
            'logo_url': '/static/images/companies/logos/pt-cyber-network-asia.svg',
            'banner_url': 'https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1200&q=80',
            'website_url': 'https://cybernetwork.asia',
            'address': 'Menara Prima Lt. 8, Mega Kuningan',
            'city': 'Jakarta Selatan',
            'province': 'DKI Jakarta',
            'rating': 4.7,
            'review_count': 24,
            'accepts_pkl': True,
            'accepts_internship': True,
            'gallery': [
                ('https://images.unsplash.com/photo-1544197150-b99a580bb7a8?auto=format&fit=crop&w=800&q=80', 'Data Center Tier 3 & Server Monitoring PKL'),
            ]
        },
        {
            'key': 'comp_5',
            'email': 'karir@dataprimasolusindo.com',
            'username': 'dataprema_hr',
            'first_name': 'Maya Safitri (People Lead)',
            'company_name': 'PT Data Prima Solusindo',
            'slug': 'pt-data-prima-solusindo',
            'industry': 'Teknologi Informasi & Software',
            'company_size': '51-200',
            'description': 'Perusahaan teknologi yang berfokus pada pengembangan sistem informasi terintegrasi dan platform analitik big data enterprise untuk perbankan dan retail nasional.',
            'logo_url': '/static/images/companies/logos/pt-data-prima-solusindo.svg',
            'banner_url': 'https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1200&q=80',
            'website_url': 'https://dataprimasolusindo.com',
            'address': 'Sinarmas MSIG Tower Lt. 22, Jl. Jend. Sudirman',
            'city': 'Jakarta Pusat',
            'province': 'DKI Jakarta',
            'rating': 4.9,
            'review_count': 33,
            'accepts_pkl': False,
            'accepts_internship': True,
            'gallery': [
                ('https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=800&q=80', 'Area Kolaborasi Developer & Data Engineer'),
            ]
        },
        {
            'key': 'comp_6',
            'email': 'hrd@arthafinance.id',
            'username': 'arthafinance_hr',
            'first_name': 'Citra Handayani (Lead Auditor)',
            'company_name': 'PT Artha Solusi Finansial',
            'slug': 'pt-artha-solusi-finansial',
            'industry': 'Akuntansi & Keuangan',
            'company_size': '11-50',
            'description': 'Kantor Jasa Akuntan Publik & Konsultan Pajak resmi. Membimbing siswa SMK Akuntansi (AKL) dalam pembukuan jurnal riil, rekonsiliasi bank, dan aplikasi e-Faktur.',
            'logo_url': '/static/images/companies/logos/pt-artha-solusi-finansial.svg',
            'banner_url': 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80',
            'website_url': 'https://arthafinance.id',
            'address': 'Intiland Tower Lantai 7, Jl. Panglima Sudirman',
            'city': 'Surabaya',
            'province': 'Jawa Timur',
            'rating': 4.6,
            'review_count': 19,
            'accepts_pkl': True,
            'accepts_internship': True,
            'gallery': [
                ('https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=800&q=80', 'Ruang Kerja Tim Akuntansi & Pembukuan Kas'),
            ]
        },
        {
            'key': 'comp_7',
            'email': 'halo@hexakreasi.id',
            'username': 'hexakreasi_hr',
            'first_name': 'Yoga Prasetya (Product Design)',
            'company_name': 'PT Hexa Kreasi Digital',
            'slug': 'pt-hexa-kreasi-digital',
            'industry': 'Desain Grafis & Multimedia',
            'company_size': '11-50',
            'description': 'Product design and digital agency yang berfokus pada user research, UI/UX mobile apps, dan design system. Sangat cocok bagi mahasiswa desain yang ingin magang terarah.',
            'logo_url': '/static/images/companies/logos/pt-hexa-kreasi-digital.svg',
            'banner_url': 'https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?auto=format&fit=crop&w=1200&q=80',
            'website_url': 'https://hexakreasi.id',
            'address': 'Jl. Palagan Tentara Pelajar Km. 9',
            'city': 'Yogyakarta',
            'province': 'DI Yogyakarta',
            'rating': 4.8,
            'review_count': 22,
            'accepts_pkl': False,
            'accepts_internship': True,
            'gallery': [
                ('https://images.unsplash.com/photo-1531403009284-440f080d1e12?auto=format&fit=crop&w=800&q=80', 'Ruang Diskusi Wireframing & Prototyping UI/UX'),
            ]
        },
        {
            'key': 'comp_8',
            'email': 'recruitment@precisionastra.co.id',
            'username': 'astra_precision_hr',
            'first_name': 'Joko Susanto (Plant HR)',
            'company_name': 'PT Precision Astra Manufacturing',
            'slug': 'pt-precision-astra-manufacturing',
            'industry': 'Otomotif & Manufaktur',
            'company_size': '201+',
            'description': 'Pabrik manufaktur komponen presisi otomotif berstandar Jepang. Memiliki fasilitas mesin CNC modern dan program magang teknisi mekatronika terakreditasi nasional.',
            'logo_url': '/static/images/companies/logos/pt-precision-astra-manufacturing.svg',
            'banner_url': 'https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=1200&q=80',
            'website_url': 'https://precisionastra.co.id',
            'address': 'Kawasan Industri MM2100 Blok N-12, Cikarang Barat',
            'city': 'Bekasi',
            'province': 'Jawa Barat',
            'rating': 4.7,
            'review_count': 41,
            'accepts_pkl': True,
            'accepts_internship': False,
            'gallery': [
                ('https://images.unsplash.com/photo-1581092162384-8987c1d64718?auto=format&fit=crop&w=800&q=80', 'Lini Perakitan Mesin Presisi & Mesin CNC Vokasi'),
            ]
        },
        {
            'key': 'comp_9',
            'email': 'hr@sentralogistik.co.id',
            'username': 'sentralogistik_hr',
            'first_name': 'Anisa Wulandari (HR Admin)',
            'company_name': 'PT Sentra Mitra Logistik & Perkantoran',
            'slug': 'pt-sentra-mitra-logistik',
            'industry': 'Administrasi Perkantoran',
            'company_size': '51-200',
            'description': 'Penyedia jasa operasional perkantoran, tata kelola dokumen bisnis, dan supply chain logistik. Membina siswa SMK OTKP dalam korespondensi digital dan kearsipan modern.',
            'logo_url': '/static/images/companies/logos/pt-sentra-mitra-logistik.svg',
            'banner_url': 'https://images.unsplash.com/photo-1497215728101-856f4ea42174?auto=format&fit=crop&w=1200&q=80',
            'website_url': 'https://sentralogistik.co.id',
            'address': 'Wisma HSBC Lantai 5, Jl. Gajah Mada No. 135',
            'city': 'Semarang',
            'province': 'Jawa Tengah',
            'rating': 4.5,
            'review_count': 18,
            'accepts_pkl': True,
            'accepts_internship': True,
            'gallery': [
                ('https://images.unsplash.com/photo-1497366811353-6870744d04b2?auto=format&fit=crop&w=800&q=80', 'Ruang Tata Kelola Dokumen & Administrasi Bisnis'),
            ]
        },
        {
            'key': 'comp_10',
            'email': 'talent@brandbooster.id',
            'username': 'brandbooster_hr',
            'first_name': 'Kevin Tanuwijaya (Growth Lead)',
            'company_name': 'PT Brand Booster Indonesia',
            'slug': 'pt-brand-booster-indonesia',
            'industry': 'Pemasaran & Digital Marketing',
            'company_size': '11-50',
            'description': 'Agency periklanan digital, creator management, dan social commerce TikTok/Instagram. Membuka pintu bagi talenta muda kreatif untuk mengelola live streaming dan copy promosi.',
            'logo_url': '/static/images/companies/logos/pt-brand-booster-indonesia.svg',
            'banner_url': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1200&q=80',
            'website_url': 'https://brandbooster.id',
            'address': 'Neo Soho Capital Lt. 19, Jl. Letjen S. Parman',
            'city': 'Jakarta Barat',
            'province': 'DKI Jakarta',
            'rating': 4.9,
            'review_count': 26,
            'accepts_pkl': True,
            'accepts_internship': True,
            'gallery': [
                ('https://images.unsplash.com/photo-1557804506-669a67965ba0?auto=format&fit=crop&w=800&q=80', 'Studio Live Streaming Creator & Media Planning'),
            ]
        },
        {
            'key': 'comp_11',
            'email': 'recruitment@grandroyalresorts.com',
            'username': 'grandroyal_hr',
            'first_name': 'Chef Hendra Wiguna (HR & F&B)',
            'company_name': 'Grand Royal Hotel & Resorts',
            'slug': 'grand-royal-hotel-resorts',
            'industry': 'Perhotelan & Kuliner',
            'company_size': '201+',
            'description': 'Hotel resor bintang 4 dengan standar keramahan internasional. Menjadi mitra penempatan PKL resmi jurusan Tata Boga, Pastry, dan Perhotelan dengan sertifikat industri.',
            'logo_url': '/static/images/companies/logos/grand-royal-hotel-resorts.svg',
            'banner_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1200&q=80',
            'website_url': 'https://grandroyalresorts.com',
            'address': 'Jl. Setiabudi No. 269, Isola, Sukasari',
            'city': 'Bandung',
            'province': 'Jawa Barat',
            'rating': 4.9,
            'review_count': 52,
            'accepts_pkl': True,
            'accepts_internship': True,
            'gallery': [
                ('https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=800&q=80', 'Dapur Utama Standar Restoran Bintang 4 Peserta PKL'),
            ]
        }
    ]

    companies_dict = {}
    for c_data in companies_info:
        user_u, _ = User.objects.get_or_create(
            email=c_data['email'],
            defaults={
                'username': c_data['username'],
                'first_name': c_data['first_name'],
                'role': 'RECRUITER',
                'is_verified': True
            }
        )
        user_u.set_password('password123')
        user_u.save()

        comp, _ = CompanyProfile.objects.get_or_create(
            user=user_u,
            defaults={
                'company_name': c_data['company_name'],
                'slug': c_data['slug'],
                'industry': c_data['industry'],
                'company_size': c_data['company_size'],
                'description': c_data['description'],
                'logo_url': c_data['logo_url'],
                'banner_url': c_data['banner_url'],
                'website_url': c_data['website_url'],
                'address': c_data['address'],
                'city': c_data['city'],
                'province': c_data['province'],
                'is_verified': True,
                'accepts_pkl': c_data['accepts_pkl'],
                'accepts_internship': c_data['accepts_internship'],
                'rating': c_data['rating'],
                'review_count': c_data['review_count'],
            }
        )
        # Update always to ensure correct URLs
        comp.company_name = c_data['company_name']
        comp.slug = c_data['slug']
        comp.industry = c_data['industry']
        comp.logo_url = c_data['logo_url']
        comp.banner_url = c_data['banner_url']
        comp.website_url = c_data['website_url']
        comp.address = c_data['address']
        comp.city = c_data['city']
        comp.province = c_data['province']
        comp.is_verified = True
        comp.rating = c_data['rating']
        comp.review_count = c_data['review_count']
        comp.accepts_pkl = c_data['accepts_pkl']
        comp.accepts_internship = c_data['accepts_internship']
        comp.save()

        # Update gallery photos
        comp.gallery_photos.all().delete()
        for g_url, g_cap in c_data['gallery']:
            CompanyGalleryPhoto.objects.create(company=comp, photo_url=g_url, caption=g_cap)

        companies_dict[c_data['key']] = comp

    print(f"[OK] {len(companies_dict)} Akun perusahaan demo dengan logo & foto unik berhasil disiapkan.")

    # 6. Data 11 Lowongan Kerja & PKL Contoh (Setiap Lowongan Terhubung ke Perusahaan Berbeda)
    job_listings_data = [
        # 1. Lowongan PKL SMK: Web Developer Junior (PT Nusantara Teknologi Mandiri)
        {
            'company': companies_dict['comp_1'],
            'title': 'Magang Web Developer Junior (Khusus PKL SMK RPL)',
            'category': categories['teknologi-informasi'],
            'majors': [majors['Rekayasa Perangkat Lunak (RPL)']],
            'opportunity_type': 'PKL',
            'employment_type': 'INTERNSHIP',
            'workplace_type': 'HYBRID',
            'city': 'Jakarta Selatan',
            'province': 'DKI Jakarta',
            'duration': '3 - 6 Bulan (Sesuai Kurikulum)',
            'requires_pkl_letter': True,
            'min_salary': 1500000,
            'max_salary': 2500000,
            'is_salary_disclosed': True,
            'description': """Kami membuka kesempatan Praktik Kerja Lapangan (PKL) bagi siswa SMK jurusan Rekayasa Perangkat Lunak (RPL).

Tugas & Pembelajaran:
1. Membantu slicing desain UI ke HTML, Tailwind CSS, dan komponen template.
2. Mempelajari version control menggunakan Git & GitHub di lingkungan kerja nyata.
3. Mendapatkan pembimbingan langsung dari Senior Developer setiap minggu.
4. Mengerjakan proyek nyata sistem informasi internal perusahaan.""",
            'requirements': """1. Siswa aktif SMK kelas XI atau XII jurusan RPL.
2. Memahami dasar HTML, CSS, dan logika dasar pemrograman.
3. Membawa laptop sendiri untuk keperluan praktik.
4. Memiliki motivasi belajar tinggi, tepat waktu, dan komunikatif.
5. Wajib melampirkan Surat Pengantar PKL resmi dari pihak sekolah.""",
            'benefits_and_allowance': """- Uang saku transport & makan Rp 1.500.000 - Rp 2.500.000 / bulan
- Sertifikat resmi selesai PKL dari industri teknologi terdaftar
- Mentoring 1-on-1 dengan Senior Software Engineer
- Fasilitas workstation lab & WiFi kecepatan tinggi
- Kesempatan direkrut langsung setelah lulus sekolah"""
        },
        # 2. Lowongan PKL SMK: Mekanik Servis Ringan Kendaraan (PT Wahana Otomotif Nusantara)
        {
            'company': companies_dict['comp_2'],
            'title': 'Mekanik Servis Ringan Mobil (PKL SMK Otomotif / TKRO)',
            'category': categories['otomotif-manufaktur'],
            'majors': [majors['Teknik Kendaraan Ringan Otomotif (TKRO)']],
            'opportunity_type': 'PKL',
            'employment_type': 'INTERNSHIP',
            'workplace_type': 'ONSITE',
            'city': 'Karawang',
            'province': 'Jawa Barat',
            'duration': '6 Bulan',
            'requires_pkl_letter': True,
            'min_salary': 1800000,
            'max_salary': 2500000,
            'is_salary_disclosed': True,
            'description': """Praktik kerja lapangan perawatan berkala kendaraan roda empat, penggantian oli, pengecekan rem, spooring & balancing, serta pengoperasian engine scanner.""",
            'requirements': """1. Siswa aktif SMK jurusan Teknik Kendaraan Ringan Otomotif (TKRO).
2. Mengerti dasar-dasar keselamatan kerja bengkel (K3).
3. Bersedia mengikuti jam kerja operasional bengkel.""",
            'benefits_and_allowance': """- Uang transport & makan
- Disediakan baju seragam bengkel resmi & sepatu safety
- Sertifikat magang resmi agen tunggal pemegang merk (ATPM)"""
        },
        # 3. Lowongan PKL SMK: Desain Grafis & Medsos (Studio Animasi Mandiri)
        {
            'company': companies_dict['comp_3'],
            'title': 'Desainer Grafis & Video Editor Medsos (PKL SMK DKV)',
            'category': categories['desain-multimedia'],
            'majors': [majors['Desain Komunikasi Visual (DKV) / Animasi']],
            'opportunity_type': 'PKL',
            'employment_type': 'INTERNSHIP',
            'workplace_type': 'HYBRID',
            'city': 'Bandung',
            'province': 'Jawa Barat',
            'duration': '3 - 6 Bulan',
            'requires_pkl_letter': True,
            'min_salary': 1500000,
            'max_salary': 2200000,
            'is_salary_disclosed': True,
            'description': """Membantu tim kreatif dalam pembuatan aset konten visual Instagram, TikTok Reels, editing video promosi, serta ilustrasi vektor.""",
            'requirements': """1. Siswa SMK jurusan DKV atau Animasi.
2. Menguasai Adobe Photoshop/Illustrator, Canva Pro, atau CapCut/Premiere.
3. Kreatif dan update terhadap tren media sosial.""",
            'benefits_and_allowance': """- Uang saku Rp 1.500.000 - Rp 2.200.000 / bulan
- Akses pen tablet Wacom & workstation editing di studio
- Portofolio karya nyata berlisensi industri"""
        },
        # 4. Lowongan PKL SMK: Teknisi Jaringan & IT Support (PT Cyber Network Asia)
        {
            'company': companies_dict['comp_4'],
            'title': 'Teknisi Jaringan Komputer & Cloud IT Support (PKL SMK TKJ)',
            'category': categories['teknologi-informasi'],
            'majors': [majors['Teknik Komputer dan Jaringan (TKJ)']],
            'opportunity_type': 'PKL',
            'employment_type': 'INTERNSHIP',
            'workplace_type': 'ONSITE',
            'city': 'Jakarta Selatan',
            'province': 'DKI Jakarta',
            'duration': '3 Bulan',
            'requires_pkl_letter': True,
            'min_salary': 1200000,
            'max_salary': 2000000,
            'is_salary_disclosed': True,
            'description': """Program PKL penanganan jaringan kantor, konfigurasi router Mikrotik/Cisco, crimping LAN kabel, instalasi workstation PC kantor, dan pengenalan server cloud.""",
            'requirements': """1. Siswa aktif SMK jurusan Teknik Komputer dan Jaringan (TKJ).
2. Paham IP subnetting, crimping RJ45, dan troubleshooting OS Windows/Linux.
3. Rajin dan siap bekerja sama dalam tim support.""",
            'benefits_and_allowance': """- Uang saku bulanan
- Sertifikat kompetensi industri jaringan
- Makan siang harian di kantor"""
        },
        # 5. Lowongan Kerja Profesional: Fullstack Developer (PT Data Prima Solusindo)
        {
            'company': companies_dict['comp_5'],
            'title': 'Junior Fullstack Web Developer (Django + HTMX)',
            'category': categories['teknologi-informasi'],
            'majors': [majors['Rekayasa Perangkat Lunak (RPL)'], majors['Teknik Informatika']],
            'opportunity_type': 'JOB',
            'employment_type': 'FULL_TIME',
            'workplace_type': 'HYBRID',
            'city': 'Jakarta Pusat',
            'province': 'DKI Jakarta',
            'duration': '',
            'requires_pkl_letter': False,
            'min_salary': 7000000,
            'max_salary': 11000000,
            'is_salary_disclosed': True,
            'description': """Membangun dan mengembangkan fitur-fitur baru pada platform analitik data dan portal enterprise dengan arsitektur modern Django dan HTMX.""",
            'requirements': """1. Pengalaman dengan framework Django / Python minimal 1 tahun (fresh graduate dipersilakan).
2. Memahami HTMX, Tailwind CSS, dan database relational (PostgreSQL / SQLite).
3. Mampu bekerja sama dalam tim agile / scrum.""",
            'benefits_and_allowance': """- Gaji Rp 7.000.000 - Rp 11.000.000
- BPJS Kesehatan & Ketenagakerjaan
- Laptop operasional kerja (ThinkPad / MacBook)
- Budget pengembangan skill & sertifikasi tahunan"""
        },
        # 6. Lowongan PKL SMK: Staf Keuangan & Pembukuan Kas (PT Artha Solusi Finansial)
        {
            'company': companies_dict['comp_6'],
            'title': 'Staf Keuangan & Pembukuan Kas (Khusus PKL SMK AKL)',
            'category': categories['akuntansi-keuangan'],
            'majors': [majors['Akuntansi dan Keuangan Lembaga (AKL)']],
            'opportunity_type': 'PKL',
            'employment_type': 'INTERNSHIP',
            'workplace_type': 'ONSITE',
            'city': 'Surabaya',
            'province': 'Jawa Timur',
            'duration': '3 - 6 Bulan',
            'requires_pkl_letter': True,
            'min_salary': 1400000,
            'max_salary': 2000000,
            'is_salary_disclosed': True,
            'description': """Praktik kerja lapangan pencatatan bukti transaksi kas masuk/keluar, penyusunan jurnal umum, rekonsiliasi bank, dan pengenalan software akuntansi modern.""",
            'requirements': """1. Siswa aktif SMK kelas XI / XII jurusan Akuntansi dan Keuangan Lembaga (AKL).
2. Memahami siklus dasar akuntansi dan rumus Excel/Spreadsheet.
3. Teliti, jujur, dan memiliki integritas tinggi.""",
            'benefits_and_allowance': """- Uang saku bulanan
- Pelatihan langsung software akuntansi Accurate & Excel Lanjutan
- Sertifikat praktik kerja resmi kantor akuntan publik"""
        },
        # 7. Lowongan Magang Kuliah: UI/UX Designer (PT Hexa Kreasi Digital)
        {
            'company': companies_dict['comp_7'],
            'title': 'Magang Mahasiswa UI/UX Designer',
            'category': categories['desain-multimedia'],
            'majors': [majors['Desain Komunikasi Visual (DKV) / Animasi'], majors['Sistem Informasi']],
            'opportunity_type': 'INTERNSHIP',
            'employment_type': 'INTERNSHIP',
            'workplace_type': 'REMOTE',
            'city': 'Yogyakarta',
            'province': 'DI Yogyakarta',
            'duration': '6 Bulan',
            'requires_pkl_letter': False,
            'min_salary': 2000000,
            'max_salary': 3500000,
            'is_salary_disclosed': True,
            'description': """Merancang antarmuka aplikasi web dan mobile, membuat wireframe, interactive prototype di Figma, dan melakukan usability testing bersama mentor desain.""",
            'requirements': """1. Mahasiswa aktif jurusan DKV, Sistem Informasi, atau Teknik Informatika.
2. Memiliki portofolio desain UI di Behance, Dribbble, atau Notion/Figma.
3. Memahami prinsip User-Centered Design dan Design System.""",
            'benefits_and_allowance': """- Uang saku Rp 2.000.000 - Rp 3.500.000 / bulan
- Kesempatan kerja 100% Remote / WFH fleksibel
- Mentoring dari Head of Product Design"""
        },
        # 8. Lowongan PKL SMK: Teknisi Mesin & Mekatronika (PT Precision Astra Manufacturing)
        {
            'company': companies_dict['comp_8'],
            'title': 'Peserta PKL Teknisi Mesin Kendaraan & Mekatronika',
            'category': categories['otomotif-manufaktur'],
            'majors': [majors['Teknik Mekatronika & Elektronika'], majors['Teknik Kendaraan Ringan Otomotif (TKRO)']],
            'opportunity_type': 'PKL',
            'employment_type': 'INTERNSHIP',
            'workplace_type': 'ONSITE',
            'city': 'Bekasi',
            'province': 'Jawa Barat',
            'duration': '6 Bulan',
            'requires_pkl_letter': True,
            'min_salary': 2000000,
            'max_salary': 3000000,
            'is_salary_disclosed': True,
            'description': """Praktik industri pemeliharaan mesin manufaktur, kalibrasi komponen otomotif presisi, dan pengoperasian instrumen sensor otomatisasi.""",
            'requirements': """1. Siswa SMK jurusan Teknik Mekatronika, Elektronika Industri, atau Otomotif.
2. Disiplin tinggi terhadap SOP dan Keselamatan & Kesehatan Kerja (K3).
3. Bersedia ditempatkan di kawasan pabrik Cikarang.""",
            'benefits_and_allowance': """- Uang saku dan uang makan harian pabrik
- Antar-jemput bus karyawan dari meeting point
- Seragam safety lengkap & sertifikat industri manufaktur Astra"""
        },
        # 9. Lowongan PKL SMK: Administrasi Perkantoran (PT Sentra Mitra Logistik)
        {
            'company': companies_dict['comp_9'],
            'title': 'Staf Administrasi & Tata Kelola Dokumen (PKL SMK OTKP)',
            'category': categories['administrasi-perkantoran'],
            'majors': [majors['Otomatisasi & Tata Kelola Perkantoran (OTKP)']],
            'opportunity_type': 'PKL',
            'employment_type': 'INTERNSHIP',
            'workplace_type': 'ONSITE',
            'city': 'Semarang',
            'province': 'Jawa Tengah',
            'duration': '3 Bulan',
            'requires_pkl_letter': True,
            'min_salary': 1200000,
            'max_salary': 1800000,
            'is_salary_disclosed': True,
            'description': """Membantu pengelolaan arsip surat menyurat kantor, input data inventaris operasional, menyusun jadwal pertemuan, dan menerima telepon tamu dinas.""",
            'requirements': """1. Siswa aktif SMK kelas XI jurusan Otomatisasi & Tata Kelola Perkantoran (OTKP).
2. Terampil mengoperasikan Ms. Word, Excel, dan Google Workspace.
3. Ramah, berpenampilan rapi, dan komunikatif.""",
            'benefits_and_allowance': """- Uang transport bulanan
- Sertifikat verifikasi kompetensi administrasi
- Bimbingan langsung supervisor operasional"""
        },
        # 10. Lowongan Kerja & Magang: Digital Marketing Specialist (PT Brand Booster Indonesia)
        {
            'company': companies_dict['comp_10'],
            'title': 'Spesialis Digital Marketing & Content Creator Medsos',
            'category': categories['pemasaran-digital'],
            'majors': [majors['Desain Komunikasi Visual (DKV) / Animasi']],
            'opportunity_type': 'JOB',
            'employment_type': 'FULL_TIME',
            'workplace_type': 'HYBRID',
            'city': 'Jakarta Barat',
            'province': 'DKI Jakarta',
            'duration': '',
            'requires_pkl_letter': False,
            'min_salary': 5000000,
            'max_salary': 8500000,
            'is_salary_disclosed': True,
            'description': """Mengelola kampanye iklan Meta Ads & TikTok Ads, memproduksi konten storytelling visual, serta menganalisis performa engagement brand.""",
            'requirements': """1. Lulusan SMK / D3 / S1 dengan passion tinggi di digital advertising dan content creation.
2. Memahami metrik CTR, ROAS, dan algoritma media sosial terbaru.
3. Memiliki kemampuan copywriting yang persuasif.""",
            'benefits_and_allowance': """- Gaji Pokok Rp 5.000.000 - Rp 8.500.000 + Bonus performa campaign
- Fasilitas studio podcast & gadget kreator
- Jam kerja fleksibel (hybrid)"""
        },
        # 11. Lowongan PKL SMK: Tata Boga & Perhotelan (Grand Royal Hotel & Resorts)
        {
            'company': companies_dict['comp_11'],
            'title': 'Trainee Perhotelan & Asisten Chef (PKL SMK Tata Boga)',
            'category': categories['perhotelan-kuliner'],
            'majors': [majors['Tata Boga & Perhotelan']],
            'opportunity_type': 'PKL',
            'employment_type': 'INTERNSHIP',
            'workplace_type': 'ONSITE',
            'city': 'Bandung',
            'province': 'Jawa Barat',
            'duration': '6 Bulan',
            'requires_pkl_letter': True,
            'min_salary': 1600000,
            'max_salary': 2400000,
            'is_salary_disclosed': True,
            'description': """Praktik kerja di dapur utama hotel bintang 4, mempelajari persiapan mise en place hidangan nusantara & internasional, standar sanitasi HACCP, serta food presentation.""",
            'requirements': """1. Siswa aktif SMK jurusan Tata Boga atau Perhotelan.
2. Memahami dasar kebersihan dapur dan handling pisau/peralatan masak.
3. Siap bekerja dengan sistem shift hotel dan berjiwa hospitality tinggi.""",
            'benefits_and_allowance': """- Uang saku bulanan
- Disediakan seragam chef resmi & makan 2x sehari saat shift
- Sertifikat PKL resmi hotel bintang 4 bertaraf internasional"""
        }
    ]

    # Hapus lowongan contoh lama yang duplikat agar data rapi dan terhubung benar
    JobListing.objects.all().delete()

    created_jobs = []
    for item in job_listings_data:
        m_list = item.pop('majors')
        comp = item.pop('company')
        job = JobListing.objects.create(
            company=comp,
            created_by=comp.user,
            **item
        )
        job.target_majors.set(m_list)
        created_jobs.append(job)

    print(f"[OK] Berhasil membuat {len(created_jobs)} lowongan contoh yang masing-masing terhubung ke perusahaan unik.")

    # 7. Buat Contoh Lamaran Masuk (Untuk demo dashboard & ATS)
    pkl_job = created_jobs[0]
    import datetime
    from django.utils import timezone

    app_ahmad, _ = Application.objects.get_or_create(
        job_listing=pkl_job,
        applicant=ahmad_user,
        defaults={
            'status': 'INTERVIEW',
            'cover_letter': 'Selamat pagi HRD PT Nusantara Teknologi Mandiri. Saya Ahmad Fauzi siswa kelas XI SMK RPL ingin mengajukan diri mengikuti program PKL di perusahaan Bapak/Ibu. Saya memiliki portofolio web dan surat pengantar dari sekolah.',
        }
    )
    app_ahmad.status = 'INTERVIEW'
    app_ahmad.interview_datetime = timezone.now() + datetime.timedelta(days=3, hours=2)
    app_ahmad.interview_location = 'Gedung Cyber 2 Lantai 14, Ruang Rapat Alpha, Jl. HR Rasuna Said, Jakarta Selatan / Google Meet'
    app_ahmad.interview_notes = 'Harap mengenakan seragam sekolah rapi, membawa laptop pribadi untuk tes praktek slicing, dan membawa Surat Pengantar PKL asli dari sekolah.'
    app_ahmad.save()

    ApplicationStatusHistory.objects.get_or_create(
        application=app_ahmad,
        from_status='SUBMITTED',
        to_status='INTERVIEW',
        defaults={
            'notes': 'Portofolio slicing web Anda sangat rapi. Kami mengundang Anda untuk sesi wawancara perkenalan via Google Meet / Kantor pada Kamis pkl 10.00 WIB.',
            'changed_by': companies_dict['comp_1'].user
        }
    )

    # 8. Buat Contoh Percakapan Chat Aktif (Siswa Ahmad ↔ HRD Dewi Lestari)
    conversation, _ = Conversation.objects.get_or_create(
        applicant=ahmad_user,
        company=companies_dict['comp_1'],
        job_listing=pkl_job
    )

    sample_chat_messages = [
        (ahmad_user, "Selamat siang Ibu Dewi, saya Ahmad Fauzi dari SMKN 1 Jakarta jurusan RPL. Saya ingin menanyakan apakah untuk posisi Web Developer Junior (PKL) saat ini masih ada kuota untuk penempatan 3 bulan?"),
        (companies_dict['comp_1'].user, "Halo Ahmad! Selamat siang. Iya betul, kuota penempatan PKL untuk kompetensi RPL masih terbuka untuk 2 orang siswa. Kami mencari yang sudah paham dasar HTML, CSS, dan Tailwind ya."),
        (ahmad_user, "Baik Ibu, saya sudah melampirkan portofolio mini project web dan Surat Pengantar PKL dari kepala sekolah di sistem Rekrut Mudah. Mohon kesediaannya untuk ditinjau ya Bu."),
        (companies_dict['comp_1'].user, "Bagus sekali Ahmad, berkasmu sudah masuk ke sistem kami dan sedang dalam peninjauan mentor teknis. Kami sudah jadwalkan interview singkat, silakan cek dashboard lamaranmu ya!"),
    ]

    for sender, text in sample_chat_messages:
        ChatMessage.objects.get_or_create(
            conversation=conversation,
            sender=sender,
            message=text,
            defaults={'is_read': True}
        )

    print("\n[SELESAI] Seluruh data contoh Rekrut Mudah telah diperbarui dengan foto & logo berbeda dan valid!")

if __name__ == '__main__':
    run_seed()
