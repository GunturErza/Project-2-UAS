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
Area Panjer, Denpasar merupakan salah satu kawasan strategis yang padat penduduk, khususnya bagi kalangan mahasiswa karena lokasinya yang berdekatan dengan berbagai institusi pendidikan tinggi, salah satunya adalah Institut Bisnis dan Teknologi Indonesia (INSTIKI). Setiap tahunnya, gelombang mahasiswa rantau berdatangan dan menghadapi tantangan yang serupa, yaitu mencari tempat tinggal atau rumah kost yang ideal. Proses pencarian ini sering kali bersifat subjektif, melelahkan, dan tidak terukur karena mahasiswa harus mempertimbangkan banyak kriteria secara bersamaan, seperti batasan anggaran (*budget*), kelengkapan fasilitas, hingga jarak geografis menuju kampus.

Selain itu, kompleksitas tata kota di area Panjer, seperti adanya aturan jalan satu arah (*one-way*) pada persimpangan tertentu, sering kali luput dari pertimbangan manual. Akibatnya, mahasiswa rentan salah memilih lokasi kost yang berujung pada inefisiensi waktu tempuh harian akibat harus memutar jauh demi mematuhi rambu lalu lintas. 

Untuk mengatasi masalah tersebut, diperlukan sebuah Sistem Pendukung Keputusan (Decision Support System/DSS) yang mampu memodelkan jaringan jalan sekaligus menganalisis alternatif kost secara objektif. Teori Graf (*Graph Theory*) merupakan pendekatan terbaik untuk memetakan masalah ini, di mana lokasi kost dan persimpangan bertindak sebagai simpul (*Node*), dan jalan raya sebagai sisi (*Edge*). Dengan mengimplementasikan Algoritma Dijkstra yang dioptimasi menggunakan antrean prioritas *Min-Heap* serta dikombinasikan dengan *AI Smart Scoring Engine*, sistem ini mampu menyajikan navigasi rute terpendek yang patuh hukum sekaligus memberikan rekomendasi hunian dengan kalkulasi yang rasional dan seimbang.

### 1.2 Rumusan Masalah
1. Bagaimana mengabstraksikan jaringan jalan nyata dan aturan lalu lintas satu arah (*one-way*) di area Panjer ke dalam model struktur data Graf (*Adjacency List*) yang efisien di memori?
2. Bagaimana mengimplementasikan Algoritma Dijkstra dengan optimasi *Min-Heap* (`heapq`) agar kalkulasi rute terpendek dari kost ke kampus INSTIKI berjalan instan dan siap untuk skala data yang lebih luas (*scalable*)?
3. Bagaimana merancang formula penilaian (*Scoring Engine*) yang adil untuk menyatukan berbagai variabel dengan dimensi satuan yang berbeda (harga jutaan rupiah, jarak ratusan meter, dan rating skala kecil) tanpa saling mendominasi?

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
1. Menentukan Filter Budget Kost (Menggunakan slider input).
2. Melihat Rekomendasi Kost Terbaik AI (Hasil kalkulasi utilitas tertinggi).
3. Memilih Kost untuk Dianalisis (Melalui dropdown selectbox).
4. Melihat Analisis Breakdown Skor AI (Rincian bobot rating, fasilitas, penalti jarak, dan harga).
5. Melihat Rute Terpendek & Live Route Map (Integrasi peta Folium dan algoritma Dijkstra).

<img width="1408" height="768" alt="UseCase" src="https://github.com/user-attachments/assets/46f0f3a3-5655-45be-9288-1857d1825eb2" />



### 3.5 Detail Struktur Node dan Edge pada Sistem
Sesuai dengan basis data yang tertanam (hardcoded) pada sistem, berikut rincian datanya:

## 1. Struktur Node

### **INSTIKI (Kampus)**
Tipe: Tujuan
Koordinat: Lat -8.681600, Lon 115.227100
Atribut: Biaya Rp 0, Rating Maps 5.0, Fasilitas 10

