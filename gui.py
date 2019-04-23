from tkinter import *
import simulation
import traceback
from functools import partial

# TODO
# Add dropdown for either 1. regular 2. Euclidean (need rows/cols)

# Page that allows for simulating/animating graph given parameters
def loadSimPage(window):
    # Clear
    clearWindow(window)

    # Prompt to enter parameters
    explainWidth=50
    lbl = Label(window, text="Enter parameters below")
    i = 0
    lbl.grid(column=0, row=i)

    explainLbl = Label(window, width=explainWidth, text="What are these?", anchor="w")
    explainLbl.grid(column=2, row=i)

    # Parameters and default values
    paramArr = ["m", "k", "n", "f", "s", "r", # parameters shared among all graphs
                "rows", "cols", # parameters present in only Euclidean
                "num_hubs" # parameters present in only network graph
                ]
    indOfEuc = 6
    indOfHub = 8
    defVals = [10, 5, 10, 20, 30, 10, 1, 1, 1]
    textArr = ["Message length",
               "Number of message bits in each block",
               "Size of codeword after adding redundancy",
               "Number of friends on graph that may hold bits",
               "Size/number of nodes on graph",
               "Degree of each node (only in Regular graphs)",
               "Number of rows (only in Euclidean graphs)",
               "Number of columns (only in Euclidean graphs)",
               "Number of hubs (only in Network graphs)"]

    # Set up area to enter info
    entrySpace = []
    entryLabels = []
    explainLabels = []
    i += 1
    entryWidth = 10
    count = 0

    for p in paramArr:
        entryLabel = Label(window, text=p + ": ")
        entryLabel.grid(column=0, row=i)
        currEntry = Entry(window, width=entryWidth)
        currEntry.insert(END, defVals[count])
        currEntry.grid(column=1, row=i)
        explainLabel = Label(window, text=textArr[count], width=explainWidth, anchor="w")
        explainLabel.grid(column=2, row=i)

        i += 1
        count += 1
        entrySpace.append(currEntry)
        entryLabels.append(entryLabel)
        explainLabels.append(explainLabel)

    # clickedLabel - displays results
    clickedLabel = Label(window,
                         text="Default values provided- either run animation or find the time taken to simulate")
    animTextPre = "Running animation on the given parameters..."
    animTextPost = "Running animation on parameters- check other window"
    timeTextPre = "Finding the time taken on the given parameters..."
    timeTextPost = "Time required to run simulation on given parameters: "

    # Perform animation on the given parameters
    def clickedAnimation():
        try:
            currType = graphOptionVal.get()
            vals = [int(entry.get()) for entry in entrySpace]
            m, k, n, f, s, r, rows, cols, num_hubs = vals
            clickedLabel.configure(text=animTextPre)
            simulation.animate(m, k, n, f, s, r, graph_type = currType, rows = rows, cols = cols, num_hubs=num_hubs)
            clickedLabel.configure(text=animTextPost)
        except Exception as error:
            clickedLabel.configure(text=traceback.format_exc())

    # Perform simulation (find time only) on the given parameters
    def clickedTime():
        try:
            currType = graphOptionVal.get()
            vals = [int(entry.get()) for entry in entrySpace]
            m, k, n, f, s, r, rows, cols, num_hubs = vals
            clickedLabel.configure(text=timeTextPre)
            time = simulation.simulate(m, k, n, f, s, r, graph_type = currType, rows = rows, cols = cols, num_hubs=num_hubs)
            clickedLabel.configure(text=timeTextPost + str(time))
        except Exception as error:
            clickedLabel.configure(text=traceback.format_exc())

    def updateTests(*args):
        nTests=dropDownVal.get()
        nTestsText = "Will run " + str(nTests) + " tests"
        confirmLabel.configure(text=nTestsText)

    def updateGraphType(*args):
        currType = graphOptionVal.get()
        graphText = "Simulate on " + currType + " graph"
        graphLabel.configure(text=graphText)
        if currType == "Euclidean":
            entrySpace[indOfEuc-1].config(state=DISABLED, bg="gray")
            entrySpace[indOfEuc].config(state=NORMAL, bg="white")
            entrySpace[indOfEuc+1].config(state=NORMAL, bg="white")
            entrySpace[indOfHub].config(state=DISABLED, bg="gray")
        elif currType == "Regular":
            entrySpace[indOfEuc-1].config(state=NORMAL, bg="white")
            entrySpace[indOfEuc].config(state=DISABLED, bg="gray")
            entrySpace[indOfEuc+1].config(state=DISABLED, bg="gray")
            entrySpace[indOfHub].config(state=DISABLED, bg="gray")
        elif currType == "Network":
            entrySpace[indOfEuc-1].config(state=DISABLED, bg="gray")
            entrySpace[indOfEuc].config(state=DISABLED, bg="gray")
            entrySpace[indOfEuc+1].config(state=DISABLED, bg="gray")
            entrySpace[indOfHub].config(state=NORMAL, bg="white")
            # print("Option not supported yet\n")
            # showwarning("Error", "Network graphs not supported yet :(")
        # else:
        #     print("Unknown graph selected\n")
        #     showerror("Error", "Graph selection error")
        graphOptionVal.set(currType)


    # Option to toggle between graphs
    i += 1
    graphTypes = ["Regular",
                  "Euclidean",
                  "Network"]
    currType = graphTypes[0]
    # Black out Euclidean parameters
    entrySpace[indOfEuc].config(state=DISABLED, bg="gray")
    entrySpace[indOfEuc+1].config(state=DISABLED, bg="gray")
    # Black out Network parameters
    entrySpace[indOfHub].config(state=DISABLED, bg="gray")

    graphText = "Simulate on " + currType + " graph"
    graphLabel = Label(window, text=graphText)

    graphOptionVal = StringVar(window)
    graphOptionVal.set(currType)
    graphOptionLabel = Label(window, text="Choose type of graph")
    graphOptionLabel.grid(column=0, row=i)

    graphOptions = OptionMenu(window, graphOptionVal, *graphTypes,\
                              command=updateGraphType)
    graphOptions.grid(column=1, row=i)

    # Option to determine number of tests to run
    i += 1
    nTests = 1
    nTestsText="Will run " + str(nTests) + " tests"
    maxTests = 10
    testArr = range(1, maxTests, 1)
    confirmLabel = Label(window, text=nTestsText)

    dropDownVal = IntVar(window)
    dropDownVal.set(nTests)
    testOptionLabel = Label(window, text="Choose number of tests...")
    testOptionLabel.grid(column=0, row=i)

    testOptions = OptionMenu(window, dropDownVal, *testArr,\
                             command=updateTests)
    testOptions.grid(column=1, row=i)

    # Option to determine range of values

    # Confirmation label to summarize the results to test
    i += 1
    summaryLabel = Label(window, text="Summary of inputs")
    summaryLabel.grid(column=0, row=i)

    # Show number of tests to run
    i += 1
    confirmLabel.grid(column=0, row=i)

    # Show type of graph
    i += 1
    graphLabel.grid(column=0, row=i)

    # Buttons for animation and simulation
    i += 1
    animBtn = Button(window, text="Run Animation", command=clickedAnimation)
    animBtn.grid(column=0, row=i)

    timeBtn = Button(window, text="Find time", command=clickedTime)
    timeBtn.grid(column=1, row=i)

    # Display clickedLabel after buttons
    i += 1
    clickedLabel.grid(column=0, row=i)

    # Navigate back to title
    i += 1
    titleBtn = Button(window, text="Back to title page", command=partial(loadTitlePage, window))
    titleBtn.grid(column=0, row=i)

    window.mainloop()

# The landing page for the simulator
def loadTitlePage(window):
    # Clear
    clearWindow(window)

    # Welcome text
    welcometext = "Fast, Covert, and Robust Exchange of Messages on a Graph - Simulator"
    titleLbl = Label(window, text=welcometext)
    i = 0
    titleLbl.grid(column=0, row=i)

    # Buttons to navigate to other pages
    i += 1

    simBtn = Button(window, text="Try simulation", command=partial(loadSimPage, window))
    simBtn.grid(column=0, row=i)

    window.mainloop()

def allChildren(window):
    _list = window.winfo_children()

    for item in _list:
        if item.winfo_children():
            _list.extend(item.winfo_children())

    return _list

def clearWindow(window):
    widgetList = allChildren(window)
    for item in widgetList:
        item.grid_forget()

if __name__ == "__main__":
    # Set up window for simulation
    window = Tk()
    window.title("GUI Simulator")
    windowDim = "900x600"
    window.geometry(windowDim)
    # Load title page initially
    loadTitlePage(window)