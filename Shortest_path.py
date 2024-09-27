

import networkx as nx
import matplotlib.pyplot as plt #import untuk generate grafik

# Fungsi untuk mencari semua jalur dari A ke K menggunakan brute force
def find_all_paths(graph, start, end, path=[]):#(fungsi ini nantinya mengambil grafik, node awal, node akhir, dan list untuk menyimpan current path)
    path = path + [start] #(Menambahkan node awal ke jalur yang sedang dibangun.)
    if start == end:
        return [path]#(Memeriksa apakah node awal sama dengan node akhir. Jika sama, fungsi ini mengembalikan jalur saat ini dalam bentuk daftar.)
    if start not in graph:
        return [] #(Memeriksa apakah node awal ada dalam graf. Jika tidak, mengembalikan daftar kosong, yang menunjukkan bahwa tidak ada jalur yang dapat ditemukan.)
    paths = [] #(membuat list kosong utk menyimpan jalur yang valid dari start ke end)
    for node in graph[start]:#(Mengiterasi melalui setiap tetangga dari node awal dalam graf.)
        if node not in path:  # Hindari siklus
            new_paths = find_all_paths(graph, node, end, path)#(memanggil fungsi find_all_paths)
            for new_path in new_paths:
                paths.append(new_path) #(ditambahkan ke dalam daftar paths)
    return paths

# Fungsi untuk menghitung panjang jalur
def calculate_path_length(graph, path):
    length = 0 #(total panjang jalur)
    for i in range(len(path) - 1): #(Mengiterasi melalui setiap node dalam jalur, berhenti sebelum node terakhir.)
        length += graph[path[i]][path[i+1]]
    return length#(Menambahkan jarak antara node yang berurutan dalam jalur ke total panjang.)

# Fungsi untuk menemukan jalur terpendek menggunakan greedy dari hasil brute force
def greedy_choose_shortest_path(all_paths, graph):
    shortest_path = None
    shortest_distance = float('inf')#(Menginisialisasi variabel: shortest_path untuk menyimpan jalur terbaik yang ditemukan dan shortest_distance ke angka yang sangat besar (tak terhingga) untuk memastikan jalur yang ditemukan lebih pendek.)

    # Loop melalui semua jalur
    for path in all_paths:
        total_distance = calculate_path_length(graph, path) #(menghitung total jarak dgn fungsi yang dipanggil)

        # Greedy: Pilih jalur dengan jarak total terpendek
        if total_distance < shortest_distance: #(algoritma greedy untuk mencari jarak terpendek dan mengembalikan jalur serta jaraknya)
            shortest_distance = total_distance
            shortest_path = path

    return shortest_path, shortest_distance

# Fungsi untuk memvisualisasikan graf dan jalur terpendek
def visualize_graph(graph, shortest_path=None):
    G = nx.Graph()#(membuat graph baru dengan nama G mengguakan networkX)

    # Tambahkan edge ke graf
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            G.add_edge(node, neighbor, weight=weight)#(menambahkan edge ke graf)

    pos = nx.spring_layout(G)  # Tata letak graf
    edges = G.edges(data=True)
    edge_labels = {(u, v): f'{d["weight"]}' for u, v, d in edges}#(Mengambil edge beserta bobotnya dan membuat kamus untuk label edge.)

    # Gambar node dan edges
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=3000, font_size=14, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10) #(menggambar graf)

    if shortest_path:
        # Highlight jalur terpendek
        path_edges = [(shortest_path[i], shortest_path[i+1]) for i in range(len(shortest_path)-1)]#(memeriksa apkh ada jalur terpendek utk divisualisasikan)
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2.5)

    plt.title("Graph Visualization with Shortest Path")
    plt.show()#(ngasih judul)

# Definisi graf
# Contoh graf (graph)
graph = {
    'A': {'B': 5, 'C': 3.8, 'D': 7},
    'B': {'A': 5, 'F': 6, 'H': 9.4},
    'C': {'A': 3.8, 'F': 4},
    'D': {'A': 7, 'E': 2, 'G': 5},
    'E': {'D': 2, 'G': 14, 'L': 17},
    'F': {'B': 6, 'C': 4, 'G': 3, 'H': 7, 'I': 9},
    'G': {'D': 5, 'E': 14, 'F': 3, 'J': 6},
    'H': {'B': 9.4, 'F': 7, 'K': 24},
    'I': {'F': 9, 'J': 4, 'K': 29, 'L': 5},
    'J': {'G': 6, 'I': 4},
    'K': {'H': 24, 'I': 29, 'L': 8},
    'L': {'E': 17, 'I': 5, 'K': 8}
}
# Cari semua jalur dari A ke K (brute force)
all_paths = find_all_paths(graph, 'A', 'K')

# Pilih jalur terpendek menggunakan greedy dari hasil brute force
shortest_path, shortest_distance = greedy_choose_shortest_path(all_paths, graph)

# Tampilkan hasil
print("Jalur terpendek:", shortest_path, "dengan panjang:", shortest_distance)

# Visualisasikan graf dan jalur terpendek
visualize_graph(graph, shortest_path)
