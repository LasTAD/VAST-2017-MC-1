import numpy as np

f = open("Lekagul Sensor Data.csv", "r")
data = f.readlines()
f.close()

traces = []
gates = set()
for line in data:
    args = line.split(";")
    gates.add(args[3])
    traces.append(args)
gates = sorted(gates)

print(gates)

groupedTraces = {}
for t in traces:
    if t[1] in groupedTraces:
        groupedTraces[t[1]].append(t)
    else:
        groupedTraces[t[1]] = [t]

vectors = []
f = open("output.txt", "w+")
for name, gt in groupedTraces.items():
    groupGates = np.zeros(len(gates))
    for t in gt:
        groupGates[gates.index(t[3])] += 1
    groupGates = [x / len(gt) for x in groupGates]
    vectors.append(groupGates)
    for rec in groupGates:
        f.write(str(rec))
        f.write(";")
    f.write("\n")
f.close()
