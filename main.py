import streamlit as st
import heapq
import folium
from streamlit_folium import st_folium
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(page_title="DSS Kost INSTIKI | KELOMPOK CHUY", layout="wide", page_icon="🎓")

st.markdown("""
<style>
    .main { background-color: #f8fafc; }
    h1, h2, h3 { color: #0f172a; font-family: 'Inter', sans-serif; }
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #ef4444;
    }
    .ai-badge {
        background: linear-gradient(135deg, #ef4444 0%, #f97316 100%);
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
    }
    .kriteria-box {
        background-color: #e0f2fe;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #0284c7;
        margin-bottom: 20px;
        font-size: 0.9rem;
    }
    .reason-box {
        background-color: #f0fdf4;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #22c55e;
        margin-top: 15px;
        font-size: 0.95rem;
        color: #166534;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR UNTUK DOSEN PENGUJI (KRITERIA UAS)
# ==========================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Logo_INSTIKI.png/600px-Logo_INSTIKI.png", width=150)
    st.title("📌 Info Project UAS")
    st.markdown("**Pengembang:** KELOMPOK CIHUY")
    st.divider()
    
    st.markdown("""
    <div class='kriteria-box'>
    <b>✅ Fitur Analisis Graf Terintegrasi:</b><br><br>
    • <b>Adjacency List & Matrix Basis</b><br>
    • <b>Weighted & Directed Graph</b><br>
    • <b>Centrality Analysis:</b> Menghitung titik paling krusial di sekitar Panjer.<br>
    • <b>Dynamic Topology Graph:</b> Visualisasi murni struktur graf via NetworkX.<br>
    • <b>AI Multi-Criteria Scoring Breakdown</b>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# DATASET (INSTIKI & AREA SEKITAR)
# ==========================================
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
        'Simpang Pakerisan 2': {'INSTIKI (Kampus)': 150, 'Simpang Petanu': 150}, # Directed One-Way
        'Simpang Petanu': {'Simpang Pakerisan 2': 150, 'Kost Griya Petanu 34': 100}
    }

# ==========================================
# ENGINES & ALGORITHMS
# ==========================================
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

def get_score_breakdown(kost_name, distance):
    if distance == float('infinity'):
        return {"total": 0, "rating_component": 0, "facility_component": 0, "distance_penalty": 0, "price_penalty": 0}
    
    data = st.session_state.nodes[kost_name]
    
    # BEDAH BOBOT PENILAIAN SESUAI PERMINTAAN
    r_comp = data['rating_maps'] * 20       # Pengaruh besar rating maps
    f_comp = data['fasilitas'] * 10        # Pengaruh poin fasilitas
    d_pent = distance * 0.05               # Penalti jarak (makin jauh makin memotong skor)
    p_pent = data['biaya'] / 10000         # Penalti harga (makin mahal makin memotong skor)
    
    total = round(r_comp + f_comp - d_pent - p_pent, 2)
    return {
        "total": total,
        "rating_component": round(r_comp, 2),
        "facility_component": round(f_comp, 2),
        "distance_penalty": round(d_pent, 2),
        "price_penalty": round(p_pent, 2)
    }

def generate_ai_reason(selected, rankings):
    if not rankings:
        return "Tidak ada analisis tersedia."
    
    top_kost = rankings[0]['kost']
    selected_data = next(item for item in rankings if item["kost"] == selected)
    
    node_details = st.session_state.nodes[selected]
    
    if selected == top_kost:
        return f"💡 **Mengapa AI Memilih {selected}?** Kost ini mendapatkan peringkat 1 karena menawarkan efisiensi terbaik. Meskipun mungkin harganya bukan yang paling murah, kombinasi **Rating Maps yang tinggi (⭐{node_details['rating_maps']})** dan **jarak optimal berbobot ({selected_data['jarak']}m)** melahirkan nilai utilitas tertinggi dibandingkan opsi lainnya."
    else:
        return f"💡 **Analisis Perbandingan AI:** {selected} menduduki peringkat di bawah {top_kost}. Hal ini disebabkan karena nilai komponen penalti harganya yang cukup besar atau jarak tempuh rutenya memakan waktu lebih lama, meskipun fasilitasnya sudah bersaing."

