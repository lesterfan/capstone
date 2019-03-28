from matplotlib.lines import Line2D
from multiprocessing import Process
import matplotlib.pyplot as plt
import networkx as nx 
import matplotlib.animation
import random
import copy

class Simulation:
    def __init__(self, f, s, r):
        self.G = None
        self.F = set([])
        self.owners_list = []
        self.path = []
        self.batch_nums = []
        self.fig, self.pos, self.ax = None, None, None
        self.ani_title = ""
        self.num_times = 0
        self.ani = None
        self.f = f
        self.s = s
        self.r = r
        self.make_reg_graph(f, s, r)

    def make_reg_graph(self, f, s, r):
        self.G = nx.random_regular_graph(r, s)
        while not nx.is_connected(self.G):
            self.G = nx.random_regular_graph(r, s)
        self.F = set(random.sample(range(s), f))

    def simulate_once(self, k, n, batch_num = 1):
        """
        Simulates the communication of a single block of n code bits made into k
        message bits through redundancy. This is done on an r-regular graph of size
        s, in which we have f friends that act as people to which we can possibly send
        a message.
        """
        assert(k <= n <= self.f <= self.s)
        bit_owners = set([])
        # Disseminate
        time_elapsed = 0
        num_distributed = 0
        curr_index = random.randint(0, self.s - 1)
        while num_distributed < n:
            if curr_index in self.F and curr_index not in bit_owners:
                num_distributed += 1
                bit_owners.add(curr_index)
            self.owners_list.append(copy.deepcopy(bit_owners))
            self.path.append( ("disseminate", curr_index) )
            self.batch_nums.append(batch_num)
            time_elapsed += 1
            curr_index = random.choice(list(self.G.adj[curr_index]))
        # Collect
        num_collected = 0
        curr_index = random.randint(0, self.s - 1)
        while num_collected < k:
            if curr_index in bit_owners:
                num_collected += 1
                bit_owners.remove(curr_index)
            self.owners_list.append(copy.deepcopy(bit_owners))
            self.path.append( ("collect", curr_index) )
            self.batch_nums.append(batch_num)
            time_elapsed += 1
            curr_index = random.choice(list(self.G.adj[curr_index]))
        return time_elapsed

    def simulate(self, m, k, n):
        """
        Simulates the communication of a message of size m through sending
        blocks of n code bits made into k
        message bits through redundancy. This is done on an r-regular graph of size
        s, in which we have f friends to which we can possibly send a message.
        """
        self.num_times = m // k
        return sum([self.simulate_once(k, n, batch_num=i + 1) for i in range(self.num_times)])

def update_canvas(sim_obj):
    def closure(i):
        curr_owners = sim_obj.owners_list[i]
        stage, curr_node = sim_obj.path[i]
        reg_color = "yellow"
        friend_color = "green"
        owner_color = "red"
        disseminate_color = "blue"
        collect_color = "purple"
        path_color = disseminate_color if stage == "disseminate" else collect_color
        handles = [Line2D([0], [0], color=color, lw=4) for color in (reg_color, friend_color, owner_color, disseminate_color, collect_color)]
        labels = ["Other", "Friends", "Bit Owners", "Disseminator", "Collector"]
        sim_obj.ax.clear()
        nx.draw_networkx_edges(sim_obj.G, pos=sim_obj.pos, edge_color="black", ax=sim_obj.ax)
        nx.draw_networkx_nodes(sim_obj.G, pos=sim_obj.pos, nodelist=sim_obj.G.nodes(), node_color=reg_color, ax=sim_obj.ax)
        nx.draw_networkx_nodes(sim_obj.G, pos=sim_obj.pos, nodelist=sim_obj.F, node_color=friend_color, ax=sim_obj.ax)
        nx.draw_networkx_nodes(sim_obj.G, pos=sim_obj.pos, nodelist=curr_owners, node_color=owner_color, ax=sim_obj.ax)
        nx.draw_networkx_nodes(sim_obj.G, pos=sim_obj.pos, nodelist=[curr_node], node_color=path_color, ax=sim_obj.ax)
        plt.axis('off')
        sim_obj.ax.set_title(sim_obj.ani_title + f' (batch {sim_obj.batch_nums[i]}/{sim_obj.num_times}, t = {i + 1})')
        sim_obj.ax.legend(handles, labels)
    return closure
    
def simulate_once(self, k, n, f, s, r):
    simul = Simulation(f, s, r)
    return simul.simulate_once(k, n)

def simulate(m, k, n, f, s, r):
    simul = Simulation(f, s, r)
    return simul.simulate(m, k, n)

def raw_animate(m, k, n, f, s, r, update_interval, repeat):  
    simul = Simulation(f, s, r)
    simul.simulate(m, k, n)
    simul.fig, simul.ax = plt.subplots()
    simul.pos = nx.circular_layout(simul.G)
    simul.ani_title = f'k = {k}, n = {n}, f = {f}, s = {s}, m = {m}, r = {r}'
    update_func = update_canvas(simul)
    simul.ani = matplotlib.animation.FuncAnimation(simul.fig, update_func, frames=len(simul.owners_list), interval=update_interval, repeat=repeat)
    plt.show()

def animate(m, k, n, f, s, r, update_interval = 500, repeat = False):
    p = Process(target=raw_animate, args=(m, k, n, f, s, r, update_interval, repeat))
    p.start()

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
    animate(m, k, n, f, s, r, update_interval=500)

def run_animations():
    ks = [5, 10]
    ns = [10, 14]
    m = 10
    f = 20
    s = 30
    r = 10
    for i in range(len(ks)):
        k, n = ks[i], ns[i]
        animate(m, k, n, f, s, r)

if __name__ == "__main__":
    # run_sims()
    run_animation()
    # run_animations()