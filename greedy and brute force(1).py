import networkx as nx
import matplotlib.pyplot as plt

# Definisi graf
graph = {
    'Atambua': {'Labuan Bajo': 2, 'Bea': 4},      # Atambua
    'Labuan Bajo': {'Atambua': 2, 'Maumere': 4, 'Tambolaka': 1},  # Labuan Bajo
    'Bea': {'Atambua': 4, 'Waingapu': 3},      # Bea
    'Maumere': {'Labuan Bajo': 4, 'Ruteng': 2},      # Maumere
    'Tambolaka': {'Labuan Bajo': 1, 'Lewoleba': 4},      # Tambolaka
    'Waingapu': {'Bea': 3, 'Lewoleba': 2},      # Waingapu
    'Ruteng': {'Maumere': 2, 'Kalabahi': 3},      # Ruteng
    'Lewoleba': {'Tambolaka': 4, 'Waingapu': 2, 'Kalabahi': 5},  # Lewoleba
    'Kalabahi': {'Ruteng': 3, 'Lewoleba': 5}       # Kalabahi
}

############################################################################ Menggunakan algoritma Greedy#############################################################################

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
path, total_distance = greedy_shortest_path(graph, 'Atambua', 'Kalabahi')  # Memanggil fungsi dengan graf, node awal, dan node tujuan

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
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=4100, font_size=10, font_weight='bold')

# Menggambar edge labels (jarak antar node)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Highlight jalur terpendek yang ditemukan
path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2)

plt.title("Visualisasi Jalur Terpendek (Greedy)")
plt.show()

############################################################################## Meggunakan Algoritma Brute Force ####################################################################
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
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=4100, font_size=10, font_weight='bold')

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
start_node = 'Atambua'  # Tentukan node awal
end_node = 'Kalabahi'  # Tentukan node tujuan
shortest_path, min_distance, all_paths = find_shortest_path(start_node, end_node)  # Temukan jalur terpendek

# Menampilkan hasil
print("\nSemua jalur yang ditemukan:")  # Cetak header untuk semua jalur
for path, distance in all_paths:  # Loop melalui semua jalur yang ditemukan
    print(f"Jalur: {path}, Jarak: {distance}")  # Cetak setiap jalur dan jaraknya

print(f'Jalur terpendek (brute force) dari {start_node} ke {end_node}: {shortest_path} dengan jarak {min_distance}')  # Cetak jalur terpendek dan jaraknya

# Memanggil fungsi untuk menggambar graf
draw_graph(graph, shortest_path, all_paths)
