from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from collections import Counter

data = np.loadtxt('output.txt', delimiter=';', usecols=range(40))
k = 15
kmeans = KMeans(n_clusters=k, random_state=0).fit(data)
labels = kmeans.labels_
f = open("Data/target_k-means.txt", "w+")
for x in labels:
    f.write(str(x))
    f.write("\n")
f.close()

poi_coords = np.loadtxt('gates-map.txt', delimiter=';', usecols=range(2))

with cbook.get_sample_data('/Users/nikolaikobyzev/Documents/Для учебы/Лабораторные/10 сем/ИАД/VAST 2017 MC-1/Lekagul Roadways labeled v2.jpg') as image_file:
    image = plt.imread(image_file)

num = 0
car = 0
plot = []
poi_freq = np.zeros(40, 1)
for cnt, xx in enumerate(data):
    if labels[cnt] == 0:
        for cnt_y, yy in enumerate(xx):
            if yy != 0:
                plot.append(poi_coords[num])
                poi_freq[cnt_y] += 1
            num += 1
    plt.scatter(plot[:][0], plot[:][1], c='red')
    num = 0
size = Counter(plot)

plot = np.array(plot)
size = np.array(size)
print(size)
fig, ax = plt.subplots()
ax.imshow(image)

plt.scatter(poi_coords[:, 0], poi_coords[:, 1])
# plt.scatter(plot[:, 0], plot[:, 1], c='red', s=size)

ax.set_title('')
fig.set_figwidth(7)
fig.set_figheight(7)
plt.show()