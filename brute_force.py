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

# Fungsi untuk menghitung jarak total dari suatu jalur
def calculate_path_distance(path):
    total_distance = 0  # Inisialisasi total jarak menjadi nol
    for i in range(len(path) - 1):  # Loop melalui jalur
        total_distance += graph[path[i]].get(path[i + 1], float('inf'))  # Tambahkan jarak ke node berikutnya
    return total_distance  # Kembalikan total jarak dari jalur

# Fungsi untuk menemukan jalur terpendek dan semua jalur
def find_shortest_path(start, end):
    shortest_path = None  # Inisialisasi jalur terpendek menjadi None
    min_distance = float('inf')  # Inisialisasi jarak minimum menjadi tak terhingga
    all_paths = []  # Daftar untuk menyimpan semua jalur yang ditemukan

    # Fungsi rekursif untuk menghasilkan semua jalur
    def generate_paths(current_path):
        nonlocal shortest_path, min_distance  # Memungkinkan akses ke variabel dari fungsi luar
        current_node = current_path[-1]  # Ambil node terakhir dalam jalur saat ini

        if current_node == end:  # Periksa jika node terakhir adalah node tujuan
            current_distance = calculate_path_distance(current_path)  # Hitung jarak jalur saat ini
            all_paths.append((list(current_path), current_distance))  # Simpan jalur yang ditemukan dan jaraknya
            if current_distance < min_distance:  # Periksa jika ini adalah jalur terpendek yang ditemukan
                min_distance = current_distance  # Perbarui jarak minimum
                shortest_path = list(current_path)  # Perbarui jalur terpendek
            return  # Keluar dari fungsi

        for neighbor in graph[current_node]:  # Loop melalui tetangga dari node saat ini
            if neighbor not in current_path:  # Periksa untuk menghindari siklus dalam jalur
                current_path.append(neighbor)  # Tambahkan tetangga ke jalur saat ini
                generate_paths(current_path)  # Rekursi dengan jalur baru
                current_path.pop()  # Mundur dengan menghapus node terakhir

    # Mulai pembuatan jalur dari node awal
    generate_paths([start])  # Mulai pencarian rekursif dari node awal

    return shortest_path, min_distance, all_paths  # Kembalikan jalur terpendek, jaraknya, dan semua jalur yang ditemukan

# Fungsi untuk menggambar graf dengan NetworkX dan matplotlib
def draw_graph(graph, shortest_path, all_paths):
    G = nx.Graph()

    # Menambahkan edge ke graf
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            G.add_edge(node, neighbor, weight=weight)

    # Menggunakan circular layout agar posisi node tetap
    pos = nx.circular_layout(G)

    # Menggambar graf
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, font_size=12, font_weight='bold')

    # Menggambar edge labels (jarak antar node)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Highlight semua jalur yang ditemukan
    for path, _ in all_paths:
        path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='gray', width=1, style='dashed')

    # Highlight jalur terpendek yang ditemukan
    if shortest_path:
        path_edges = [(shortest_path[i], shortest_path[i+1]) for i in range(len(shortest_path)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)

    plt.title("Visualisasi Jalur Terpendek dan Semua Jalur yang Ditemukan")
    plt.show()

# Contoh penggunaan
start_node = 'A'  # Tentukan node awal
end_node = 'I'  # Tentukan node tujuan
shortest_path, min_distance, all_paths = find_shortest_path(start_node, end_node)  # Temukan jalur terpendek

# Menampilkan hasil
print("\nSemua jalur yang ditemukan:")  # Cetak header untuk semua jalur
for path, distance in all_paths:  # Loop melalui semua jalur yang ditemukan
    print(f"Jalur: {path}, Jarak: {distance}")  # Cetak setiap jalur dan jaraknya

print(f'Jalur terpendek dari {start_node} ke {end_node}: {shortest_path} dengan jarak {min_distance}')  # Cetak jalur terpendek dan jaraknya

# Memanggil fungsi untuk menggambar graf
draw_graph(graph, shortest_path, all_paths)
