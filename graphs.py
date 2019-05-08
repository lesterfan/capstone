import simulation
import sys
import numpy as np
import matplotlib.pyplot as plt

def simulateN(m, k, n, f, s, r, N):
    """
    Compute the N simulations given the parameters m, k, n, f, s, r
    and return the average result
    """
    totalTime = 0  
    for i in range(0, N):
        totalTime = totalTime + simulation.simulate(m, k, n, f, s, r)  
    return totalTime      

if __name__ == "__main__":

    m = 100  
    f = 20  
    s = 30  
    r = 29  
    
    N = 50  
    
    # sys.stdout = open("sim1.txt","w")  
    # for k in range(1, f+1):
        # for n in range(k, f+1):
            # currTime = simulateN(m, k, n, f, s, r, N)  
            # print(currTime,end=" ",flush=True)  
        # print("")  
        
    vals = []  
    count = 0  
    with open("sim1.txt") as file:
        for line in file:
            count += 1  
            int_list = ([0]*count) + [int(x) for x in line.split()]  
            vals.append(int_list)  
    vals = np.asarray(vals).reshape((f,f+1))  
    # print(vals)  
    
    contarr=np.arange(600,1400,20)  
    X,Y = np.meshgrid(range(f+1),range(f))  
    fig,ax = plt.subplots()
    CS = ax.contourf(X,Y,vals/50,contarr,cmap='summer',extend='max')  
    # ax.set_title('Delay Time vs. Coding Parameters {n,k}')  
    ax.set_xlabel('n')  
    ax.set_ylabel('k')  
    tick_location = np.linspace(0.01, 20, num=5, endpoint=True)
    ax.set_xticks(tick_location)
    tick_labels = [0,5,10,15,20]
    ax.set_xticklabels(tick_labels)
    ax.set_yticks(tick_location)
    ax.set_yticklabels(tick_labels)
    fig.colorbar(CS)  
    plt.show()  