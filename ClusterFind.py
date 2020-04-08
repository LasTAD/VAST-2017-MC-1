import numpy as np
from SOM import SOM
import DataPrep as dp

data = np.loadtxt('output.txt', delimiter=';', usecols=range(40))

som = SOM(20, 20)  # initialize the SOM
som.fit(data, 10000, decay='linear')
# som.plot_error_history(filename='images/som_error.png')  # plot the training error history

targets = np.loadtxt('target.txt', dtype='int')

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
som.plot_point_map(data, targets, names, filename='images/som.png')
# som.plot_class_density(data, targets, t=0, name='Vehicles', filename='images/density.png')
# som.plot_distance_map(filename='images/distance_map.png')  # plot the distance map after training