### **Kosanku Bali**
Tipe: Kost
Koordinat: Lat -8.680000, Lon 115.226500
Atribut: Biaya Rp 800.000, Rating Maps 4.3, Fasilitas 7

### **Kost Kartika Sari**
Tipe: Kost
Koordinat: Lat -8.678200, Lon 115.226000
Atribut: Biaya Rp 900.000, Rating Maps 4.5, Fasilitas 8

### **Kost Griya Petanu 34**
Tipe: Kost
Koordinat: Lat -8.685000, Lon 115.229000
Atribut: Biaya Rp 1.000.000, Rating Maps 4.7, Fasilitas 9

### **Kost Batanghari**
Tipe: Kost
Koordinat: Lat -8.676000, Lon 115.224000
Atribut: Biaya Rp 1.200.000, Rating Maps 4.8, Fasilitas 9

### **Simpang Pakerisan 1**
Tipe: Jalan
Koordinat: Lat -8.679000, Lon 115.226200
Atribut: Biaya Rp 0, Rating Maps 0, Fasilitas 0

### **Simpang Pakerisan 2**
Tipe: Jalan
Koordinat: Lat -8.683000, Lon 115.227500
Atribut: Biaya Rp 0, Rating Maps 0, Fasilitas 0

### **Simpang Petanu**
Tipe: Jalan
Koordinat: Lat -8.684000, Lon 115.228500
Atribut: Biaya Rp 0, Rating Maps 0, Fasilitas 0

## 2. Struktur Edge

### **Asal: INSTIKI (Kampus)**
* Ke Kosanku Bali (Jarak: 200m)
* Ke Simpang Pakerisan 2 (Jarak: 150m)
* Ke Simpang Pakerisan 1 (Jarak: 300m)

### **Asal: Kosanku Bali**
* Ke INSTIKI (Kampus) (Jarak: 200m)
* Ke Simpang Pakerisan 1 (Jarak: 100m)

### **Asal: Kost Kartika Sari**
* Ke Simpang Pakerisan 1 (Jarak: 150m)
* Ke Kost Batanghari (Jarak: 300m)

### **Asal: Kost Griya Petanu 34**
* Ke Simpang Petanu (Jarak: 100m)

### **Asal: Kost Batanghari**
* Ke Kost Kartika Sari (Jarak: 300m)
* Ke Simpang Pakerisan 1 (Jarak: 400m)

### **Asal: Simpang Pakerisan 1**
* Ke INSTIKI (Kampus) (Jarak: 300m)
* Ke Kosanku Bali (Jarak: 100m)
* Ke Kost Kartika Sari (Jarak: 150m)
* Ke Kost Batanghari (Jarak: 400m)
* Ke Simpang Pakerisan 2 (Jarak: 250m)

### **Asal: Simpang Pakerisan 2**
* Ke INSTIKI (Kampus) (Jarak: 150m)
* Ke Simpang Petanu (Jarak: 150m)

### **Asal: Simpang Petanu**
* Ke Simpang Pakerisan 2 (Jarak: 150m)
* Ke Kost Griya Petanu 34 (Jarak: 100m)

## 3. Spesifikasi Pemodelan Graf

### **Tipe Graf**
Directed Graph (Graf Berarah). Aliran perpindahan dari satu titik ke titik lain memiliki arah spesifik yang memengaruhi penentuan jalur pulang dan pergi.

### **Bobot (Weight)**
Jarak fisik antarsimpul dalam satuan meter. Bobot ini menjadi variabel utama yang diakumulasikan oleh algoritma Dijkstra untuk menentukan rute terpendek menuju Kampus INSTIKI.

---

## BAB 4: IMPLEMENTASI
## 4.1 Implementasi Program
### Perangkat Lunak & Library yang Digunakan
Berikut adalah daftar perangkat lunak dan library Python yang digunakan dalam pengembangan sistem pendukung keputusan (DSS) pemilihan kost:

* **Python Interpreter**
  Bahasa pemrograman utama untuk menjalankan algoritma Dijkstra dan seluruh logika sistem.
* **Web Browser**
  Media antarmuka (User Interface) untuk menampilkan aplikasi web interaktif.
