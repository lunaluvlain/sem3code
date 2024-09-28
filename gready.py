import networkx as nx
import matplotlib.pyplot as plt

# Definisi graf
graph = {
    'A': {'B': 2, 'C': 4},      # Node A terhubung ke B dan C
    'B': {'A': 2, 'D': 4, 'E': 1},  # Node B terhubung ke A, D, dan E
    'C': {'A': 4, 'F': 3},      # Node C terhubung ke A dan F
    'D': {'B': 4, 'G': 2},      # Node D terhubung ke B dan G
    'E': {'B': 1, 'H': 4},      # Node E terhubung ke B dan H
    'F': {'C': 3, 'H': 2},      # Node F terhubung ke C dan H
    'G': {'D': 2, 'I': 3},      # Node G terhubung ke D dan I
    'H': {'E': 4, 'F': 2, 'I': 5},  # Node H terhubung ke E, F, dan I
    'I': {'G': 3, 'H': 5}       # Node I terhubung ke G dan H
}

def greedy_shortest_path(graph, start, end):
    visited = set()  # Set untuk menyimpan node yang sudah dikunjungi
    path = []  # List untuk menyimpan jalur yang dilalui
    total_distance = 0  # Variabel untuk menyimpan total jarak
    current_node = start  # Memulai dari node awal

    while current_node != end:  # Selama node saat ini bukan node tujuan
        visited.add(current_node)  # Tandai node saat ini sebagai sudah dikunjungi
        path.append(current_node)  # Tambahkan node saat ini ke jalur
        
        neighbors = graph[current_node]  # Ambil semua tetangga dari node saat ini
        next_node = None  # Node berikutnya yang akan dipilih
        min_distance = float('inf')  # Inisialisasi jarak minimum sebagai tak hingga

        # Iterasi melalui semua tetangga untuk menemukan node terdekat
        for neighbor, weight in neighbors.items():
            if neighbor not in visited:  # Hanya pertimbangkan tetangga yang belum dikunjungi
                if weight < min_distance or (neighbor == end):  # Tambahkan logika untuk memastikan kita bisa mencapai tujuan
                    next_node = neighbor  # Update node berikutnya
                    min_distance = weight  # Update jarak minimum

        if next_node is None:  # Jika tidak ada node berikutnya yang ditemukan
            return None, 0  # Tidak ada jalur yang ditemukan

        # Tambahkan jarak ke total
        total_distance += min_distance
        current_node = next_node  # Pindah ke node berikutnya

    path.append(end)  # Tambahkan node tujuan ke jalur
    return path, total_distance  # Kembalikan jalur yang ditemukan dan total jarak


# Mencari jalur terpendek dari A ke I menggunakan algoritma greedy
path, total_distance = greedy_shortest_path(graph, 'A', 'I')  # Memanggil fungsi dengan graf, node awal, dan node tujuan

# Menampilkan hasil
if path is not None:
    print("Jalur terpendek (Greedy):", path)
    print("Total panjang jarak:", total_distance)
else:
    print("Tidak ada jalur yang ditemukan.")

# Visualisasi graf dengan NetworkX dan Matplotlib
G = nx.Graph()

# Menambahkan edge ke graf
for node, neighbors in graph.items():
    for neighbor, weight in neighbors.items():
        G.add_edge(node, neighbor, weight=weight)

# Posisi node dalam bentuk layout circular
pos = nx.spring_layout(G)

# Menggambar graf
plt.figure(figsize=(8, 6))
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, font_size=10, font_weight='bold')

# Menggambar edge labels (jarak antar node)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Highlight jalur terpendek yang ditemukan
path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2)

plt.title("Visualisasi Jalur Terpendek (Greedy)")
plt.show()
