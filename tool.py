import PySimpleGUI as sg
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from SOM import SOM

# define the window layout
layout = [[sg.Text('SOM for VAST 2017 MC1', font='Any 18')],
          [sg.Text('Path to data'), sg.FileBrowse(key='-Path-data-')],
          [sg.Text('Path to target'), sg.FileBrowse(key='-Path-target-')],
          [sg.Text('SOM size:'), sg.InputText('20', key='-width-', size=(2, 1)),
           sg.InputText('20', key='-height-', size=(2, 1))],
          [sg.Text('Number of epochs'), sg.InputText(10000, key='-epochs-', size=(6, 1))],
          [sg.Text('Type of decay'), sg.Radio('Hill', 'DECAY', True, key='hill'), sg.Radio('Linear', 'DECAY', key='linear')],
          [sg.Button('Start SOM', key='-start-'), sg.Button('Exit')]
          ]

# create the form and show it without the plot
window = sg.Window('SOM for VAST 2017 MC1',
                   layout, finalize=True)



def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


while (True):
    event, values = window.read()
    if event == '-start-':
        data = np.loadtxt(values['-Path-data-'], delimiter=';', usecols=range(40))

        som = SOM(int(values['-width-']), int(values['-height-']))  # initialize the SOM
        print(values[5])
        som.fit(data, int(values['-epochs-']))  # fit the SOM for 10000 epochs, save the error every 100 steps
        # som.plot_error_history(filename='images/som_error.png')  # plot the training error history

        targets = np.loadtxt(values['-Path-target-'])
        targets = targets - 1
        names = ['2 axle car (or motorcycle)',
                 '2 axle truck',
                 '3 axle truck',
                 '4 axle (and above) truck',
                 '2 axle bus',
                 '3 axle bus',
                 'Ranger truck'
                 ]
        # names = ['Campings', 'Entrances', 'Gates', 'General gates', 'Ranger base', 'Ranger stops']
        # now visualize the learned representation with the class labels
        fig1 = som.plot_point_map_gui(data, targets, names)
        fig2 = som.plot_class_density_gui(data, targets, t=0, name='Vehicles')
        # som.plot_distance_map(filename='images/distance_map.png')  # plot the distance map after training
        fig1.set_size_inches(6, 6)
        fig2.set_size_inches(6, 6)
        figure1_x, figure1_y, figure1_w, figure1_h = fig1.bbox.bounds
        figure_x, figure2_y, figure2_w, figure2_h = fig2.bbox.bounds

        layout2 = [[sg.Text('Density SOM', font='Any 18')],
                   [sg.Canvas(size=(figure1_w, figure1_h), key='canvas_density'), sg.Canvas(size=(figure2_w, figure2_h), key='canvas_som')],
                   [sg.OK('OK'), sg.Button('Print result', key='-print-')]
                   ]

        # create the form and show it without the plot
        window2 = sg.Window('SOM Result',
                            layout2, finalize=True)

        fig_canvas_agg = draw_figure(window2['canvas_density'].TKCanvas, fig2)
        fig_canvas_agg = draw_figure(window2['canvas_som'].TKCanvas, fig1)
        while (True):
            event2, values2 = window2.read()
            if event2 == 'OK':
                window2.close()
                break
            if event2 == '-print-':
                som.plot_point_map(data, targets, ['Vehicles'], filename='images/som.png')
                som.plot_class_density(data, targets, t=0, name='Vehicles', filename='images/density.png')

    if event == 'Exit':
        window.close()
        break
pass
