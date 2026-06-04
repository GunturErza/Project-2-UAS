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
### 2.1 Struktur Data Graph
Graph (Graf) adalah struktur data non-linear yang terdiri dari sekumpulan simpul ($V$ atau Vertex/Node) dan sekumpulan sisi ($E$ atau Edge) yang menghubungkan sepasang simpul. Secara matematis dinotasikan sebagai $G = (V, E)$.

* *Undirected Graph:* Graf yang sisinya tidak memiliki arah, artinya jika ada sisi yang menghubungkan simpul $A$ dan $B$, maka perjalanan dapat dilakukan dari $A$ ke $B$ maupun dari $B$ ke $A$ dengan bobot yang sama.

* *Weighted Graph:* Graf yang setiap sisinya memiliki nilai atau bobot (weight) tertentu yang merepresentasikan jarak, biaya, atau waktu tempuh. Pada sistem ini, bobot merepresentasikan jarak dalam satuan meter.

### 2.2 Decision Support System (DSS)
Decision Support System (DSS) atau Sistem Pendukung Keputusan adalah sistem berbasis komputer yang membantu pengambilan keputusan dengan mengeksplorasi berbagai alternatif solusi berdasarkan data dan kriteria tertentu. DSS dalam proyek ini bekerja dengan metode eliminasi batasan (constraint-based filtering) untuk menyaring harga kost, dilanjutkan dengan metode optimasi rute terpendek (shortest path).

### 2.3 Algoritma Dijkstra
Algoritma Dijkstra adalah algoritma rakus (greedy algorithm) yang digunakan untuk mencari jalur terpendek dari satu simpul sumber (single-source shortest path) ke simpul lainnya pada sebuah graf berbobot positif. Algoritma ini bekerja dengan cara:
1. Menentukan nilai jarak awal ke semua simpul sebesar tak hingga ($\infty$), kecuali simpul awal yang diberi nilai $0$.
2. Menyimpan simpul ke dalam antrean prioritas (priority queue / min-heap) berdasarkan bobot terkecil.
3. Mengunjungi simpul tetangga yang belum dikunjungi, memperbarui nilai jaraknya jika jalur baru lebih pendek (relaxation), dan memasukkannya kembali ke antrean prioritas hingga simpul tujuan tercapai.

   ---------------------------

## BAB 3: ANALISIS DAN PERANCANGAN   
### 3.1 Analisis Masalah
Mahasiswa sering kesulitan menentukan kost karena informasi jarak ke kampus tidak linear dengan jalan pintas atau posisi fasilitas umum di sekitarnya. Oleh karena itu, entitas lingkungan sekitar kampus dipecah menjadi beberapa titik simpul dengan relasi antartitik yang memiliki bobot jarak tertentu.

### 3.2 Desain Graph
Sistem ini menggunakan jenis graf *Undirected Weighted Graph*.
* *Struktur Node (Simpul):* Merepresentasikan lokasi. Memiliki atribut ID, Label, Tipe (Kampus, Kost, Fasilitas), dan Biaya sewa (khusus tipe Kost).
* *Struktur Edge (Sisi):* Merepresentasikan akses jalan penghubung antarlokasi dengan atribut bobot berupa jarak dalam meter.

