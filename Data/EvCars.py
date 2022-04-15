import jsonpickle


class EvCars:
    my_writer_obj = open("../Data/csvjson.txt", mode='r')
    json_data = my_writer_obj.read()
    print(json_data)
    print()

    Cars = jsonpickle.decode(json_data)

    def __init__(self, par_brand, par_model, par_accel, par_topspeed, par_range, par_efficiency, par_fastcharge,
                 par_rapidcharge, par_powertrain, par_plugtype, par_bodystyle, par_segment, par_seats, par_priceeuro):
        self.__car = EvCars.Cars

    @staticmethod
    def AllCars():
        carmodelandbrand = []
        for x in EvCars.Cars:
            y = x['Brand'],x['Model']
            carmodelandbrand.append(y)
        return carmodelandbrand