# ==========================================
# GEOGRAPHICAL MAP (FOLIUM)
# ==========================================
def create_folium_map(path=None, ai_recommended=None):
    kampus_lat, kampus_lon = st.session_state.nodes['INSTIKI (Kampus)']['lat'], st.session_state.nodes['INSTIKI (Kampus)']['lon']
    m = folium.Map(location=[kampus_lat, kampus_lon], zoom_start=16, tiles="CartoDB positron")

    for node, neighbors in st.session_state.adj_list.items():
        node_coords = [st.session_state.nodes[node]['lat'], st.session_state.nodes[node]['lon']]
        for neighbor in neighbors:
            neighbor_coords = [st.session_state.nodes[neighbor]['lat'], st.session_state.nodes[neighbor]['lon']]
            if node == 'Simpang Pakerisan 1' and neighbor == 'Simpang Pakerisan 2':
                folium.PolyLine(locations=[node_coords, neighbor_coords], color="#f97316", weight=3, dash_array='5, 5', tooltip="Jalan Satu Arah").add_to(m)
            else:
                folium.PolyLine(locations=[node_coords, neighbor_coords], color="#cbd5e1", weight=2, opacity=0.8).add_to(m)

    if path:
        path_coords = [[st.session_state.nodes[p]['lat'], st.session_state.nodes[p]['lon']] for p in path]
        folium.PolyLine(locations=path_coords, color="#ef4444", weight=6, opacity=0.9).add_to(m)

    for node, data in st.session_state.nodes.items():
        if node == 'INSTIKI (Kampus)':
            icon, color = 'education', 'red'
        elif node == ai_recommended:
            icon, color = 'star', 'purple'
        elif data['type'] == 'Kost':
            icon, color = 'home', 'green' if path and node in path else 'cadetblue'
        else: continue

        folium.Marker(
            location=[data['lat'], data['lon']],
            tooltip=node,
            icon=folium.Icon(color=color, icon=icon)
        ).add_to(m)
    return m

# ==========================================
# LAYOUT UTAMA STREAMLIT
# ==========================================
st.title("🎓 Smart DSS Pemilihan Kost INSTIKI")
st.markdown("Sistem Pendukung Keputusan Berbasis Struktur Data Graf Terintegrasi")
st.divider()

# Membagi Halaman Menjadi Tab untuk Tampilan Akademik yang Rapi
tab1, tab2 = st.tabs(["🗺️ Peta Navigasi & SPK", "📊 Analisis Topologi Jaringan & Centrality"])

# Membangun Objek Graph NetworkX untuk Digunakan Bersama
G = nx.DiGraph()
for node, neighbors in st.session_state.adj_list.items():
    for neighbor, w in neighbors.items():
        G.add_edge(node, neighbor, weight=w)

