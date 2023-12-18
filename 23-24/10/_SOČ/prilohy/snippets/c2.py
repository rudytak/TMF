down_vals = lmap(lambda j: ydata[j], lfilt(lambda j: down_intervals[i][0] < xdata[j] < down_intervals[i][1], range(len(ydata))))
up_vals = lmap(lambda j: ydata[j], lfilt(lambda j: up_intervals[i][0] < xdata[j] < up_intervals[i][1], range(len(ydata))))

down_avg = np.average(down_vals)
up_avg = np.average(up_vals)

amp = (up_avg - down_avg) / 2

down_error = [
    np.average(lmap(lambda x: down_avg - x, lfilt(lambda x: x <= down_avg, down_vals))),
    np.average(lmap(lambda x: x - down_avg, lfilt(lambda x: x > down_avg , down_vals)))
] 
up_error = [
    np.average(lmap(lambda x: up_avg - x, lfilt(lambda x: x <= up_avg, up_vals))),
    np.average(lmap(lambda x: x - up_avg, lfilt(lambda x: x > up_avg , up_vals)))
] 