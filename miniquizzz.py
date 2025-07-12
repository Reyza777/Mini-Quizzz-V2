import random
import os
import time

# --- Data Pertanyaan (Dictionary) ---
data_pertanyaan = {
    "ppkn": {
        "mudah": {
            "1": {"pertanyaan": "Dasar negara Indonesia adalah...", "a": "Pancasila", "b": "UUD 1945", "c": "Bhineka Tunggal Ika", "d": "Keadilan Sosial", "jawaban": "a"},
            "2": {"pertanyaan": "Lambang negara Indonesia adalah...", "a": "Garuda Pancasila", "b": "Bintang", "c": "Bung Bang", "d": "Eks", "jawaban": "a"},
            "3": {"pertanyaan": "Sistem pemerintahan di Indonesia adalah...", "a": "Demokrasi", "b": "Pancasila", "c": "Desentralisasi", "d": "Pusat", "jawaban": "a"},
            "4": {"pertanyaan": "Hak asasi manusia adalah...", "a": "Hak yang melekat pada setiap orang", "b": "Kewajiban yang harus dipenuhi", "c": "Peraturan yang dibuat pemerintah", "d": "Sistem hukum", "jawaban": "a"},
            "5": {"pertanyaan": "Tugas presiden adalah...", "a": "Membuat undang-undang", "b": "Mengendalikan kejaksaan", "c": "Kepala negara dan kepala pemerintahan", "d": "Memimpin DPR", "jawaban": "c"},
        },
        "sedang": {
            "1": {"pertanyaan": "Sila keempat Pancasila dilambangkan dengan...", "a": "Kepala Banteng", "b": "Pohon Beringin", "c": "Rantai", "d": "Padi dan Kapas", "jawaban": "a"},
            "2": {"pertanyaan": "Jumlah provinsi di Indonesia saat ini (2024) adalah...", "a": "34", "b": "38", "c": "36", "d": "32", "jawaban": "b"},
            "3": {"pertanyaan": "Undang-Undang Dasar Negara Republik Indonesia Tahun 1945 disahkan pada tanggal...", "a": "17 Agustus 1945", "b": "18 Agustus 1945", "c": "1 Juni 1945", "d": "28 Oktober 1945", "jawaban": "b"},
            "4": {"pertanyaan": "Konsep 'Bhinneka Tunggal Ika' memiliki arti...", "a": "Berbeda-beda tetapi tetap satu jua", "b": "Persatuan dalam keberagaman", "c": "Keadilan sosial bagi seluruh rakyat", "d": "Musyawarah mufakat", "jawaban": "a"},
            "5": {"pertanyaan": "Lembaga negara yang memiliki wewenang untuk menguji undang-undang terhadap UUD adalah...", "a": "Mahkamah Agung", "b": "Mahkamah Konstitusi", "c": "Komisi Yudisial", "d": "Dewan Perwakilan Rakyat", "jawaban": "b"},
        },
        "sulit": {
            "1": {"pertanyaan": "Amandemen UUD 1945 pertama kali dilakukan pada tahun...", "a": "1998", "b": "1999", "c": "2000", "d": "2001", "jawaban": "b"},
            "2": {"pertanyaan": "Istilah 'Staatsfundamentalnorm' merujuk pada...", "a": "Pancasila", "b": "UUD 1945", "c": "TAP MPR", "d": "Perpu", "jawaban": "a"},
            "3": {"pertanyaan": "Siapakah tokoh yang pertama kali mencetuskan gagasan Pancasila?", "a": "Soekarno", "b": "Mohammad Yamin", "c": "Soepomo", "d": "Ki Hajar Dewantara", "jawaban": "a"},
            "4": {"pertanyaan": "Hak imunitas bagi anggota DPR berarti...", "a": "Tidak dapat diganggu gugat", "b": "Tidak dapat dituntut di pengadilan karena pernyataan di sidang", "c": "Bebas dari pajak", "d": "Dapat melakukan apa saja tanpa batasan hukum", "jawaban": "b"},
            "5": {"pertanyaan": "Menurut UUD 1945, Presiden memegang kekuasaan pemerintahan menurut...", "a": "Kehendak rakyat", "b": "Konstitusi", "c": "DPR", "d": "MPR", "jawaban": "b"},
        }
    },
    "matematika": {
        "mudah": {
            "1": {"pertanyaan": "Berapakah hasil dari 5 + 3?", "a": "7", "b": "8", "c": "9", "d": "10", "jawaban": "b"},
            "2": {"pertanyaan": "Jika x = 10, berapakah nilai dari 2x?", "a": "10", "b": "12", "c": "20", "d": "22", "jawaban": "c"},
            "3": {"pertanyaan": "Sebuah segitiga memiliki 3 sisi. Berapa jumlah sudutnya?", "a": "1", "b": "2", "c": "3", "d": "4", "jawaban": "c"},
            "4": {"pertanyaan": "Berapakah hasil dari 15 - 7?", "a": "6", "b": "7", "c": "8", "d": "9", "jawaban": "c"},
            "5": {"pertanyaan": "Jika setiap hari Budi makan 2 apel, berapa apel yang dimakan Budi dalam seminggu?", "a": "7", "b": "10", "c": "12", "d": "14", "jawaban": "d"},
        },
        "sedang": {
            "1": {"pertanyaan": "Berapakah hasil dari (7 * 8) - 4?", "a": "50", "b": "52", "c": "56", "d": "60", "jawaban": "b"},
            "2": {"pertanyaan": "Jika 3x + 5 = 20, berapakah nilai x?", "a": "3", "b": "5", "c": "7", "d": "8", "jawaban": "b"},
            "3": {"pertanyaan": "Keliling persegi dengan sisi 6 cm adalah...", "a": "12 cm", "b": "24 cm", "c": "36 cm", "d": "48 cm", "jawaban": "b"},
            "4": {"pertanyaan": "Faktorisasi prima dari 28 adalah...", "a": "2^2 * 7", "b": "2 * 14", "c": "4 * 7", "d": "2 * 2 * 7", "jawaban": "a"},
            "5": {"pertanyaan": "Sebuah lingkaran memiliki diameter 10 cm. Berapakah jari-jarinya?", "a": "2.5 cm", "b": "5 cm", "c": "10 cm", "d": "20 cm", "jawaban": "b"},
        },
        "sulit": {
            "1": {"pertanyaan": "Turunan pertama dari f(x) = x^2 + 3x - 5 adalah...", "a": "2x + 3", "b": "x + 3", "c": "2x - 5", "d": "x^2 + 3", "jawaban": "a"},
            "2": {"pertanyaan": "Jika sebuah dadu dilempar, berapa peluang muncul angka genap?", "a": "1/6", "b": "1/3", "c": "1/2", "d": "2/3", "jawaban": "c"},
            "3": {"pertanyaan": "Luas permukaan kubus dengan sisi 4 cm adalah...", "a": "16 cm^2", "b": "64 cm^2", "c": "96 cm^2", "d": "128 cm^2", "jawaban": "c"},
            "4": {"pertanyaan": "Nilai dari log2(8) adalah...", "a": "2", "b": "3", "c": "4", "d": "8", "jawaban": "b"},
            "5": {"pertanyaan": "Jika sin(x) = 0.5 dan x di kuadran I, berapakah nilai x dalam derajat?", "a": "30", "b": "45", "c": "60", "d": "90", "jawaban": "a"},
        }
    },
    "ipa": {
        "mudah": {
            "1": {"pertanyaan": "Planet ketiga dari Matahari adalah...", "a": "Mars", "b": "Bumi", "c": "Venus", "d": "Jupiter", "jawaban": "b"},
            "2": {"pertanyaan": "Gas yang paling melimpah di atmosfer Bumi adalah...", "a": "Oksigen", "b": "Karbon dioksida", "c": "Nitrogen", "d": "Argon", "jawaban": "c"},
            "3": {"pertanyaan": "Organ tubuh yang berfungsi memompa darah adalah...", "a": "Paru-paru", "b": "Hati", "c": "Jantung", "d": "Ginjal", "jawaban": "c"},
            "4": {"pertanyaan": "Bagian tumbuhan yang berfungsi menyerap air dan nutrisi dari tanah adalah...", "a": "Batang", "b": "Daun", "c": "Akar", "d": "Bunga", "jawaban": "c"},
            "5": {"pertanyaan": "Satuan dasar massa dalam Sistem Internasional (SI) adalah...", "a": "Gram", "b": "Kilogram", "c": "Pound", "d": "Miligram", "jawaban": "b"},
        },
        "sedang": {
            "1": {"pertanyaan": "Proses perubahan wujud dari padat menjadi gas tanpa melalui fase cair disebut...", "a": "Mencair", "b": "Membeku", "c": "Menyublim", "d": "Menguap", "jawaban": "c"},
            "2": {"pertanyaan": "Fotosintesis adalah proses yang dilakukan tumbuhan untuk membuat makanannya sendiri dengan bantuan...", "a": "Oksigen", "b": "Karbon dioksida dan cahaya matahari", "c": "Air dan nitrogen", "d": "Mineral tanah", "jawaban": "b"},
            "3": {"pertanyaan": "Bagian sel tumbuhan yang bertanggung jawab untuk fotosintesis adalah...", "a": "Mitokondria", "b": "Vakuola", "c": "Kloroplas", "d": "Nukleus", "jawaban": "c"},
            "4": {"pertanyaan": "Hukum Newton yang menyatakan 'setiap aksi memiliki reaksi yang sama dan berlawanan' adalah hukum Newton ke...", "a": "Pertama", "b": "Kedua", "c": "Ketiga", "d": "Nol", "jawaban": "c"},
            "5": {"pertanyaan": "Lapisan atmosfer Bumi yang tempat terjadinya fenomena cuaca adalah...", "a": "Stratosfer", "b": "Mesosfer", "c": "Termosfer", "d": "Troposfer", "jawaban": "d"},
        },
        "sulit": {
            "1": {"pertanyaan": "Apa nama ilmiah untuk manusia?", "a": "Homo Erectus", "b": "Homo Habilis", "c": "Homo Sapiens", "d": "Neanderthal", "jawaban": "c"},
            "2": {"pertanyaan": "Proses pembelahan sel yang menghasilkan dua sel anak identik dengan sel induk disebut...", "a": "Meiosis", "b": "Mitosis", "c": "Fertilisasi", "d": "Mutasi", "jawaban": "b"},
            "3": {"pertanyaan": "Berapa jumlah kromosom pada sel somatik manusia normal?", "a": "23", "b": "46", "c": "48", "d": "24", "jawaban": "b"},
            "4": {"pertanyaan": "Unsur kimia dengan simbol 'Fe' adalah...", "a": "Fosfor", "b": "Fluorin", "c": "Besi", "d": "Emas", "jawaban": "c"},
            "5": {"pertanyaan": "Sifat magnetik suatu bahan yang sangat kuat tertarik oleh medan magnet disebut...", "a": "Paramagnetik", "b": "Diamagnetik", "c": "Feromagnetik", "d": "Antiferomagnetik", "jawaban": "c"},
        }
    }
}

