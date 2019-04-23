from matplotlib.lines import Line2D
from multiprocessing import Process
import matplotlib.pyplot as plt
import networkx as nx 
import matplotlib.animation
import matplotlib.markers as mrks
import random
import copy
import itertools
import player

class Simulation:
    def __init__(self, f, s, r, graph_type = "Regular", rows = -1, cols = -1, num_hubs = -1):
        self.G = None
        self.F = set([])
        self.owners_list = []
        self.collected = []
        self.path = []
        self.batch_nums = []
        self.fig, self.pos, self.ax = None, None, None
        self.ani_title = ""
        self.num_times = 0
        self.ani = None
        self.f = f
        self.s = s
        self.r = r
        self.graph_type = graph_type
        self.num_hubs = num_hubs
        if graph_type == "Regular":
            self.G = self.make_reg_graph(f, s, r)
        elif graph_type == "Euclidean":
            assert(s == rows * cols)
            self.G = nx.grid_2d_graph(rows, cols)
        elif graph_type == "Network":
            assert( num_hubs > 0 )
            # sequence = nx.generators.degree_seq.create_degree_sequence(s, nx.utils.powerlaw_sequence)
            # self.G = nx.configuration_model(sequence)
            assert( (3 * s) // num_hubs < s )
            # Check all combinations of feasible degrees to see if we can make a valid graph
            hub_degrees = range( (2 * s) // num_hubs, (3 * s) // num_hubs )
            non_hub_degrees = range( 1, 4 )
            for degree_seq in itertools.product( *[hub_degrees for _ in range(num_hubs)], *[non_hub_degrees for _ in range(s - num_hubs)] ):
                if sum(degree_seq) % 2 != 0:
                    continue
                G_curr = nx.configuration_model(degree_seq)
                if nx.is_connected(G_curr):
                    self.G = G_curr
                    break
            assert( self.G != None )
        self.F = set(random.sample(self.G.nodes, f))

    def make_reg_graph(self, f, s, r):
        G = nx.random_regular_graph(r, s)
        while not nx.is_connected(G):
            G = nx.random_regular_graph(r, s)
        return G

    def simulate_once(self, k, n, batch_num = 1):
        """
        Simulates the communication of a single block of k code bits made into n
        message bits through redundancy. This is done on an r-regular graph of size
        s, in which we have f friends that act as people to which we can possibly send
        a message.
        """
        assert(k <= n <= self.f <= self.s)
        bit_owners = set([])
        # Disseminate
        time_elapsed = 0
        num_distributed = 0
        curr_index = random.choice(list(self.G.nodes))
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
        curr_index = random.choice(list(self.G.nodes))
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
        blocks of k code bits made into n
        message bits through redundancy. This is done on an r-regular graph of size
        s, in which we have f friends to which we can possibly send a message.
        """
        assert(k <= m)
        self.num_times = m // k
        return sum([self.simulate_once(k, n, batch_num=i + 1) for i in range(self.num_times)])

    def animate(self, m, k, n, repeat):
        self.fig, self.ax = plt.subplots()
        if self.graph_type == "Regular":
            self.pos = nx.circular_layout(self.G)
        elif self.graph_type == "Euclidean":
            self.pos = nx.spectral_layout(self.G)
        elif self.graph_type == "Network":
            self.pos = nx.spring_layout(self.G)
        self.ani_title = f'k = {k}, n = {n}, f = {self.f}, s = {self.s}, m = {m}, r = {self.r}'
        update_func = self.canvas_update_closure()
        # self.ani = matplotlib.animation.FuncAnimation(self.fig, update_func, frames=len(self.owners_list), interval=update_interval, repeat=repeat)
        self.ani = player.Player(
            self.fig, 
            update_func, 
            frames=len(self.owners_list), 
            repeat=repeat,
            maxi = len(self.owners_list) - 1
        )
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        plt.show()

    def canvas_update_closure(self):
        def closure(i):
            curr_owners = self.owners_list[i]
            stage, curr_node = self.path[i]
            prev_stage, prev_node = self.path[i - 1] if i > 0 else (None, None)
            reg_color = "white"
            friend_color = "yellow"
            owner_color = "red"
            disseminate_color = "blue"
            collect_color = "purple"
            collected_color = "orange"
            path_color = disseminate_color if stage == "disseminate" else collect_color
            handles = [Line2D([0], [0], color=color, lw=4) for color in (reg_color, friend_color, owner_color, collected_color, disseminate_color, collect_color)]
            labels = ["Other", "Friends", "Bit Owners", "Collected Bits", "Disseminator", "Collector"]
            other_nodes = set(self.G.nodes()) - set(self.F)
            if prev_stage == "collect" and stage == "disseminate":
                self.collected = []
            if i >= 1:
                prev_owners = self.owners_list[i - 1]
                if curr_node not in curr_owners and curr_node in prev_owners:
                    self.collected.append(curr_node)
            self.ax.clear()
            nx.draw_networkx_edges(self.G, pos=self.pos, edge_color="black", ax=self.ax)
            if prev_stage == stage and prev_node is not None:
                nx.draw_networkx_edges(self.G, pos=self.pos, edgelist = [(prev_node, curr_node)], edge_color=path_color, ax=self.ax, width = 3.0)
            nx.draw_networkx_nodes(self.G, pos=self.pos, nodelist=other_nodes, node_color=reg_color, ax=self.ax, linewidths=1.5, edgecolors="black")
            nx.draw_networkx_nodes(self.G, pos=self.pos, nodelist=self.F, node_color=friend_color, ax=self.ax)
            nx.draw_networkx_nodes(self.G, pos=self.pos, nodelist=curr_owners, node_color=owner_color, ax=self.ax)
            nx.draw_networkx_nodes(self.G, pos=self.pos, nodelist=self.collected, node_color=collected_color, ax=self.ax)
            nx.draw_networkx_nodes(self.G, pos=self.pos, nodelist=[curr_node], node_color=path_color, ax=self.ax)
            plt.axis('off')
            self.ax.set_title(self.ani_title + f' (batch {self.batch_nums[i]}/{self.num_times}, t = {i + 1})')
            self.ax.legend(handles, labels)
        return closure
    
def simulate_once(self, k, n, f, s, r, graph_type = "Regular", rows = 0, cols = 0, num_hubs = -1):
    simul = Simulation(f, s, r, graph_type = graph_type, rows = rows, cols = cols, num_hubs = num_hubs)
    return simul.simulate_once(k, n)

def simulate(m, k, n, f, s, r, graph_type = "Regular", rows = 0, cols = 0, num_hubs = -1):
    simul = Simulation(f, s, r, graph_type = graph_type, rows = rows, cols = cols, num_hubs = num_hubs)
    return simul.simulate(m, k, n)

def animate(m, k, n, f, s, r, repeat = False, graph_type = "Regular", rows = 0, cols = 0, num_hubs = -1):
    simul = Simulation(f, s, r, graph_type = graph_type, rows = rows, cols = cols, num_hubs=num_hubs)
    simul.simulate(m, k, n)
    p = Process(target=simul.animate, args=(m, k, n, repeat))
    p.start()
    # simul.animate(m, k, n, repeat)

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

def run_animation_euclidean():
    k = 5
    n = 10
    m = 10
    f = 20
    s = 25
    r = 10
    graph_type = "Euclidean"
    rows = 5
    cols = 5
    animate(m, k, n, f, s, r, graph_type=graph_type, rows=rows, cols=cols)

def run_animation_network():
    k = 5
    n = 10
    m = 10
    f = 20
    s = 25
    r = 10
    graph_type = "Network"
    num_hubs = 4
    animate(m, k, n, f, s, r, graph_type=graph_type, num_hubs=num_hubs)

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
    # run_animation()
    # run_animation_euclidean()
    run_animation_network()
    # run_animations()