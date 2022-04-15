import logging
import socket
import tkinter
from tkinter import *
import jsonpickle
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pickle


class DataView(Frame):
    def __init__(self, master, server):
        Frame.__init__(self, master)
        self.master = master
        self.server = server
        self.init_window()

    def init_window(self):
        self.master.title("Electric cars")
        self.pack(fill=BOTH, expand=1)

        self.icn_search = PhotoImage(file='../Assets/search.png').subsample(2)
        self.icn_speed = PhotoImage(file='../Assets/speed.png').subsample(2)
        self.icn_range = PhotoImage(file='../Assets/range.png').subsample(2)
        self.icn_effic = PhotoImage(file='../Assets/efficiency.png').subsample(2)
        self.icn_speed = PhotoImage(file='../Assets/speed.png').subsample(2)
        self.icn_drive = PhotoImage(file='../Assets/drive.png').subsample(2)
        self.icn_plug = PhotoImage(file='../Assets/plug.png').subsample(2)
        self.icn_fast = PhotoImage(file='../Assets/fast.png').subsample(2)

        Label(self, text="Search a car", font=('Arial', 15, 'bold')).grid(row=0, column=0, sticky=E + W, columnspan=2)

        self.entry_search = Entry(self, width=30)
        self.entry_search.grid(row=1, column=0, sticky=E + W, padx=(5, 5), pady=(5, 5))

        self.btn_search = Button(self, image=self.icn_search, height=30, width=30)
        self.btn_search.grid(row=1, column=1, sticky=E + W, padx=(5, 5), pady=(5, 5))

        self.lst_searchresult = Listbox(self)
        self.lst_searchresult.grid(row=2, column=0, columnspan=2, rowspan=5, sticky=W + E + N + S, padx=(5, 5),
                                   pady=(5, 5))

        self.spt_split = ttk.Separator(self, orient='vertical').grid(row=0, column=2, rowspan=8, sticky=N + S,pady=(5, 5), padx=(5, 5), )

        self.lbl_brand = Label(self, text="Audi", font=('Arial', 15, 'bold'))
        self.lbl_brand.grid(row=0, column=3, sticky=W, padx=(5, 5), pady=(5, 5))

        self.lbl_model = Label(self, text="E-Tron rs gt", font=('Arial', 15), height=1)
        self.lbl_model.grid(row=1, column=3, sticky=W, padx=(5, 5), pady=(5, 5))

        self.img_temp = PhotoImage(file='../Assets/temp.png').subsample(2)
        self.img_car = Label(self, width=400, height=200,image=self.img_temp)
        self.img_car.grid(row=0, column=4, rowspan=3, sticky=W + E, padx=(5, 5), pady=(5, 5))

        self.spt_split = ttk.Separator(self, orient='horizontal').grid(row=3, column=3, columnspan=2, sticky=E + W)

        Label(self, text="Specs", font=('Arial', 15, 'bold')).grid(row=4, column=3, sticky=E + W, columnspan=2,
                                                                   pady=(5, 5), padx=(5, 5))

        self.cnv_speccanvas_main = Canvas(self, width=300, height=100)
        self.cnv_speccanvas_main.grid(row=5, column=3, columnspan=2)
        self.cnv_speccanvas_main.rowconfigure(7, weight=1)
        self.cnv_speccanvas_main.columnconfigure(1, weight=1)

        self.cnv_speccanvas1 = Canvas(self.cnv_speccanvas_main, width=300, height=100)
        self.cnv_speccanvas1.grid(row=0, column=0, sticky=W)

        self.cnv_speccanvas2 = Canvas(self.cnv_speccanvas_main, width=300, height=100)
        self.cnv_speccanvas2.grid(row=1, column=0, sticky=W)

        self.cnv_speccanvas3 = Canvas(self.cnv_speccanvas_main, width=300, height=100)
        self.cnv_speccanvas3.grid(row=2, column=0, sticky=W)

        self.cnv_speccanvas4 = Canvas(self.cnv_speccanvas_main, width=300, height=100)
        self.cnv_speccanvas4.grid(row=3, column=0, sticky=W)

        self.cnv_speccanvas5 = Canvas(self.cnv_speccanvas_main, width=300, height=100)
        self.cnv_speccanvas5.grid(row=4, column=0, sticky=W)

        self.cnv_speccanvas6 = Canvas(self.cnv_speccanvas_main, width=300, height=100)
        self.cnv_speccanvas6.grid(row=5, column=0, sticky=W)

        self.cnv_speccanvas7 = Canvas(self.cnv_speccanvas_main, width=300, height=100)
        self.cnv_speccanvas7.grid(row=6, column=0, sticky=W)

        self.cnv_speccanvas8 = Canvas(self.cnv_speccanvas_main, width=300, height=100)
        self.cnv_speccanvas8.grid(row=7, column=0, sticky=W)

        Label(self.cnv_speccanvas1, image=self.icn_speed).pack(side=LEFT)
        Label(self.cnv_speccanvas1, text='Topspeed:', font=('Arial', 15)).pack(side=LEFT)
        self.lbl_topspeed = Label(self.cnv_speccanvas1, text='250', font=('Arial', 15, 'bold'))
        self.lbl_topspeed.pack(side=LEFT)
        Label(self.cnv_speccanvas1, text='km/h', font=('Arial', 15, 'bold')).pack(side=LEFT)

        Label(self.cnv_speccanvas2, image=self.icn_speed).pack(side=LEFT)
        Label(self.cnv_speccanvas2, text='Acceleration:', font=('Arial', 15)).pack(side=LEFT)
        self.lbl_acceleration = Label(self.cnv_speccanvas2, text='250', font=('Arial', 15, 'bold'))
        self.lbl_acceleration.pack(side=LEFT)
        Label(self.cnv_speccanvas2, text='s', font=('Arial', 15, 'bold')).pack(side=LEFT)

        Label(self.cnv_speccanvas3, image=self.icn_range).pack(side=LEFT)
        Label(self.cnv_speccanvas3, text='Range:', font=('Arial', 15)).pack(side=LEFT)
        self.lbl_range = Label(self.cnv_speccanvas3, text='250', font=('Arial', 15, 'bold'))
        self.lbl_range.pack(side=LEFT)
        Label(self.cnv_speccanvas3, text='km', font=('Arial', 15, 'bold')).pack(side=LEFT)

        Label(self.cnv_speccanvas4, image=self.icn_effic).pack(side=LEFT)
        Label(self.cnv_speccanvas4, text='Efficiency:', font=('Arial', 15)).pack(side=LEFT)
        self.lbl_efficiency = Label(self.cnv_speccanvas4, text='250', font=('Arial', 15, 'bold'))
        self.lbl_efficiency.pack(side=LEFT)
        Label(self.cnv_speccanvas4, text='Wh/km', font=('Arial', 15, 'bold')).pack(side=LEFT)

        Label(self.cnv_speccanvas5, image=self.icn_fast).pack(side=LEFT)
        Label(self.cnv_speccanvas5, text='Fast charging:', font=('Arial', 15)).pack(side=LEFT)
        self.lbl_fastcharging = Label(self.cnv_speccanvas5, text='250', font=('Arial', 15, 'bold'))
        self.lbl_fastcharging.pack(side=LEFT)
        Label(self.cnv_speccanvas5, text='km/h', font=('Arial', 15, 'bold')).pack(side=LEFT)

        Label(self.cnv_speccanvas6, image=self.icn_fast).pack(side=LEFT)
        Label(self.cnv_speccanvas6, text='Rapid charging:', font=('Arial', 15)).pack(side=LEFT)
        self.lbl_rapidcharging = Label(self.cnv_speccanvas6, text='No', font=('Arial', 15, 'bold'))
        self.lbl_rapidcharging.pack(side=LEFT)

        Label(self.cnv_speccanvas7, image=self.icn_drive).pack(side=LEFT)
        Label(self.cnv_speccanvas7, text='Power train:', font=('Arial', 15)).pack(side=LEFT)
        self.lbl_powertrain = Label(self.cnv_speccanvas7, text='AWD', font=('Arial', 15, 'bold'))
        self.lbl_powertrain.pack(side=LEFT)

        Label(self.cnv_speccanvas8, image=self.icn_plug).pack(side=LEFT)
        Label(self.cnv_speccanvas8, text='Plug type:', font=('Arial', 15)).pack(side=LEFT)
        self.lbl_plug = Label(self.cnv_speccanvas8, text='Type 2 CSS', font=('Arial', 15, 'bold'))
        self.lbl_plug.pack(side=LEFT)

        Grid.rowconfigure(self, 5, weight=1)
        Grid.columnconfigure(self, 5, weight=1)

        host = socket.gethostname()
        port = 9999
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.s.connect((host, port))






    def ask_image(self):
        try:
            pickle.dump("get_random_image", self.in_out_server)
            self.in_out_server.flush()

            #image binnenhalen
            answer = pickle.load(self.in_out_server)
            number_of_sends = int(answer)

            with open('received_file', 'wb+') as f:
                for i in range(0, number_of_sends):
                    data = self.s.recv(1024)
                    f.write(data)

            logging.info('Successfully get the image')

            # showing image
            im = Image.open('received_file')
            im.resize(400,200)
            self.img = ImageTk.PhotoImage(im)

            self.img_car['image'] = self.img
            #change size window
            width, height = im.size
            self.master.geometry("%dx%d" %(width, height))

        except Exception as ex:
            logging.error("Foutmelding: %s" % ex)
            messagebox.showinfo("Get image from server", "Something has gone wrong...")



    def disconnect_from_server(self):
        self.server.close_connection()
        self.master.switch_frame("start", None)


