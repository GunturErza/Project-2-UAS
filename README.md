# Project 2 UAS
## Semester Genap 2025/2026
## Mata Kuliah: Struktur Data
## Jenis Tugas: Project Kelompok
## Tema: DSS ROUTE TOURING MOTOR BALI

----------------------------------

## NAMA ANGGOTA KELOMPOK
1. I GEDE WIRA YOGA (2501010086)
2. I KADEK GUNTUR ERZA PRAMUDYA (2501010071)
3. I MADE BAGUS ABIYOGA PRAWIRA (2501010089)

   ---------------------------

# LAPORAN PROJECT STRUKTUR DATA: IMPLEMENTASI GRAPH PADA DSS PEMILIHAN KOST

## BAB 1: PENDAHULUAN
### 1.1 Latar Belakang
Pemilihan tempat tinggal atau kost bagi mahasiswa baru maupun mahasiswa aktif merupakan salah satu keputusan penting yang memengaruhi kenyamanan belajar dan efisiensi finansial. Seringkali mahasiswa menghadapi dilema dalam menyeimbangkan antara batasan anggaran (budget) bulanan dengan aksesibilitas lokasi, seperti jarak tempuh menuju kampus serta kedekatan dengan fasilitas penunjang (minimarket, tempat makan, atau laundry).

Untuk mempermudah proses pengambilan keputusan ini, diperlukan sebuah sistem pendukung keputusan atau Decision Support System (DSS) yang tidak hanya memfilter data secara tabular, tetapi juga mampu memodelkan relasi spasial antar lokasi.   Struktur data Graph (Graf) merupakan model matematika yang sangat ideal untuk merepresentasikan entitas lokasi sebagai simpul (node/vertex) dan jalur penghubung beserta jaraknya sebagai sisi (edge). Dengan mengimplementasikan algoritma pencarian jalur terpendek seperti Dijkstra pada jaringan graf ini, sistem dapat memberikan rekomendasi kost terbaik yang sesuai dengan anggaran sekaligus mengoptimalkan rute perjalanan harian mahasiswa menuju kampus.

### 1.2 Rumusan Masalah
 1. Bagaimana cara memodelkan data kost, fasilitas penunjang, dan kampus ke dalam struktur data Graph?
 2. Bagaimana cara mengimplementasikan Algoritma Dijkstra dalam melakukan pencarian jalur terpendek dan optimasi keputusan pemilihan kost berdasarkan batas budget pengguna?
 3. Bagaimana merancang interface aplikasi DSS yang interaktif untuk memvisualisasikan jaringan graf secara real-time?

### 1.3 Tujuan
1. Memahami dan mengaplikasikan implementasi nyata dari struktur data graph dalam pemecahan masalah dunia nyata.
2. Mengimplementasikan Algoritma Dijkstra untuk menghitung akumulasi bobot terkecil (jarak terpendek) pada DSS Pemilihan Kost.
3. Membangun aplikasi DSS interaktif menggunakan teknologi Python dan Streamlit yang dilengkapi visualisasi graf terintegrasi.

### 1.4 Manfaat
* *Bagi Mahasiswa:* Mempermudah pencarian kost yang efisien secara jarak dan sesuai dengan kondisi finansial secara cepat dan akurat.
* *Bagi Pengembang:* Meningkatkan pemahaman teknis mengenai pemodelan data relasional, kalkulasi kompleksitas algoritma, dan visualisasi data berbasis network.
  
   ---------------------------

## BAB 2: DASAR TEORI  
