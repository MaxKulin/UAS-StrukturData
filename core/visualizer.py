# visualizer.py
# Menggambar graph Pulau Bali menggunakan networkx + matplotlib

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from core.graph import GRAPH, NODE_TYPES, get_all_edges

NODE_COLORS = {
    "depot": "#DC2626",
    "hub": "#2563EB",
    "zone": "#059669",
}

EDGE_COLOR_DEFAULT = "#CBD5E1"

SEGMENT_COLORS = [
    "#F59E0B",
    "#EAB308",
    "#0EA5E9",
    "#8B5CF6",
    "#10B981",
    "#FB923C",
]


def build_nx_graph():
    G = nx.Graph()
    for node in NODE_TYPES:
        G.add_node(node, node_type=NODE_TYPES[node])
    for a, b, w in get_all_edges():
        G.add_edge(a, b, weight=w)
    return G




def get_layout(G):
    return {
        "Depot Denpasar": (0, 0),
        "Hub Badung": (-3, -1),
        "Hub Tabanan": (-5, 2),
        "Hub Gianyar": (3, 1),
        "Hub Klungkung": (6, -1),
        "Zona Mengwi": (-4, 1),
        "Zona Kediri": (-7, 3),
        "Zona Ubud": (2, 3),
        "Zona Sukawati": (5, 2),
        "Zona Kuta": (-5, -3),
        "Zona Jimbaran": (-2, -4),
        "Zona Semarapura": (7, 0),
        "Zona Nusa Penida": (10, -3),
    }

def get_node_color_list(G):
    return [NODE_COLORS[NODE_TYPES[n]] for n in G.nodes()]

def draw_graph(path=None, segments=None, title="Pulau Bali — Jaringan Distribusi"):
    G = build_nx_graph()
    pos = get_layout(G)

    fig, ax = plt.subplots(figsize=(18, 11), dpi=120)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    edge_color_map = {}
    edge_width_map = {}
    all_path_nodes = set()

    if segments:
        for seg_idx, seg_path in enumerate(segments):
            color = SEGMENT_COLORS[seg_idx % len(SEGMENT_COLORS)]
            if len(seg_path) > 1:
                for i in range(len(seg_path) - 1):
                    u, v = seg_path[i], seg_path[i + 1]
                    key = tuple(sorted([u, v]))
                    edge_color_map[key] = color
                    edge_width_map[key] = 4.5
                all_path_nodes.update(seg_path)

    elif path and len(path) > 1:
        color = SEGMENT_COLORS[0]
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            key = tuple(sorted([u, v]))
            edge_color_map[key] = color
            edge_width_map[key] = 4.5
        all_path_nodes.update(path)

    edge_colors = []
    edge_widths = []

    for u, v in G.edges():
        key = tuple(sorted([u, v]))
        if key in edge_color_map:
            edge_colors.append(edge_color_map[key])
            edge_widths.append(edge_width_map[key])
        else:
            edge_colors.append(EDGE_COLOR_DEFAULT)
            edge_widths.append(1.5)

    nx.draw_networkx_edges(
        G, pos,
        edge_color=edge_colors,
        width=edge_widths,
        ax=ax,
        alpha=0.85,
    )

    nx.draw_networkx_nodes(
        G, pos,
        node_color=get_node_color_list(G),
        node_size=1200,
        ax=ax,
    )

    if all_path_nodes:
        nx.draw_networkx_nodes(
            G, pos,
            nodelist=list(all_path_nodes),
            node_color=SEGMENT_COLORS[0],
            node_size=1400,
            ax=ax,
        )

    nx.draw_networkx_labels(
        G, pos,
        font_size=9,
        font_color="#1E293B",
        font_weight="bold",
        ax=ax,
    )

    edge_labels = nx.get_edge_attributes(G, "weight")
    edge_label_formatted = {k: f"{v} km" for k, v in edge_labels.items()}

    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=edge_label_formatted,
        font_size=8,
        font_color="#475569",
        bbox=dict(
            boxstyle="round,pad=0.2",
            fc="#F8FAFC",
            ec="#CBD5E1",
            alpha=1,
        ),
        ax=ax,
    )

    legend_items = [
        mpatches.Patch(color=NODE_COLORS["depot"], label="Pusat Distribusi"),
        mpatches.Patch(color=NODE_COLORS["hub"], label="Pusat Konsolidasi"),
        mpatches.Patch(color=NODE_COLORS["zone"], label="Area Pengiriman"),
    ]

    ax.legend(
        handles=legend_items,
        loc="upper right",
        facecolor="white",
        edgecolor="#CBD5E1",
        labelcolor="#334155",
        fontsize=9,
        framealpha=1,
    )

    ax.set_title(
        title,
        color="#0F172A",
        fontsize=14,
        pad=18,
        fontweight="bold",
    )

    ax.axis("off")
    plt.tight_layout(pad=1.5)

    return fig