* **Code Editor (VS Code / PyCharm)**
  Perangkat lunak untuk menulis dan menyunting kode program.
* **Streamlit**
  Framework utama untuk membangun antarmuka web dan komponen interaktif seperti slider, selectbox, dan tab.
* **Folium**
  Library untuk membuat peta geografis interaktif berbasis koordinat bumi asli.
* **Streamlit-Folium**
  Pustaka integrator untuk menampilkan peta Folium di dalam halaman web Streamlit dengan lancar.
* **NetworkX**
  Library matematika graf untuk memodelkan topologi jalan berarah serta menghitung metrik sentralitas (Degree & Closeness Centrality).
* **Heapq**
  Library bawaan Python untuk mengoptimalkan performa kecepatan pencarian rute terpendek pada algoritma Dijkstra.
* **Matplotlib**
  Library visualisasi untuk menggambar struktur jaringan graf abstrak yang berisi simpul, garis, dan label jarak.
* **Pandas**
  Library pengolah data untuk menyusun, mengurutkan, dan menampilkan hasil analisis sentralitas dalam bentuk tabel (DataFrame).

## 4.2 Penjelasan Kode
### Inisialisasi Dataset & Struktur Data Graf
Sistem menyimpan data lokasi (*spatial*) dan keterhubungan antar-jalan menggunakan konsep *State Management* dari Streamlit yang diintegrasikan ke dalam struktur data dictionary (*Adjacency List*).

```python
if 'nodes' not in st.session_state:
    st.session_state.nodes = {
        'INSTIKI (Kampus)': {'type': 'Tujuan', 'biaya': 0, 'rating_maps': 5.0, 'fasilitas': 10, 'lat': -8.681600, 'lon': 115.227100},
        'Kosanku Bali': {'type': 'Kost', 'biaya': 800000, 'rating_maps': 4.3, 'fasilitas': 7, 'lat': -8.680000, 'lon': 115.226500},
        'Kost Kartika Sari': {'type': 'Kost', 'biaya': 900000, 'rating_maps': 4.5, 'fasilitas': 8, 'lat': -8.678200, 'lon': 115.226000},
        'Kost Griya Petanu 34': {'type': 'Kost', 'biaya': 1000000, 'rating_maps': 4.7, 'fasilitas': 9, 'lat': -8.685000, 'lon': 115.229000},
        'Kost Batanghari': {'type': 'Kost', 'biaya': 1200000, 'rating_maps': 4.8, 'fasilitas': 9, 'lat': -8.676000, 'lon': 115.224000},
        'Simpang Pakerisan 1': {'type': 'Jalan', 'biaya': 0, 'rating_maps': 0, 'fasilitas': 0, 'lat': -8.679000, 'lon': 115.226200},
        'Simpang Pakerisan 2': {'type': 'Jalan', 'biaya': 0, 'rating_maps': 0, 'fasilitas': 0, 'lat': -8.683000, 'lon': 115.227500},
        'Simpang Petanu': {'type': 'Jalan', 'biaya': 0, 'rating_maps': 0, 'fasilitas': 0, 'lat': -8.684000, 'lon': 115.228500}
    }

if 'adj_list' not in st.session_state:
    st.session_state.adj_list = {
        'INSTIKI (Kampus)': {'Kosanku Bali': 200, 'Simpang Pakerisan 2': 150, 'Simpang Pakerisan 1': 300},
        'Kosanku Bali': {'INSTIKI (Kampus)': 200, 'Simpang Pakerisan 1': 100},
        'Kost Kartika Sari': {'Simpang Pakerisan 1': 150, 'Kost Batanghari': 300},
        'Kost Griya Petanu 34': {'Simpang Petanu': 100},
        'Kost Batanghari': {'Kost Kartika Sari': 300, 'Simpang Pakerisan 1': 400},
        'Simpang Pakerisan 1': {'INSTIKI (Kampus)': 300, 'Kosanku Bali': 100, 'Kost Kartika Sari': 150, 'Kost Batanghari': 400, 'Simpang Pakerisan 2': 250}, 
        'Simpang Pakerisan 2': {'INSTIKI (Kampus)': 150, 'Simpang Petanu': 150},
        'Simpang Petanu': {'Simpang Pakerisan 2': 150, 'Kost Griya Petanu 34': 100}
    }
```
* st.session_state.nodes: Menyimpan metadata spasial simpul seperti tipe lokasi, biaya sewa, rating Google Maps, jumlah fasilitas, serta titik koordinat lintang (latitude) dan bujur (longitude).

