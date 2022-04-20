# https://pythonprogramming.net/python-3-tkinter-basics-tutorial/
from email import message
import logging
import socket
from queue import Queue
from sqlite3 import Row
from threading import Thread
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.tix import AUTO
from turtle import left, st, width
from numpy import imag

from pyparsing import col
from sklearn.utils import column_or_1d

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
        self.lstnumbers = Listbox(self.master_tab, yscrollcommand=self.scrollbar.set)
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
        Label(self.user_tab, text="User list", font=('Arial', 15, 'bold')).grid(row=0, column=0, columnspan=2, sticky=W)

        self.lst_clients = ttk.Treeview(self.user_tab, columns=('user', 'mail', 'ip', 'id'), show='headings')
        self.lst_clients.grid(row=1, column=0, columnspan=2, rowspan=2, sticky=E + W)
        self.lst_clients.heading('user', text='User Name')
        self.lst_clients.heading('mail', text='E-mail')
        self.lst_clients.heading('ip', text='IP address')
        self.lst_clients.heading('id', text='id')
        self.lst_clients.column('user', width=100)
        self.lst_clients.column('mail', width=100)
        self.lst_clients.column('ip', width=100)
        self.lst_clients.column('id', width=100)
        self.lst_clients.bind('<<TreeviewSelect>>', self.lst_callback)

        self.txt_message_to_client = Text(self.user_tab, width=20, height=1.5)
        self.txt_message_to_client.grid(row=3, column=0, sticky=E + W,padx=(5, 5))

        self.icn_send = PhotoImage(file='../Assets/send.png').subsample(2)
        self.btnsend_message = Button(self.user_tab, image=self.icn_send, width=30, height=30, command=self.send_message_to_client)
        self.btnsend_message.grid(row=3, column=1, sticky=W, padx=(5, 5))

        ttk.Separator(self.user_tab, orient='vertical').grid(row=0, column=3, rowspan=4, sticky=N + S,pady=(5, 5), padx=(5, 5), )

        Label(self.user_tab, text="History", font=('Arial', 15, 'bold')).grid(row=0, column=4, sticky=W)

        self.cnv_history = Canvas(self.user_tab)
        self.cnv_history.grid(row=1, column=4, sticky=W+E)

        variable = StringVar(self.cnv_history)
        variable.set("All")
        self.cmb_clients = ttk.Combobox(self.cnv_history, textvariable=variable)
        self.cmb_clients.pack(side=LEFT)
        self.cmb_clients.bind('<<ComboboxSelected>>', self.combobox_callback)

        self.icn_refresh = PhotoImage(file='../Assets/refresh.png').subsample(2)
        self.btn_refresh_history = Button(self.cnv_history, image=self.icn_refresh, command=self.refresh_user_data)
        self.btn_refresh_history.pack(side=LEFT)

        self.lst_history = Listbox(self.user_tab, width=50)
        self.lst_history.grid(row=2, column=4, rowspan=2, sticky=N + E + S + W)

        Grid.rowconfigure(self.master_tab, 2, weight=1)
        Grid.columnconfigure(self.master_tab, 2, weight=1)

        # Stats
        self.icn_search = PhotoImage(file='../Assets/search.png').subsample(2)
        self.icn_stat = PhotoImage(file='../Assets/stat.png').subsample(2)
        self.icn_all = PhotoImage(file='../Assets/all.png').subsample(2)


        Label(self.stats_tab, text="Stats", font=('Arial', 15, 'bold')).grid(row=0, column=0, sticky=W+E)

        self.cnv_main = Canvas(self.stats_tab, width=300, height=500)
        self.cnv_main.grid(row=1, column=0, sticky=W + E)
        self.cnv_main.rowconfigure(3, weight=1)
        self.cnv_main.columnconfigure(4, weight=1)

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

        Button(self.cnv_main, text='Refresh', command=self.refresh_stats).grid(row=3, column=0, sticky=W)

        Grid.rowconfigure(self.stats_tab, 3, weight=1)
        Grid.columnconfigure(self.stats_tab, 1, weight=1)

    def refresh_stats(self):
        stats = ClientHandler.search_list
        self.txt_all.set(stats['all'])
        self.txt_search.set(stats['search'])
        self.txt_graph.set(stats['graph'])

    def lst_callback(self, event):
        for selected_item in self.lst_clients.selection():
            item = self.lst_clients.item(selected_item)
            print(item)

    def refresh_user_data(self):
        self.lst_history.delete(0, END)
        lijst = []
        lijst_unique = []
        
        for i, x in enumerate(ClientHandler.request_list):
            lijst.append(x[0])
            self.lst_history.insert(i, x[1])

        for x in lijst:
            if x not in lijst_unique:
                lijst_unique.append(x)

        self.cmb_clients['values'] = lijst_unique

    def send_message_to_client(self):
        item = ''

        for selected_item in self.lst_clients.selection():
            item = self.lst_clients.item(selected_item)

        print(item)

        if item != '' and self.txt_message_to_client != '':
            for client in ClientHandler.client_list:
                if client.id == item['values'][3]:
                    print('{"return": "message", "data": "' + self.txt_message_to_client.get("1.0",'end-1c') + '"}\n')
                    client.writer.write('{"return": "message", "data": "' + self.txt_message_to_client.get("1.0",'end-1c') + '"}\n')
                    client.writer.flush()
        else:
            messagebox.showerror('Error sending message!', 'There must be a client selected \nTextbox must not be empty')

    def start_stop_server(self):
        if self.server is not None:
            self.__stop_server()
        else:
            self.__start_server()
            self.lst_history.insert(0, 'No data yet (refresh)')

    def combobox_callback(self, event):
        selected = self.cmb_clients.get()
        self.lst_history.delete(0, END)
        for i, x in enumerate(ClientHandler.request_list):
            if str(x[0]) == selected:
                self.lst_history.insert(i, x[1])   

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
        for selected_item in self.lst_clients.get_children():
            self.lst_clients.delete(selected_item)

        for index, client in enumerate(clients):
            text = (client.name, client.email, client.ip, client.id)
            self.lst_clients.insert('', END, values=text)
