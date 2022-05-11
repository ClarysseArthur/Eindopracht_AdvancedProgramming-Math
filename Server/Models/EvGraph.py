import base64
import jsonpickle
from matplotlib import pyplot as plt

class EvGraph:
    def __init__(self, brand):
        self.brand = brand

    def graph(self):
        my_writer_obj = open("../Assets/cars.json", mode='r')
        json_data = my_writer_obj.read()

        self.Cars = jsonpickle.decode(json_data)
        self.range = []
        self.model = []

        for x in self.Cars:
            if (x['Brand'] == self.brand):
                self.range.append(x['Range'])
                self.model.append(x['Model'])

        self.fig = plt
        self.fig.clf();
        self.fig.xticks(rotation=80)
        self.fig.xlabel("Model")
        self.fig.ylabel("Range in km")
        self.fig.title(f"Range per model - {self.brand}")
        self.fig.bar(self.model, self.range,color='green')
        self.fig.tight_layout()


        self.fig.savefig('graph.png')
        with open(f"graph.png", "rb") as image2string: 
            self.imageString = base64.b64encode(image2string.read())

        return self.imageString
