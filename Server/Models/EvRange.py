import jsonpickle


class EvRange:
    def __init__(self, cars):
        self.cars = cars

    def rangecar(self, query):
        car = []
        for x in self.cars:
            if int(x.range) >= int(query):
                car.append(x)
        print(car)
        return car
