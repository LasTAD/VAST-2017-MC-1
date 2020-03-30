import numpy as np
from SOM import SOM

data = np.loadtxt('output.txt', delimiter=';', usecols=range(40))

som = SOM(20, 20)  # initialize the SOM
som.fit(data, 10000, save_e=True, interval=100)  # fit the SOM for 10000 epochs, save the error every 100 steps
som.plot_error_history(filename='images/som_error.png')  # plot the training error history

targets = np.array(18708 * [0])

# names = ['Campings', 'Entrances', 'Gates', 'General gates', 'Ranger base', 'Ranger stops']
# now visualize the learned representation with the class labels
som.plot_point_map(data, targets, ['Vehicles'], filename='images/som.png')
som.plot_class_density(data, targets, t=0, name='Vehicles', filename='images/density.png')
som.plot_distance_map(filename='images/distance_map.png')  # plot the distance map after training