# https://pythonprogramming.net/python-3-tkinter-basics-tutorial/
from argparse import Action
import logging
import socket
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import jsonpickle

from data_view import DataView


class StartApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.switch_frame("start", None)

    # we switchen tss 3 frames: startframe <> bmiframe, startframe <> numbersframe

    def switch_frame(self, name_class, server):
        """Destroys current frame and replaces it with a new one."""
        if self._frame is not None:
            self._frame.destroy()

        if name_class == "start":
            new_frame = Start(self)
        elif name_class == "data":
            new_frame = DataView(self, server)

        if new_frame is not None:
            self._frame = new_frame
            self._frame.pack()


class Start(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.init_window(master)

    def init_window(self, master):
        self.master.title("Connect to server")
        self.pack(fill=BOTH, expand=1)

        Label(self, text="Username:").grid(row=0, sticky=E)
        Label(self, text="Email:", pady=10).grid(row=1, sticky=E)

        self.entry_username = Entry(self, width=40)
        self.entry_email = Entry(self, width=40)

        self.entry_username.grid(
            row=0, column=1, sticky=E + W, padx=(5, 5), pady=(5, 5))
        self.entry_email.grid(row=1, column=1, sticky=E +
                              W, padx=(5, 5), pady=(5, 0))

        self.btn_connect = Button(
            self, text="Connect to sever", command=lambda: self.make_connection_server(master))
        self.btn_connect.grid(row=3, column=0, columnspan=2, pady=(
            0, 5), padx=(5, 5), sticky=N + S + E + W)

        Grid.rowconfigure(self, 2, weight=1)
        Grid.columnconfigure(self, 1, weight=1)

    def __del__(self):
        logging.info("Closing frame")
        self.close_connection()

    def make_connection_server(self, master):
        if (self.entry_username.get() != '' and self.entry_email.get() != ''):
            logging.info("Making connection with server...")

            host = socket.gethostname()
            port = 9999
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            self.s.connect((host, port))
            self.in_out_server = self.s.makefile(mode='rw')
            logging.info("Open connection with server succesfully")

            master.switch_frame("data", self)

        else:
            messagebox.showerror("Connect to server",
                                 "All fields must be filled in!")

    def close_connection(self):
        try:
            logging.info("Close connection with server...")
            self.in_out_server.write("CLOSE\n")
            self.in_out_server.flush()
            self.s.close()
        except Exception as ex:
            logging.error("Error: close connection with server failed")


logging.basicConfig(level=logging.INFO)

root = StartApp()
root.mainloop()
