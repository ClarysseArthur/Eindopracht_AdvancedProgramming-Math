import socket
import pandas as pd

class Server():
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        port = 6666

        self.server_socket.bind((host, port))
        self.server_socket.listen(50)

        while True:
            print('Waiting for a client')
            self.client_socket, addr = self.server_socket.accept()

            print(f'Got a conection from {addr}')

            io_stream_client = self.client_socket.makefile(mode='rw')
            io_stream_client.write('Connected')
            io_stream_client.flush()
            
            self.socket_to_client, addr = self.server_socket.accept()
            io_stream_client = self.socket_to_client.makefile(mode='rw')
            commando = io_stream_client.readline().rstrip('\n')

            name = io_stream_client.readline().rstrip('\n')
            print(name)

            nick = io_stream_client.readline().rstrip('\n')
            print(f"Number 2: {nick}")

            mail = io_stream_client.readline().rstrip('\n')
            print(f"Number 2: {mail}")


class ReadingCSV():
    df = pd.read_csv('../Data/ElectricCarData_Norm.csv')

    def __init__(self):
        df = pd.read_csv('../Data/ElectricCarData_Norm.csv')
        print(df[['Brand','Model']])





#server = Server()
CSV = ReadingCSV()