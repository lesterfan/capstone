from matplotlib.lines import Line2D
from multiprocessing import Process
import matplotlib.pyplot as plt
import networkx as nx 
import matplotlib.animation
import matplotlib.markers as mrks
import random
import copy
import player

class Simulation:
    def __init__(self, f, s, r):
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
        assert(k <= m)
        self.num_times = m // k
        return sum([self.simulate_once(k, n, batch_num=i + 1) for i in range(self.num_times)])

    def animate(self, m, k, n, repeat):
        self.fig, self.ax = plt.subplots()
        self.pos = nx.circular_layout(self.G)
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
    
def simulate_once(self, k, n, f, s, r):
    simul = Simulation(f, s, r)
    return simul.simulate_once(k, n)

def simulate(m, k, n, f, s, r):
    simul = Simulation(f, s, r)
    return simul.simulate(m, k, n)

def animate(m, k, n, f, s, r, repeat = False):
    simul = Simulation(f, s, r)
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