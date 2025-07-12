from flask import Flask, render_template, request, jsonify
import random
import os
import time

# --- Impor data_pertanyaan dari miniquiz.py Anda ---
# Pastikan miniquiz.py berada di direktori yang sama atau diimpor dengan benar
from miniquiz import data_pertanyaan, DaftarPertanyaan, GrafKuis

app = Flask(__name__)

# Menginisialisasi ulang koleksi_pertanyaan agar mudah diakses di Flask
koleksi_pertanyaan = {}
for kategori, data_level in data_pertanyaan.items():
    daftar_pertanyaan_kategori = {}
    for level, daftar_pertanyaan_dict in data_level.items():
        objek_daftar_pertanyaan_level = DaftarPertanyaan()
        for data_pertanyaan_item in daftar_pertanyaan_dict.values():
            objek_daftar_pertanyaan_level.tambah_pertanyaan(data_pertanyaan_item)
        daftar_pertanyaan_kategori[level] = objek_daftar_pertanyaan_level
    koleksi_pertanyaan[kategori.capitalize()] = daftar_pertanyaan_kategori

# Inisialisasi GrafKuis di sini agar bisa diakses oleh rute
objek_graf_kuis = GrafKuis()

# --- Endpoint API untuk Data Kuis ---
@app.route('/api/kuis/<kategori_req>/<level_req>', methods=['GET'])
def dapatkan_pertanyaan_kuis(kategori_req, level_req):
    kategori_format = kategori_req.capitalize()
    if kategori_format in koleksi_pertanyaan and level_req in koleksi_pertanyaan[kategori_format]:
        daftar_data_kuis = koleksi_pertanyaan[kategori_format][level_req].ambil_pertanyaan_acak(5) # Ambil 5 pertanyaan acak
        # Format pertanyaan untuk respons JSON
        pertanyaan_terformat = []
        for p in daftar_data_kuis:
            opsi = {k.upper(): v for k, v in p.pilihan.items()} # Mengakses p.pilihan
            pertanyaan_terformat.append({
                "pertanyaan": p.pertanyaan, # Mengakses p.pertanyaan
                "opsi": opsi,
                "jawaban": p.jawaban.upper() # Mengakses p.jawaban
            })
        return jsonify(pertanyaan_terformat)
    return jsonify({"error": "Kategori atau level tidak ditemukan"}), 404

# --- Endpoint API untuk Menyimpan Skor (disederhanakan untuk demonstrasi) ---
@app.route('/api/simpan_skor', methods=['POST'])
def simpan_skor_api():
    data = request.get_json()
    nama_pemain = data.get('nama_pemain')
    skor = data.get('skor')
    kategori_level = data.get('kategori_level')
    waktu_tempuh = data.get('waktu_tempuh')

    if not all([nama_pemain, skor, kategori_level, waktu_tempuh]):
        return jsonify({"error": "Data tidak lengkap"}), 400

    try:
        with open("riwayat_skor.txt", "a") as f:
            f.write(f"{nama_pemain},{skor},{kategori_level},{waktu_tempuh}\n")
        return jsonify({"pesan": "Skor berhasil disimpan"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Endpoint API untuk Mendapatkan Semua Skor (disederhanakan untuk demonstrasi) ---
@app.route('/api/skor', methods=['GET'])
def dapatkan_semua_skor():
    daftar_skor = []
    if os.path.exists("riwayat_skor.txt"):
        with open("riwayat_skor.txt", "r") as f:
            for baris in f:
                try:
                    nama, skor, kategori_level, waktu_tempuh = baris.strip().split(",")
                    daftar_skor.append({
                        "nama": nama,
                        "skor": int(skor),
                        "kategori_level": kategori_level,
                        "waktu_tempuh": float(waktu_tempuh)
                    })
                except ValueError:
                    continue # Lewati baris yang tidak valid
    return jsonify(daftar_skor)

# --- Endpoint API untuk mendapatkan data graf/pohon ---
@app.route('/api/data_graf', methods=['GET'])
def dapatkan_data_graf_api():
    return jsonify(objek_graf_kuis.dapatkan_data_graf())

# --- Rute utama untuk menyajikan halaman HTML ---
@app.route('/')
def indeks():
    kategori = list(koleksi_pertanyaan.keys())
    return render_template('indeks.html', kategori=kategori)

if __name__ == '__main__':
    # Pastikan riwayat_skor.txt ada
    if not os.path.exists("riwayat_skor.txt"):
        with open("riwayat_skor.txt", "w") as f:
            pass # Buat file kosong jika tidak ada

    app.run(debug=True) # debug=True untuk pengembangan, matikan untuk produksi