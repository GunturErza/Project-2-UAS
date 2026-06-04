import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import heapq

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

@st.cache_resource
def init_dss_graph():
    dss = DSSGraph()
    dss.add_node("KAMPUS", "Kampus Utama", "Kampus")
    dss.add_node("KOST_A", "Kost Exclusif A", "Kost", 1500000)
    dss.add_node("KOST_B", "Kost Muslimah B", "Kost", 800000)
    dss.add_node("KOST_C", "Kost Campur C", "Kost", 1100000)
    dss.add_node("FAC_1", "Warmindo & Laundry", "Fasilitas")
    dss.add_node("FAC_2", "Minimarket", "Fasilitas")

    dss.add_edge("KOST_A", "FAC_1", 200)
    dss.add_edge("FAC_1", "KAMPUS", 500)
    dss.add_edge("KOST_B", "FAC_2", 400)
    dss.add_edge("FAC_2", "KAMPUS", 600)
    dss.add_edge("KOST_C", "FAC_1", 300)
    dss.add_edge("KOST_C", "FAC_2", 350)
    dss.add_edge("FAC_1", "FAC_2", 150)
    
    return dss

dss = init_dss_graph()

st.set_page_config(page_title="DSS Pemilihan Kost", layout="wide")
st.title("🌐 Decision Support System (DSS) Pemilihan Kost Berbasis Graph")
st.caption("Mata Kuliah: Struktur Data | Algoritma: Dijkstra's Shortest Path")

st.sidebar.header("🔍 Filter & Kriteria Keputusan")
budget = st.sidebar.slider("Budget Maksimal Kost (Rp/Bulan)", 500000, 2000000, 1200000, step=50000)
bobot_jarak = st.sidebar.checkbox("Prioritaskan Jalur Terpendek", value=True)

valid_kost = [node for node, info in dss.node_info.items() if info["type"] == "Kost" and info["cost"] <= budget]

st.sidebar.subheader("Pilih Kost yang Tersedia:")
selected_kost = st.sidebar.selectbox("Daftar Kost Sesuai Budget:", valid_kost, format_func=lambda x: f"{dss.node_info[x]['label']} (Rp {dss.node_info[x]['cost']:,})")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 Analisis Keputusan & Rekomendasi")
    
    if selected_kost:
        jarak_terpendek, jalur = dss.dijkstra(selected_kost, "KAMPUS")
        
        st.success(f"**Rekomendasi Terpilih:** {dss.node_info[selected_kost]['label']}")
        st.metric(label="Total Jarak ke Kampus", value=f"{jarak_terpendek} Meter")
        
        st.markdown("### 🛤️ Jalur yang Dilewati:")
        jalur_text = " ➡️ ".join([dss.node_info[node]['label'] for node in jalur])
        st.info(jalur_text)
        
        st.markdown("""
        **Analisis Logika Keputusan:**
        Sistem memfilter kost berdasarkan batas finansial (budget) pengguna. Selanjutnya, algoritma Dijkstra menghitung bobot akumulatif terkecil dari simpul kost terpilih menuju simpul target (Kampus).
        """)
    else:
        st.warning("Tidak ada kost yang memenuhi kriteria budget Anda. Silakan naikkan budget pada sidebar.")

with col2:
    st.subheader("📍 Visualisasi Jaringan Jaringan Graph")
    
    G = nx.Graph()
    
    for u, neighbors in dss.graph.items():
        for v, weight in neighbors.items():
            G.add_edge(dss.node_info[u]['label'], dss.node_info[v]['label'], weight=weight)
            
    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(6, 5))
    
    color_map = []
    for node in G:
        node_id = [k for k, v in dss.node_info.items() if v['label'] == node][0]
        if node_id == "KAMPUS":
            color_map.append('#ff4b4b')
        elif dss.node_info[node_id]['type'] == "Kost":
            color_map.append('#1f77b4')
        else:
            color_map.append('#2ca02c')
            
    nx.draw_networkx_nodes(G, pos, node_color=color_map, node_size=800, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=9, font_color="black", font_weight="bold", ax=ax)
    
    if selected_kost and len(jalur) > 1:
        path_edges = [(dss.node_info[jalur[i]]['label'], dss.node_info[jalur[i+1]]['label']) for i in range(len(jalur)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='#ff4b4b', width=3, ax=ax)
        
        remain_edges = [edge for edge in G.edges() if edge not in path_edges and (edge[1], edge[0]) not in path_edges]
        nx.draw_networkx_edges(G, pos, edgelist=remain_edges, edge_color='gray', style='dashed', ax=ax)
    else:
        nx.draw_networkx_edges(G, pos, edge_color='gray', ax=ax)
        
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, ax=ax)
    
    plt.axis('off')
    st.pyplot(fig)
