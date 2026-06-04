from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

# Konfigurasi Database SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///perpustakaan.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ================= SKEMA DATABASE =================
class Buku(db.Model):
    id_buku = db.Column(db.String(20), primary_key=True)
    judul = db.Column(db.String(100))
    pengarang = db.Column(db.String(100))
    penerbit = db.Column(db.String(100))
    genre = db.Column(db.String(100))

class Anggota(db.Model):
    id_anggota = db.Column(db.String(20), primary_key=True)
    nama = db.Column(db.String(100))
    jenis_kelamin = db.Column(db.String(20))
    no_hp = db.Column(db.String(20))
    kelas = db.Column(db.String(50))

class Peminjaman(db.Model):
    id_peminjaman = db.Column(db.String(20), primary_key=True)
    judul_buku = db.Column(db.String(100))
    peminjam = db.Column(db.String(100))
    tanggal_peminjaman = db.Column(db.String(50))
    jatuh_tempo = db.Column(db.String(50))

with app.app_context():
    db.create_all()

# ================= API BUKU =================
@app.route('/api/buku', methods=['GET', 'POST'])
def kelola_buku():
    if request.method == 'GET':
        buku_list = Buku.query.all()
        return jsonify([{'id_buku': b.id_buku, 'judul': b.judul, 'pengarang': b.pengarang, 'penerbit': b.penerbit, 'genre': b.genre} for b in buku_list])
    
    if request.method == 'POST':
        data = request.json
        buku_baru = Buku(id_buku=data['id_buku'], judul=data['judul'], pengarang=data['pengarang'], penerbit=data['penerbit'], genre=data['genre'])
        db.session.add(buku_baru)
        db.session.commit()
        return jsonify({'message': 'Berhasil tambah buku'})

@app.route('/api/buku/<id>', methods=['PUT', 'DELETE'])
def edit_hapus_buku(id):
    buku = Buku.query.get(id)
    if not buku: return jsonify({'message': 'Tidak ditemukan'}), 404

    if request.method == 'PUT':
        data = request.json
        buku.judul, buku.pengarang, buku.penerbit, buku.genre = data['judul'], data['pengarang'], data['penerbit'], data['genre']
        db.session.commit()
        return jsonify({'message': 'Berhasil edit buku'})
        
    if request.method == 'DELETE':
        db.session.delete(buku)
        db.session.commit()
        return jsonify({'message': 'Berhasil hapus buku'})

# ================= API ANGGOTA =================
@app.route('/api/anggota', methods=['GET', 'POST'])
def kelola_anggota():
    if request.method == 'GET':
        anggota_list = Anggota.query.all()
        return jsonify([{'id_anggota': a.id_anggota, 'nama': a.nama, 'jenis_kelamin': a.jenis_kelamin, 'no_hp': a.no_hp, 'kelas': a.kelas} for a in anggota_list])
    
    if request.method == 'POST':
        data = request.json
        anggota_baru = Anggota(id_anggota=data['id_anggota'], nama=data['nama'], jenis_kelamin=data['jenis_kelamin'], no_hp=data['no_hp'], kelas=data['kelas'])
        db.session.add(anggota_baru)
        db.session.commit()
        return jsonify({'message': 'Berhasil tambah anggota'})

@app.route('/api/anggota/<id>', methods=['PUT', 'DELETE'])
def edit_hapus_anggota(id):
    anggota = Anggota.query.get(id)
    if not anggota: return jsonify({'message': 'Tidak ditemukan'}), 404

    if request.method == 'PUT':
        data = request.json
        anggota.nama, anggota.jenis_kelamin, anggota.no_hp, anggota.kelas = data['nama'], data['jenis_kelamin'], data['no_hp'], data['kelas']
        db.session.commit()
        return jsonify({'message': 'Berhasil edit anggota'})
        
    if request.method == 'DELETE':
        db.session.delete(anggota)
        db.session.commit()
        return jsonify({'message': 'Berhasil hapus anggota'})

# ================= API PEMINJAMAN =================
@app.route('/api/peminjaman', methods=['GET', 'POST'])
def kelola_peminjaman():
    if request.method == 'GET':
        pinjam_list = Peminjaman.query.all()
        return jsonify([{'id_peminjaman': p.id_peminjaman, 'judul_buku': p.judul_buku, 'peminjam': p.peminjam, 'tanggal_peminjaman': p.tanggal_peminjaman, 'jatuh_tempo': p.jatuh_tempo} for p in pinjam_list])
    
    if request.method == 'POST':
        data = request.json
        pinjam_baru = Peminjaman(id_peminjaman=data['id_peminjaman'], judul_buku=data['judul_buku'], peminjam=data['peminjam'], tanggal_peminjaman=data['tanggal_peminjaman'], jatuh_tempo=data['jatuh_tempo'])
        db.session.add(pinjam_baru)
        db.session.commit()
        return jsonify({'message': 'Berhasil tambah peminjaman'})

@app.route('/api/peminjaman/<id>', methods=['PUT', 'DELETE'])
def edit_hapus_peminjaman(id):
    pinjam = Peminjaman.query.get(id)
    if not pinjam: return jsonify({'message': 'Tidak ditemukan'}), 404

    if request.method == 'PUT':
        data = request.json
        pinjam.judul_buku, pinjam.peminjam, pinjam.tanggal_peminjaman, pinjam.jatuh_tempo = data['judul_buku'], data['peminjam'], data['tanggal_peminjaman'], data['jatuh_tempo']
        db.session.commit()
        return jsonify({'message': 'Berhasil edit peminjaman'})
        
    if request.method == 'DELETE':
        db.session.delete(pinjam)
        db.session.commit()
        return jsonify({'message': 'Berhasil hapus peminjaman'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)