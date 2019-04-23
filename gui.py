from tkinter import *
import simulation
import traceback
from functools import partial

# Page that allows for simulating/animating graph given parameters
def loadSimPage(window):
    # Clear
    clearWindow(window)

    # Prompt to enter parameters
    lbl = Label(window, text="Enter parameters")
    i = 0
    lbl.grid(column=0, row=i)

    # Paramters and default values
    paramArr = ["m", "k", "n", "f", "s", "r"]
    defVals = [10, 5, 10, 20, 30, 10]

    # Set up area to enter info
    entrySpace = []
    entryLabels = []
    i += 1
    setWidth = 10
    count = 0
    for p in paramArr:
        entryLabel = Label(window, text=p + ": ")
        entryLabel.grid(column=0, row=i)
        currEntry = Entry(window, width=setWidth)
        currEntry.insert(END, defVals[count])
        currEntry.grid(column=1, row=i)
        i += 1
        count += 1
        entrySpace.append(currEntry)
        entryLabels.append(entryLabel)

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
            vals = []
            vals = [int(entry.get()) for entry in entrySpace]
            clickedLabel.configure(text=animTextPre)
            simulation.animate(*vals)
            clickedLabel.configure(text=animTextPost)
        except Exception as error:
            clickedLabel.configure(text=traceback.format_exc())

    # Perform simulation (find time only) on the given parameters
    def clickedTime():
        try:
            vals = []
            vals = [int(entry.get()) for entry in entrySpace]
            clickedLabel.configure(text=timeTextPre)
            time = simulation.simulate(*vals)
            clickedLabel.configure(text=timeTextPost + str(time))
        except Exception as error:
            clickedLabel.configure(text=traceback.format_exc())

    # Buttons for animation and simulation
    animBtn = Button(window, text="Run Animation", command=clickedAnimation)
    animBtn.grid(column=0, row=i)

    timeBtn = Button(window, text="Find time", command=clickedTime)
    timeBtn.grid(column=1, row=i)

    # Display clickedLabel after buttons
    i += 1
    clickedLabel.grid(column=0, row=i)

    # Navigate back to title
    i += 1
    titleBtn = Button(window, text ="Back to title page", command=partial(loadTitlePage, window))
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

    explainBtn = Button(window, text="Overview of parameters/project", command=partial(loadExplainPage, window))
    simBtn = Button(window, text="Try simulation", command=partial(loadSimPage, window))
    explainBtn.grid(column=0, row=i)
    simBtn.grid(column=1, row=i)

    window.mainloop()

# Load explanation page
def loadExplainPage(window):
    # Clear
    clearWindow(window)

    # Provide explanation title page here
    toptext="Explanation of parameters and project"
    topLbl=Label(window, text=toptext)
    i = 0
    topLbl.grid(column=0, row=i)

    # Body of explanation here
    i += 1
    mainText="Update text here with formatting"
    mainLbl=Label(window, text=mainText)
    mainLbl.grid(column=0, row=i)

    # Buttons to navigate to other pages
    i += 1
    titleBtn = Button(window, text="Back to title", command=partial(loadTitlePage, window))
    simBtn = Button(window, text="Try simulation", command=partial(loadSimPage, window))
    titleBtn.grid(column=0, row=i)
    simBtn.grid(column=1, row=i)

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
    windowDim = "700x400"
    window.geometry(windowDim)
    # Load title page initially
    loadTitlePage(window)