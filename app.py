# app.py
# Antarmuka utama DSS Rute Pengiriman Paket — Di bali
# Jalankan dengan: streamlit run app.py

import streamlit as st
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend, wajib untuk Streamlit

from core.graph import get_all_nodes, NODE_TYPES
from core.dijkstra import dijkstra, get_step_by_step
from core.visualizer import draw_graph


# -----------------------------------------------------------
# KONFIGURASI HALAMAN
# -----------------------------------------------------------

st.set_page_config(
    page_title="Sistem Optimasi Distribusi Bali",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# -----------------------------------------------------------
# CSS KUSTOM
# Mengikuti palet warna visualizer: dark navy + aksen oranye
# -----------------------------------------------------------

st.markdown("""
<style>
    .stApp {
        background-color: #FFFFFF;
        color: #1E293B;
    }

    [data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }

    [data-testid="stSidebar"] * {
        color: #334155 !important;
    }

    .sidebar-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #2563EB !important;
        margin-bottom: 0.4rem;
        letter-spacing: 0.03em;
    }

    .result-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 5px solid #2563EB;
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    .step-item {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 0.7rem 1rem;
        margin-bottom: 0.5rem;
        color: #334155;
    }

    .step-arrow {
        color: #2563EB;
        font-weight: bold;
    }

    .badge-depot {
        background-color: #DC2626;
        color: white;
        padding: 3px 9px;
        border-radius: 12px;
        font-size: 0.72rem;
        font-weight: 600;
    }

    .badge-hub {
        background-color: #2563EB;
        color: white;
        padding: 3px 9px;
        border-radius: 12px;
        font-size: 0.72rem;
        font-weight: 600;
    }

    .badge-zone {
        background-color: #059669;
        color: white;
        padding: 3px 9px;
        border-radius: 12px;
        font-size: 0.72rem;
        font-weight: 600;
    }

    .distance-display {
        font-size: 2.5rem;
        font-weight: 800;
        color: #2563EB;
        line-height: 1.1;
    }

    .distance-label {
        font-size: 0.85rem;
        color: #64748B;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .main-header {
        font-size: 1.8rem;
        font-weight: 800;
        color: #0F172A;
    }

    .main-subtitle {
        font-size: 0.95rem;
        color: #64748B;
        margin-top: -0.3rem;
        margin-bottom: 1.2rem;
    }

    hr {
        border-color: #E2E8F0 !important;
    }

    .stSelectbox label,
    .stRadio label {
        color: #475569 !important;
    }

    .stButton > button {
        background-color: #2563EB;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        width: 100%;
        font-weight: 700;
    }

    .stButton > button:hover {
        background-color: #1D4ED8;
        color: white;
    }

    .stAlert {
        background-color: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
        color: #334155 !important;
    }
    /* Selectbox utama */
.stSelectbox div[data-baseweb="select"] > div {
    background-color: #FEF3C7 !important;
    border: 2px solid #F59E0B !important;
    border-radius: 8px !important;
}

/* Teks yang terpilih */
.stSelectbox div[data-baseweb="select"] span {
    color: #92400E !important;
    font-weight: 600 !important;
}

/* Ikon panah dropdown */
.stSelectbox svg {
    color: #92400E !important;
}

/* Menu dropdown */
div[role="listbox"] {
    background-color: white !important;
    border: 1px solid #F59E0B !important;
}

/* Item dalam dropdown */
div[role="option"] {
    color: #1E293B !important;
}

/* Hover item */
div[role="option"]:hover {
    background-color: #FEF3C7 !important;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------
# HELPER: badge HTML untuk tipe node
# -----------------------------------------------------------

def node_badge(node_name):
    t = NODE_TYPES.get(node_name, "zone")
    label = {"depot": "Gudang Pusat", "hub": "Hub Transit", "zone": "Drop Point"}.get(t, t)
    return f'<span class="badge-{t}">{label}</span>'


def node_display(node_name):
    return f"{node_name} &nbsp;{node_badge(node_name)}"


# -----------------------------------------------------------
# SIDEBAR: Panel Input
# -----------------------------------------------------------

with st.sidebar:
    st.markdown('<div class="sidebar-title"> Pulau Bali</div>', unsafe_allow_html=True)
    st.markdown("**Decision Support System**  \nRute Pengiriman Paket", unsafe_allow_html=False)
    st.divider()

    all_nodes = get_all_nodes()

    st.markdown("**Titik Asal**")
    start_node = st.selectbox(
        label="Asal",
        options=all_nodes,
        index=0,
        label_visibility="collapsed",
        key="start_node",
    )
    st.markdown(node_badge(start_node), unsafe_allow_html=True)

    st.markdown(" ")
    st.markdown("**Titik Tujuan**")

    # Default tujuan: node terakhir (Zone Haven), hindari sama dengan asal
    default_end_index = len(all_nodes) - 1 if all_nodes[-1] != start_node else len(all_nodes) - 2
    end_node = st.selectbox(
        label="Tujuan",
        options=all_nodes,
        index=default_end_index,
        label_visibility="collapsed",
        key="end_node",
    )
    st.markdown(node_badge(end_node), unsafe_allow_html=True)

    st.markdown(" ")
    cari_button = st.button("🔍 Cari Rute Terpendek")

    st.divider()

    # Legenda
    st.markdown("**Legenda**")
    st.markdown(
        '<span class="badge-depot">Gudang Pusat</span>&nbsp; Titik distribusi utama<br><br>'
        '<span class="badge-hub">Hub Transit</span>&nbsp; Titik perantara<br><br>'
        '<span class="badge-zone">Drop Point</span>&nbsp; Titik pengiriman akhir',
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------
# MAIN CONTENT
# -----------------------------------------------------------

st.markdown('<div class="main-header"> DSS Rute Pengiriman — Distribusi Bali</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="main-subtitle">Sistem Penentuan Rute Terpendek berbasis Algoritma Dijkstra</div>',
    unsafe_allow_html=True,
)

# -----------------------------------------------------------
# STATE MANAGEMENT
# Simpan hasil pencarian di session_state supaya tidak hilang
# saat widget lain berubah
# -----------------------------------------------------------

if "last_result" not in st.session_state:
    st.session_state.last_result = None  # {path, distance, start, end}

# Proses pencarian saat tombol ditekan
if cari_button:
    if start_node == end_node:
        st.warning("Titik asal dan tujuan tidak boleh sama.")
        st.session_state.last_result = None
    else:
        with st.spinner("Menghitung rute terpendek..."):
            path, distance = dijkstra(start_node, end_node)

        if path is None:
            st.error("Tidak ditemukan rute yang menghubungkan kedua titik ini.")
            st.session_state.last_result = None
        else:
            st.session_state.last_result = {
                "path"     : path,
                "distance" : distance,
                "start"    : start_node,
                "end"      : end_node,
            }

# -----------------------------------------------------------
# TAMPILAN HASIL + VISUALISASI
# -----------------------------------------------------------

result = st.session_state.last_result

# Layout: kolom kiri (grafik) | kolom kanan (info rute)
col_graph, col_info = st.columns([2.2, 1], gap="large")

with col_graph:
    if result:
        fig = draw_graph(
            path=result["path"],
            title=f"Rute: {result['start']} → {result['end']}",
        )
    else:
        fig = draw_graph(title="Pulau bali — Jaringan Distribusi")

    st.pyplot(fig, use_container_width=True)

with col_info:
    if result:
        path   = result["path"]
        dist   = result["distance"]
        start  = result["start"]
        end    = result["end"]
        steps  = get_step_by_step(path)

        # --- Ringkasan jarak ---
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown(
            f'<div class="distance-label">Total Jarak</div>'
            f'<div class="distance-display">{dist} km</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<br><b>Dari:</b> &nbsp;{node_badge(start)} {start}<br>'
            f'<b>Ke:</b> &nbsp;&nbsp;&nbsp;{node_badge(end)} {end}',
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # --- Jalur lengkap ---
        st.markdown("**Jalur yang Dilalui**")
        full_path_str = " → ".join(path)
        st.markdown(
            f'<div class="step-item">🗺️ {full_path_str}</div>',
            unsafe_allow_html=True,
        )

        # --- Step by step ---
        st.markdown(" ")
        st.markdown(f"**Rincian Langkah** &nbsp;({len(steps)} segmen)", unsafe_allow_html=True)

        # Ambil bobot tiap segmen dari GRAPH
        from core.graph import GRAPH as _GRAPH
        for i, step in enumerate(steps):
            fr  = step["from"]
            to  = step["to"]
            seg_dist = _GRAPH[fr].get(to, _GRAPH.get(to, {}).get(fr, "?"))
            st.markdown(
                f'<div class="step-item">'
                f'<b>{i+1}.</b> {fr} <span class="step-arrow">→</span> {to} '
                f'<span style="color:#7F8C9A; font-size:0.82rem;">({seg_dist} km)</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

        # --- Jumlah node singgah ---
        transit_nodes = path[1:-1]
        if transit_nodes:
            st.markdown(" ")
            st.markdown(f"**Node Transit** &nbsp;({len(transit_nodes)} titik)", unsafe_allow_html=True)
            for n in transit_nodes:
                st.markdown(
                    f'<div class="step-item">⬡ {n} &nbsp;{node_badge(n)}</div>',
                    unsafe_allow_html=True,
                )
    else:
        # Belum ada pencarian
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown(
            "**Pilih titik asal dan tujuan** di panel kiri, "
            "lalu klik **Cari Rute Terpendek** untuk melihat hasil.",
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # Tampilkan info singkat semua node
        st.markdown("**Node dalam Jaringan**")
        for node, ntype in NODE_TYPES.items():
            label = {"depot": "Gudang Pusat", "hub": "Hub Transit", "zone": "Drop Point"}[ntype]
            st.markdown(
                f'<div class="step-item">⬡ {node} &nbsp;<span class="badge-{ntype}">{label}</span></div>',
                unsafe_allow_html=True,
            )


# -----------------------------------------------------------
# FOOTER
# -----------------------------------------------------------

st.divider()
st.markdown(
    '<div style="text-align:center; color:#3D5166; font-size:0.78rem;">'
    'DSS Rute Pengiriman Paket · Kota Syntara · Algoritma Dijkstra · Struktur Data'
    '</div>',
    unsafe_allow_html=True,
)
