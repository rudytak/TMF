    results = {}
    interval = 1
    step = 0.1
    curTime = startTime
    x = 0
    while x < len(peaks):
        if (peaks[x] > curTime+interval):
            # if the peaks are positioned outside the interval stop
            # and reposition the interval by step
            curTime += step
            x = 0
        elif (peaks[x] > curTime and peaks[x] < curTime+interval):
            # a peak is positioned in the time interval
            if (not curTime in results): results[curTime] = 0
            results[curTime] += 1 # increase the count amount 
        x += 1

    with open(f"./outputs/Spinner_{id}_decay_rate_PROCESSED_FLOATING_AVERAGE.csv", 'w') as res:
        res.write("t, peaks/s, omega \n")
        # go through all the results
        for x in range(4, len(results.keys())):
            # create a 5 element floating average
            flAverage = 0
            for y in range(5):
                flAverage += results[list(results.keys())[x-y]]
            flAverage = flAverage/5

            # write the time, avg. peak count and avg. omega to file
            res.write(str(round(list(results.keys())[x-y], 1)) + "," + str(flAverage) + "," + str(flAverage*2*math.pi/3) + "\n")
    # return the output file location
    return f"./outputs/Spinner_{id}_decay_rate_PROCESSED_FLOATING_AVERAGE.csv"