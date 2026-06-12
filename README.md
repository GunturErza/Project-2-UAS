# Project 2 UAS
## Semester Genap 2025/2026
## Mata Kuliah: Struktur Data
## Jenis Tugas: Project Kelompok
## Tema: DSS PEMILIHAN KOST UNTUK MAHASISWA

---

## NAMA ANGGOTA KELOMPOK
1. I GEDE WIRA YOGA (2501010086)
2. I KADEK GUNTUR ERZA PRAMUDYA (2501010071)
3. I MADE BAGUS ABIYOGA PRAWIRA (2501010089)

---

# LAPORAN PROJECT STRUKTUR DATA: IMPLEMENTASI GRAPH PADA DSS PEMILIHAN KOST

## BAB 1: PENDAHULUAN
### 1.1 Latar Belakang
Menemukan tempat tinggal atau kost yang strategis, ekonomis, dan memiliki fasilitas memadai merupakan salah satu permasalahan utama yang dihadapi oleh mahasiswa rantau di Institut Bisnis dan Teknologi Indonesia (INSTIKI). Wilayah Panjer, Denpasar memiliki kompleksitas tinggi terkait variasi harga sewa, kelengkapan fasilitas, serta kondisi lalu lintas seperti jalur satu arah (one-way). Proses pemilihan yang dilakukan secara manual sering kali tidak objektif dan memakan waktu lama.

Untuk mengatasi masalah tersebut, konsep teori Graph (Graf) dapat diterapkan sebagai basis pemodelan sistem relasional dunia nyata. Dengan memetakan lokasi kost dan persimpangan jalan sebagai simpul (node), serta jarak jalan raya sebagai sisi (edge), kita dapat membangun sebuah Decision Support System (DSS) atau Sistem Pendukung Keputusan yang cerdas. Melalui integrasi algoritma pencarian lintasan terpendek dan pembobotan multi-kriteria, sistem ini mampu menghasilkan rekomendasi hunian terbaik secara cepat, efisien, dan terukur.

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
  
---

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

---

## BAB 3: ANALISIS DAN PERANCANGAN   
### 3.1 Analisis Masalah
Mahasiswa sering kesulitan menentukan kost karena informasi jarak ke kampus tidak linear dengan jalan pintas atau posisi fasilitas umum di sekitarnya. Oleh karena itu, entitas lingkungan sekitar kampus dipecah menjadi beberapa titik simpul dengan relasi antartitik yang memiliki bobot jarak tertentu.

### 3.2 Desain Graph
Sistem ini menggunakan jenis graf *Undirected Weighted Graph*.
* *Struktur Node (Simpul):* Merepresentasikan lokasi. Memiliki atribut ID, Label, Tipe (Kampus, Kost, Fasilitas), dan Biaya sewa (khusus tipe Kost).
* *Struktur Edge (Sisi):* Merepresentasikan akses jalan penghubung antarlokasi dengan atribut bobot berupa jarak dalam meter.

### 3.3 Flowchart Sistem
<img width="1380" height="752" alt="Flowchart" src="https://github.com/user-attachments/assets/33f1d318-abf7-4e27-99f7-48cad48eac0b" />


### 3.4 Use Case Diagram
*Aktor:* Pengguna / Mahasiswa.

* Aktivitas:
1. Melihat Informasi Proyek UAS (Melalui Sidebar).
2. Menentukan Filter Budget Kost (Menggunakan slider input).
3. Melihat Rekomendasi Kost Terbaik AI (Hasil kalkulasi utilitas tertinggi).
4. Memilih Kost untuk Dianalisis (Melalui dropdown selectbox).
5. Melihat Analisis Breakdown Skor AI (Rincian bobot rating, fasilitas, penalti jarak, dan harga).
6. Melihat Rute Terpendek & Live Route Map (Integrasi peta Folium dan algoritma Dijkstra).
7. Melihat Analisis Teori Struktur Graf (Topologi Jaringan NetworkX & Tabel Analisis Sentralitas).

<img width="1408" height="768" alt="UseCase" src="https://github.com/user-attachments/assets/46f0f3a3-5655-45be-9288-1857d1825eb2" />



### 3.5 Detail Struktur Node dan Edge pada Sistem
Sesuai dengan basis data yang tertanam (hardcoded) pada sistem, berikut rincian datanya:
* *Daftar Node ($V$):*
1. KAMPUS (Label: Kampus Utama, Tipe: Kampus)
2. KOST_A (Label: Kost Exclusif A, Tipe: Kost, Harga: Rp 1.500.000)
3. KOST_B (Label: Kost Muslimah B, Tipe: Kost, Harga: Rp 800.000)
4. KOST_C (Label: Kost Campur C, Tipe: Kost, Harga: Rp 1.100.000)
5. FAC_1 (Label: Warmindo & Laundry, Tipe: Fasilitas)
6. FAC_2 (Label: Minimarket, Tipe: Fasilitas)