class Pertanyaan:
    def __init__(self, pertanyaan, pilihan_a, pilihan_b, pilihan_c, pilihan_d, jawaban):
        self.pertanyaan = pertanyaan
        self.pilihan = {
            "A": pilihan_a,
            "B": pilihan_b,
            "C": pilihan_c,
            "D": pilihan_d
        }
        self.jawaban = jawaban.upper() # Pastikan jawaban dalam huruf kapital

    def tampilkan_pertanyaan(self, nomor_pertanyaan):
        print(f"Pertanyaan {nomor_pertanyaan}: {self.pertanyaan}")
        for kunci, nilai in self.pilihan.items():
            print(f"  {kunci}. {nilai}")

    def cek_jawaban(self, jawaban_pengguna):
        return jawaban_pengguna.upper() == self.jawaban

class DaftarPertanyaan:
    def __init__(self):
        self.daftar_pertanyaan = []

    def tambah_pertanyaan(self, data_pertanyaan_item):
        pertanyaan_obj = Pertanyaan(
            data_pertanyaan_item["pertanyaan"],
            data_pertanyaan_item["a"],
            data_pertanyaan_item["b"],
            data_pertanyaan_item["c"],
            data_pertanyaan_item["d"],
            data_pertanyaan_item["jawaban"]
        )
        self.daftar_pertanyaan.append(pertanyaan_obj)

    def ambil_pertanyaan_acak(self, jumlah=5):
        # Pastikan tidak mengambil lebih dari yang tersedia
        jumlah = min(jumlah, len(self.daftar_pertanyaan))
        return random.sample(self.daftar_pertanyaan, jumlah)

    def dapatkan_jumlah_pertanyaan(self):
        return len(self.daftar_pertanyaan)

