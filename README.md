# Tugas 5: Sistem Pakar Forward Chaining untuk Laptop Lambat atau Panas

## 1. Identitas

| | |
|---|---|
| Nama | MARDATILAH |
| NIM | F1D02510014 |

## 2. Topik dan Cara Menjalankan

**Topik:** penyebab laptop lambat atau panas, beserta saran penanganannya.

**Bahasa dan versi:** Python 3.8 atau lebih baru (diuji dengan Python 3.12). Tidak ada pustaka tambahan, hanya modul bawaan `json` dan `sys`.

**Perintah:**

```bash
python fc_laptop.py kb_laptop.json
```
Jawab setiap pertanyaan dengan `y` (ya) atau `t` (tidak).

**Isi repositori:**

```text
.
├── fc_laptop.py     # mesin forward chaining + antarmuka CLI
├── kb_laptop.json   # basis pengetahuan (aturan dan sumber)
├── screenshot/      # tangkapan layar kasus uji
└── README.md
```

## 3. Sumber dan Tabel Aturan

### Daftar sumber

| Kode | Judul | Penerbit | URL |
|------|-------|----------|-----|
| S1 | Tips to improve PC performance in Windows | Microsoft Support | https://support.microsoft.com/en-us/help/4002019 | **ISI TANGGAL** |
| S2 | How to Prevent Overheating: Tips for Cooling Your PC or Laptop | Dell Support | https://www.dell.com/support/contents/article/product-support/self-support-knowledgebase/battery-and-power/fan | **ISI TANGGAL** |
| S3 | How to Stop Computer and Laptop Overheating and Shut Down Issues | Dell Support | https://www.dell.com/support/kbdoc/en-us/000130867 | **ISI TANGGAL** |

### Tabel aturan (8 aturan, 3 kesimpulan)

| Aturan | IF | THEN | Sumber |
|--------|----|------|--------|
| R1 | banyak tab/aplikasi terbuka **OR** program startup banyak | beban sistem tinggi | S1 |
| R2 | ventilasi berdebu **OR** dipakai di kasur/bantal | aliran udara terhambat | S2, S3 |
| R3 | aliran udara terhambat **AND** kipas berisik | pendinginan buruk | S3 |
| R4 | pendinginan buruk **AND** lemot saat panas | thermal throttling | S2, S3 |
| R5 | disk hampir penuh | ruang penyimpanan rendah | S1 |
| R6 | thermal throttling **AND** pendinginan buruk | **saran: bersihkan ventilasi dan kipas** | S3 |
| R7 | beban sistem tinggi | **saran: tutup aplikasi dan matikan program startup** | S1 |
| R8 | ruang penyimpanan rendah | **saran: bebaskan ruang disk** | S1 |

Tiga kesimpulan akhir adalah R6, R7, dan R8 (cetak tebal). Aturan yang memakai hasil aturan lain: R3 (memakai hasil R2), R4 (memakai hasil R3), R6 (memakai hasil R4 dan R3), R7 (memakai hasil R1), dan R8 (memakai hasil R5). Rantai terpanjang: R2 → R3 → R4 → R6.

### Format file aturan (`kb_laptop.json`)

| Field | Keterangan |
|-------|------------|
| `judul` | Judul yang ditampilkan di awal program |
| `batas` | Batas keberlakuan, ditampilkan di akhir keluaran |
| `sumber` | Objek kode sumber (`S1`, `S2`, ...) beserta rujukannya |
| `aturan[].id` | Pengenal aturan |
| `aturan[].jika` | Daftar syarat |
| `aturan[].mode` | `"dan"` (semua syarat harus ada) atau `"atau"` (salah satu cukup) |
| `aturan[].maka` | Fakta hasil aturan |
| `aturan[].sumber` | Kode sumber aturan |

## 4. Metode yang Dipilih: Forward Chaining

**Alasan memilih forward chaining:**

1. Pengguna biasanya hanya tahu gejala (kipas berisik, laptop lemot, disk penuh), bukan penyebabnya. Forward chaining bergerak dari gejala menuju kesimpulan, sesuai dengan cara pengguna mengalami masalah.
2. Satu kumpulan gejala bisa menghasilkan beberapa saran sekaligus (lihat kasus uji 2). Forward chaining menurunkan semua kesimpulan yang mungkin, sedangkan backward chaining harus memilih satu tujuan terlebih dulu.
3. Jumlah fakta dasar kecil (7 pertanyaan), jadi menanyakan semuanya di awal tidak merepotkan pengguna.

**Cara kerja:**

```text
memori <- fakta yang dijawab "y" oleh user
ULANGI:
    cocok <- aturan yang syaratnya terpenuhi oleh memori DAN hasilnya belum ada di memori
    JIKA cocok kosong: BERHENTI
    r <- cocok[0]                    # aturan pertama (urutan di JSON)
    tambahkan r.maka ke memori
    catat bahwa r.maka berasal dari r  # bahan "alasan"
```