* *Daftar Edge ($E$) dan Bobot Jarak:*
  
1. KOST_A ── FAC_1 : 200 meter 
2. FAC_1 ── KAMPUS : 500 meter 
3. KOST_B ── FAC_2 : 400 meter 
4. FAC_2 ── KAMPUS : 600 meter 
5. KOST_C ── FAC_1 : 300 meter
6. KOST_C ── FAC_2 : 350 meter 
7. FAC_1 ── FAC_2 : 150 meter 

---

## BAB 4: IMPLEMENTASI
## 4.1 Implementasi Program

### 4.1.1 Perangkat Lunak & Library yang Digunakan
* **Bahasa Pemrograman:** Python 3.x
* **Framework Antarmuka:** `streamlit` (Menyediakan komponen GUI web interaktif)
* **Pemodelan Struktur Data:** `networkx` (Digunakan untuk representasi struktur data Graph)
* **Render Visualisasi:** `matplotlib` (Digunakan untuk menggambar plot grafik jaringan)
* **Optimasi Algoritma:** `heapq` (Struktur data Priority Queue bawaan Python untuk mempercepat pencarian jalur terpendek)

### 4.1.2 Dataset Lingkungan Jaringan (Graph)
Sistem menginisialisasi sebuah jaringan lokasi di sekitar kampus yang terdiri dari 3 jenis simpul (*Nodes*):
1. **Kampus:** Target akhir (`KAMPUS`)
2. **Kost:** `KOST_A` (Rp 1.500.000), `KOST_B` (Rp 800.000), `KOST_C` (Rp 1.100.000)
3. **Fasilitas Umum:** `FAC_1` (Warmindo & Laundry), `FAC_2` (Minimarket)

Bobot antar-sisi (*Edges Weight*) merepresentasikan jarak fisik antar tempat dalam satuan **Meter**.

## 4.2 Penjelasan Kode
### 4.2.1 Struktur Data Graph
Class `DSSGraph` merepresentasikan peta wilayah menggunakan konsep *Adjacency List*.

```python
class DSSGraph:
    def __init__(self):
        self.graph = {}
        self.node_info = {}

    def add_node(self, node, label, node_type, cost=0):
        self.graph[node] = {}
        self.node_info[node] = {"label": label, "type": node_type, "cost": cost}

    def add_edge(self, u, v, weight):
        if u in self.graph and v in self.graph:
            self.graph[u][v] = weight
            self.graph[v][u] = weight
```
* add_node: Menyimpan simpul baru beserta meta-data seperti nama lokasi, tipe tempat, dan harga sewa.
* add_edge: Menghubungkan dua simpul secara timbal balik (Undirected Graph) dengan beban jarak tertentu.

### 4.2.2 Algoritma Dijkstra (Pencarian Rute Terpendek)
Fungsi ini melakukan komputasi pencarian rute terefisien dari titik kost asal menuju titik kampus.

```python
def dijkstra(self, start, end):
    queue = [(0, start, [])]
    visited = set()
    
    while queue:
        (cost, node, path) = heapq.heappop(queue)
        
        if node not in visited:
            visited.add(node)
            path = path + [node]
            
            if node == end:
                return cost, path
            
            for neighbor, weight in self.graph[node].items():
                if neighbor not in visited:
                    heapq.heappush(queue, (cost + weight, neighbor, path))
                    
    return float("inf"), []
```
* Menggunakan teknik Min-Heap (heapq.heappop) agar kompleksitas waktu pencarian tetap optimal dengan memprioritaskan akumulasi jarak terkecil pada setiap iterasi simpul.

### 4.2.3 Logika Filter Keputusan (Decision Support System)
Sistem menyaring opsi kost secara real-time berdasarkan budget yang dimasukkan oleh pengguna di halaman web.
```python
valid_kost = [node for node, info in dss.node_info.items() if info["type"] == "Kost" and info["cost"] <= budget]
```

## 4.3 Tampilan Sistem
<img width="1920" height="1041" alt="Capture" src="https://github.com/user-attachments/assets/ffbff446-2450-4b1a-b3bc-075fb7b10be8" />

