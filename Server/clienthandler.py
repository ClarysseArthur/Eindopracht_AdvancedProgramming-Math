import threading
import jsonpickle
from Models.EvGraph import EvGraph


class ClientHandler(threading.Thread):

    numbers_clienthandlers = 0

    client_list = []
    search_list = {'all': 0, 'search': 0, 'graph': 0, 'range': 0, 'compare': 0}
    request_list = []

    def __init__(self, socketclient, addr, messages_queue, evcars_calc, evcars_range, gui):
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
        self.evcars_range = evcars_range
        self.my_writer_obj = self.socketclient.makefile(mode='rw')

    def run(self):
        commando = self.in_out_clh.readline().rstrip('\n')

        client = jsonpickle.decode(commando)
        client.set_id_ip_writer(self.addr[1], self.addr[0], self.my_writer_obj)
        ClientHandler.client_list.append(client)
        self.gui.show_connected_users(ClientHandler.client_list)
        self.client = client
        self.print_bericht_gui_server(f'New client: {client}')

        commando = ''
        list_cars = self.evcars_calc.all_cars()
        list_cars = sorted(list_cars)
        data = jsonpickle.encode(list_cars)
        client.writer.write('{"return": "all", "data": ' + data + '}\n')
        client.writer.flush()
        ClientHandler.search_list['all'] += 1
        self.print_bericht_gui_server(f'Send ALL info for startup to {client}')

        while commando != "CLOSE":
            if commando != '':
                req = jsonpickle.decode(commando)

                if req['request'] == 'search':
                    data = jsonpickle.encode(self.evcars_calc.select_car(req['query']))
                    client.writer.write('{"return": "search", "data": ' + data + '}\n')
                    client.writer.flush()
                    ClientHandler.search_list['search'] += 1
                    self.print_bericht_gui_server(f'Send SEARCH info after request from {client}')
                    ClientHandler.request_list.append([client, f"{client} searched for \'{req['query']}\'"])

                elif req['request'] == 'graph':
                    graph = EvGraph(req['query'])
                    client.writer.write('{"return": "graph", "data": "' + str(graph.graph()) + '"}\n')
                    client.writer.flush()
                    ClientHandler.search_list['graph'] += 1
                    self.print_bericht_gui_server(f'Send GRAPH info after request from {client}')
                    ClientHandler.request_list.append([client, f"{client} graphed \'{req['query']}\'"])

                elif req['request'] == 'range':
                    data = jsonpickle.encode(sorted(self.evcars_range.rangecar(req['query'])))
                    client.writer.write('{"return": "range", "data": ' + data + '}\n')
                    client.writer.flush()
                    ClientHandler.search_list['range'] += 1
                    self.print_bericht_gui_server(f'Send RANGE info after request from {client}')
                    ClientHandler.request_list.append([client, f"{client} RANGED \'{req['query']}\'"])

                elif req['request'] == 'compare':
                    data = jsonpickle.encode(self.evcars_calc.compare_car(req['query']['name']))

                    if req['query']['combo'] == '1':
                        client.writer.write('{"return": "compare1", "data": ' + data + '}\n')
                    else:
                        client.writer.write('{"return": "compare2", "data": ' + data + '}\n')
                    client.writer.flush()
                    ClientHandler.search_list['compare'] += 1
                    self.print_bericht_gui_server(f'Send {str(data)} to compare - {client}')
                    ClientHandler.request_list.append([client, f"{client} compared \'{req['query']['name']}\'"])

            commando = self.in_out_clh.readline().rstrip('\n')

        self.print_bericht_gui_server(f"Connection with {client} closed...")
        self.socketclient.close()
        ClientHandler.client_list.remove(self.client)
        self.gui.show_connected_users(ClientHandler.client_list)

    def print_bericht_gui_server(self, message):
        self.messages_queue.put(f"CLH {self.id}:> {message}")