We want to send a message of size m covertly.
To do this, we break the message of size m in to m // k blocks, where // is integer division.
For each block, we do the following:
We have to send a dataword of size k, which will correspond to a codeword of size n by adding redundancy,
which we want to covertly send through the coupon collection procedure. 
We do this by working on a connected graph of size s, in which you have f friends. 
The disseminator will give n out of the f friends a bit each of the codeword to send the message.
The collector will need to visit any k out of the n people the disseminator visited in order to receive the message.
We are interested in the expected time before the collector will have received the message.