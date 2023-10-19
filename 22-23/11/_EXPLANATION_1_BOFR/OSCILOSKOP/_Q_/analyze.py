fo = open("./ferrite_15kHz_Q.csv")
lines = fo.readlines()
fo.close()

data = []
for l in lines[1:]:
    data.append(abs(float(l.split(",")[1].strip())))

start_id = int(lines[1].split(",")[0])

max_size = 10
sample_reduction = 10
red = []
for i in range(0, data.__len__() - max_size, sample_reduction):
    red.append(
        max(data[i:i+max_size])
        )

f = open("ferrite_15kHz_Q_REDUCED.csv", "w+")
f.write(lines[0])

for i in range(red.__len__()):
    f.write(f"{start_id + i * sample_reduction}, {red[i]}\n")

f.close()