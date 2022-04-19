# https://pythonprogramming.net/python-3-tkinter-basics-tutorial/
import logging
import socket
from queue import Queue
from threading import Thread
from tkinter import *
from tkinter import ttk
from tkinter.tix import AUTO
from turtle import left

from pyparsing import col

from Server import Server
from clienthandler import ClientHandler


class ServerWindow(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.server = None
        self.thread_listener_queue = None
        self.init_messages_queue()

    def init_window(self):
        self.master.title("Server")
        self.pack(fill=BOTH, expand=1)

        # Tabs
        self.parent_tab = ttk.Notebook(self)

        self.master_tab = Frame(self.parent_tab)
        self.user_tab = Frame(self.parent_tab)
        self.stats_tab = Frame(self.parent_tab)

        self.parent_tab.add(self.master_tab, text="Server")
        self.parent_tab.add(self.user_tab, text="Users")
        self.parent_tab.add(self.stats_tab, text="Stats")

        self.parent_tab.pack(expand=1, fill=BOTH)

        # Master
        Label(self.master_tab, text="Log-berichten server:").grid(row=0)
        self.scrollbar = Scrollbar(self.master_tab, orient=VERTICAL)
        self.lstnumbers = Listbox(
            self.master_tab, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lstnumbers.yview)

        self.lstnumbers.grid(row=1, column=0, sticky=N + S + E + W)
        self.scrollbar.grid(row=1, column=1, sticky=N + S)

        self.btn_text = StringVar()
        self.btn_text.set("Start server")
        self.buttonServer = Button(self.master_tab, textvariable=self.btn_text, command=self.start_stop_server)
        self.buttonServer.grid(row=3, column=0, columnspan=2, pady=(5, 5), padx=(5, 5), sticky=N + S + E + W)

        Grid.rowconfigure(self.master_tab, 1, weight=1)
        Grid.columnconfigure(self.master_tab, 0, weight=1)

        # Users
        Label(self.user_tab, text="User list", font=(
            'Arial', 15, 'bold')).grid(row=0, column=0)

        self.cnv_user = Canvas(self.user_tab, width=300)
        self.cnv_user.grid(row=1, column=0, sticky=W + E)

        self.cnv_user.rowconfigure(10, weight=1)
        self.cnv_user.columnconfigure(4, weight=1)

        Grid.rowconfigure(self.master_tab, 2, weight=1)
        Grid.columnconfigure(self.master_tab, 0, weight=1)

        # Stats
        self.icn_search = PhotoImage(file='../Assets/search.png').subsample(2)
        self.icn_stat = PhotoImage(file='../Assets/stat.png').subsample(2)
        self.icn_all = PhotoImage(file='../Assets/all.png').subsample(2)


        Label(self.stats_tab, text="Stats", font=(
            'Arial', 15, 'bold')).grid(row=0, column=0, sticky=W+E)

        self.cnv_main = Canvas(self.stats_tab, width=300, height=500)
        self.cnv_main.grid(row=1, column=0, sticky=W + E)
        self.cnv_main.rowconfigure(3, weight=1)
        self.cnv_main.columnconfigure(1, weight=1)

        self.cnv_speccanvas1 = Canvas(self.cnv_main, width=300, height=100)
        self.cnv_speccanvas1.grid(row=0, column=0, sticky=W)

        self.cnv_speccanvas2 = Canvas(self.cnv_main, width=300, height=100)
        self.cnv_speccanvas2.grid(row=1, column=0, sticky=W)

        self.cnv_speccanvas3 = Canvas(self.cnv_main, width=300, height=100)
        self.cnv_speccanvas3.grid(row=2, column=0, sticky=W)

        self.txt_all = StringVar()
        self.txt_all.set('0')
        Label(self.cnv_speccanvas1, image=self.icn_all,font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_speccanvas1, text="All:",font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_speccanvas1, textvariable=self.txt_all, font=('Arial', 15, 'bold')).pack(side=LEFT)

        self.txt_search = StringVar()
        self.txt_search.set('0')
        Label(self.cnv_speccanvas2, image=self.icn_search,font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_speccanvas2, text="Search:",font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_speccanvas2, textvariable=self.txt_search, font=('Arial', 15, 'bold')).pack(side=LEFT)

        self.txt_graph = StringVar()
        self.txt_graph.set('0')
        Label(self.cnv_speccanvas3, image=self.icn_stat,font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_speccanvas3, text="Graph:",font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_speccanvas3, textvariable=self.txt_graph, font=('Arial', 15, 'bold')).pack(side=LEFT)

        Button(self.cnv_main, text='Refresh', command=self.refresh_stats).grid(row=3, column=0, sticky=W + E)

        Grid.rowconfigure(self.stats_tab, 3, weight=1)
        Grid.columnconfigure(self.stats_tab, 1, weight=1)

    def refresh_stats(self):
        stats = ClientHandler.search_list
        self.txt_all.set(stats['all'])
        self.txt_search.set(stats['search'])
        self.txt_graph.set(stats['graph'])

    def start_stop_server(self):
        if self.server is not None:
            self.__stop_server()
        else:
            self.__start_server()

    def __stop_server(self):
        self.server.stop_server()
        self.server = None
        logging.info("Server stopped")
        self.btn_text.set("Start server")

    def __start_server(self):
        self.server = Server(socket.gethostname(), 9999,
                             self.messages_queue, self)
        self.server.init_server()
        self.server.start()  # in thread plaatsen!
        logging.info("Server started")
        self.btn_text.set("Stop server")

    def init_messages_queue(self):
        self.messages_queue = Queue()
        self.thread_listener_queue = Thread(
            target=self.print_messsages_from_queue, name="Queue_listener_thread", daemon=True)
        self.thread_listener_queue.start()

    def print_messsages_from_queue(self):
        message = self.messages_queue.get()
        while message != "CLOSE_SERVER":
            self.lstnumbers.insert(END, message)
            self.messages_queue.task_done()
            message = self.messages_queue.get()

    def show_connected_users(self, clients):
        for child in self.cnv_user.winfo_children():
            child.destroy()

        i = 0
        for client in clients:
            Label(self.cnv_user, text=client.name, font=(
                "Arial", 15)).grid(row=i, column=0, sticky=W + E)
            Label(self.cnv_user, text=client.email, font=(
                "Arial", 15)).grid(row=i, column=1, sticky=W + E)
            Label(self.cnv_user, text=client.ip, font=("Arial", 15)).grid(
                row=i, column=2, sticky=W + E)
            Label(self.cnv_user, text=client.id, font=("Arial", 15)).grid(
                row=i, column=3, sticky=W + E)
            ttk.Separator(self.cnv_user, orient='horizontal').grid(
                row=i+1, column=0, columnspan=4, sticky=W + E)
            i += 2
