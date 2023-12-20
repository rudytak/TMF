# imports
import math
def lmap(f,x):
    return list(map(f,x))

# function that converts the B/t relation to omega/t relation
def process_raw_decay_data(
        id, 
        startTime = -1, 
        threshold = 0.7):
    # the times of the found peaks
    peaks = []
    with open(f"./inputs/Spinner_{id}_decay_rate.csv") as inp:
        # parse in the data lines
        lines = inp.read().split("\n") 
        # find the starting index from which the data points are after startTime
        startInd = 1 
        while (float(lines[startInd].split(",")[0]) < startTime): 
            startInd += 1
        
        hitPeak = False # keeps track of if we found the sttart of a peak
        startPeak, endPeak = 0 # bounding times of the peak
        for i in range(
            startInd, 
            len(lines)-1):
            # going through each line
            row = lines[i].split(",")

            # if we go over the threshold, the peak has started
            if (float(row[1]) >= threshold and not hitPeak):
                # we start the peak
                hitPeak = True
                startPeak = float(row[0])

            # if we go back under and have found a start
            if (float(row[1]) < threshold and hitPeak):
                # we end the peak
                hitPeak = False
                endPeak = float(row[0])
                # and save it's middle value
                peaks.append((endPeak+startPeak)/2)                
