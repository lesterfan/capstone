from tkinter import *
from tkinter import messagebox
import simulation
import traceback
from functools import partial

# TODO
# 1. Implement range-based testing
# 2. Mutliple testing feature
# 3. Given parameters, output all results of a test in a tabulated second window/file


# Setup output window for simulation
def initOutputWindow(graphType, numTests):
    wind = Tk()
    wind.title("Output")
    windowDim = "600x500"
    wind.geometry(windowDim)

    titleText = "Simulation over range of values for " + graphType + " graph\n" +\
        "With " + str(numTests) + " tests for each set of parameters\n"
    titleMessage = Message(wind, width=400, text = titleText)
    titleMessage.grid(column=0, row=0)
    return wind

# Add time associated with a specific simulation to output window
def addToOutWind(wind, indTime, rowToUpdate, \
                 m, k, n, f, s, r, rows, cols, num_hubs,\
                 graphType):
    params = ["m", "k", "n", "f", "s"]
    paramVals = [m, k, n, f, s]
    textBody = ""
    count = 0
    for p in params:
        textBody += p + " = " + str(paramVals[count]) + ", "
        count += 1
    if(graphType == "Regular"):
        textBody += "r = " + str(r)
    elif(graphType == "Euclidean"):
        textBody += "cols = " + str(cols) +\
            ", rows = " + str(rows)
    elif(graphType == "Network"):
        textBody += "num_hubs = " + str(num_hubs)

    textBody += ": " + str(indTime) + " seconds"
    newMessage = Message(wind, width=400, text=textBody)
    newMessage.grid(column=0, row=rowToUpdate)


# Method to perform repeated simulation given range parameters, graphType, option (simulate/animate)
# Runs number of batches of individual tests for each set of fixed parameters
# For the simulation option (option == 1) returns the total amount of time needed to run ALL simulations
# Would also like it to update some sort of table somewhere as well for the simulation option
def repeatedSimulation(min_m, min_k, min_n, min_f, min_s, min_r, min_rows, min_cols, min_num_hubs,
                max_m, max_k, max_n, max_f, max_s, max_r, max_rows, max_cols, max_num_hubs,
                graphType, option, batch):
    totalTime = 0
    indTime = 0
    totalTests = 0
    outWind = -1
    rowToUpdate = 1
    if(option == 1): # setup output window for each result
        outWind = initOutputWindow(graphType, batch)

    for m in range(min_m, max_m + 1):
        for k in range(min_k, max_k + 1):
            for n in range(min_n, max_n + 1):
                for f in range(min_f, max_f + 1):
                    for s in range(min_s, max_s + 1):
                        if(graphType == "Regular"):
                            for r in range(min_r, max_r + 1):
                                if(option == 0):
                                    simulation.animate(m, k, n, f, s, r, graph_type=graphType,
                                        rows=0, cols=0, num_hubs=0, num_batch=batch)
                                else:
                                    indTime = simulation.simulate(m, k, n, f, s, r, graph_type=graphType,
                                        rows=0, cols=0, num_hubs=0, num_batch=batch)
                                    addToOutWind(outWind, indTime, rowToUpdate, \
                                                 m, k, n, f, s, r, 0, 0, 0, \
                                                 graphType)
                                    rowToUpdate += 1
                                    totalTime += indTime
                                    totalTests += 1
                        elif(graphType == "Euclidean"):
                                for rows in range(min_rows, max_rows + 1):
                                    for cols in range(min_cols, max_cols + 1):
                                        if(option == 0):
                                            simulation.animate(m, k, n, f, s, 0, graph_type=graphType,
                                                rows=rows, cols=cols, num_hubs=0, num_batch=batch)
                                        else:
                                            indTime = simulation.simulate(m, k, n, f, s, 0, graph_type=graphType,
                                                rows=rows, cols=cols, num_hubs=0, num_batch=batch)
                                            addToOutWind(outWind, indTime, rowToUpdate, \
                                                         m, k, n, f, s, 0, rows, cols, 0, \
                                                         graphType)
                                            rowToUpdate += 1
                                            totalTime += indTime
                                            totalTests += 1
                        elif(graphType == "Network"):
                                for num_hubs in range(min_num_hubs, max_num_hubs + 1):
                                    if(option == 0):
                                        simulation.animate(m, k, n, f, s, 0, graph_type=graphType,
                                            rows=0, cols=0, num_hubs=num_hubs, num_batch=batch)
                                    else:
                                        indTime = simulation.simulate(m, k, n, f, s, 0, graph_type=graphType,
                                            rows=0, cols=0, num_hubs=num_hubs, num_batch=batch)
                                        addToOutWind(outWind, indTime, rowToUpdate, \
                                                     m, k, n, f, s, 0, 0, 0, num_hubs, \
                                                     graphType)
                                        rowToUpdate += 1
                                        totalTime += indTime
                                        totalTests += 1
    print("Total number of tests: " + str(totalTests) + "\n")
    if option == 1:
        return totalTime


