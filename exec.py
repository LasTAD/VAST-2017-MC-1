import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from SOM import SOM
import seaborn as sb


conn = sqlite3.connect('Data/data.db')
cur = conn.cursor()

data = np.loadtxt('Data/output.txt', delimiter=';', usecols=range(40))
som = SOM(20, 20)  # initialize the SOM
som.fit(data, 10000, decay='hill')

# som = SOM(10, 10)  # initialize the SOM
# som.load('Data/SOM')

targets = np.loadtxt('Data/target.txt', dtype='int')

targets = targets - 1

names = ['Автомобиль',
         'Грузовик 2',
         'Грузовик 3',
         'Грузовик 4+',
         'Автобус 2',
         'Автобус 3',
         'Грузовик рейнджеров'
         ]
# now visualize the learned representation with the class labels
som.plot_point_map(data, targets, names, filename='images/SOM/som.png')
som.save('Data/SOM')

cur.execute('select car_id from dataset')
cars = cur.fetchall()

data = np.loadtxt('Data/output.txt', delimiter=';', usecols=range(40))
k = 25
kmeans = KMeans(n_clusters=k).fit(data)
# kmeans = KMeans(init='k-means++').fit(data)
labels = kmeans.labels_
f = open("Data/target_k-means.txt", "w+")
cur.execute('delete from k_mean')
conn.commit()
for cnt, xx in enumerate(labels):
    f.write(str(xx))
    f.write("\n")
    cur.execute("insert into k_mean (cluster, car_id) values (?, ?);", (str(xx), cars[cnt][0],))
f.close()
conn.commit()
print('k-mean ready')

cur.execute('select max(cluster) from k_mean')
clus = cur.fetchone()
k = int(clus[0]) + 1
print(k)



cur.execute('select * from barchart')
bar_chart = cur.fetchall()
barchart = []
for x in bar_chart:
    barchart.append(x[1:])
chart = np.array(barchart).T.tolist()
print(chart)
cur.execute('select gate_name from gate_coord')
names = cur.fetchall()
N = k

ind = np.arange(N)  # the x locations for the groups
sensor_layer = []
sensor_layer.append(plt.bar(ind, chart[0]))
for x in range(39):
    sensor_layer.append(plt.bar(ind, chart[x+1], bottom=chart[x+1]))
plt.ylabel('Количество срабатываний')
plt.title('Количество срабатываний датчиков по кластерам')
plt.legend(sensor_layer, names, prop={'size': 4})
plt.savefig('images/Barcharts/Barchart для ' + str(N) + ' кластеров.png')
plt.show()


data = np.loadtxt('Data/output.txt', delimiter=';', usecols=range(40))
# k = 25
targets = np.loadtxt('Data/target_k-means.txt', delimiter=';', usecols=(0), dtype='int')
print('K-means ready!')

som = SOM(15, 15)
som.load('Data/SOM')
name = 0
names = []
for x in range(k):
    names.append(str(name))
    name += 1
colors = sb.color_palette(n_colors=k)
som.plot_point_map(data, targets, names, filename='images/SOM/som_test.png', colors=colors)
