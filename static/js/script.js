document.addEventListener('DOMContentLoaded', () => {
    const layarAwal = document.getElementById('layar-awal');
    const layarKuis = document.getElementById('layar-kuis');
    const layarHasil = document.getElementById('layar-hasil');
    const layarPeringkat = document.getElementById('layar-peringkat');
    const layarTampilanPohon = document.getElementById('layar-tampilan-pohon'); // Elemen baru

    const inputNamaPemain = document.getElementById('nama-pemain');
    const tombolKategori = document.querySelectorAll('.tombol-kategori');
    const tombolLihatStrukturKuis = document.getElementById('lihat-struktur-kuis'); // Tombol baru

    const spanKategoriSaatIni = document.getElementById('kategori-saat-ini');
    const spanLevelSaatIni = document.getElementById('level-saat-ini');
    const spanNomorPertanyaan = document.getElementById('nomor-pertanyaan');
    const spanTotalPertanyaan = document.getElementById('total-pertanyaan');
    const teksPertanyaan = document.getElementById('teks-pertanyaan');
    const wadahOpsi = document.getElementById('wadah-opsi');
    const tombolKirimJawaban = document.getElementById('kirim-jawaban');

    const spanSkorAkhir = document.getElementById('skor-akhir');
    const spanWaktuTempuh = document.getElementById('waktu-tempuh');
    const tombolMainLagi = document.getElementById('main-lagi');
    const tombolLihatPeringkat = document.getElementById('lihat-peringkat');

    const daftarPeringkatKeseluruhan = document.getElementById('daftar-peringkat-keseluruhan');
    const pilihPeringkatKategori = document.getElementById('pilih-peringkat-kategori');
    const daftarPeringkatKategori = document.getElementById('daftar-peringkat-kategori');
    const tombolKembaliKeAwal = document.getElementById('kembali-ke-awal');
    const tombolKembaliDariTampilanPohon = document.getElementById('kembali-dari-tampilan-pohon'); // Tombol baru

    const wadahPohonKuis = document.getElementById('wadah-pohon-kuis'); // Wadah pohon

    let namaPemain = '';
    let kategoriTerpilih = '';
    let pertanyaanSaatIni = [];
    let indeksPertanyaanSaatIni = 0;
    let skor = 0;
    let waktuMulai = 0;
    let levelKuis = ['mudah', 'sedang', 'sulit'];
    let indeksLevelKuisSaatIni = 0;
    let totalPertanyaanDalamKuis = 0;

    // --- Fungsi Alur Permainan ---
    function tampilkanLayar(layar) {
        layarAwal.style.display = 'none';
        layarKuis.style.display = 'none';
        layarHasil.style.display = 'none';
        layarPeringkat.style.display = 'none';
        layarTampilanPohon.style.display = 'none'; // Sembunyikan layar pohon
        layar.style.display = 'block';
    }

    async function mulaiKuis() {
        namaPemain = inputNamaPemain.value.trim();
        if (!namaPemain) {
            alert('Mohon masukkan nama pemain!');
            return;
        }

        skor = 0;
        indeksPertanyaanSaatIni = 0;
        indeksLevelKuisSaatIni = 0;
        totalPertanyaanDalamKuis = levelKuis.length * 5;
        waktuMulai = Date.now();

        spanKategoriSaatIni.textContent = kategoriTerpilih;
        spanTotalPertanyaan.textContent = totalPertanyaanDalamKuis;

        await muatLevelBerikutnya();
        tampilkanLayar(layarKuis);
    }

    async function muatLevelBerikutnya() {
        const level = levelKuis[indeksLevelKuisSaatIni];
        spanLevelSaatIni.textContent = level.charAt(0).toUpperCase() + level.slice(1);

        try {
            const respons = await fetch(`/api/kuis/${kategoriTerpilih}/${level}`);
            if (!respons.ok) {
                throw new Error(`Kesalahan HTTP! status: ${respons.status}`);
            }
            const pertanyaan = await respons.json();
            pertanyaanSaatIni = pertanyaan;
            indeksPertanyaanSaatIni = 0;
            tampilkanPertanyaan();
        } catch (error) {
            console.error('Kesalahan saat memuat pertanyaan:', error);
            alert('Gagal memuat pertanyaan. Silakan coba lagi.');
        }
    }

    function tampilkanPertanyaan() {
        if (indeksPertanyaanSaatIni < pertanyaanSaatIni.length) {
            const pertanyaan = pertanyaanSaatIni[indeksPertanyaanSaatIni];
            spanNomorPertanyaan.textContent = (indeksLevelKuisSaatIni * 5) + indeksPertanyaanSaatIni + 1;
            teksPertanyaan.innerHTML = pertanyaan.pertanyaan;
            wadahOpsi.innerHTML = '';

            for (const kunci in pertanyaan.opsi) {
                const tombolOpsi = document.createElement('button');
                tombolOpsi.classList.add('tombol-opsi');
                tombolOpsi.dataset.kunci = kunci;
                tombolOpsi.innerHTML = `${kunci}. ${pertanyaan.opsi[kunci]}`;
                tombolOpsi.addEventListener('click', () => {
                    wadahOpsi.querySelectorAll('.tombol-opsi').forEach(btn => {
                        btn.classList.remove('terpilih');
                    });
                    tombolOpsi.classList.add('terpilih');
                });
                wadahOpsi.appendChild(tombolOpsi);
            }
            tombolKirimJawaban.disabled = false;
        } else {
            indeksLevelKuisSaatIni++;
            if (indeksLevelKuisSaatIni < levelKuis.length) {
                muatLevelBerikutnya();
            } else {
                selesaiKuis();
            }
        }
    }

    async function cekJawaban() {
        const opsiTerpilih = wadahOpsi.querySelector('.tombol-opsi.terpilih');
        if (!opsiTerpilih) {
            alert('Mohon pilih jawaban Anda!');
            return;
        }

        tombolKirimJawaban.disabled = true;

        const jawabanPengguna = opsiTerpilih.dataset.kunci;
        const jawabanBenar = pertanyaanSaatIni[indeksPertanyaanSaatIni].jawaban;

        wadahOpsi.querySelectorAll('.tombol-opsi').forEach(btn => {
            btn.style.pointerEvents = 'none';
            if (btn.dataset.kunci === jawabanBenar) {
                btn.classList.add('benar');
            } else if (btn.dataset.kunci === jawabanPengguna) {
                btn.classList.add('salah');
            }
        });

        if (jawabanPengguna === jawabanBenar) {
            skor += 20;
            console.log('Benar! Skor saat ini:', skor);
        } else {
            console.log('Salah. Jawaban yang benar adalah:', jawabanBenar);
        }

        setTimeout(() => {
            indeksPertanyaanSaatIni++;
            tampilkanPertanyaan();
        }, 1500);
    }

    async function selesaiKuis() {
        const waktuSelesai = Date.now();
        const waktuTempuh = ((waktuSelesai - waktuMulai) / 1000).toFixed(2);

        spanSkorAkhir.textContent = skor;
        spanWaktuTempuh.textContent = waktuTempuh;

        try {
            await fetch('/api/simpan_skor', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    nama_pemain: namaPemain,
                    skor: skor,
                    kategori_level: `${kategoriTerpilih}_${levelKuis[indeksLevelKuisSaatIni -1]}`,
                    waktu_tempuh: parseFloat(waktuTempuh)
                })
            });
            console.log('Skor disimpan!');
        } catch (error) {
            console.error('Kesalahan saat menyimpan skor:', error);
            alert('Gagal menyimpan skor.');
        }

        tampilkanLayar(layarHasil);
    }

    async function tampilkanPeringkat() {
        tampilkanLayar(layarPeringkat);
        await muatPeringkatKeseluruhan();
        pilihPeringkatKategori.value = '';
        daftarPeringkatKategori.innerHTML = '';
    }

    async function muatPeringkatKeseluruhan() {
        try {
            const respons = await fetch('/api/skor');
            if (!respons.ok) {
                throw new Error(`Kesalahan HTTP! status: ${respons.status}`);
            }
            const semuaSkor = await respons.json();

            const totalSkorPerPemain = {};
            semuaSkor.forEach(s => {
                totalSkorPerPemain[s.nama] = (totalSkorPerPemain[s.nama] || 0) + s.skor;
            });

            const peringkatTerurut = Object.entries(totalSkorPerPemain).sort(([, skorA], [, skorB]) => skorB - skorA);

            daftarPeringkatKeseluruhan.innerHTML = '';
            if (peringkatTerurut.length > 0) {
                peringkatTerurut.forEach(([nama, totalSkor], indeks) => {
                    const li = document.createElement('li');
                    li.textContent = `${indeks + 1}. ${nama}: ${totalSkor} poin`;
                    daftarPeringkatKeseluruhan.appendChild(li);
                });
            } else {
                daftarPeringkatKeseluruhan.innerHTML = '<li>Belum ada skor.</li>';
            }
        } catch (error) {
            console.error('Kesalahan saat memuat peringkat keseluruhan:', error);
            daftarPeringkatKeseluruhan.innerHTML = '<li>Gagal memuat peringkat.</li>';
        }
    }

    async function muatPeringkatKategori(kategori) {
        try {
            const respons = await fetch('/api/skor');
            if (!respons.ok) {
                throw new Error(`Kesalahan HTTP! status: ${respons.status}`);
            }
            const semuaSkor = await respons.json();

            const skorKategoriPerPemain = {};
            semuaSkor.forEach(s => {
                const bagianKategori = s.kategori_level.split('_');
                const namaKategoriSaja = bagianKategori[0];
                if (namaKategoriSaja.toLowerCase() === kategori.toLowerCase()) {
                    skorKategoriPerPemain[s.nama] = (skorKategoriPerPemain[s.nama] || 0) + s.skor;
                }
            });

            const peringkatTerurut = Object.entries(skorKategoriPerPemain).sort(([, skorA], [, skorB]) => skorB - skorA);

            daftarPeringkatKategori.innerHTML = '';
            if (peringkatTerurut.length > 0) {
                peringkatTerurut.forEach(([nama, totalSkor], indeks) => {
                    const li = document.createElement('li');
                    li.textContent = `${indeks + 1}. ${nama}: ${totalSkor} poin`;
                    daftarPeringkatKategori.appendChild(li);
                });
            } else {
                daftarPeringkatKategori.innerHTML = `<li>Belum ada skor untuk kategori ${kategori}.</li>`;
            }
        } catch (error) {
            console.error('Kesalahan saat memuat peringkat kategori:', error);
            daftarPeringkatKategori.innerHTML = '<li>Gagal memuat peringkat kategori.</li>';
        }
    }

    // --- Fungsi untuk Tampilan Pohon ---
    async function tampilkanTampilanPohon() {
        tampilkanLayar(layarTampilanPohon);
        wadahPohonKuis.innerHTML = 'Memuat struktur kuis...';
        try {
            const respons = await fetch('/api/data_graf'); // Menggunakan endpoint baru
            if (!respons.ok) {
                throw new Error(`Kesalahan HTTP! status: ${respons.status}`);
            }
            const dataGraf = await respons.json();
            console.log("Data Graf:", dataGraf); // Debugging

            // Bangun struktur pohon menggunakan daftar bersarang
            wadahPohonKuis.innerHTML = ''; // Bersihkan kontainer
            const ul = document.createElement('ul');

            // Kelompokkan simpul berdasarkan kategori
            const kategoriPohon = {};
            dataGraf.simpul.forEach(simpul => { // Mengakses dataGraf.simpul
                if (simpul.tipe === 'kategori') { // Mengakses simpul.tipe
                    kategoriPohon[simpul.id] = { simpul: simpul, level: {} };
                } else if (simpul.tipe === 'level') { // Mengakses simpul.tipe
                    if (!kategoriPohon[simpul.kategori]) {
                        kategoriPohon[simpul.kategori] = { simpul: {id: simpul.kategori, tipe: 'kategori'}, level: {} };
                    }
                    kategoriPohon[simpul.kategori].level[simpul.level] = simpul;
                }
            });

            const urutanLevel = ['mudah', 'sedang', 'sulit'];

            for (const idKategori in kategoriPohon) {
                const dataKategori = kategoriPohon[idKategori];
                const liKategori = document.createElement('li');
                liKategori.classList.add('simpul-kategori');
                liKategori.textContent = dataKategori.simpul.id;

                const ulLevel = document.createElement('ul');
                urutanLevel.forEach(namaLevel => {
                    if (dataKategori.level[namaLevel]) {
                        const liLevel = document.createElement('li');
                        liLevel.classList.add('simpul-level');
                        liLevel.textContent = `Level: ${namaLevel.charAt(0).toUpperCase() + namaLevel.slice(1)}`;
                        ulLevel.appendChild(liLevel);
                    }
                });
                if (ulLevel.children.length > 0) {
                     liKategori.appendChild(ulLevel);
                }
                ul.appendChild(liKategori);
            }
            wadahPohonKuis.appendChild(ul);

        } catch (error) {
            console.error('Kesalahan saat memuat struktur kuis:', error);
            wadahPohonKuis.innerHTML = 'Gagal memuat struktur kuis.';
        }
    }


    // --- Event Listener ---
    tombolKategori.forEach(button => {
        button.addEventListener('click', (event) => {
            kategoriTerpilih = event.target.dataset.kategori;
            mulaiKuis();
        });
    });

    tombolKirimJawaban.addEventListener('click', cekJawaban);
    tombolMainLagi.addEventListener('click', () => {
        inputNamaPemain.value = '';
        tampilkanLayar(layarAwal);
    });
    tombolLihatPeringkat.addEventListener('click', tampilkanPeringkat);
    tombolKembaliKeAwal.addEventListener('click', () => {
        inputNamaPemain.value = '';
        tampilkanLayar(layarAwal);
    });

    pilihPeringkatKategori.addEventListener('change', (event) => {
        const kategoriTerpilihUntukPeringkat = event.target.value;
        if (kategoriTerpilihUntukPeringkat) {
            muatPeringkatKategori(kategoriTerpilihUntukPeringkat);
        } else {
            daftarPeringkatKategori.innerHTML = '';
        }
    });

    // Event listener baru untuk tombol "Lihat Struktur Kuis (Pohon)"
    tombolLihatStrukturKuis.addEventListener('click', tampilkanTampilanPohon);
    // Event listener baru untuk tombol "Kembali dari Tampilan Pohon"
    tombolKembaliDariTampilanPohon.addEventListener('click', () => {
        tampilkanLayar(layarAwal);
    });

    // Layar awal
    tampilkanLayar(layarAwal);
});