* st.session_state.adj_list: Berperan sebagai matriks ketetanggaan graf berarah (Weighted Directed Graph), di mana nama simpul luar memetakan simpul tetangga beserta bobot jaraknya dalam satuan meter.

### 4.3 Algoritma Dijkstra (Pencarian Rute Terpendek)
Fungsi ini melakukan komputasi pencarian rute terefisien dari titik kost asal menuju titik kampus.

```python
def dijkstra(graph, start, end):
    queue = []
    heapq.heappush(queue, (0, start))
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    previous_nodes = {node: None for node in graph}

    while queue:
        current_distance, current_node = heapq.heappop(queue)
        if current_node == end: break
        if current_distance > distances[current_node]: continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    path, current_node = [], end
    if previous_nodes[current_node] is None and current_node != start:
        return float('infinity'), []
        
    while previous_nodes[current_node] is not None:
        path.insert(0, current_node)
        current_node = previous_nodes[current_node]
    if path: path.insert(0, start)
    
    return distances[end], path
```

* Min-Heap Optimization (heapq): Struktur antrean prioritas digunakan agar simpul dengan akumulasi jarak terkecil senantiasa diproses terlebih dahulu, mereduksi kompleksitas waktu berjalan menjadi O((V+E)logV).

* Backtracking Path: Menggunakan struktur data pencatatan simpul asal previous_nodes untuk menyusun kembali urutan jalan yang dilewati secara runut dari titik kost awal hingga tiba di gerbang kampus target.

### 4.2.3 Logika Filter Keputusan (Decision Support System)
Sistem menyaring opsi kost secara real-time berdasarkan budget yang dimasukkan oleh pengguna di halaman web.
```python
valid_kost = [node for node, info in dss.node_info.items() if info["type"] == "Kost" and info["cost"] <= budget]
```

## 4.3 Tampilan Sistem
<img width="1600" height="850" alt="WhatsApp Image 2026-06-12 at 13 43 47" src="https://github.com/user-attachments/assets/ce01eedf-ab3e-4f4f-b94f-1d1802ec571c" />


## BAB 5: Pengujian dan Analisis
## Skenario Pengujian:

### 📌 Kasus Uji 1: Budget Ketat (Rp 900.000)
* **Skenario:** Pengguna menggeser slider budget maksimal ke angka **Rp 900.000**.
* **Hasil Filter Finansial:** Sistem berhasil memfilter dataset. Hanya properti dengan harga sewa $\le \text{Rp } 900.000$ yang muncul di menu pilihan, yaitu:
  * `Kosanku Bali` (Rp 800.000)
  * `Kost Kartika Sari` (Rp 900.000)
* **Eksekusi Dijkstra (Sampel: Kosanku Bali menuju INSTIKI):**
  * **Total Jarak:** 200 Meter.
  * **Analisis Jalur Lintasan:** `Kosanku Bali ➔ INSTIKI (Kampus)`.
* **Kalkulasi Skor Utilitas AI:** Sistem berhasil menghitung skor akurat sebesar **66.0** (Rating tinggi memitigasi penalti harga).


