# Capstone
This is our capstone project.

## Problem Statement
We want to send a message of size m covertly.
To do this, we break the message of size m in to m // k blocks, where // is integer division.
For each block, we do the following:
We have to send a dataword of size n, which will correspond to a codeword of size k by adding redundancy,
which we want to covertly send through the coupon collection procedure. 
We do this by working on an r-regular graph of size s, in which you have f friends. 
The disseminator will give n out of the f friends a bit each of the codeword to send the message.
The collector will need to visit any k out of the n people the disseminator visited in order to receive the message.
We are interested in the expected time before the collector will have received the message.
This repository contains our simulation.

## How to Run

### Using Anaconda 3
You can run the gui directly if you have Anaconda 3 installed by opening the anaconda prompt and running
    
    python gui.py


### Using Python 3
Otherwise, you can first (optionally) create a virtual environment by running

    python -m venv .venv

and then 

    .\.venv\Scripts\activate.bat

on Windows or 

    source ./env/bin/activate

on Linux.

Install the requirements by running

    pip install -r requirements.txt

and then run the simulation with 

    python gui.py


