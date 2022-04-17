import base64
import io
import sys
from tkinter import Image

import jsonpickle
from matplotlib import pyplot as plt


class EvGraph:
    def __init__(self, brand):
        self.brand = brand


    def graph(self):
        my_writer_obj = open("csvjson.txt", mode='r')
        json_data = my_writer_obj.read()
        print(json_data)
        print()

        self.Cars = jsonpickle.decode(json_data)
        self.range = []
        self.model = []

        for x in self.Cars:
            if (x['Brand'] == self.brand):
                self.range.append(x['Range'])
                self.model.append(x['Model'])

        self.fig = plt.figure()
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.bar(range, self.model)
        self.ax.set_ylabel('Range')

        plt.show()
        self.img_graph = io.BytesIO()
        plt.savefig(self.img_graph, format='png')
        self.image = base64.b64encode(self.img_graph.read())


        return self.image

        # self.brand = het merk weer een grafiek van gemaakt moet worden
        # Maak gwn een grafiek van elk model met de range om te beginnen
        # return moet een gehashte string zijn van de foto -> zie Server.py lijn 44