### 📌 Kasus Uji 2: Budget Menengah (Rp 1.200.000)
* **Skenario:** Pengguna menggeser slider budget maksimal ke angka **Rp 1.200.000**.
* **Hasil Filter Finansial:** Sistem membuka akses ke lebih banyak pilihan kost yang masuk dalam *range* anggaran: `Kosanku Bali`, `Kost Kartika Sari`, `Kost Griya Petanu 34`, dan `Kost Batanghari`.
* **Eksekusi Dijkstra (Sampel Kasus Khusus: Kost Griya Petanu 34 menuju INSTIKI):**
  * **Total Jarak:** 400 Meter.
  * **Analisis Jalur Lintasan:** `Kost Griya Petanu 34 ➔ Simpang Petanu ➔ Simpang Pakerisan 2 ➔ INSTIKI (Kampus)`.
  * **Catatan Validasi Graf Berarah:** Jalur murni dunia nyata sebenarnya bisa memotong lewat *Simpang Pakerisan 1*, namun karena aturan graf satu arah (*directed edge*) pada `Simpang Pakerisan 2 ➔ Simpang Petanu`, sistem berhasil mendeteksi rute memutar yang valid dan aman secara aturan lalu lintas sepanjang 400 meter.


### 📌 Kasus Uji 3: Budget Terlalu Rendah (Rp 500.000)
* **Skenario:** Pengguna menurunkan slider ke batas minimum absolut yaitu **Rp 500.000**.
* **Hasil Ekspektasi Sistem:** Karena tidak ada properti kost di dalam database `st.session_state.nodes` yang memiliki harga sewa di bawah Rp 800.000, sistem langsung menghentikan kalkulasi Dijkstra untuk mencegah *crash*.
* **Output Antarmuka UI:** Sistem memunculkan pesan peringatan kontekstual (kotak alert merah): 
  > ⚠️ Tidak ada kost dalam range budget tersebut.


### 📌 Kasus Uji 4: Validasi Tab Analisis Topologi & Sentralitas
* **Skenario:** Pengguna membuka **Tab 2: Analisis Topologi Jaringan & Centrality**.
* **Hasil Matriks Teori Graf:**
  * **Visualisasi Jaringan:** Matplotlib dan NetworkX berhasil merender simpul `INSTIKI (Kampus)` dengan warna merah pembeda (`#ef4444`).
  * **Metrik Konektivitas:** Node `Simpang Pakerisan 1` berhasil divalidasi oleh sistem sebagai titik paling krusial dengan nilai **Degree Centrality tertinggi (0.714)**, membuktikan secara matematika bahwa simpul tersebut adalah persimpangan jalan terpadat/memiliki cabang terbanyak di sekitar area Panjer.

## 5.2 Kompleksitas Algoritma

## 🛠️ Analisis Kompleksitas Algoritma

Aplikasi ini menggunakan dua komponen komputasi utama: **Algoritma Dijkstra** untuk pencarian rute terpendek dan **Metrik Sentralitas NetworkX** untuk analisis topologi jaringan.

### 1. Algoritma Dijkstra (Pencarian Rute)
Kode mengimplementasikan Dijkstra menggunakan *Priority Queue* berbasis Min-Heap via pustaka `heapq`.

* **Kompleksitas Waktu (Time Complexity):** $$O((V + E) \log V)$$
  * *Penjelasan:* Di mana $V$ adalah jumlah simpul (node/persimpangan) dan $E$ adalah jumlah sisi (edge/jalan). Operasi `heappop` dan `heappush` membutuhkan waktu $O(\log V)$, yang dieksekusi untuk setiap simpul dan tetangganya. Ini adalah pendekatan yang sangat efisien untuk graf berukuran kecil hingga menengah.
* **Kompleksitas Ruang (Space Complexity):** $O(V + E)$
  * *Penjelasan:* Memori digunakan untuk menyimpan struktur data `distances`, `previous_nodes`, dan elemen di dalam heap yang berbanding lurus dengan jumlah simpul dan jalur yang terdaftar.

### 2. Analisis Sentralitas (Tab 2)
Fungsi `nx.degree_centrality(G)` dan `nx.closeness_centrality(G)` memiliki beban komputasi yang berbeda:
* **Degree Centrality:** $O(V)$ karena hanya menghitung jumlah *edge* yang terhubung langsung pada tiap *node*.
* **Closeness Centrality:** $O(V \times E)$ karena sistem harus menghitung jarak terpendek dari *setiap* simpul ke *seluruh* simpul lainnya dalam graf (menggunakan algoritma *All-Pairs Shortest Path*).