## BAB 5: Pengujian dan Analisis
## 5.1 Skenario Pengujian
Pengujian dilakukan untuk membuktikan keakuratan sistem pendukung keputusan dalam memfilter finansial dan menghitung jarak.

  Kasus Uji 1: Budget Ketat (Rp 900.000)
  Skenario: Pengguna menggeser slider ke angka Rp 900.000.
  Hasil Filter: Hanya KOST_B (Kost Muslimah B, Rp 800.000) yang muncul di menu pilihan.


  Eksekusi Dijkstra: KOST_B menuju KAMPUS.
  Hasil Rekomendasi: Total Jarak = 1000 Meter.
  Jalur: Kost Muslimah B ➡️ Minimarket ➡️ Kampus Utama.


  Kasus Uji 2: Budget Menengah (Rp 1.200.000)
  Skenario: Pengguna menggeser slider ke angka Rp 1.200.000.
  Hasil Filter: Menampilkan KOST_B dan KOST_C (Rp 1.100.000).


  Eksekusi Pilihan: Pengguna memilih KOST_C.
  Hasil Rekomendasi: Total Jarak = 800 Meter.
  Jalur: Kost Campur C ➡️ Warmindo & Laundry ➡️ Kampus Utama. (Catatan: Jalur alternatif lewat FAC_2 memiliki total jarak $350 + 600 = 950$ meter, sistem berhasil mendeteksi jalur lewat FAC_1 sepanjang 800 meter sebagai
  yang terpendek).


  Kasus Uji 3: Budget Terlalu Rendah (Rp 500.000)
  Skenario: Pengguna menurunkan slider ke batas minimum Rp 500.000.
  Hasil: Sistem memunculkan pesan peringatan kontekstual berwarna kuning: "Tidak ada kost yang memenuhi kriteria budget Anda...".

## 5.2 Kompleksitas Algoritma
### 5.2.1 Analisis Kompleksitas Algoritma

**Kompleksitas Waktu (Time Complexity):** Menggunakan struktur Adjacency List dan Min-Heap Priority Queue, kompleksitas algoritma Dijkstra yang diimplementasikan adalah *$O((V + E) \log V)$*, di mana $V$ adalah jumlah simpul dan $E$ adalah jumlah sisi. Proses ini sangat cepat untuk ukuran graf skala lokal.

**Kompleksitas Ruang (Space Complexity):** Kompleksitas ruang berukuran *$O(V + E)$* untuk menyimpan representasi data struktur graf dan status kunjungan array algoritma di dalam memori.



### 5.2.2 Kelebihan dan Kekurangan Sistem

**Kelebihan:** 
* Interface interaktif, responsif, dan mudah digunakan langsung lewat web browser berkat framework Streamlit.
* Visualisasi graf bersifat dinamis; jalur solusi rute yang terpilih otomatis berubah warna menjadi merah tebal sehingga intuitif bagi pengguna.
* Menggunakan manajemen memori yang baik dengan fitur caching data (st.cache_resource).




**Kekurangan:**
* Data simpul graf dan harga masih bersifat statis di dalam kode (hardcoded), belum terhubung ke database eksternal formal.
* Kriteria pencarian keputusan baru didasarkan pada dua parameter utama (Budget dan Jarak fisik), belum mengukur variabel eksternal seperti rating kenyamanan kost secara mendalam.

## BAB 6: Saran dan Keimpulan
### 6.1 Kesimpulan

Proyek ini berhasil membuktikan bahwa teori struktur data *Graph* bukan sekadar materi konseptual akademis, melainkan dapat ditransformasikan secara nyata menjadi fondasi utama sistem pendukung keputusan (Decision Support System). Melalui perpaduan pemfilteran batasan data biaya dan eksekusi *Algoritma Dijkstra*, sistem terbukti akurat dalam mengevaluasi rute alternatif serta menyajikan rekomendasi kost dengan akumulasi bobot jarak terpendek menuju kampus utama.

### 6.2 Saran Pengembangan

Untuk meningkatkan nilai guna sistem di masa mendatang, beberapa poin pengembangan yang disarankan meliputi:

1. *Integrasi Database Graf (Bonus Kriteria):* Mengganti penyimpanan lokal adjacency list dengan sistem database graf asli seperti Neo4j untuk mendukung skalabilitas ribuan data kost.


2. *Visualisasi Real-Time Lanjutan:* Menggunakan pustaka Streamlit-AgGraph atau pyvis agar graf hasil visualisasi dapat digeser (drag), diperbesar (zoom in/out), dan diklik secara interaktif oleh pengguna langsung pada layar.


3. *Metode Keputusan Hybrid:* Menambahkan algoritma pengambil keputusan multi-kriteria seperti AHP (Analytic Hierarchy Process) atau TOPSIS untuk menggabungkan bobot jarak, fasilitas AC/non-AC, dan rating kebersihan bersamaan dengan Algoritma Dijkstra.
---