# Inisialisasi koleksi_pertanyaan secara global
koleksi_pertanyaan = {}
for kategori, level_data in data_pertanyaan.items():
    daftar_pertanyaan_kategori = {}
    for level, pertanyaan_list_dict in level_data.items():
        daftar_pertanyaan_level = DaftarPertanyaan()
        for pertanyaan_data_item in pertanyaan_list_dict.values():
            daftar_pertanyaan_level.tambah_pertanyaan(pertanyaan_data_item)
        daftar_pertanyaan_kategori[level] = daftar_pertanyaan_level
    koleksi_pertanyaan[kategori.capitalize()] = daftar_pertanyaan_kategori


# --- Kelas untuk merepresentasikan Graf Kuis ---
class GrafKuis:
    def __init__(self):
        self.simpul = {}  # {'kategori_level': {'data': ..., 'tetangga': [...]}}
        self.sisi = []  # List of tuples (simpul1, simpul2, deskripsi)

        self._bangun_graf()

    def _bangun_graf(self):
        # Tambahkan simpul untuk setiap kategori dan level
        for kategori, level_data in koleksi_pertanyaan.items():
            # Simpul untuk kategori itu sendiri (opsional, tergantung bagaimana Anda ingin memvisualisasikan)
            self.tambah_simpul(kategori, tipe='kategori')
            simpul_level_sebelumnya = None
            for nama_level in ['mudah', 'sedang', 'sulit']: # Pastikan urutan level
                if nama_level in level_data:
                    id_simpul = f"{kategori}_{nama_level}"
                    self.tambah_simpul(id_simpul, tipe='level', kategori=kategori, level=nama_level)
                    # Tambahkan sisi dari kategori ke level mudah
                    if nama_level == 'mudah':
                        self.tambah_sisi(kategori, id_simpul, deskripsi=f"Mulai {nama_level.capitalize()}")
                    # Tambahkan sisi antar level dalam satu kategori
                    if simpul_level_sebelumnya:
                        self.tambah_sisi(simpul_level_sebelumnya, id_simpul, deskripsi=f"Lanjut ke {nama_level.capitalize()}")
                    simpul_level_sebelumnya = id_simpul
            # Reset simpul_level_sebelumnya untuk kategori berikutnya
            simpul_level_sebelumnya = None


    def tambah_simpul(self, id_simpul, **kwargs):
        if id_simpul not in self.simpul:
            self.simpul[id_simpul] = {'id': id_simpul, 'data': kwargs, 'tetangga': []}

    def tambah_sisi(self, id_simpul1, id_simpul2, deskripsi=""):
        if id_simpul1 in self.simpul and id_simpul2 in self.simpul:
            self.simpul[id_simpul1]['tetangga'].append({'ke': id_simpul2, 'deskripsi': deskripsi})
            # Jika ini adalah graf tak berarah, tambahkan juga dari simpul2 ke simpul1
            # self.simpul[id_simpul2]['tetangga'].append({'ke': id_simpul1, 'deskripsi': deskripsi})
            self.sisi.append((id_simpul1, id_simpul2, deskripsi)) # Simpan sisi juga

    def dapatkan_data_graf(self):
        # Mengembalikan data graf dalam format yang mudah diproses (misalnya untuk JSON)
        daftar_simpul = [{'id': id_simpul, **data_simpul['data']} for id_simpul, data_simpul in self.simpul.items()]
        daftar_sisi = [{'dari': sisi[0], 'ke': sisi[1], 'deskripsi': sisi[2]} for sisi in self.sisi]
        return {'simpul': daftar_simpul, 'sisi': daftar_sisi}

    def jalankan_kuis_bertahap(self, nama_pemain, kategori_dipilih):
        skor_akhir = 0
        waktu_mulai_kuis = time.time()

        # Dapatkan simpul kategori awal
        id_simpul_kategori = kategori_dipilih.capitalize()
        if id_simpul_kategori not in self.simpul:
            print(f"Kategori '{kategori_dipilih}' tidak ditemukan dalam graf.")
            return

        urutan_level = ['mudah', 'sedang', 'sulit'] # Urutan level yang tetap

        for nama_level in urutan_level:
            id_simpul_saat_ini = f"{id_simpul_kategori}_{nama_level}"
            if id_simpul_saat_ini in self.simpul:
                pertanyaan_level = koleksi_pertanyaan[id_simpul_kategori][nama_level]
                print(f"\n--- Memulai Kuis {kategori_dipilih.capitalize()} - Level {nama_level.capitalize()} ---")

                pertanyaan_acak = pertanyaan_level.ambil_pertanyaan_acak(5) # Ambil 5 pertanyaan acak per level
                skor_level = 0
                for i, objek_pertanyaan in enumerate(pertanyaan_acak):
                    objek_pertanyaan.tampilkan_pertanyaan(i + 1)
                    while True:
                        jawaban_pengguna = input("Jawaban Anda (A/B/C/D): ").strip().upper()
                        if jawaban_pengguna in ['A', 'B', 'C', 'D']:
                            break
                        else:
                            print("Jawaban tidak valid. Mohon masukkan A, B, C, atau D.")

                    if objek_pertanyaan.cek_jawaban(jawaban_pengguna):
                        print("Jawaban Benar! 🎉")
                        skor_level += 20
                    else:
                        print(f"Jawaban Salah. Jawaban yang benar adalah {objek_pertanyaan.jawaban}. 😞")
                    print("-" * 30)
                    time.sleep(0.5) # Memberi jeda sebentar

                skor_akhir += skor_level
                print(f"Skor Anda untuk level {nama_level.capitalize()}: {skor_level} / {len(pertanyaan_acak) * 20}")
            else:
                print(f"Level '{nama_level.capitalize()}' tidak ditemukan untuk kategori '{kategori_dipilih}'.")

        waktu_selesai_kuis = time.time()
        waktu_tempuh = waktu_selesai_kuis - waktu_mulai_kuis

        print(f"\n--- Kuis {kategori_dipilih.capitalize()} Selesai ---")
        print(f"Skor Akhir Anda: {skor_akhir}")
        print(f"Waktu Tempuh: {waktu_tempuh:.2f} detik")

        simpan_riwayat_skor(nama_pemain, skor_akhir, kategori_dipilih, waktu_tempuh)
        return skor_akhir, waktu_tempuh