with tab1:
    col1, col2 = st.columns([1.2, 2])
    
    with col1:
        st.subheader("⚙️ Filter & Bobot Keputusan")
        budget_maksimal = st.slider("Budget Maksimal Kost (Rp):", 500000, 1500000, 1000000, 100000)
        
        kost_tersedia = {k: v for k, v in st.session_state.nodes.items() if v['type'] == 'Kost' and v['biaya'] <= budget_maksimal}
        
        if not kost_tersedia:
            st.error("⚠️ Tidak ada kost dalam range budget tersebut.")
        else:
            ai_rankings = []
            for k in kost_tersedia.keys():
                jarak, rute = dijkstra(st.session_state.adj_list, k, 'INSTIKI (Kampus)')
                if rute:
                    bd = get_score_breakdown(k, jarak)
                    ai_rankings.append({'kost': k, 'jarak': jarak, 'rute': rute, 'score': bd['total'], 'breakdown': bd})
            
            if ai_rankings:
                ai_rankings = sorted(ai_rankings, key=lambda x: x['score'], reverse=True)
                top_kost = ai_rankings[0]['kost']
                
                st.markdown(f"<div class='ai-badge'>✨ Rekomendasi Terbaik AI: {top_kost}</div>", unsafe_allow_html=True)
                
                pilihan_kost = st.selectbox("Pilih rumah kost untuk dianalisis:", [k['kost'] for k in ai_rankings])
                selected_node_data = next(item for item in ai_rankings if item["kost"] == pilihan_kost)
                
                # Menampilkan alasan dinamis AI
                reason_html = generate_ai_reason(pilihan_kost, ai_rankings)
                st.markdown(f"<div class='reason-box'>{reason_html}</div>", unsafe_allow_html=True)
                
                # TAMPILKAN BOBOT MEMPENGARUHI RATING MAPS SUEAI PERMINTAAN
                st.write("### 📐 Breakdown Bobot Skor AI:")
                bd_vals = selected_node_data['breakdown']
                
                st.write(f"- 📈 **Poin Utama Rating Maps (Rating × 25):** `+{bd_vals['rating_component']}`")
                st.write(f"- 🛏️ **Poin Utama Fasilitas (Skor × 10):** `+{bd_vals['facility_component']}`")
                st.write(f"- 📐 **Penalti Jarak Graf (Jarak Meter × 0.05):** `-{bd_vals['distance_penalty']}`")
                st.write(f"- 💵 **Penalti Harga Sewa (Biaya / 10000):** `-{bd_vals['price_penalty']}`")
                st.write(f"👉 **Skor Akhir Utilitas:** `{bd_vals['total']}`")
                
    with col2:
        st.subheader("🗺️ Live Route Map")
        if kost_tersedia and ai_rankings:
            m1, m2 = st.columns(2)
            m1.metric("Jarak Lintasan Terpendek", f"{selected_node_data['jarak']} Meter")
            m2.metric("Biaya Kost Per Bulan", f"Rp {st.session_state.nodes[pilihan_kost]['biaya']:,}")
            
            peta_folium = create_folium_map(path=selected_node_data['rute'], ai_recommended=top_kost)
            st_folium(peta_folium, width=750, height=420)
            st.info(f"🛣️ **Simpul Rute Dijkstra:** {' ➔ '.join(selected_node_data['rute'])}")

with tab2:
    st.subheader("📊 Analisis Teori Struktur Graf")
    st.write("Bagian ini menampilkan representasi matematika murni dari struktur data jaringan jalan yang digunakan aplikasi.")
    
    c1, c2 = st.columns([1.5, 1])
    
    with c1:
        st.write("### 🕸️ Jaringan Graph Dinamis (Network Topology)")
        # Menggambar grafik topologi murni menggunakan matplotlib & networkx
        fig, ax = plt.subplots(figsize=(7, 5))
        pos = nx.spring_layout(G, seed=42)
        
        # Bedakan warna node tujuan (Kampus) dan node biasa
        node_colors = ['#ef4444' if n == 'INSTIKI (Kampus)' else '#3b82f6' if st.session_state.nodes[n]['type'] == 'Kost' else '#94a3b8' for n in G.nodes()]
        
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=900, ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold', font_color='black', ax=ax)
        
        # Gambar Edge berarah
        nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='#64748b', arrows=True, arrowsize=15, ax=ax)
        
        # Label Bobot Jarak Jaringan
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=7, ax=ax)
        
        plt.axis('off')
        st.pyplot(fig)
        
    with c2:
        st.write("### 📐 Analisis Centrality (Sentralitas)")
        st.write("Analisis sentralitas digunakan untuk mengetahui simpul (node) mana yang paling kritis/penting dalam sistem jaringan.")
        
        # Hitung Nilai Metric Centrality
        degree_cent = nx.degree_centrality(G)
        closeness_cent = nx.closeness_centrality(G)
        
        centrality_data = []
        for node in G.nodes():
            centrality_data.append({
                "Nama Simpul Node": node,
                "Degree Centrality (Konektivitas)": round(degree_cent[node], 3),
                "Closeness Centrality (Akses Terdekat)": round(closeness_cent[node], 3)
            })
            
        df_centrality = pd.DataFrame(centrality_data).sort_values(by="Degree Centrality (Konektivitas)", ascending=False)
        st.dataframe(df_centrality, use_container_width=True)
        
        st.caption("💡 **Catatan Akademik:** Nilai Degree Centrality tinggi menunjukkan node tersebut memiliki cabang persimpangan jalan terbanyak di dunia nyata.")
