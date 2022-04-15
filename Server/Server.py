import logging
import socket
import threading
import os
import math
import pickle

import jsonpickle

from clienthandler import ClientHandler
from Data.EvCars import EvCars
class Server(threading.Thread):
    def __init__(self, host, port, messages_queue):
        threading.Thread.__init__(self, name="Thread-Server", daemon=True)
        self.serversocket = None
        self.__is_connected = False
        self.host = host
        self.port = port
        self.messages_queue = messages_queue

    @property
    def is_connected(self):
        return self.__is_connected

    def init_server(self):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind((self.host, self.port))
        self.serversocket.listen(5)
        self.__is_connected = True
        self.print_bericht_gui_server("SERVER STARTED")

    def stop_server(self):
        if self.serversocket is not None:
            self.serversocket.close()
            self.serversocket = None
            self.__is_connected = False
            logging.info("Serversocket closed")

    def run(self):
        number_received_message = 0
        try:
            while True:
                logging.debug("Server waiting for a new client")
                self.print_bericht_gui_server("waiting for a new client...")

                # establish a connection
                socket_to_client, addr = self.serversocket.accept()
                self.print_bericht_gui_server(f"Got a connection from {addr}")
                clh = ClientHandler(socket_to_client, self.messages_queue)
                clh.start()




        except Exception as ex:
            self.print_bericht_gui_server("Serversocket afgesloten")
            logging.debug("Thread server ended")


    def print_bericht_gui_server(self, message):
        self.messages_queue.put(f"Server:> {message}")


    def send_image(self):

        filename = '../Assets/Auto/tesla/modelslongrange.png'
        f = open(filename, 'rb')
        print(os.path.getsize(filename))

        size_in_bytes = os.path.getsize(filename)

        number_sends = size_in_bytes // 1024
        print(math.ceil(size_in_bytes / 1024))
        print(number_sends)

        pickle.dump("%d" % number_sends, self.in_out_clh)
        self.in_out_clh.flush()
        self.print_bericht_gui_server(f"Current Thread count: {threading.active_count()}.")
        l = f.read(1024)
        while (l):
            self.socketclient.send(l)
            # volgende 1024 bytes inlezen
            l = f.read(1024)
