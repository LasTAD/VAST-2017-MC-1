import numpy as np
from SOM import SOM


data = np.loadtxt('Data/output.txt', delimiter=';', usecols=range(40))

###SOM
som = SOM(10, 10)  # initialize the SOM
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

# for name in names:
#     som.plot_class_density(data, targets, t=names.index(name), name=name, filename='images/SOM/density ' + name + '.png')

# som.save('SOM')