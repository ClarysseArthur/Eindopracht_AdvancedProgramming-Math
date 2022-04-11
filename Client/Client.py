# https://pythonprogramming.net/python-3-tkinter-basics-tutorial/
import logging
import socket
from tkinter import *
from tkinter import messagebox


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("Connect to a server")

        self.pack(fill=BOTH, expand=1)

        Label(self, text="Naam:").grid(row=0, sticky=E)
        Label(self, text="Nickname:").grid(row=1, sticky=E)
        Label(self, text="Email:").grid(row=2, sticky=E)

        self.name = Entry(self, width=40)
        self.name.grid(row=0, column=1, sticky=E + W, padx=(5, 5), pady=(5, 5))

        self.nick = Entry(self, width=40)
        self.nick.grid(row=1, column=1, sticky=E + W, padx=(5, 5), pady=(5, 5))

        self.mail = Entry(self, width=40)
        self.mail.grid(row=2, column=1, sticky=E + W, padx=(5, 5), pady=(5, 5))

        Button(self, text="Connect to the server", command=self.make_connection_with_server).grid(
            row=4, column=0, columnspan=2, pady=(0, 5), padx=(5, 5), sticky=N + S + E + W)

        Grid.rowconfigure(self, 4, weight=1)
        Grid.columnconfigure(self, 1, weight=1)

    def __del__(self):
        self.close_connection()

    def make_connection_with_server(self):
        try:
            logging.info("Making connection with server...")
            host = socket.gethostname()
            port = 6666
            self.socket_to_server = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            self.socket_to_server.connect((host, port))
            self.my_writer_obj = self.socket_to_server.makefile(mode='rw')
            logging.info("Open connection with server succesfully")

            self.my_writer_obj.write(self.name.get())
            self.my_writer_obj.flush()
            self.my_writer_obj.write(self.nick.get())
            self.my_writer_obj.flush()
            self.my_writer_obj.write(self.mail.get())
            self.my_writer_obj.flush()

        except Exception as ex:
            logging.error(f"Foutmelding: {ex}")

    def close_connection(self):
        try:
            logging.info("Close connection with server...")
            self.my_writer_obj.write("CLOSE\n")
            self.my_writer_obj.flush()
            self.socket_to_server.close()
        except Exception as ex:
            logging.error(f"Foutmelding: {ex}")
            messagebox.showinfo("Sommen", "Something has gone wrong...")


logging.basicConfig(level=logging.INFO)

root = Tk()
# root.geometry("400x300")
app = Window(root)
root.mainloop()
