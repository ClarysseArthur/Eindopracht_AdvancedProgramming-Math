# https://pythonprogramming.net/python-3-tkinter-basics-tutorial/
from argparse import Action
import logging
import socket
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import jsonpickle



class DataView(Frame):
    def __init__(self, master, server):
        Frame.__init__(self, master)
        self.master = master
        self.server = server
        self.init_window()

    def init_window(self):
        self.master.title("Connect to server")
        self.pack(fill=BOTH, expand=1)

        self.btn_connect = Button(
            self, text="Disconnect from server", command=self.disconnect_from_server)
        self.btn_connect.grid(row=3, column=0, columnspan=2, pady=(
            0, 5), padx=(5, 5), sticky=N + S + E + W)

        Grid.rowconfigure(self, 2, weight=1)
        Grid.columnconfigure(self, 1, weight=1)

    def disconnect_from_server(self):
        self.server.close_connection()
        self.master.switch_frame("start", None)
