import glob, os
import msilib
import numpy as np
import matplotlib.pyplot as plt
import json

def getMaxesInFiles():
    os.chdir("./m2")

    values = {}
    files = glob.glob("*.txt")

    for file in files:
        print(file)
        with open(file, "r") as reader:
            lines = reader.readlines()
            values[file] = []
    
            for l in lines:
                val = float(l.replace("\n", "").split("\t")[1])
                values[file].append(val)

    maxes = {}
    for file in values:
        maxes[file] = max(values[file])
    
    out = ""
    for file in maxes:
        out += f"{file.split('_')[1]}, {maxes[file]}\n" 
    
    with open("out.csv", "w") as w:
        w.writelines(out)

def compileAllTrajectories():
    os.chdir("./m2")

    values = {}
    files = glob.glob("*.txt")

    for file in files:
        print(file)
        with open(file, "r") as reader:
            lines = reader.readlines()
            values[file] = {"x":[],"y":[]}
            frst_x = -1
    
            for l in lines:
                x = tToMs(l.replace("\n", "").split("\t")[0])
                y = float(l.replace("\n", "").split("\t")[1])

                if(y > 5):
                    if (frst_x == -1):
                        frst_x = x
                    
                    values[file]["x"].append(x - frst_x)
                    values[file]["y"].append(y)

    for val in values:
        plt.plot(values[val]["x"], values[val]["y"])
    plt.show()

    jsonstr = json.dumps(values)
    with open("out.json", "w") as w:
        w.writelines(jsonstr)

def tToMs(t):
    ms = t.split(".")[1]
    tt = t.split(".")[0].split(":")
    return int(tt[0])*3600000 + int(tt[1])*60000 + int(tt[2])*1000 + int(ms)

compileAllTrajectories()