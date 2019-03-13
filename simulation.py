import networkx as nx 
import random

def make_regular_graph(s, r):
    """
    Makes a r-regular graph of size s.
    Follows the answer given in:
    https://math.stackexchange.com/questions/142112/how-to-construct-a-k-regular-graph
    """
    assert( r <= s and (r % 2 == 0 or s % 2 == 0) )
    G = nx.Graph()
    for i in range(s):
        G.add_node(i, has_bit = False)
    # Arrange vertices around in a circle, and join each to its r//2 nearest neighbors.
    for i in range(s):
        for offset in range(-(r//2), r//2 + 1):
            if offset == 0:
                continue
            j = (i + offset) % s
            G.add_edge(i, j)
    # If r is odd, also connect each vertex to the one directly opposite it.
    if r % 2 != 0:
        for i in range(s):
            j = (i + (s // 2)) % s
            G.add_edge(i, j)
    # print(f'Here are the degrees of all the vertices: {[len(G.adj[x]) for x in range(s)]}')
    return G

def simulate_once(k, n, f, s, r):
    """
    Simulates the communication of a single block of n code bits made into k
    message bits through redundancy. This is done on an r-regular graph of size
    s, in which we have f friends that act as people to which we can possibly send
    a message.
    """
    assert(k <= n <= f <= s)
    # Make a random r-regular graph of size s
    G = make_regular_graph(s, r)
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
    r = 14
    for i in range(len(ks)):
        k, n = ks[i], ns[i]
        total_time = simulate(m, k, n, f, s, r)
        print(f'For k = {k}, n = {n}, f = {f}, s = {s}, m = {m}, total_time = {total_time}')

