import PySimpleGUI as sg
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from SOM import SOM

layout = [[sg.Text('SOM для VAST 2017 MC1', font='Any 18')],
          # [sg.Text('Path to data'), sg.FileBrowse('output.txt', key='-Path-data-')],
          # [sg.Text('Path to target'), sg.FileBrowse('targets.txt', key='-Path-target-')],
          [sg.Text('Размер сетки SOM:'), sg.InputText('20', key='-width-', size=(2, 1)), sg.Text('на'),
           sg.InputText('20', key='-height-', size=(2, 1))],
          [sg.Text('Количество эпох'), sg.InputText(10000, key='-epochs-', size=(6, 1))],
          [sg.Text('Тип "Decay"'), sg.Radio('hill', 'DECAY', True, key='hill'),
           sg.Radio('linear', 'DECAY', key='linear')],
          [sg.Button('Начать расчет', key='-start-'), sg.Button('Выход', key="Exit")]
          ]

# create the form and show it without the plot
window = sg.Window('Аналитический инструмент для SOM',
                   layout, finalize=True)


def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


while True:
    event, values = window.read()
    if event == '-start-':
        data = np.loadtxt('output.txt', delimiter=';', usecols=range(40))

        som = SOM(int(values['-width-']), int(values['-height-']))  # initialize the SOM
        if values['hill']:
            som.fit(data, int(values['-epochs-']), decay='hill')
        if values['linear']:
            som.fit(data, int(values['-epochs-']), decay='linear')

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
        codes = ['1', '2', '3', '4', '5', '6', '2P']
        fig1 = som.plot_point_map_gui(data, targets, codes)
        # fig2 = som.plot_class_density_gui(data, targets, t=0, name=names[0])
        fig1.set_size_inches(7, 7)
        # fig2.set_size_inches(6, 6)
        figure1_x, figure1_y, figure1_w, figure1_h = fig1.bbox.bounds
        # figure_x, figure2_y, figure2_w, figure2_h = fig2.bbox.bounds

        layout2 = [[sg.Canvas(size=(figure1_w, figure1_h), key='canvas_som')],
                   [sg.OK('OK'), sg.Button('Print result', key='-print-')]
                   ]

        window2 = sg.Window('SOM Result',
                            layout2, finalize=True)

        # fig_canvas_agg = draw_figure(window2['canvas_density'].TKCanvas, fig2)
        fig_canvas_agg = draw_figure(window2['canvas_som'].TKCanvas, fig1)
        while True:
            event2, values2 = window2.read()
            if event2 == 'OK':
                window2.close()
                break
            if event2 == '-print-':
                som.plot_point_map(data, targets, names, filename='images/som.png')
                # som.plot_class_density(data, targets, t=0, name='Vehicles', filename='images/density.png')

    if event == 'Exit':
        window.close()
        break
pass
