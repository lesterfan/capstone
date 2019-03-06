import networkx as nx 
import random

def simulate_once(k, m, f, s):
    assert(k <= m <= f <= s)
    # Make an undirected, connected graph of size s
    G = nx.Graph()
    for i in range(s):
        G.add_node(i, has_bit = False)
    for i in range(s):
        for j in range(i + 1, s):
            G.add_edge(i, j)
    # Disseminate
    F = random.sample(range(s), f)
    for i in random.sample(F, m):
        G.nodes[i]['has_bit'] = True
    # Collect
    num_collected = 0
    curr_index = random.randint(0, s - 1)
    time_elapsed = 0
    while num_collected < k:
        if G.nodes[curr_index]['has_bit'] == True:
            num_collected += 1
            G.nodes[curr_index]['has_bit'] = False
        curr_index = random.choice(list(G.adj[curr_index]))
        time_elapsed += 1
    return time_elapsed

if __name__ == "__main__":
    num_times = 30
    k = 5
    m = 10
    f = 20
    s = 30
    for i in range(num_times):
        print(simulate_once(k, m, f, s))
    