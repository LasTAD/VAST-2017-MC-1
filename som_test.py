from sklearn.cluster import KMeans
import numpy as np
from SOM import SOM
import seaborn as sb

data = np.loadtxt('output.txt', delimiter=';', usecols=range(40))
k = 15
kmeans = KMeans(n_clusters=k, random_state=0).fit(data)
targets = kmeans.labels_
print('K-means ready!')

som = SOM(20, 20)  # initialize the SOM
som.load('SOM')
name = 0
names = []
for x in range(k):
    names.append(str(name))
    name += 1
colors = sb.color_palette(n_colors=k)
som.plot_point_map(data, targets, names, filename='images/SOM/som_test.png', colors=colors)


