import sys

from matplotlib import pyplot as plt


class EvGraph:
    def __init__(self, cars):
        self.cars = cars


    def graph(self):
        range = []
        price = []
        model = []

        for x in self.cars:
            if (x['Brand'] == 'Tesla'):
                range.append(x['Range'])
                model.append(x['Model'])
                #price.append(x['PriceEuro'])

        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(range, model)
        ax.set_ylabel('Range')

        plt.show()