# graph.py
# Struktur data utama: representasi graph distribusi Bali
# Menggunakan Adjacency List (dictionary) dengan bobot jarak (km)

# -----------------------------------------------------------
# TIPE NODE
# Setiap node punya tipe: "depot", "hub", atau "zone"
# -----------------------------------------------------------

NODE_TYPES = {
    "Depot Denpasar"     : "depot",
    "Hub Tabanan"        : "hub",
    "Hub Gianyar"        : "hub",
    "Hub Badung"         : "hub",
    "Hub Klungkung"      : "hub",
    "Zona Mengwi"        : "zone",
    "Zona Kediri"        : "zone",
    "Zona Ubud"          : "zone",
    "Zona Sukawati"      : "zone",
    "Zona Kuta"          : "zone",
    "Zona Jimbaran"      : "zone",
    "Zona Semarapura"    : "zone",
    "Zona Nusa Penida"   : "zone",
}

# -----------------------------------------------------------
# ADJACENCY LIST
# Format: { "NodeA": {"NodeB": jarak, "NodeC": jarak}, ... }
# Graph ini UNDIRECTED
# -----------------------------------------------------------

GRAPH = {
    "Depot Denpasar": {
        "Hub Tabanan"   : 18,
        "Hub Gianyar"   : 16,
        "Hub Badung"    : 12,
        "Hub Klungkung" : 28,
    },

    "Hub Tabanan": {
        "Depot Denpasar" : 18,
        "Hub Gianyar"    : 22,
        "Zona Mengwi"    : 8,
        "Zona Kediri"    : 6,
        "Zona Semarapura": 35,
    },

    "Hub Gianyar": {
        "Depot Denpasar" : 16,
        "Hub Tabanan"    : 22,
        "Zona Ubud"      : 7,
        "Zona Sukawati"  : 5,
        "Zona Jimbaran"  : 27,
    },

    "Hub Badung": {
        "Depot Denpasar" : 12,
        "Hub Klungkung"  : 32,
        "Zona Kuta"      : 6,
        "Zona Jimbaran"  : 9,
    },

    "Hub Klungkung": {
        "Depot Denpasar" : 28,
        "Hub Badung"     : 32,
        "Zona Semarapura": 4,
        "Zona Nusa Penida": 18,
    },

    "Zona Mengwi": {
        "Hub Tabanan": 8,
    },

    "Zona Kediri": {
        "Hub Tabanan": 6,
    },

    "Zona Ubud": {
        "Hub Gianyar": 7,
    },

    "Zona Sukawati": {
        "Hub Gianyar": 5,
    },

    "Zona Kuta": {
        "Hub Badung": 6,
    },

    "Zona Jimbaran": {
        "Hub Badung": 9,
        "Hub Gianyar": 27,
    },

    "Zona Semarapura": {
        "Hub Klungkung": 4,
        "Hub Tabanan": 35,
    },

    "Zona Nusa Penida": {
        "Hub Klungkung": 18,
    },
}

def get_neighbors(node):
    return GRAPH.get(node, {})
    
def get_all_nodes():
    return list(NODE_TYPES.keys())


def get_all_edges():
    edges = []
    visited = set()
    for node, neighbors in GRAPH.items():
        for neighbor, weight in neighbors.items():
            pair = tuple(sorted([node, neighbor]))
            if pair not in visited:
                edges.append((node, neighbor, weight))
                visited.add(pair)
    return edges


