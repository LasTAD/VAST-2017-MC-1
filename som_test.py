from sklearn.cluster import KMeans
import numpy as np
from SOM import SOM
import seaborn as sb

data = np.loadtxt('Data/output.txt', delimiter=';', usecols=range(40))
k = 18
# targets = np.loadtxt('Data/target_k-means.txt', delimiter=';', usecols=(0), dtype='int')
print('K-means ready!')

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

som = SOM(20, 20)  # initialize the SOM
som.load('Data/SOM')
# name = 0
# names = []
# for x in range(k):
#     names.append(str(name))
#     name += 1
colors = sb.color_palette(n_colors=7)
som.plot_point_map(data, targets, names, filename='images/SOM/som_test.png', colors=colors)