def printMessageBox(enteredParams, graphType, numberOfTests):
    simTextBody = ""
    currCount = 0
    currTests = 1
    params = ["m", "k", "n", "f", "s", "r", # parameters shared among all graphs
                "rows", "cols", # parameters present in only Euclidean
                "num_hubs" # parameters present in only network graph
                ]
    nParams = len(params)
    for p in params:
        # update logic if not correct
        if( (graphType == "Regular" and p != "rows" and p != "cols" and p != "num_hubs")
                or (graphType == "Euclidean" and p != "r" and p != "num_hubs")
                or (graphType == "Network" and p != "r" and p != "rows" and p != "cols")):
            simTextBody += p + ": " + \
                str(enteredParams[currCount]) + \
                " to " + \
                str(enteredParams[currCount + nParams]) + \
                " inclusive \n"
        currTests *= (enteredParams[currCount + nParams] - enteredParams[currCount] + 1)
        currCount += 1

    simTextBody += "Graph type: " + graphType + "\n"
    simTextBody += "Number of tests for each fixed parameter: " + str(numberOfTests) + "\n"
    simTextBody += "Number of tests to be performed in total: " + str(numberOfTests * currTests)
    messagebox.showinfo("Final simulation input", simTextBody)

# Page that allows for simulating/animating graph given parameters
def loadSimPage(window):
    centerCol = 1
    # Title
    titletext = "Fast, Covert, and Robust Exchange of Messages on a Graph - Simulator"
    titleMessage = Message(window, width=400, text=titletext)
    i = 0
    titleMessage.grid(column=0, row=i)

    # Prompt to enter parameters
    explainWidth=50
    lbl = Label(window, text="Enter parameters below")
    i += 1
    lbl.grid(column=0, row=i)

    explainLbl = Label(window, width=explainWidth, text="What are these?", anchor="w")
    explainLbl.grid(column=2, row=i)

    # Parameters and default values
    paramArr = ["m", "k", "n", "f", "s", "r", # parameters shared among all graphs
                "rows", "cols", # parameters present in only Euclidean
                "num_hubs" # parameters present in only network graph
                ]
    nParams = len(paramArr)
    defVals = [10, 5, 10, 20, 30, 10, 1, 1, 4]
    textArr = ["Message length",
               "Number of message bits in each block",
               "Size of codeword after adding redundancy",
               "Number of friends on graph that may hold bits",
               "Size/number of nodes on graph",
               "Degree of each node",
               "Number of rows",
               "Number of columns",
               "Number of hubs"]

    # Set up area to enter info
    entrySpace = []
    entryLabels = []
    explainLabels = []
    i += 1
    labelWidth = 10
    entryWidth = 10
    count = 0

    # When the user presses return, clicks on another entry object, or their mouse leaves
    # the widget, perform the callback
    def bindEntryTo(entryInst, funcCallback):
        entryInst.bind('<Return>', (lambda _: funcCallback()))
        entryInst.bind('<FocusOut>', (lambda _: funcCallback()))
        entryInst.bind('<Leave>', (lambda _: funcCallback()))

    for p in paramArr:
        entryLabel = Label(window, width=labelWidth, text=p + ": ")
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
    clickedLabel = Message(window, width=200, anchor="w",
                         text="Default values provided- either run animation or find the time taken to simulate")
    animTextPre = "Running animation on the given parameters..."
    animTextPost = "Running animation on parameters- check other window"
    timeTextPre = "Finding the time taken on the given parameters..."
    timeTextPost = "Time required to run simulation on given parameters: "
    timeTextPost2 = "Average time required per test: "

    # validate all parameters and output corresponding error message instead of traceback
    # return the array of inputs; break the corresponding ranges as necessary
    def validateEntries():
        paramsToInt=list(range(nParams * 2))
        j = 0
        for entry in entrySpace:
            posOfColon = entry.get().find(":")
            if entry.get().isdigit() and int(entry.get()) > 0:
                paramsToInt[j] = int(entry.get())
                paramsToInt[j + nParams] = int(entry.get())
            elif posOfColon != -1:
                s1 = entry.get()[0:posOfColon]
                s2 = entry.get()[posOfColon + 1: len(entry.get())]
                if( (not s1.isdigit() or int(s1) <= 0) or (not s2.isdigit() or int(s2) <= 0)):
                    clickedLabel.configure(text="Error for parameter "\
                                                + paramArr[j] + " usage for range based detection")
                    return []
                elif int(s2) < int(s1):
                    clickedLabel.configure(text="Error for parameter " + paramArr[j] +\
                                                ": The second parameter must be larger than the first!")
                    return []
                paramsToInt[j] = int(s1)
                paramsToInt[j + nParams] = int(s2)
            else:
                clickedLabel.configure(text="Invalid parameter input detected- either not positive or incorrect range-based usage")
                return []
            j += 1
        if not testOptions.get().isdigit() or int(testOptions.get()) <= 0:
                clickedLabel.configure(text="Invalid parameter input detected- either not positive or incorrect range-based usage")
                return []
        return paramsToInt

    # Proceed to simulation with the given parameters m, k, n, f, s, r, ... and type of graph
    # Update output label as needed
    def validateParams(m, k, n, f, s, r, rows, cols, num_hubs,
                       max_m, max_k, max_n, max_f, max_s, max_r, max_rows, max_cols, max_num_hubs,
                       currType):
        if (k > max_m):
            clickedLabel.configure(
                text="Error: k cannot be greater than largest value of m! You can't split the message into more blocks than its length.")
            return False
        if (k > max_n):
            clickedLabel.configure(
                text="Error: Maximum value of n cannot be less than k! You need to encode into more blocks than you started with.")
            return False
        if (n > max_f):
            clickedLabel.configure(
                text="Error: Maximum value of f cannot be less than n! You need at least n relays to hold your code blocks.")
            return False
        if (currType != "Euclidean" and f > max_s):
            clickedLabel.configure(
                text="Error: Maximum value of s cannot be less than f! You need to fit all of the relays on the graph.")
            return False
        if (currType == "Euclidean" and rows * cols > max_s):
            clickedLabel.configure(
                text="Error: rows*cols cannot be less than s! You need to fit all of the relays on the graph.")
            return False
        return True

    # Perform animation on the given parameters
    def clickedAnimation():
        try:
            currType = graphOptionVal.get()
            vals = validateEntries()
            if len(vals) == 0:
                return
            #m, k, n, f, s, r, rows, cols, num_hubs,\
                #max_m, max_k, max_n, max_f, max_s, max_r, max_rows, max_cols, max_num_hubs = vals
            batch = int(testOptions.get())

            proceedToSim=validateParams(*vals, currType)
            if not proceedToSim:
                return

            # printMessageBox(vals, currType, nTests)
            clickedLabel.configure(text=animTextPre)
            repeatedSimulation(*vals, currType, 0, batch)
            #simulation.animate(m, k, n, f, s, r, graph_type = currType, rows = rows, cols = cols, num_hubs=num_hubs, num_batch=batch)
            clickedLabel.configure(text=animTextPost)
        except Exception as error:
            clickedLabel.configure(text=traceback.format_exc())

    # Perform simulation (find time only) on the given parameters
    def clickedTime():
        try:
            currType = graphOptionVal.get()
            vals = validateEntries()
            if len(vals) == 0:
                return
            m, k, n, f, s, r, rows, cols, num_hubs, \
            max_m, max_k, max_n, max_f, max_s, max_r, max_rows, max_cols, max_num_hubs = vals
            batch = int(testOptions.get())
            proceedToSim=validateParams(*vals, currType)
            if not proceedToSim:
                return
            # printMessageBox(vals, currType, nTests)
            clickedLabel.configure(text=timeTextPre)
            totalTime = repeatedSimulation(*vals, currType, 1, batch)
            #time = simulation.simulate(m, k, n, f, s, r, graph_type = currType, rows = rows, cols = cols, num_hubs=num_hubs, num_batch=batch)
            clickedLabel.configure(text=timeTextPost + str(totalTime) + "\n"\
                                        + timeTextPost2 + str(totalTime/batch))
        except Exception as error:
            clickedLabel.configure(text=traceback.format_exc())

    def updateTests(*args):
        nTests=dropDownVal.get()
        nTestsText = "Will run " + str(nTests) + " tests"
        confirmLabel.configure(text=nTestsText)

    def updateVisibility(A):
        k = 0
        cnt = 0
        for index in range(4,9):
            if (A[k] == 0):
                entryLabels[index].grid_forget()
                entrySpace[index].grid_forget()
                explainLabels[index].grid_forget()
            else:
                entryLabels[index].grid(column=0, row=5+cnt)
                entrySpace[index].grid(column=1, row=5+cnt)
                explainLabels[index].grid(column=2, row=5+cnt)
                cnt = cnt+1
            k = k+1
    
    def updateGraphType(*args):
        currType = graphOptionVal.get()
        graphText = "Simulate on " + currType + " graph"
        graphLabel.configure(text=graphText)
        if currType == "Euclidean":
            updateVisibility([0,0,1,1,0])
        elif currType == "Regular":
            updateVisibility([1,1,0,0,0])
        elif currType == "Network":
            updateVisibility([1,0,0,0,1])
        graphOptionVal.set(currType)


    # Option to toggle between graphs
    i += 1
    graphTypes = ["Regular",
                  "Euclidean",
                  "Network"]
    currType = graphTypes[0]
    updateVisibility([1,1,0,0,0])

    graphText = "Simulate on " + currType + " graph"
    graphLabel = Label(window, text=graphText)

    graphOptionVal = StringVar(window)
    graphOptionVal.set(currType)
    graphOptionLabel = Label(window, text="Choose type of graph")
    graphOptionLabel.grid(column=0, row=i)

    graphOptions = OptionMenu(window, graphOptionVal, *graphTypes,
                              command=updateGraphType)
    graphOptions.grid(column=1, row=i)

    # Option to determine number of tests to run
    i += 1
    nTests = 1
    nTestsText="Will run " + str(nTests) + " tests"
    confirmLabel = Label(window, text=nTestsText)

    testOptionLabel = Label(window, text="Enter number of tests...")
    testOptionLabel.grid(column=0, row=i)

    nTestVal = StringVar()
    nTestVal.set(nTests)

    def testOptionCallback():

        if(not nTestVal.get().isdigit() or int(nTestVal.get()) <= 0):
            nTestsText = "Error: The number of tests must be an integer larger than 0!"
            confirmLabel.configure(text=nTestsText)
        else:
            nTests = nTestVal.get()
            nTestsText = "Will run " + str(nTests) + " tests"
            confirmLabel.configure(text=nTestsText)

    testOptions = Entry(window, textvariable=nTestVal)
    bindEntryTo(testOptions, testOptionCallback)
    testOptions.grid(column=1, row=i)


    # Confirmation label to summarize the results to test
    i += 1
    summaryLabel = Message(window, width=200, text="Summary of inputs")
    summaryLabel.grid(column=centerCol, row=i)

    # Show number of tests to run
    i += 1
    confirmLabel.grid(column=centerCol, row=i)

    # Show type of graph
    i += 1
    graphLabel.grid(column=centerCol, row=i)

    # Also provide further explanation/notes here
    i += 1
    etcLabel = Message(window, width=400, text="More detailed summary may be found by clicking either\n"
                                               "'run time' or 'animate'\n")
    etcLabel.grid(column=centerCol, row=i)

    # Buttons for animation and simulation
    i += 1
    animBtn = Button(window, text="Run Animation", command=clickedAnimation)
    animBtn.grid(column=0, row=i)

    timeBtn = Button(window, text="Find time", command=clickedTime)
    timeBtn.grid(column=1, row=i)

    # Display clickedLabel after buttons
    i += 1
    clickedLabel.grid(column=centerCol, row=i)

    window.mainloop()

if __name__ == "__main__":
    # Set up window for simulation
    window = Tk()
    window.title("GUI Simulator")
    windowDim = "1000x600"
    window.geometry(windowDim)
    # Load simulation page
    loadSimPage(window)
