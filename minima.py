import simulation

def simulateN(m, k, n, f, s, r, N):
	"""
	Compute the N simulations given the parameters m, k, n, f, s, r
	and return the average result
	"""
	totalTime = 0 
	for i in range(0, N):
		totalTime = totalTime + simulation.simulate(m, k, n, f, s, r) 
	return totalTime/N 	

if __name__ == "__main__":
	# Fix m, s, f - consider changing these parameters as it takes over an hour to simulate
	m = 100 
	f = 20 
	s = 30 

        # 3 <= r <= 10
	rBegin = 3 
	rEnd = 10 

	tCount = 0 

        # Keep track of minimal time and values of k, n, r
	minTime = -1 
	minK = -1 
	minN = -1 
	minR = -1 

        # run the simulation for fixed parameters N times
	N = 10  
	
        # total number of times simulateN is called - for estimating time needed to run program
	totalNSims = f * ((f+1)/2) * (rEnd - rBegin + 1) 
	
	"""
	Vary all combinations for 1 <= k <= n <= f and 3 <= r <= 10
        and find the k, n, r that generates the minimum time
        """
	for k in range(1, f+1):
		for n in range(k, f+1):
			for r in range(rBegin, rEnd + 1):
				currTime = simulateN(m, k, n, f, s, r, N) 
				if currTime < minTime or tCount == 0:
  	        			minTime = currTime 
  	        			minK = k 
  	        			minN = n 
  	        			minR = r 
				if tCount % 5 == 0:	
					print(f'{tCount}/{totalNSims}')  
				tCount += 1 

	if minTime == -1:
		print(f'An error occurred in the simulation') 
	else:
		print(f'Given m = {m}, f = {f}, s = {s} the minimum values for k, n, and f for when {N} simulations are done gives the average time {minTime} and k = {minK}, n = {minN}, r = {minR}') 
			
