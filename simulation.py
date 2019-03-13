import networkx as nx 
import random

def simulate_once(k, n, f, s):
    assert(k <= n <= f <= s)
    # Make an undirected, connected graph of size s
    G = nx.Graph()
    for i in range(s):
        G.add_node(i, has_bit = False)
    for i in range(s):
        for j in range(i + 1, s):
            G.add_edge(i, j)
    time_elapsed = 0
    # Disseminate
    F = set(random.sample(range(s), f))
    num_distributed = 0
    curr_index = random.randint(0, s - 1)
    while num_distributed < n:
        if curr_index in F and G.nodes[curr_index]['has_bit'] == False:
            num_distributed += 1
            G.nodes[curr_index]['has_bit'] = True
        curr_index = random.choice(list(G.adj[curr_index]))
        time_elapsed += 1
    # Collect
    num_collected = 0
    curr_index = random.randint(0, s - 1)
    while num_collected < k:
        if G.nodes[curr_index]['has_bit'] == True:
            num_collected += 1
            G.nodes[curr_index]['has_bit'] = False
        curr_index = random.choice(list(G.adj[curr_index]))
        time_elapsed += 1
    return time_elapsed

if __name__ == "__main__":
    ks = [5, 10, 10, 10, 9, 11]
    ns = [10, 14, 13, 15, 14, 14]
    m = 1000
    f = 20
    s = 30
    for i in range(len(ks)):
        k, n = ks[i], ns[i]
        num_times = int(m/k)
        total_time = sum([simulate_once(k, n, f, s) for _ in range(num_times)])
        print(f'For k = {k}, n = {n}, f = {f}, s = {s}, m = {m}, total_time = {total_time}')
    

