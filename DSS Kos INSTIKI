import streamlit as st
import heapq
import folium
from streamlit_folium import st_folium

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(page_title="DSS Kost INSTIKI | KELOMPOK SUKA KENCANG", layout="wide", page_icon="🎓")

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
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .kriteria-box {
        background-color: #e0f2fe;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #0284c7;
        margin-bottom: 20px;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR UNTUK DOSEN PENGUJI (KRITERIA UAS)
# ==========================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Logo_INSTIKI.png/600px-Logo_INSTIKI.png", width=150) # Logo opsional
    st.title("📌 Info Project UAS")
    st.markdown("**Pengembang:** I Gede Wira Yoga")
    st.divider()
    
    st.markdown("""
    <div class='kriteria-box'>
    <b>✅ Implementasi Graph Terpakai:</b><br><br>
    <b>1. Adjacency List:</b><br>
    Struktur data menggunakan nested dictionary Python.<br><br>
    <b>2. Weighted Graph:</b><br>
    Edge memiliki bobot berupa jarak nyata (meter).<br><br>
    <b>3. Undirected Graph:</b><br>
    Mayoritas jalan raya bersifat dua arah.<br><br>
    <b>4. Directed Graph:</b><br>
    Terdapat jalur <i>Satu Arah (One-Way)</i> dari Simpang Pakerisan 1 menuju Simpang Pakerisan 2.
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# DATA DUNIA NYATA (INSTIKI & KOST PANJER AREA)
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
        
        # IMPLEMENTASI DIRECTED GRAPH (Jalan Satu Arah)
        # Simpang 1 bisa menuju Simpang 2 (Jarak 250m)
        'Simpang Pakerisan 1': {'INSTIKI (Kampus)': 300, 'Kosanku Bali': 100, 'Kost Kartika Sari': 150, 'Kost Batanghari': 400, 'Simpang Pakerisan 2': 250}, 
        
        # Simpang 2 TIDAK BISA kembali ke Simpang 1 (Koneksi searah / perboden)
        'Simpang Pakerisan 2': {'INSTIKI (Kampus)': 150, 'Simpang Petanu': 150}, 
        
        'Simpang Petanu': {'Simpang Pakerisan 2': 150, 'Kost Griya Petanu 34': 100}
    }

# ==========================================
# ALGORITMA DIJKSTRA & AI SCORING
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

    # Rekonstruksi rute jika jalur ditemukan
    path, current_node = [], end
    if previous_nodes[current_node] is None and current_node != start:
        return float('infinity'), [] # Tidak ada jalur (antisipasi jalan buntu karena One-Way)
        
    while previous_nodes[current_node] is not None:
        path.insert(0, current_node)
        current_node = previous_nodes[current_node]
    if path: path.insert(0, start)
    
    return distances[end], path

def calculate_ai_score(kost_name, distance):
    # Jika tidak ada jalur karena aturan jalan satu arah, skor di-nol-kan
    if distance == float('infinity'):
        return 0
        
    data = st.session_state.nodes[kost_name]
    score = (data['rating_maps'] * 20) + (data['fasilitas'] * 10) - (distance * 0.05) - (data['biaya'] / 10000)
    return round(score, 2)

# ==========================================
# PETA FOLIUM
# ==========================================
def create_map(path=None, ai_recommended=None):
    kampus_lat = st.session_state.nodes['INSTIKI (Kampus)']['lat']
    kampus_lon = st.session_state.nodes['INSTIKI (Kampus)']['lon']
    m = folium.Map(location=[kampus_lat, kampus_lon], zoom_start=16, tiles="CartoDB positron")

    # Gambar semua garis jalan (Edges)
    for node, neighbors in st.session_state.adj_list.items():
        node_coords = [st.session_state.nodes[node]['lat'], st.session_state.nodes[node]['lon']]
        for neighbor in neighbors:
            neighbor_coords = [st.session_state.nodes[neighbor]['lat'], st.session_state.nodes[neighbor]['lon']]
            
            # Beri warna khusus (orange putus-putus) untuk jalan Satu Arah (Directed Edge)
            if node == 'Simpang Pakerisan 1' and neighbor == 'Simpang Pakerisan 2':
                folium.PolyLine(locations=[node_coords, neighbor_coords], color="#f97316", weight=3, dash_array='5, 5', tooltip="Jalan Satu Arah").add_to(m)
            else:
                folium.PolyLine(locations=[node_coords, neighbor_coords], color="#cbd5e1", weight=2, opacity=0.8).add_to(m)

    # Highlight rute Dijkstra
    if path and len(path) > 0:
        path_coords = []
        for p in path:
            path_coords.append([st.session_state.nodes[p]['lat'], st.session_state.nodes[p]['lon']])
        folium.PolyLine(locations=path_coords, color="#ef4444", weight=6, opacity=0.9).add_to(m)

    # Tambahkan Marker
    for node, data in st.session_state.nodes.items():
        if node == 'INSTIKI (Kampus)':
            icon_color = 'red'
            icon_type = 'education'
            popup_text = f"<b>🎓 {node}</b>"
        elif node == ai_recommended:
            icon_color = 'purple'
            icon_type = 'star'
            popup_text = f"<b>⭐ {node}</b><br>Rating: {data['rating_maps']}/5<br>Harga: Rp {data['biaya']:,}"
        elif data['type'] == 'Kost':
            icon_color = 'green' if path and node in path else 'cadetblue'
            icon_type = 'home'
            popup_text = f"<b>🏠 {node}</b><br>Rating: {data['rating_maps']}/5<br>Harga: Rp {data['biaya']:,}"
        else:
            icon_color = 'lightgray'
            icon_type = 'info-sign'
            popup_text = node

        if data['type'] != 'Jalan':
            folium.Marker(
                location=[data['lat'], data['lon']],
                popup=folium.Popup(popup_text, max_width=200),
                tooltip=node,
                icon=folium.Icon(color=icon_color, prefix='glyphicon', icon=icon_type)
            ).add_to(m)

    return m

# ==========================================
# TAMPILAN UTAMA
# ==========================================
st.title("🎓 Smart DSS Pemilihan Kost INSTIKI")
st.markdown("Sistem Rekomendasi Terintegrasi Maps | Oleh: **I GD WIRA NATANAEL**")
st.divider()

col1, col2 = st.columns([1.2, 2])

with col1:
    st.subheader("⚙️ Parameter Filter (Real-time)")
    
    budget_maksimal = st.slider("Budget Maksimal Per Bulan (Rp):", min_value=500000, max_value=1500000, value=900000, step=100000)
    kost_tersedia = {k: v for k, v in st.session_state.nodes.items() if v['type'] == 'Kost' and v['biaya'] <= budget_maksimal}
    
    if not kost_tersedia:
        st.error("⚠️ Budget terlalu kecil. Tidak ada kost yang ditemukan di area INSTIKI.")
    else:
        ai_rankings = []
        for k in kost_tersedia.keys():
            jarak, rute = dijkstra(st.session_state.adj_list, k, 'INSTIKI (Kampus)')
            if rute: # Hanya rekomendasikan jika ada jalur yang masuk akal
                score = calculate_ai_score(k, jarak)
                ai_rankings.append({'kost': k, 'jarak': jarak, 'rute': rute, 'score': score})
        
        if ai_rankings:
            ai_rankings = sorted(ai_rankings, key=lambda x: x['score'], reverse=True)
            top_kost = ai_rankings[0]
            
            st.markdown(f"<span class='ai-badge'>✨ AI Top Recommendation: {top_kost['kost']}</span>", unsafe_allow_html=True)
            st.write("") 
            
            pilihan_kost = st.selectbox("Pilih Kost untuk melihat rute ke INSTIKI:", [k['kost'] for k in ai_rankings])
            selected_data = next(item for item in ai_rankings if item["kost"] == pilihan_kost)
            
            st.write("### Detail Atribut Kost")
            d1, d2 = st.columns(2)
            d1.metric("Rating Google Maps", f"⭐ {st.session_state.nodes[pilihan_kost]['rating_maps']}")
            d2.metric("Skor Fasilitas", f"{st.session_state.nodes[pilihan_kost]['fasilitas']}/10")
        else:
            st.error("Terisolasi karena aturan jalan satu arah.")

with col2:
    st.subheader("🗺️ Live Map & Navigasi")
    
    if kost_tersedia and ai_rankings:
        m1, m2, m3 = st.columns(3)
        m1.metric(label="Jarak ke INSTIKI", value=f"{selected_data['jarak']} Meter")
        m2.metric(label="Harga Sewa", value=f"Rp {st.session_state.nodes[pilihan_kost]['biaya']:,}")
        m3.metric(label="AI Smart Score", value=f"{selected_data['score']}")
        
        peta = create_map(path=selected_data['rute'], ai_recommended=top_kost['kost'])
        st_folium(peta, width=700, height=450)
        
        st.info(f"**Rute:** {' ➔ '.join(selected_data['rute'])}")
    else:
        st.write("Sesuaikan budget untuk menampilkan hasil peta.")
        peta = create_map()
        st_folium(peta, width=700, height=450)
