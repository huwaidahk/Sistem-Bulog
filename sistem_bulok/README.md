# Sistem Bulok

Sistem Bulok adalah aplikasi manajemen pemasokan, penyortiran, penyimpanan, dan distribusi beras.

## Persyaratan
- Python 3.8+
- MySQL server aktif (database named `bulok`)

## Instalasi
1. Clone atau extract project ke folder lokal.
2. (Opsional) Buat virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependency:

```bash
pip install -r requirements.txt
```

4. Siapkan database MySQL (tidak menggunakan password user root by default). Di MySQL client jalankan:

```sql
CREATE DATABASE bulok;
```

atau set environment variable `DATABASE_URL` jika Anda ingin koneksi lain, misal:

```bash
export DATABASE_URL='mysql+pymysql://user:password@host/bulok'
```

5. Jalankan aplikasi:

```bash
python app.py
```

6. Buka browser ke `http://127.0.0.1:5000`.

## Catatan
- Aplikasi ini **tidak menggunakan autentikasi** (sesuai permintaan) — pastikan menambahkan autentikasi jika hendak dipakai di lingkungan multi-user.
- Saat pertama kali dijalankan, aplikasi akan otomatis membuat tabel dan **mengisi data dummy** (supplier, tipe beras, item, gudang, konsumen, transaksi) jika database masih kosong.
- Untuk mengganti koneksi database tanpa mengubah file `config.py`, set environment variable `DATABASE_URL` sebelum menjalankan aplikasi.

## Struktur proyek
Lihat struktur folder utama di root: `app.py`, `models.py`, `forms.py`, `config.py`, folder `templates` dan `static`.

Selamat mencoba!
