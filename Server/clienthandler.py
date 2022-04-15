import threading
import jsonpickle
import json

from Models.EvCarsCalc import EvCarsCalc


class ClientHandler(threading.Thread):

    numbers_clienthandlers = 0

    client_list = []

    def __init__(self, socketclient, messages_queue, evcars_calc):
        threading.Thread.__init__(self)
        # connectie with client
        self.socketclient = socketclient
        # message queue -> link to gui server
        self.messages_queue = messages_queue
        # id clienthandler
        self.id = ClientHandler.numbers_clienthandlers
        self.in_out_clh = self.socketclient.makefile(mode='rw')
        ClientHandler.numbers_clienthandlers += 1

        self.evcars_calc = evcars_calc
        self.my_writer_obj = self.socketclient.makefile(mode='rw')

    def run(self):
        commando = self.in_out_clh.readline().rstrip('\n')
        client = jsonpickle.decode(commando)
        ClientHandler.client_list.append(client)

        print(ClientHandler.client_list)

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
                    data = jsonpickle.encode(
                        self.evcars_calc.select_car(req['query']))
                    self.my_writer_obj.write(
                        '{"return": "search", "data": ' + data + '}\n')
                    self.my_writer_obj.flush()

            commando = self.in_out_clh.readline().rstrip('\n')

        self.print_bericht_gui_server("Connection with client closed...")
        self.socketclient.close()

    def print_bericht_gui_server(self, message):
        self.messages_queue.put(f"CLH {self.id}:> {message}")
