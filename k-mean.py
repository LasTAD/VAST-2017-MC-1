from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import sqlite3
import seaborn as sb
from SOM import SOM


conn = sqlite3.connect('Data/data.db')
cur = conn.cursor()
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

poi_coords = np.loadtxt('Data/gates-map.txt', delimiter=';', usecols=(1, 2))

with cbook.get_sample_data(
        '/Users/nikolaikobyzev/Documents/Для учебы/Лабораторные/10 сем/ИАД/VAST 2017 MC-1/images/Maps/Exmpl/Lekagul Roadways labeled v2.jpg') as image_file:
    image = plt.imread(image_file)

cur.execute('select gate_name from gate_coord order by gate_name')
gates = cur.fetchall()

colors = sb.color_palette(n_colors=4)

for kl_num in range(k):
    fig, ax = plt.subplots()
    ax.imshow(image)
    size = np.zeros((40, 1))
    plt.axis('off')
    for cnt, xx in enumerate(cars):
        if labels[cnt] == kl_num:
            plot = []
            # noinspection SqlResolve
            cur.execute(
                "select x, y from sensor_data sd join gate_coord gc on sd.gate_name = gc.gate_name where car_id = ? order by Timestamp;",
                xx)
            plot = cur.fetchall()
            plot = np.array(plot)
            plt.plot(plot[:, 0], plot[:, 1], c=colors[1], marker='o', markerfacecolor=colors[0])
            cur.execute(
                "select sd.gate_name from sensor_data sd join gate_coord gc on sd.gate_name = gc.gate_name where car_id = ? order by Timestamp;",
                xx)
            route = cur.fetchall()
            for gate in route:
                size[gates.index(gate)] += 1
    plt.scatter(poi_coords[:, 0], poi_coords[:, 1], s=size, c='green')
    ax.set_title('Кластер ' + str(kl_num))
    fig.set_figwidth(7)
    fig.set_figheight(7)
    plt.savefig('images/Maps/Кластер ' + str(kl_num) + '.png')
    print('images/Maps/Кластер ' + str(kl_num) + ' ready')
    # plt.show()

for kl_num in range(k):
    plt.axis('off')
    cur.execute('select * from k_mean where cluster = ? order by random() limit 3;', (kl_num,))
    data = cur.fetchall()
    fig, ax = plt.subplots()
    ax.imshow(image)
    for cnt, x in enumerate(data):
        plot = []
        # noinspection SqlResolve
        cur.execute(
            "select x, y from sensor_data sd join gate_coord gc on sd.gate_name = gc.gate_name where car_id = ? order by Timestamp;",
            (x[1],))
        plot = cur.fetchall()
        plot = np.array(plot)
        plt.plot(plot[:, 0] + 2 * np.random.randn(1), plot[:, 1] + 1 * np.random.randn(1), c=colors[cnt + 1],
                 marker='o', markerfacecolor=colors[0])
    plt.scatter(poi_coords[:, 0], poi_coords[:, 1], c='green', s=100)
    ax.set_title('Кластер ' + str(kl_num) + ' и 3 случайных маршрута')
    fig.set_figwidth(7)
    fig.set_figheight(7)
    plt.savefig('images/Maps/Кластер ' + str(kl_num) + ' и маршрут.png')
    print('images/Maps/Кластер ' + str(kl_num) + 'и маршрут ready')
    # plt.show()

    data = np.loadtxt('Data/output.txt', delimiter=';', usecols=range(40))
    # k = 25
    targets = np.loadtxt('Data/target_k-means.txt', delimiter=';', usecols=(0), dtype='int')
    print('K-means ready!')

    som = SOM(20, 20)  # initialize the SOM
    som.load('Data/SOM')
    name = 0
    names = []
    for x in range(k):
        names.append(str(name))
        name += 1
    colors = sb.color_palette(n_colors=k)
    som.plot_point_map(data, targets, names, filename='images/SOM/som_test.png', colors=colors)