- Fakta dasar (yang ditanyakan ke user) ditentukan otomatis: fakta di bagian `jika` yang tidak pernah menjadi `maka` aturan mana pun.
- Kesimpulan akhir: fakta turunan yang tidak dipakai sebagai syarat aturan lain.
- Alasan ditelusuri mundur dari tiap kesimpulan sampai ke fakta dasar, lengkap dengan ID aturan dan sumber.

## 5. Kasus Uji

Semua keluaran di bawah adalah hasil asli dari program (urutan 7 pertanyaan: tab/aplikasi, startup, ventilasi berdebu, kasur/bantal, kipas berisik, lemot saat panas, disk penuh).

| # | Jawaban "ya" | Kesimpulan yang diharapkan |
|---|--------------|----------------------------|
| 1 | ventilasi berdebu, kipas berisik, lemot saat panas | saran: bersihkan ventilasi dan kipas |
| 2 | banyak tab/aplikasi terbuka, disk hampir penuh | saran: tutup aplikasi dan matikan program startup; saran: bebaskan ruang disk |
| 3 | kipas berisik, lemot saat panas | **tidak ada** (kasus negatif) |

### Kasus 1: rantai panjang R2 → R3 → R4 → R6

![Kasus uji 1](screenshot/kasus1.png)

```text
Fakta awal: ventilasi berdebu, kipas berisik, lemot saat panas

Siklus 1: R2 -> aliran udara terhambat
Siklus 2: R3 -> pendinginan buruk
Siklus 3: R4 -> thermal throttling
Siklus 4: R6 -> saran: bersihkan ventilasi dan kipas
Siklus 5: tidak ada aturan baru, berhenti

Kesimpulan:
  - saran: bersihkan ventilasi dan kipas
Alasan:
  saran: bersihkan ventilasi dan kipas  <- R6 (thermal throttling, pendinginan buruk) [S3]
    thermal throttling  <- R4 (pendinginan buruk, lemot saat panas) [S2, S3]
      pendinginan buruk  <- R3 (aliran udara terhambat, kipas berisik) [S3]
        aliran udara terhambat  <- R2 (ventilasi berdebu) [S2, S3]
```

### Kasus 2: dua kesimpulan sekaligus

![Kasus uji 2](screenshot/kasus2.png)

```text
Fakta awal: banyak tab/aplikasi terbuka, disk hampir penuh

Siklus 1: R1 -> beban sistem tinggi
Siklus 2: R5 -> ruang penyimpanan rendah
Siklus 3: R7 -> saran: tutup aplikasi dan matikan program startup
Siklus 4: R8 -> saran: bebaskan ruang disk
Siklus 5: tidak ada aturan baru, berhenti

Kesimpulan:
  - saran: tutup aplikasi dan matikan program startup
  - saran: bebaskan ruang disk
Alasan:
  saran: tutup aplikasi dan matikan program startup  <- R7 (beban sistem tinggi) [S1]
    beban sistem tinggi  <- R1 (banyak tab/aplikasi terbuka) [S1]
  saran: bebaskan ruang disk  <- R8 (ruang penyimpanan rendah) [S1]
    ruang penyimpanan rendah  <- R5 (disk hampir penuh) [S1]
```

### Kasus 3: tidak ada kesimpulan (negatif)

Gejala ada, tetapi penyebab awalnya (ventilasi berdebu atau dipakai di kasur) tidak diketahui, sehingga R3 tidak terpenuhi (mode `dan` butuh kedua syarat).

![Kasus uji 3](screenshot/kasus3.png)

```text
Fakta awal: kipas berisik, lemot saat panas

Siklus 1: tidak ada aturan baru, berhenti

Kesimpulan: tidak ada kesimpulan dari fakta yang diberikan.
Alasan: tidak ada aturan yang syaratnya terpenuhi sampai ke saran.
```

## 6. Batas Keberlakuan

Aturan dalam program ini berasal dari dokumentasi resmi Microsoft Support dan Dell Support, sehingga hanya berlaku untuk laptop Windows (dan perangkat Dell untuk bagian pendinginan) dan belum tentu cocok untuk macOS, Linux, atau merek lain. Program hanya menalar dari jawaban ya/tidak tanpa tingkat keyakinan dan tidak memeriksa kondisi perangkat keras secara langsung, sehingga hasilnya adalah saran awal, bukan diagnosis atau keputusan akhir. Jika masalah berlanjut setelah laptop dibersihkan dan dioptimalkan, bawa ke teknisi. Batas ini juga ditampilkan di akhir keluaran program.

## 7. Penggunaan Alat Bantu AI

**ISI SESUAI KENYATAAN.** Contoh: "Claude (Anthropic) dipakai untuk membantu menyusun README ini dan memverifikasi keluaran kasus uji. Pemilihan topik, pencarian sumber, penulisan aturan, dan kode mesin inferensi dikerjakan sendiri." Jika tidak memakai AI sama sekali, tulis "tidak dipakai".