def simpan_riwayat_skor(nama_pemain, skor, kategori, waktu_tempuh):
    if not os.path.exists("riwayat_skor.txt"):
        with open("riwayat_skor.txt", "w") as f:
            pass # Buat file jika tidak ada

    with open("riwayat_skor.txt", "a") as f:
        f.write(f"{nama_pemain},{skor},{kategori},{waktu_tempuh:.2f}\n")

def tampilkan_riwayat_skor():
    print("\n--- Riwayat Skor ---")
    if not os.path.exists("riwayat_skor.txt") or os.stat("riwayat_skor.txt").st_size == 0:
        print("Belum ada riwayat skor.")
        return

    data_skor = []
    with open("riwayat_skor.txt", "r") as f:
        for baris in f:
            try:
                nama, skor_str, kategori, waktu_str = baris.strip().split(",")
                data_skor.append({
                    "nama": nama,
                    "skor": int(skor_str),
                    "kategori": kategori,
                    "waktu": float(waktu_str)
                })
            except ValueError:
                continue # Lewati baris yang tidak valid

    if not data_skor:
        print("Belum ada riwayat skor yang valid.")
        return

    # Peringkat Skor Keseluruhan
    print("\n=== Peringkat Skor Keseluruhan ===")
    skor_total_per_pemain = {}
    for data in data_skor:
        skor_total_per_pemain[data["nama"]] = skor_total_per_pemain.get(data["nama"], 0) + data["skor"]

    peringkat_keseluruhan = sorted(skor_total_per_pemain.items(), key=lambda item: item[1], reverse=True)

    for i, (nama, total_skor) in enumerate(peringkat_keseluruhan):
        print(f"{i+1}. {nama}: {total_skor} poin")

    return data_skor # Kembalikan data skor untuk fungsi peringkat_skor_per_kategori

