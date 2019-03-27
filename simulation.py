from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import networkx as nx 
import matplotlib.animation
import random
import copy

G = None
F = set([])
owners_list = []
path = []
batch_nums = []
fig, pos, ax = None, None, None
ani_title = ""
num_times = 0
ani = None

def make_reg_graph(f, s, r):
    global G, F
    G = nx.random_regular_graph(r, s)
    while not nx.is_connected(G):
        G = nx.random_regular_graph(r, s)
    F = set(random.sample(range(s), f))

def simulate_once(k, n, f, s, r, make_graph = True, batch_num = 1):
    """
    Simulates the communication of a single block of n code bits made into k
    message bits through redundancy. This is done on an r-regular graph of size
    s, in which we have f friends that act as people to which we can possibly send
    a message.
    """
    global G, F, owners_list, path
    assert(k <= n <= f <= s)
    if make_graph:
        make_reg_graph(f, s, r)
    bit_owners = set([])
    # Disseminate
    time_elapsed = 0
    num_distributed = 0
    curr_index = random.randint(0, s - 1)
    while num_distributed < n:
        if curr_index in F and curr_index not in bit_owners:
            num_distributed += 1
            bit_owners.add(curr_index)
        owners_list.append(copy.deepcopy(bit_owners))
        path.append( ("disseminate", curr_index) )
        batch_nums.append(batch_num)
        time_elapsed += 1
        curr_index = random.choice(list(G.adj[curr_index]))
    # Collect
    num_collected = 0
    curr_index = random.randint(0, s - 1)
    while num_collected < k:
        if curr_index in bit_owners:
            num_collected += 1
            bit_owners.remove(curr_index)
        owners_list.append(copy.deepcopy(bit_owners))
        path.append( ("collect", curr_index) )
        batch_nums.append(batch_num)
        time_elapsed += 1
        curr_index = random.choice(list(G.adj[curr_index]))
    return time_elapsed

def simulate(m, k, n, f, s, r):
    """
    Simulates the communication of a message of size m through sending
    blocks of n code bits made into k
    message bits through redundancy. This is done on an r-regular graph of size
    s, in which we have f friends to which we can possibly send a message.
    """
    global num_times
    make_reg_graph(f, s, r)
    num_times = m // k
    return sum([simulate_once(k, n, f, s, r, make_graph=False, batch_num=i + 1) for i in range(num_times)])

def update_canvas(i):
    curr_owners = owners_list[i]
    stage, curr_node = path[i]
    reg_color = "yellow"
    friend_color = "green"
    owner_color = "red"
    disseminate_color = "blue"
    collect_color = "purple"
    path_color = disseminate_color if stage == "disseminate" else collect_color
    handles = [Line2D([0], [0], color=color, lw=4) for color in (reg_color, friend_color, owner_color, disseminate_color, collect_color)]
    labels = ["Other", "Friends", "Bit Owners", "Disseminator", "Collector"]
    ax.clear()
    nx.draw_networkx_edges(G, pos=pos, edge_color="black", ax=ax)
    nx.draw_networkx_nodes(G, pos=pos, nodelist=G.nodes(), node_color=reg_color, ax=ax)
    nx.draw_networkx_nodes(G, pos=pos, nodelist=F, node_color=friend_color, ax=ax)
    nx.draw_networkx_nodes(G, pos=pos, nodelist=curr_owners, node_color=owner_color, ax=ax)
    nx.draw_networkx_nodes(G, pos=pos, nodelist=[curr_node], node_color=path_color, ax=ax)
    ax.set_title(ani_title + f' (batch {batch_nums[i]}/{num_times}, t = {i + 1})')
    ax.legend(handles, labels)

def animate(m, k, n, f, s, r):  
    global fig, pos, ax, ani, ani_title
    simulate(m, k, n, f, s, r)
    fig, ax = plt.subplots()
    pos = nx.spring_layout(G)
    ani_title = f'k = {k}, n = {n}, f = {f}, s = {s}, m = {m}, r = {r}'
    ani = matplotlib.animation.FuncAnimation(fig, update_canvas, frames=len(owners_list), interval=500, repeat=False)
    plt.show()

def run_sims():
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

def run_animation():
    k = 5
    n = 10
    m = 10
    f = 20
    s = 30
    r = 10
    animate(m, k, n, f, s, r)

if __name__ == "__main__":
    # run_sims()
    run_animation()