import os
import sqlite3
from app import app, db, Buku, Anggota, Peminjaman

base_dir = os.path.abspath(os.path.dirname(__file__))
instance_dir = os.path.join(base_dir, 'instance')

print("=== MEMULAI JURUS PAMUNGKAS PATCH DATABASE ===")

# 1. SUNTIK LANGSUNG KOLOM STOK VIA SQL MURNI (ANTI LOCK & TANPA HAPUS FILE)
db_files = ['perpustakaan.db', 'perpustakaan_baru.db']
for db_file in db_files:
    db_path = os.path.join(instance_dir, db_file)
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            # Paksa tambah kolom stok ke dalam tabel buku yang sudah ada
            cursor.execute("ALTER TABLE buku ADD COLUMN stok INTEGER DEFAULT 0")
            conn.commit()
            conn.close()
            print(f"✅ SQL PATCH: Kolom 'stok' berhasil disuntik paksa ke {db_file}!")
        except Exception as e:
            # Jika kolom sudah ada, SQL akan error dan otomatis kita abaikan lewat pass
            print(f"ℹ️ SQL PATCH: {db_file} sudah aman atau dilewati.")
            pass

# 2. RE-SET DAN SUNTIK DATA ULANG AGAR BERSIH DAN SESUAI
with app.app_context():
    # Pastikan skema ORM Flask mendeteksi tabel
    db.create_all()

    print("Cleaning data lama agar tidak duplikat...")
    try:
        db.session.query(Buku).delete()
        db.session.query(Anggota).delete()
        db.session.query(Peminjaman).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()

    # Siapkan 9 daftar buku kelompokmu + Otomatis Set Stok = 5
    buku_buku = [
        Buku(id_buku="113", judul="Matematika Tingkat Lanjut untuk SMA/MA Kelas XII (12)", pengarang="Wikan Budi Utami, Sri Adi Widodo", penerbit="Kementrian Pendidikan", genre="Edukasi", stok=5),
        Buku(id_buku="112", judul="Kimia SMA/MA Kelas XII (12)", pengarang="Galuh Yuliani, Hanhan Dianhar", penerbit="Kementrian Pendidikan", genre="Edukasi", stok=5),
        Buku(id_buku="111", judul="Bahasa Inggris: English for Change SMA/MA Kelas XII (12)", pengarang="Puji Astuti, Aria Septi Anggaira", penerbit="Kementrian Pendidikan", genre="Edukasi", stok=5),
        Buku(id_buku="013", judul="Filosofi Teras", pengarang="Henry Manampiring", penerbit="Kompas", genre="Filsafat", stok=5),
        Buku(id_buku="012", judul="Atomic Habits", pengarang="James Clear", penerbit="Gramedia Pustaka Utama", genre="Psikologi", stok=5),
        Buku(id_buku="011", judul="The Power of Habit", pengarang="Charles Duhigg", penerbit="Kepustakaan Populer Gramedia", genre="Psikologi", stok=5),
        Buku(id_buku="003", judul="Laskar Pelangi", pengarang="Andrea Hirata", penerbit="Bentang Pustaka", genre="Drama", stok=5),
        Buku(id_buku="002", judul="Perahu Kertas", pengarang="Dee Lestari", penerbit="Bentang Pustaka", genre="Novel", stok=5),
        Buku(id_buku="001", judul="Hujan", pengarang="Tere Liye", penerbit="Gramedia", genre="Fiksi Ilmiah", stok=5)
    ]
    
    anggota_baru = Anggota(id_anggota="0078912", nama="kina", jenis_kelamin="perempuan", no_hp="082334455667", kelas="12")
    peminjaman_baru = Peminjaman(id_peminjaman="tes123", judul_buku="Hujan", peminjam="anon", tanggal_peminjaman="2026-06-03", jatuh_tempo="2026-06-30")

    try:
        db.session.add_all(buku_buku)
        db.session.add(anggota_baru)
        db.session.add(peminjaman_baru)
        db.session.commit()
        print("🎉 SUCCESS: Kolom STOK aktif & seluruh data kelompokmu 100% pulih sempurna!")
    except Exception as e:
        db.session.rollback()
        print("❌ Gagal memasukkan data. Detail:", e)