def peringkat_skor_per_kategori(kategori_dipilih):
    print(f"\n--- Peringkat Skor Kategori: {kategori_dipilih.capitalize()} ---")
    data_skor = []
    if not os.path.exists("riwayat_skor.txt") or os.stat("riwayat_skor.txt").st_size == 0:
        print("Belum ada riwayat skor.")
        return

    with open("riwayat_skor.txt", "r") as f:
        for baris in f:
            try:
                nama, skor_str, kategori, waktu_str = baris.strip().split(",")
                if kategori.lower() == kategori_dipilih.lower():
                    data_skor.append({
                        "nama": nama,
                        "skor": int(skor_str),
                        "waktu": float(waktu_str)
                    })
            except ValueError:
                continue

    if not data_skor:
        print(f"Belum ada skor untuk kategori '{kategori_dipilih}'.")
        return

    # Urutkan berdasarkan skor tertinggi, jika skor sama, waktu terendah
    data_skor_terurut = sorted(data_skor, key=lambda x: (x["skor"], -x["waktu"]), reverse=True)

    for i, data in enumerate(data_skor_terurut):
        print(f"{i+1}. {data['nama']}: {data['skor']} poin (Waktu: {data['waktu']:.2f} detik)")

def tampilkan_menu_utama(graf_kuis):
    while True:
        print("\n--- Menu Utama ---")
        print("1. Mulai Kuis")
        print("2. Lihat Riwayat Skor")
        print("3. Lihat Peringkat Skor per Kategori")
        print("4. Lihat Struktur Graf Kuis") # Opsi baru
        print("5. Keluar")

        pilihan = input("Pilih opsi (1-5): ").strip()

        if pilihan == '1':
            daftar_topik = list(koleksi_pertanyaan.keys())
            print("\nPilih kategori pertanyaan:")
            for i, topik in enumerate(daftar_topik, 1):
                print(f"{i}. {topik}")
            while True:
                try:
                    indeks_kategori_dipilih = int(input(f"Masukkan nomor kategori (1-{len(daftar_topik)}): ")) - 1
                    if 0 <= indeks_kategori_dipilih < len(daftar_topik):
                        kategori_dipilih = daftar_topik[indeks_kategori_dipilih]
                        break
                    else:
                        print("Nomor kategori tidak valid.")
                except ValueError:
                    print("Input tidak valid. Masukkan nomor kategori.")
            nama_pemain = input("Masukkan Nama Pemain: ").strip()
            print(f"\nSelamat Bermain, {nama_pemain}! Semoga beruntung!\n")
            graf_kuis.jalankan_kuis_bertahap(nama_pemain, kategori_dipilih)
        elif pilihan == '2':
            tampilkan_riwayat_skor()
        elif pilihan == '3':
            daftar_topik = list(koleksi_pertanyaan.keys())
            print("\nPilih kategori untuk peringkat:")
            for i, topik in enumerate(daftar_topik, 1):
                print(f"{i}. {topik}")
            while True:
                try:
                    indeks_kategori_dipilih = int(input(f"Masukkan nomor kategori (1-{len(daftar_topik)}): ")) - 1
                    if 0 <= indeks_kategori_dipilih < len(daftar_topik):
                        kategori_dipilih = daftar_topik[indeks_kategori_dipilih]
                        peringkat_skor_per_kategori(kategori_dipilih)
                        break
                    else:
                        print("Nomor kategori tidak valid.")
                except ValueError:
                    print("Input tidak valid. Masukkan nomor kategori.")
        elif pilihan == '4':
            # Menampilkan struktur graf (teks sederhana)
            print("\n--- Struktur Graf Kuis ---")
            data_graf = graf_kuis.dapatkan_data_graf()
            print("Simpul:")
            for simpul in data_graf['simpul']:
                print(f"  - {simpul['id']} (Tipe: {simpul.get('tipe', 'N/A')})")
            print("Sisi:")
            for sisi in data_graf['sisi']:
                print(f"  - {sisi['dari']} --({sisi['deskripsi']})--> {sisi['ke']}")
        elif pilihan == '5':
            print("Terima kasih telah bermain Mini Kuis! Sampai jumpa lagi. 👋")
            break
        else:
            print("Pilihan tidak valid. Mohon masukkan angka 1-5.")

def main():
    print("Selamat Datang di Mini Kuis! 🧠")
    objek_graf_kuis = GrafKuis() # Inisialisasi GrafKuis di awal
    tampilkan_menu_utama(objek_graf_kuis)

if __name__ == "__main__":
    main()