## Kelebihan Sistem (Pros)

1. **Efisiensi Manajemen State (`st.session_state`)**
   Struktur data graf disimpan di dalam *session state* Streamlit. Hal ini mencegah aplikasi melakukan inisialisasi ulang (*re-rendering*) dataset graf yang sama setiap kali pengguna menggeser slider atau mengubah pilihan menu, sehingga performa aplikasi tetap instan.

2. **Skor Utilitas Dinamis & Komprehensif**
   Sistem Pendukung Keputusan (SPK) tidak hanya terpaku pada satu parameter (seperti harga saja atau jarak saja). Formula multi-kriteria berhasil menyeimbangkan parameter positif (rating, fasilitas) dan parameter negatif (penalti biaya dan penalti jarak geografis) untuk menghasilkan rekomendasi yang rasional.

3. **Kepatuhan Terhadap Aturan Graf Berarah (*Directed Graph*)**
   Kode mampu menangani jalan satu arah (misalnya, dari `Simpang Pakerisan 2` ke `Simpang Petanu`). Ini membuktikan bahwa pemodelan graf mendekati kondisi lalu lintas dunia nyata, bukan sekadar garis lurus antar koordinat (*Euclidean distance*).

4. **Visualisasi Interaktif Dua Sisi**
   Aplikasi menyajikan visualisasi yang kaya: sisi praktis/aplikatif menggunakan peta spasial bumi asli (**Folium**) dan sisi akademis/teoretis menggunakan peta topologi struktur data murni (**NetworkX** & **Matplotlib**).


## Kekurangan Sistem & Potensi Pengembangan (Cons)

1. **Dataset Masih Bersifat Statis (*Hardcoded*)**
   Data simpul (*nodes*) dan keterhubungan jalan (*adj_list*) ditulis langsung di dalam kode. Jika ada perubahan harga kost, penambahan jalan baru, atau penutupan jalan, kode sumber harus diubah secara manual.
   * *Solusi ke depan:* Integrasikan dengan database eksternal (seperti PostgreSQL/MySQL) atau gunakan API eksternal seperti OpenStreetMap (OSM) untuk data jalan yang dinamis.

2. **Keterbatasan Skala Peta Folium**
   Fungsi `create_folium_map` merender seluruh jaringan jalan setiap kali dipanggil. Jika jumlah *nodes* berkembang menjadi ribuan, proses rendering pada browser pengguna dapat mengalami penurunan performa (*lag*).

3. **Formula Pembobotan (Scoring) Bersifat Kaku**
   Konstanta pengali pada rumus utilitas (seperti `distance * 0.05` atau `biaya / 10000`) ditanam secara permanen (*hardcoded*). Padahal, preferensi setiap mahasiswa berbeda; ada mahasiswa yang tidak masalah berjalan jauh asalkan kost murah, dan sebaliknya.
   * *Solusi ke depan:* Implementasikan metode SPK formal seperti **AHP (Analytic Hierarchy Process)** atau **TOPSIS**, di mana pengguna bisa menentukan sendiri bobot prioritas (kepentingan) antara harga, jarak, dan fasilitas secara dinamis melalui UI.

## BAB 6: Saran dan Keimpulan
### 6.1 Kesimpulan

Proyek ini berhasil membuktikan bahwa teori struktur data *Graph* bukan sekadar materi konseptual akademis, melainkan dapat ditransformasikan secara nyata menjadi fondasi utama sistem pendukung keputusan (Decision Support System). Melalui perpaduan pemfilteran batasan data biaya dan eksekusi *Algoritma Dijkstra*, sistem terbukti akurat dalam mengevaluasi rute alternatif serta menyajikan rekomendasi kost dengan akumulasi bobot jarak terpendek menuju kampus utama.

### 6.2 Saran Pengembangan

Untuk meningkatkan nilai guna sistem di masa mendatang, beberapa poin pengembangan yang disarankan meliputi:


