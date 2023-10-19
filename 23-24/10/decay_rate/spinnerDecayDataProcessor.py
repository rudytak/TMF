import math
peaks = []

startTime = 12

with open("./Data/Spinner 1 decay rate.csv") as inp:
    lines = inp.read().split("\n")

    startInd = 5
    while (float(lines[startInd].split(",")[0]) < startTime): startInd += 1
    
    hitPeak = False
    startPeak = 0
    endPeak = 0
    for i in range(startInd, len(lines)-1):
        row = lines[i].split(",")

        if (float(row[1]) >= 0.7 and not hitPeak):
            hitPeak = True
            startPeak = float(row[0])


        if (float(row[1]) < 0.7 and hitPeak):
            hitPeak = False
            endPeak = float(row[0])

            peaks.append((endPeak+startPeak)/2)                

results = {}
interval = 1
step = 0.2
curTime = startTime
x = 0
while x < len(peaks):
    if (peaks[x] > curTime+interval):
        curTime += step
        x = 0
    elif (peaks[x] > curTime and peaks[x] < curTime+interval):
        if (not curTime in results): results[curTime] = 1
        else: results[curTime] += 1
        
    x += 1

# print(results)

# with open("./Data/Spinner_1_decay_rate_PROCESSED.csv", 'w') as res:
#     for key in results.keys():
#         res.write(str(round(key, 1)) + "," + str(results[key]) + "\n")

with open("./Data/Spinner_1_decay_rate_PROCESSED_FLOATING_AVERAGE.csv", 'w') as res:
    for x in range(4, len(results.keys())):
        flAverage = 0
        for y in range(5):
            flAverage += results[list(results.keys())[x-y]]
        flAverage = flAverage/5
        res.write(str(round(list(results.keys())[x-y], 1)) + "," + str(flAverage) + "," + str(flAverage*2*math.pi/3) + "\n")