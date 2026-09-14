@echo off
title Rekrut Mudah - Local Server Runner
color 0A

echo ========================================================
echo       MENJALANKAN LOCALHOST APLIKASI REKRUT MUDAH
echo ========================================================
echo.

cd /d "%~dp0"

set PYTHON_BIN=C:\laragon\bin\python\python-3.10\python.exe

if not exist "%PYTHON_BIN%" (
    echo [!] Python Laragon tidak ditemukan di %PYTHON_BIN%
    echo [*] Mencoba python default dari PATH...
    set PYTHON_BIN=python
)

echo [*] Menggunakan Python: %PYTHON_BIN%
echo.

echo [*] Langkah 1/4: Memeriksa dan menginstal dependensi...
"%PYTHON_BIN%" -m pip install django django-htmx pillow
if %ERRORLEVEL% NEQ 0 (
    echo [!] Gagal menginstal dependensi.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [*] Langkah 2/4: Menjalankan migrasi database...
"%PYTHON_BIN%" manage.py makemigrations accounts jobs applications chat
"%PYTHON_BIN%" manage.py migrate

echo.
echo [*] Langkah 3/4: Memasukkan data contoh (Seeding Akun & Loker)...
"%PYTHON_BIN%" seed_data.py

echo.
echo [*] Langkah 4/4: Membuka browser dan menyalakan server...
start http://127.0.0.1:8000/

echo.
echo ========================================================
echo   Server sedang berjalan di http://127.0.0.1:8000/
echo   Tekan CTRL + C di jendela ini untuk menghentikan server
echo ========================================================
echo.

"%PYTHON_BIN%" manage.py runserver 127.0.0.1:8000
pause
