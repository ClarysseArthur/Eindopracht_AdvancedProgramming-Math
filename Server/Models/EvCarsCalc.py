import sys


class EvCarsCalc:
    def __init__(self, cars):
        self.cars = cars

    def select_car(self, query):
        return_list = []
        for car in self.cars:
            search = f' {str(car.brand).lower()} {str(car.model).lower()} '

            if str(query).lower() in search:
                return_list.append(car)
            else:
                pass

        print (return_list)
        return return_list

    def all_cars(self):
        sys.setrecursionlimit(3000)
        return self.cars

    def compare_car(self, query):
        for car in self.cars:
            if str(car) == query:
                return car