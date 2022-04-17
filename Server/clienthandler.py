from multiprocessing.connection import Client
import threading
import jsonpickle
import json

from Models.EvCarsCalc import EvCarsCalc
from Models.EvGraph import EvGraph


class ClientHandler(threading.Thread):

    numbers_clienthandlers = 0

    client_list = []

    def __init__(self, socketclient, addr, messages_queue, evcars_calc, gui):
        threading.Thread.__init__(self)
        # connectie with client
        self.socketclient = socketclient
        # message queue -> link to gui server
        self.messages_queue = messages_queue
        # id clienthandler
        self.id = ClientHandler.numbers_clienthandlers
        self.in_out_clh = self.socketclient.makefile(mode='rw')
        ClientHandler.numbers_clienthandlers += 1
        self.gui = gui
        self.addr = addr

        self.evcars_calc = evcars_calc
        self.my_writer_obj = self.socketclient.makefile(mode='rw')

    def run(self):
        commando = self.in_out_clh.readline().rstrip('\n')

        client = jsonpickle.decode(commando)
        client.set_id_ip(self.addr[1], self.addr[0])
        ClientHandler.client_list.append(client)
        print(ClientHandler.client_list)
        self.gui.show_connected_users(ClientHandler.client_list)
        self.client = client

        commando = ''
        test = self.evcars_calc.all_cars()
        print(test)
        data = jsonpickle.encode(test)
        self.my_writer_obj.write('{"return": "all", "data": ' + data + '}\n')
        self.my_writer_obj.flush()

        while commando != "CLOSE":
            if commando != '':
                req = jsonpickle.decode(commando)

                if req['request'] == 'search':
                    data = jsonpickle.encode(self.evcars_calc.select_car(req['query']))
                    self.my_writer_obj.write('{"return": "search", "data": ' + data + '}\n')
                    self.my_writer_obj.flush()

                elif req['request'] == 'graph':
                    graph = EvGraph(req['query'])
                    self.my_writer_obj.write('{"return": "graph", "data": ' + graph.graph() + '}\n')
                    self.my_writer_obj.flush()

            commando = self.in_out_clh.readline().rstrip('\n')

        self.print_bericht_gui_server("Connection with client closed...")
        self.socketclient.close()
        ClientHandler.client_list.remove(self.client)
        self.gui.show_connected_users(ClientHandler.client_list)

    def print_bericht_gui_server(self, message):
        self.messages_queue.put(f"CLH {self.id}:> {message}")
