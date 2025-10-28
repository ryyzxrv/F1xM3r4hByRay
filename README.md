# F1xM3r4hByRay

Bot Telegram untuk Fix Merah nomor kamu secara otomatis melalui email.

---

## Fitur

- 🧩 **Fix Merah** — Kirim nomor merah kamu untuk otomatis diproses.
- 📱 **Cek Nomor** — Cek format nomor Telegram kamu.
- 👤 **Cek ID** — Menampilkan ID Telegram kamu.
- 💎 **Premium System** — Akses fitur tertentu hanya untuk pengguna premium.
- 📄 **Email Otomatis** — Mengirim email otomatis untuk nomor merah menggunakan akun email yang telah dikonfigurasi.

---

## Persyaratan

- Python 3.10+  
- Modul Python:
- pip install -r requirements.txt
- Telegram Bot Token (dari BotFather)
- File `accounts.json` berisi akun email untuk mengirim pesan.

## Struktur Folder / File

F1xM3r4hByRay/ │ 
├─ bot.py               # Script utama bot Telegram 
├─ utils_premium.py     # Sistem premium & Owner 
├─ accounts.json        # Akun email untuk kirim Fix Merah 
├─ requirements.txt     # Dependencies Python 
├─ procfile             # (Opsional) untuk deploy ke Heroku └─ README.md

## Instalasi

1. Clone repo:

```git clone https://github.com/ryyzxrv/F1xM3r4hByRay.git cd F1xM3r4hByRay```

2. Install dependencies:

pip install -r requirements.txt

3. Buat file .env atau edit langsung bot.py untuk menambahkan token Telegram:


TELEGRAM_TOKEN = "ISI_TOKEN_KAMU"

4. Konfigurasi accounts.json:


{
  "to_email": "tujuan@example.com",
  "accounts": [
    {
      "email": "example1@gmail.com",
      "password": "password1",
      "smtp": "smtp.gmail.com",
      "port": 587
    },
    {
      "email": "example2@gmail.com",
      "password": "password2"
    }
  ]
}

## Penggunaan

1. Jalankan bot:

```python bot.py```

2. Buka Telegram dan kirim `/start` ke bot.


3. Klik tombol 🧩 Fix Merah dan ikuti instruksi.


4. Untuk menambahkan premium user (hanya Owner):

```/addprem @username 10d```

5. Untuk cek status premium:

```/premium```

## Catatan

Fitur Fix Merah hanya bisa diakses user premium.

Global cooldown 20 detik untuk menghindari spam email.

Pastikan akun email yang digunakan bisa login dan SMTP aktif.
