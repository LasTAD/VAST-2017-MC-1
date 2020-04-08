import numpy as np

f = open("Lekagul Sensor Data.csv", "r")
data = f.readlines()
f.close()

traces = []
gates = set()
cars = []
for line in data:
    args = line.split(";")
    gates.add(args[3])
    traces.append(args)
    # cars.append(args[1], args[2])
gates = sorted(gates)

groupedTraces = {}
for t in traces:
    if t[1] in groupedTraces:
        groupedTraces[t[1]].append(t)
    else:
        groupedTraces[t[1]] = [t]

target = []
for x in groupedTraces:
    target.append(groupedTraces[x][1][2])
f = open("target.txt", "w+")
for rec in target:
    if rec == '2P':
        f.write('7')
        f.write("\n")
    else:
        f.write(str(rec))
        f.write("\n")
f.close()

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
