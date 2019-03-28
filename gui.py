from tkinter import *
import simulation

if __name__ == "__main__":
    # Set up window for simulation
    window = Tk()
    window.title("GUI Simulator")
    windowDim = "700x400"
    window.geometry(windowDim)
    lbl = Label(window, text = "Enter parameters")
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
        entryLabel = Label(window, text = p + ": ")
        entryLabel.grid(column=0, row = i)
        currEntry = Entry(window, width=setWidth)
        currEntry.insert(END, defVals[count])
        currEntry.grid(column=1, row=i)
        i += 1
        count += 1
        entrySpace.append(currEntry)
        entryLabels.append(entryLabel)

    clickedLabel = Label(window, text="Default values provided- either run animation or find the time taken to simulate")
    clickedLabel.grid(column=0, row=i+1)

    animTextPre = "Running animation on the given parameters..."
    animTextPost = "Successfully ran animation on paramters- check other window"
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
            clickedLabel.configure(text=str(error))

    # Perform simulation (find time only) on the given parameters
    def clickedTime():
        try:
            vals = []
            vals = [int(entry.get()) for entry in entrySpace]
            clickedLabel.configure(text=timeTextPre)
            time = simulation.simulate(*vals)
            clickedLabel.configure(text=timeTextPost + str(time))
        except Exception as error:
            clickedLabel.configure(text=str(error))

    # Buttons for animation and simulation
    animBtn = Button(window, text="Run Animation", command=clickedAnimation)
    animBtn.grid(column=0, row=i)

    timeBtn = Button(window, text="Find time", command=clickedTime)
    timeBtn.grid(column=1, row=i)

    window.mainloop()