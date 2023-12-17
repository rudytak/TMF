import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig

lmap = lambda f,x : list(map(f, x))

peaks_s = 0
peaks_e = 0

with open("./kyvadlo.csv", "r") as read:
    # DATA
    data = read.readlines()[1:]
    data = lmap(lambda row: row.rstrip().split(","), data)

    xdata = lmap(lambda row: float(row[0]), data)
    ydata = lmap(lambda row: float(row[1]), data)
    mov = 15
    ydata_clean = np.convolve(ydata, np.ones(mov)/mov, "same")

    # plt.plot(xdata, ydata)
    samples_per_sec = (len(xdata) / max(xdata))

    peaks, heights = sig.find_peaks(
        ydata_clean,
        height=1,
        threshold=0.0001,
        distance=35
    )
    peaks_s = peaks[0] - int(samples_per_sec / 2)
    peaks_e = peaks[-1] + int(samples_per_sec / 2)

    plt.plot(
        xdata[peaks_s: peaks_e], 
        ydata_clean[peaks_s: peaks_e]
    )

    f = 1/2 * ((len(peaks)-1) / ((max(peaks) - min(peaks)) / samples_per_sec))
    print(f"{f:.2f} Hz") 
    print(max(peaks)/200 - min(peaks)/200, len(peaks)) 

    for p in peaks:
        plt.axvline(p / samples_per_sec, color="r", linestyle=":")

plt.title("Magnetic field from a spinner pendulum")
plt.ylabel("$B$ $[mT]$")
plt.xlabel("$t$ $[s]$")