import threading
import jsonpickle


class ClientHandler(threading.Thread):

    numbers_clienthandlers = 0

    def __init__(self, socketclient, messages_queue):
        threading.Thread.__init__(self)
        # connectie with client
        self.socketclient = socketclient
        # message queue -> link to gui server
        self.messages_queue = messages_queue
        # id clienthandler
        self.id = ClientHandler.numbers_clienthandlers
        self.in_out_clh = self.socketclient.makefile(mode='rw')
        ClientHandler.numbers_clienthandlers += 1

    def run(self):

        self.print_bericht_gui_server("Waiting for numbers...")

        commando = self.in_out_clh.readline().rstrip('\n')
        while commando != "CLOSE":
            # Code

            commando = self.in_out_clh.readline().rstrip('\n')

        self.print_bericht_gui_server("Connection with client closed...")
        self.socketclient.close()

    def print_bericht_gui_server(self, message):
        self.messages_queue.put(f"CLH {self.id}:> {message}")