## 1. Integrasi Database Dinamis & Back-Office Admin
* **Kondisi Saat Ini:** Data kost dan jaringan jalan masih bersifat statis (*hardcoded*) di dalam `st.session_state`.
* **Saran Pengembangan:** * Mengintegrasikan sistem dengan database relasional seperti **PostgreSQL** atau **MySQL**.
  * Membangun halaman *Dashboard Admin* khusus. Fitur ini memungkinkan pemilik kost untuk mendaftarkan atau memperbarui data harga sewa, foto, dan fasilitas secara mandiri tanpa perlu mengubah kode sumber aplikasi.

## 2. Implementasi Metode SPK Formal (AHP / TOPSIS)
* **Kondisi Saat Ini:** Rumus pembobotan utilitas AI masih menggunakan konstanta kaku (*hardcoded multipliers*), sehingga preferensi bersifat seragam untuk semua pengguna.
* **Saran Pengembangan:**
  * Menerapkan metode **AHP (Analytic Hierarchy Process)** untuk menentukan bobot kriteria secara objektif melalui kuesioner berpasangan.
  * Menggunakan metode **TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution)** untuk meranking kost berdasarkan jarak terdekat dari solusi ideal positif (harga paling murah, fasilitas paling lengkap) dan jarak terjauh dari solusi ideal negatif.
  * Menambahkan slider interaktif di UI agar mahasiswa dapat menentukan sendiri prioritas mereka (misal: mengutamakan harga murah vs mengutamakan jarak dekat).

## 3. Pemanfaatan API OpenStreetMap (OSM) & Jaringan Jalan Riil
* **Kondisi Saat Ini:** Graf jalan dibuat secara manual menggunakan koordinat buatan yang disederhanakan.
* **Saran Pengembangan:**
  * Memanfaatkan pustaka **OSMnx** untuk mengunduh data graf jaringan jalan asli di sekitar wilayah Panjer, Denpasar secara langsung dari OpenStreetMap.
  * Dengan integrasi ini, pencarian rute terpendek tidak lagi terbatas pada simpul buatan, melainkan mencakup seluruh gang dan jalan riil yang dapat dilalui oleh kendaraan roda dua maupun roda empat.

## 4. Sistem Login & Personalisasi Mahasiswa (Autentikasi)
* **Kondisi Saat Ini:** Aplikasi dapat diakses secara anonim dan tidak menyimpan riwayat pencarian.
* **Saran Pengembangan:**
  * Menambahkan fitur autentikasi pengguna (*Login/Register*) menggunakan **Firebase Auth** atau **Supabase**.
  * Fitur ini memungkinkan mahasiswa untuk menyimpan kost favorit (*bookmark*), memberikan rating/ulasan riil berbasis komunitas, serta mendapatkan rekomendasi yang dipersonalisasi berdasarkan program studi atau lokasi aktivitas harian di kampus.

## 5. Live Tracking & Navigasi Berbasis GPS
* **Kondisi Saat Ini:** Peta hanya bersifat statis menampilkan rute dari titik *A* ke titik *B*.
* **Saran Pengembangan:**

## 5. kesimpulan
* **Pemodelan yang Optimal:** Teori Graf mampu memetakan rute jalanan Panjer dan aturan satu arah dengan akurasi tinggi sesuai skenario data yang diinput.
* **Performa Masa Depan (Scalable):** Kombinasi Algoritma Dijkstra dan Min-Heap memastikan kalkulasi tetap instan, siap dikembangkan untuk skala data yang lebih luas.
* **Keputusan Lebih Objektif:** Fitur AI Smart Scoring efektif menekan faktor tebak-tebakan (subjektivitas) mahasiswa saat memilih kost.
   * Menggunakan API Geolokasi HTML5 untuk mendeteksi koordinat GPS *real-time* dari perangkat pengguna.
   * Sistem dapat memandu mahasiswa bergerak dari posisi mereka saat ini (*Current Location*) menuju lokasi kost target dengan indikator navigasi yang bergerak secara dinamis di atas peta Folium.

---
