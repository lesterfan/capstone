import networkx as nx 
import random

def simulate_once(k, n, f, s, r):
    """
    Simulates the communication of a single block of n code bits made into k
    message bits through redundancy. This is done on an r-regular graph of size
    s, in which we have f friends that act as people to which we can possibly send
    a message.
    """
    assert(k <= n <= f <= s)
    # Make a random connected r-regular graph of size s
    G = nx.random_regular_graph(r, s)
    while not nx.is_connected(G):
        G = nx.random_regular_graph(r, s)
    for i in range(s):
        G.node[i]['has_bit'] = False
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

def simulate(m, k, n, f, s, r):
    """
    Simulates the communication of a message of size m through sending
    blocks of n code bits made into k
    message bits through redundancy. This is done on an r-regular graph of size
    s, in which we have f friends to which we can possibly send a message.
    """
    num_times = m // k
    return sum([simulate_once(k, n, f, s, r) for _ in range(num_times)])

if __name__ == "__main__":
    ks = [5, 10, 10, 10, 9, 11]
    ns = [10, 14, 13, 15, 14, 14]
    m = 1000
    f = 20
    s = 30
    r = 10
    for i in range(len(ks)):
        k, n = ks[i], ns[i]
        total_time = simulate(m, k, n, f, s, r)
        print(f'For k = {k}, n = {n}, f = {f}, s = {s}, m = {m}, r = {r}, total_time = {total_time}')

