import base64
import logging
import socket
import threading
import os
import math
import pickle

import jsonpickle

from clienthandler import ClientHandler
from Models.EvCars import EvCars
from Models.EvCarsCalc import EvCarsCalc

class Server(threading.Thread):
    def __init__(self, host, port, messages_queue, gui):
        threading.Thread.__init__(self, name="Thread-Server", daemon=True)
        self.serversocket = None
        self.__is_connected = False
        self.host = host
        self.port = port
        self.messages_queue = messages_queue
        self.gui = gui

    @property
    def is_connected(self):
        return self.__is_connected

    def init_server(self):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind((self.host, self.port))
        self.serversocket.listen(5)
        self.__is_connected = True
        self.print_bericht_gui_server("SERVER STARTED")

        json_file = open("../Assets/cars.json", mode='r')
        json_data = json_file.read()

        self.cars = jsonpickle.decode(json_data)

        self.cars_object_list = []

        for car in self.cars:
            with open(f"../Assets/Img/Car/{car['Brand'].lower().replace(' ', '')}/{car['Model'].lower().replace(' ', '')}.png", "rb") as image2string: 
                car_object = EvCars(car['Brand'], car['Model'], car['Accel'], car['TopSpeed'], car['Range'], car['Efficiency'], car['FastCharge'], car['RapidCharge'], car['PowerTrain'], car['PlugType'], car['BodyStyle'], car['Segment'], car['Seats'], car['PriceEuro'], base64.b64encode(image2string.read()))
                self.cars_object_list.append(car_object)
    
        self.evcars_calc = EvCarsCalc(self.cars_object_list)

    def stop_server(self):
        if self.serversocket is not None:
            self.serversocket.close()
            self.serversocket = None
            self.__is_connected = False
            logging.info("Serversocket closed")

    def run(self):
        number_received_message = 0
        #try:
        while True:
            logging.debug("Server waiting for a new client")
            self.print_bericht_gui_server("waiting for a new client...")

            # establish a connection
            socket_to_client, addr = self.serversocket.accept()

            clh = ClientHandler(socket_to_client, addr, self.messages_queue, self.evcars_calc, self.gui)
            clh.start()
            

            self.print_bericht_gui_server(
                f"Current Thread count: {threading.active_count()}.")

        #except Exception as ex:
         #   self.print_bericht_gui_server(ex)
          #  logging.debug("Thread server ended")

    def print_bericht_gui_server(self, message):
        self.messages_queue.put(f"Server:> {message}")
