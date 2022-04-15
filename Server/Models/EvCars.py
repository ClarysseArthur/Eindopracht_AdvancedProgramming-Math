from pyexpat import model
import jsonpickle
from sklearn.preprocessing import PowerTransformer


class EvCars:
    def __init__(self, brand, model, accel, topspeed, range, efficiency, fastcharge, rapidcharge, powertrain, plugtype, bodystyle, segment, seats, priceeuro, photo):
        self.__brand = brand
        self.__model = model
        self.__accel = accel
        self.__topspeed = topspeed
        self.__range = range
        self.__efficiency = efficiency
        self.__fastcharge = fastcharge
        self.__rapidcharge = rapidcharge
        self.__powertrain = powertrain
        self.__plugtype = plugtype
        self.__bodystyle = bodystyle
        self.__segment = segment
        self.__seats = seats
        self.__priceeuro = priceeuro
        self.__photo = photo

    @property
    def brand(self):
        return self.__brand

    @property
    def model(self):
        return self.__model

    @property
    def accel(self):
        return self.__accel

    @property
    def topspeed(self):
        return self.__topspeed

    @property
    def range(self):
        return self.__range

    @property
    def efficiency(self):
        return self.__efficiency

    @property
    def fastcharge(self):
        return self.__fastcharge

    @property
    def rapidcharge(self):
        return self.__rapidcharge

    @property
    def powertrain(self):
        return self.__powertrain

    @property
    def plugtype(self):
        return self.__plugtype

    @property
    def bodystyle(self):
        return self.__bodystyle

    @property
    def segment(self):
        return self.__segment

    @property
    def seats(self):
        return self.__seats

    @property
    def priceeuro(self):
        return self.__priceeuro

    @property
    def photo(self):
        return self.__photo

    def __str__(self):
        return f'{self.brand}, {self.model}'

    def __repr__(self):
        return f'{self.brand}, {self.model}'

    def __gt__ (self, other):
        if self.model > other.model:
            return self
        else:
            return self
