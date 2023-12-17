# imports
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig

# helper function to convert the map iterator to a list
lmap = lambda f,x : list(map(f, x))
# peaks start and end points
peaks_s, peaks_e = 0

with open("./kyvadlo.csv", "r") as read:
    data = read.readlines()[1:] # load all the value rows
    # convert all rows into value arrays
    data = lmap(lambda row: row.rstrip().split(","), data)

    xdata = lmap(lambda row: float(row[0]), data) # x axis data
    ydata = lmap(lambda row: float(row[1]), data) # y axis data
    mov = 15 # the amount of smoothing
    # smooths out the data using convolution
    ydata_clean = np.convolve(ydata, np.ones(mov)/mov, "same")

    # find the peaks from the data using scipy.signal.find_peaks
    peaks, heights = sig.find_peaks(
        ydata_clean,
        height=1,
        threshold=0.0001,
        distance=35
    )
    # get the sampling frequency
    samples_per_sec = (len(xdata) / max(xdata))
    # find the start and end time of where the peaks are
    peaks_s = peaks[0] - int(samples_per_sec / 2)
    peaks_e = peaks[-1] + int(samples_per_sec / 2)

    # plot the smoothed out data
    plt.plot(xdata[peaks_s: peaks_e], ydata_clean[peaks_s: peaks_e])
    # plot all the peak lines
    for p in peaks:
        plt.axvline(p / samples_per_sec, color="r", linestyle=":")

    # set all other styling of the plot
    plt.title("Magnetic field from a spinner pendulum")
    plt.ylabel("$B$ $[mT]$")
    plt.xlabel("$t$ $[s]$")

    # calcualte and print out the resulting frequency
    f = 1/2 * ((len(peaks)-1) / ((max(peaks) - min(peaks)) / samples_per_sec))
    print(f"{f:.2f} Hz") 