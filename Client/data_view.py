import base64
from io import BytesIO
import socket
import threading
import tkinter
from tkinter import *
from tkinter import simpledialog
from tkinter.simpledialog import askstring
from tkinter.ttk import Combobox, Separator

import jsonpickle
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pickle

from pyparsing import col


class DataView(Frame):
    def __init__(self, master, server):
        Frame.__init__(self, master)
        self.master = master
        self.server = server
        self.in_out_clh = self.server.s.makefile(mode='rw')
        threading.Thread(target=self.receive_messages).start()
        self.init_window()
        # self.makeConnnectionWithServer()

    def init_window(self):
        self.master.title("Electric cars")

        self.tabControl = ttk.Notebook(self.master)

        self.cars = ttk.Frame(self.tabControl)
        self.graph = ttk.Frame(self.tabControl)
        self.range = ttk.Frame(self.tabControl)
        self.compare = ttk.Frame(self.tabControl)

        self.tabControl.add(self.cars, text='Cars')
        self.tabControl.add(self.graph, text='Graph')
        self.tabControl.add(self.range, text='Range')
        self.tabControl.add(self.compare, text='Compare')
        self.tabControl.pack(expand=1, fill="both")

        self.icn_search = PhotoImage(file='../Assets/search.png').subsample(2)
        self.icn_speed = PhotoImage(file='../Assets/speed.png').subsample(2)
        self.icn_range = PhotoImage(file='../Assets/range.png').subsample(2)
        self.icn_effic = PhotoImage(file='../Assets/efficiency.png').subsample(2)
        self.icn_speed = PhotoImage(file='../Assets/speed.png').subsample(2)
        self.icn_drive = PhotoImage(file='../Assets/drive.png').subsample(2)
        self.icn_plug = PhotoImage(file='../Assets/plug.png').subsample(2)
        self.icn_fast = PhotoImage(file='../Assets/fast.png').subsample(2)
        self.icn_price = PhotoImage(file='../Assets/price.png').subsample(2)
        self.icn_seat = PhotoImage(file='../Assets/seat.png').subsample(2)
        self.icn_style = PhotoImage(file='../Assets/style.png').subsample(2)
        self.icn_segment = PhotoImage(file='../Assets/segment.png').subsample(2)

        Label(self.cars, text="Search a car", font=('Arial', 15, 'bold')).grid(row=0, column=0, sticky=E + W,columnspan=2)

        self.entry_search = Entry(self.cars, width=30)
        self.entry_search.grid(row=1, column=0, sticky=E + W, padx=(5, 5), pady=(5, 5))

        self.btn_search = Button(self.cars, image=self.icn_search, command=self.search_car, height=30, width=30)
        self.btn_search.grid(row=1, column=1, sticky=E +W, padx=(5, 5), pady=(5, 5))

        self.lst_searchresult = Listbox(self.cars)
        self.lst_searchresult.grid(row=2, column=0, columnspan=2, rowspan=5, sticky=W + E + N + S, padx=(5, 5),pady=(5, 5))
        self.lst_searchresult.bind('<<ListboxSelect>>', self.lst_callback)

        Button(self.cars, text='Disconnect', command=self.disconnect_from_server).grid(row=12, column=0, columnspan=2)

        self.spt_split = ttk.Separator(self.cars, orient='vertical').grid(row=0, column=2, rowspan=8, sticky=N + S,pady=(5, 5), padx=(5, 5), )

        self.txt_brand = StringVar()
        self.txt_brand.set("0")
        Label(self.cars, textvariable=self.txt_brand, font=('Arial', 15, 'bold')).grid(row=0, column=3, sticky=W,padx=(5, 5), pady=(5, 5))

        self.txt_model = StringVar()
        self.txt_model.set("0")
        Label(self.cars, textvariable=self.txt_model, font=('Arial', 15), height=1).grid(row=1, column=3, sticky=W,padx=(5, 5), pady=(5, 5))

        self.img_car_data = PhotoImage(file='../Assets/temp.png').subsample(2)
        self.img_car = Label(self.cars, image=self.img_car_data,width=400, height=200, )
        self.img_car.grid(row=0, column=4, rowspan=3,sticky=W + E, padx=(5, 5), pady=(5, 5))

        self.spt_split = ttk.Separator(self.cars, orient='horizontal').grid(row=3, column=3, columnspan=2, sticky=E + W)

        Label(self.cars, text="Specs", font=('Arial', 15, 'bold')).grid(row=4, column=3, sticky=E + W, columnspan=2,pady=(5, 5), padx=(5, 5))

        self.cnv_speccanvas_main = Canvas(self.cars, width=300, height=100)
        self.cnv_speccanvas_main.grid(row=5, column=3, columnspan=2)
        self.cnv_speccanvas_main.rowconfigure(11, weight=1)
        self.cnv_speccanvas_main.columnconfigure(1, weight=1)

        self.cnv_speccanvas1 = Canvas(
            self.cnv_speccanvas_main, width=300, height=100)
        self.cnv_speccanvas1.grid(row=0, column=0, sticky=W)

        self.cnv_speccanvas2 = Canvas(
            self.cnv_speccanvas_main, width=300, height=100)
        self.cnv_speccanvas2.grid(row=1, column=0, sticky=W)

        self.cnv_speccanvas3 = Canvas(
            self.cnv_speccanvas_main, width=300, height=100)
        self.cnv_speccanvas3.grid(row=2, column=0, sticky=W)

        self.cnv_speccanvas4 = Canvas(
            self.cnv_speccanvas_main, width=300, height=100)
        self.cnv_speccanvas4.grid(row=3, column=0, sticky=W)

        self.cnv_speccanvas5 = Canvas(
            self.cnv_speccanvas_main, width=300, height=100)
        self.cnv_speccanvas5.grid(row=4, column=0, sticky=W)

        self.cnv_speccanvas6 = Canvas(
            self.cnv_speccanvas_main, width=300, height=100)
        self.cnv_speccanvas6.grid(row=5, column=0, sticky=W)

        self.cnv_speccanvas7 = Canvas(
            self.cnv_speccanvas_main, width=300, height=100)
        self.cnv_speccanvas7.grid(row=6, column=0, sticky=W)

        self.cnv_speccanvas8 = Canvas(
            self.cnv_speccanvas_main, width=300, height=100)
        self.cnv_speccanvas8.grid(row=7, column=0, sticky=W)

        self.cnv_speccanvas9 = Canvas(
            self.cnv_speccanvas_main, width=300, height=100)
        self.cnv_speccanvas9.grid(row=8, column=0, sticky=W)

        self.cnv_speccanvas10 = Canvas(
            self.cnv_speccanvas_main, width=300, height=100)
        self.cnv_speccanvas10.grid(row=9, column=0, sticky=W)

        self.cnv_speccanvas11 = Canvas(
            self.cnv_speccanvas_main, width=300, height=100)
        self.cnv_speccanvas11.grid(row=10, column=0, sticky=W)

        self.cnv_speccanvas12 = Canvas(
            self.cnv_speccanvas_main, width=300, height=100)
        self.cnv_speccanvas12.grid(row=11, column=0, sticky=W)

        self.txt_topspeed = StringVar()
        self.txt_topspeed.set("0")
        Label(self.cnv_speccanvas1, image=self.icn_speed).pack(side=LEFT)
        Label(self.cnv_speccanvas1, text='Topspeed:',
              font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_speccanvas1, textvariable=self.txt_topspeed,
              font=('Arial', 15, 'bold')).pack(side=LEFT)
        Label(self.cnv_speccanvas1, text='km/h',
              font=('Arial', 15, 'bold')).pack(side=LEFT)

        self.txt_acceleration = StringVar()
        self.txt_acceleration.set("0")
        Label(self.cnv_speccanvas2, image=self.icn_speed).pack(side=LEFT)
        Label(self.cnv_speccanvas2, text='Acceleration:',
              font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_speccanvas2, textvariable=self.txt_acceleration,
              font=('Arial', 15, 'bold')).pack(side=LEFT)
        Label(self.cnv_speccanvas2, text='s', font=(
            'Arial', 15, 'bold')).pack(side=LEFT)

        self.txt_range = StringVar()
        self.txt_range.set("0")
        Label(self.cnv_speccanvas3, image=self.icn_range).pack(side=LEFT)
        Label(self.cnv_speccanvas3, text='Range:',
              font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_speccanvas3, textvariable=self.txt_range,
              font=('Arial', 15, 'bold')).pack(side=LEFT)
        Label(self.cnv_speccanvas3, text='km', font=(
            'Arial', 15, 'bold')).pack(side=LEFT)

        self.txt_efficiency = StringVar()
        self.txt_efficiency.set("0")
        Label(self.cnv_speccanvas4, image=self.icn_effic).pack(side=LEFT)
        Label(self.cnv_speccanvas4, text='Efficiency:',
              font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_speccanvas4, textvariable=self.txt_efficiency,
              font=('Arial', 15, 'bold')).pack(side=LEFT)
        Label(self.cnv_speccanvas4, text='Wh/km',
              font=('Arial', 15, 'bold')).pack(side=LEFT)

        self.txt_fastcharging = StringVar()
        self.txt_fastcharging.set("0")
        Label(self.cnv_speccanvas5, image=self.icn_fast).pack(side=LEFT)
        Label(self.cnv_speccanvas5, text='Fast charging:',
              font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_speccanvas5, textvariable=self.txt_fastcharging,
              font=('Arial', 15, 'bold')).pack(side=LEFT)
        Label(self.cnv_speccanvas5, text='km/h',
              font=('Arial', 15, 'bold')).pack(side=LEFT)

        self.txt_rapidcharging = StringVar()
        self.txt_rapidcharging.set("0")
        Label(self.cnv_speccanvas6, image=self.icn_fast).pack(side=LEFT)
        Label(self.cnv_speccanvas6, text='Rapid charging:',
              font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_speccanvas6, textvariable=self.txt_rapidcharging,
              font=('Arial', 15, 'bold')).pack(side=LEFT)

        self.txt_powertrain = StringVar()
        self.txt_powertrain.set("0")
        Label(self.cnv_speccanvas7, image=self.icn_drive).pack(side=LEFT)
        Label(self.cnv_speccanvas7, text='Power train:',
              font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_speccanvas7, textvariable=self.txt_powertrain,
              font=('Arial', 15, 'bold')).pack(side=LEFT)

        self.txt_plugtype = StringVar()
        self.txt_plugtype.set("0")
        Label(self.cnv_speccanvas8, image=self.icn_plug).pack(side=LEFT)
        Label(self.cnv_speccanvas8, text='Plug type:',
              font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_speccanvas8, textvariable=self.txt_plugtype,
              font=('Arial', 15, 'bold')).pack(side=LEFT)

        self.txt_bodystyle = StringVar()
        self.txt_bodystyle.set("0")
        Label(self.cnv_speccanvas9, image=self.icn_style).pack(side=LEFT)
        Label(self.cnv_speccanvas9, text='Body style:',
              font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_speccanvas9, textvariable=self.txt_bodystyle,
              font=('Arial', 15, 'bold')).pack(side=LEFT)

        self.txt_segment = StringVar()
        self.txt_segment.set("0")
        Label(self.cnv_speccanvas10, image=self.icn_segment).pack(side=LEFT)
        Label(self.cnv_speccanvas10, text='Segment:',
              font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_speccanvas10, textvariable=self.txt_segment,
              font=('Arial', 15, 'bold')).pack(side=LEFT)

        self.txt_seats = StringVar()
        self.txt_seats.set("0")
        Label(self.cnv_speccanvas11, image=self.icn_seat).pack(side=LEFT)
        Label(self.cnv_speccanvas11, text='Seats:',
              font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_speccanvas11, textvariable=self.txt_seats,
              font=('Arial', 15, 'bold')).pack(side=LEFT)

        self.txt_price = StringVar()
        self.txt_price.set("0")
        Label(self.cnv_speccanvas12, image=self.icn_price).pack(side=LEFT)
        Label(self.cnv_speccanvas12, text='Price:',
              font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_speccanvas12, textvariable=self.txt_price,
              font=('Arial', 15, 'bold')).pack(side=LEFT)
        Label(self.cnv_speccanvas12, text='euro', font=(
            'Arial', 15, 'bold')).pack(side=LEFT)

        Grid.rowconfigure(self.cars, 5, weight=1)
        Grid.columnconfigure(self.cars, 5, weight=1)

        # Graph
        self.HEIGHT = 400
        self.WIDTH = 1100
        self.canvas = Canvas(self.graph, height=self.HEIGHT, width=self.WIDTH)
        self.selected_brand = StringVar()
        self.combo = Combobox(self.graph, textvariable=self.selected_brand)
        self.combo.set('Choose a brand')
        self.combo.place(relx=0.0, rely=0.0, anchor=NW)
        self.combo.bind('<<ComboboxSelected>>', self.graphdata)

        self.img_graph_data = PhotoImage(file='../Assets/temp.png').subsample(2)
        self.canvas.create_image(self.WIDTH / 2,  self.HEIGHT / 2, anchor="center", image=self.img_graph_data)
        self.canvas.pack()

        # Range
        self.columns = ('model', 'brand', 'range','price')
        self.tree = ttk.Treeview(self.range, columns=self.columns, show='headings')
        self.tree.heading('model', text='Model')
        self.tree.heading('brand', text='Brand')
        self.tree.heading('range', text='Range')
        self.tree.heading('price', text='Price')
        self.tree.grid(row=1, column=1, sticky='nsew',rowspan=3)

        self.scrollbar = Scrollbar(self.range, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=1, column=2, sticky='ns')
        Label(self.range, text="Search a car by range", font=('Arial', 15, 'bold')).grid(row=0, column=0, sticky=E + W,columnspan=2)

        self.entry_range = Entry(self.range, width=30)
        self.entry_range.grid(row=1, column=0, sticky=E + W, padx=(5, 5), pady=(5, 5))

        self.btn_search = Button(self.range, image=self.icn_search, command=self.range_car, height=30, width=30)
        self.btn_search.grid(row=2, column=0, sticky=E + W, padx=(5, 5), pady=(5, 5))

        # Compare
        self.compare.rowconfigure(4, weight=1)
        self.compare.columnconfigure(3, weight=1)

        Label(self.compare, text="Car 1:", font=('Arial', 15)).grid(row=0, column=0, sticky=W)

        self.cmb_car1 = ttk.Combobox(self.compare, width=30)
        self.cmb_car1.grid(row=1, column=0)
        self.cmb_car1.bind('<<ComboboxSelected>>', self.callback_cmb_car1)

        ttk.Separator(self.compare, orient='horizontal').grid(row=2, column=0, sticky=E + W,pady=(5, 5), padx=(5, 5))
        
        self.txt_car_name_1 = StringVar()
        self.txt_car_name_1.set('Audi e-tron gt rs')
        Label(self.compare, textvariable=self.txt_car_name_1, font=('Arial', 15, 'bold')).grid(row=3, column=0)

        self.cnv_compare1 = Canvas(self.compare, width=300, height=100)
        self.cnv_compare1.grid(row=4, column=0)
        self.cnv_compare1.rowconfigure(11, weight=1)
        self.cnv_compare1.columnconfigure(1, weight=1)

        self.cnv_compare_1_1 = Canvas(self.cnv_compare1, width=300, height=100)
        self.cnv_compare_1_1.grid(row=0, column=0, sticky=W)

        self.cnv_compare_1_2 = Canvas(self.cnv_compare1, width=300, height=100)
        self.cnv_compare_1_2.grid(row=1, column=0, sticky=W)

        self.cnv_compare_1_3 = Canvas(self.cnv_compare1, width=300, height=100)
        self.cnv_compare_1_3.grid(row=2, column=0, sticky=W)

        self.cnv_compare_1_4 = Canvas(self.cnv_compare1, width=300, height=100)
        self.cnv_compare_1_4.grid(row=3, column=0, sticky=W)

        self.cnv_compare_1_5 = Canvas(self.cnv_compare1, width=300, height=100)
        self.cnv_compare_1_5.grid(row=4, column=0, sticky=W)

        self.cnv_compare_1_6 = Canvas(self.cnv_compare1, width=300, height=100)
        self.cnv_compare_1_6.grid(row=5, column=0, sticky=W)

        self.cnv_compare_1_7 = Canvas(self.cnv_compare1, width=300, height=100)
        self.cnv_compare_1_7.grid(row=6, column=0, sticky=W)

        self.cnv_compare_1_8 = Canvas(self.cnv_compare1, width=300, height=100)
        self.cnv_compare_1_8.grid(row=7, column=0, sticky=W)

        self.cnv_compare_1_9 = Canvas(self.cnv_compare1, width=300, height=100)
        self.cnv_compare_1_9.grid(row=8, column=0, sticky=W)

        self.cnv_compare_1_10 = Canvas(self.cnv_compare1, width=300, height=100)
        self.cnv_compare_1_10.grid(row=9, column=0, sticky=W)

        self.cnv_compare_1_11 = Canvas(self.cnv_compare1, width=300, height=100)
        self.cnv_compare_1_11.grid(row=10, column=0, sticky=W)

        self.cnv_compare_1_12 = Canvas(self.cnv_compare1, width=300, height=100)
        self.cnv_compare_1_12.grid(row=11, column=0, sticky=W)

        self.txt_topspeed_1 = StringVar()
        self.txt_topspeed_1.set("0")
        Label(self.cnv_compare_1_1, image=self.icn_speed).pack(side=LEFT)
        Label(self.cnv_compare_1_1, text='Topspeed:',font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_compare_1_1, textvariable=self.txt_topspeed_1,font=('Arial', 15, 'bold')).pack(side=LEFT)
        Label(self.cnv_compare_1_1, text='km/h',font=('Arial', 15, 'bold')).pack(side=LEFT)

        self.txt_acceleration_1 = StringVar()
        self.txt_acceleration_1.set("0")
        Label(self.cnv_compare_1_2, image=self.icn_speed).pack(side=LEFT)
        Label(self.cnv_compare_1_2, text='Acceleration:',font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_compare_1_2, textvariable=self.txt_acceleration_1,font=('Arial', 15, 'bold')).pack(side=LEFT)
        Label(self.cnv_compare_1_2, text='s', font=('Arial', 15, 'bold')).pack(side=LEFT)

        self.txt_range_1 = StringVar()
        self.txt_range_1.set("0")
        Label(self.cnv_compare_1_3, image=self.icn_range).pack(side=LEFT)
        Label(self.cnv_compare_1_3, text='Range:',font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_compare_1_3, textvariable=self.txt_range_1,font=('Arial', 15, 'bold')).pack(side=LEFT)
        Label(self.cnv_compare_1_3, text='km', font=('Arial', 15, 'bold')).pack(side=LEFT)

        self.txt_efficiency_1 = StringVar()
        self.txt_efficiency_1.set("0")
        Label(self.cnv_compare_1_4, image=self.icn_effic).pack(side=LEFT)
        Label(self.cnv_compare_1_4, text='Efficiency:',font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_compare_1_4, textvariable=self.txt_efficiency_1,font=('Arial', 15, 'bold')).pack(side=LEFT)
        Label(self.cnv_compare_1_4, text='Wh/km',font=('Arial', 15, 'bold')).pack(side=LEFT)

        self.txt_fastcharging_1 = StringVar()
        self.txt_fastcharging_1.set("0")
        Label(self.cnv_compare_1_5, image=self.icn_fast).pack(side=LEFT)
        Label(self.cnv_compare_1_5, text='Fast charging:',font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_compare_1_5, textvariable=self.txt_fastcharging_1,font=('Arial', 15, 'bold')).pack(side=LEFT)
        Label(self.cnv_compare_1_5, text='km/h',font=('Arial', 15, 'bold')).pack(side=LEFT)

        self.txt_rapidcharging_1 = StringVar()
        self.txt_rapidcharging_1.set("0")
        Label(self.cnv_compare_1_6, image=self.icn_fast).pack(side=LEFT)
        Label(self.cnv_compare_1_6, text='Rapid charging:',font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_compare_1_6, textvariable=self.txt_rapidcharging_1,font=('Arial', 15, 'bold')).pack(side=LEFT)

        self.txt_powertrain_1 = StringVar()
        self.txt_powertrain_1.set("0")
        Label(self.cnv_compare_1_7, image=self.icn_drive).pack(side=LEFT)
        Label(self.cnv_compare_1_7, text='Power train:',font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_compare_1_7, textvariable=self.txt_powertrain_1,font=('Arial', 15, 'bold')).pack(side=LEFT)

        self.txt_plugtype_1 = StringVar()
        self.txt_plugtype_1.set("0")
        Label(self.cnv_compare_1_8, image=self.icn_plug).pack(side=LEFT)
        Label(self.cnv_compare_1_8, text='Plug type:',font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_compare_1_8, textvariable=self.txt_plugtype_1,font=('Arial', 15, 'bold')).pack(side=LEFT)

        self.txt_bodystyle_1 = StringVar()
        self.txt_bodystyle_1.set("0")
        Label(self.cnv_compare_1_9, image=self.icn_style).pack(side=LEFT)
        Label(self.cnv_compare_1_9, text='Body style:',font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_compare_1_9, textvariable=self.txt_bodystyle_1,font=('Arial', 15, 'bold')).pack(side=LEFT)

        self.txt_segment_1 = StringVar()
        self.txt_segment_1.set("0")
        Label(self.cnv_compare_1_10, image=self.icn_segment).pack(side=LEFT)
        Label(self.cnv_compare_1_10, text='Segment:',font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_compare_1_10, textvariable=self.txt_segment_1,font=('Arial', 15, 'bold')).pack(side=LEFT)

        self.txt_seats_1 = StringVar()
        self.txt_seats_1.set("0")
        Label(self.cnv_compare_1_11, image=self.icn_seat).pack(side=LEFT)
        Label(self.cnv_compare_1_11, text='Seats:',font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_compare_1_11, textvariable=self.txt_seats_1,font=('Arial', 15, 'bold')).pack(side=LEFT)

        self.txt_price_1 = StringVar()
        self.txt_price_1.set("0")
        Label(self.cnv_compare_1_12, image=self.icn_price).pack(side=LEFT)
        Label(self.cnv_compare_1_12, text='Price:',font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_compare_1_12, textvariable=self.txt_price_1,font=('Arial', 15, 'bold')).pack(side=LEFT)
        Label(self.cnv_compare_1_12, text='euro', font=('Arial', 15, 'bold')).pack(side=LEFT)

        ttk.Separator(self.compare, orient='vertical').grid(row=0, column=1, rowspan=5, sticky=N + S)

        Label(self.compare, text="Car 2:", font=('Arial', 15)).grid(row=0, column=2, sticky=W)

        self.cmb_car2 = ttk.Combobox(self.compare, width=30)
        self.cmb_car2.grid(row=1, column=2)
        self.cmb_car2.bind('<<ComboboxSelected>>', self.callback_cmb_car2)

        ttk.Separator(self.compare, orient='horizontal').grid(row=2, column=2, sticky=E + W,pady=(5, 5), padx=(5, 5))
        
        self.txt_car_name_2 = StringVar()
        self.txt_car_name_2.set('Audi e-tron gt rs')
        Label(self.compare, textvariable=self.txt_car_name_2, font=('Arial', 15, 'bold')).grid(row=3, column=2)

        self.cnv_compare2 = Canvas(self.compare, width=300, height=100)
        self.cnv_compare2.grid(row=4, column=2)

        self.cnv_compare2.rowconfigure(11, weight=1)
        self.cnv_compare2.columnconfigure(1, weight=1)

        self.cnv_compare_2_1 = Canvas(self.cnv_compare2, width=300, height=100)
        self.cnv_compare_2_1.grid(row=0, column=0, sticky=W)

        self.cnv_compare_2_2 = Canvas(self.cnv_compare2, width=300, height=100)
        self.cnv_compare_2_2.grid(row=1, column=0, sticky=W)

        self.cnv_compare_2_3 = Canvas(self.cnv_compare2, width=300, height=100)
        self.cnv_compare_2_3.grid(row=2, column=0, sticky=W)

        self.cnv_compare_2_4 = Canvas(self.cnv_compare2, width=300, height=100)
        self.cnv_compare_2_4.grid(row=3, column=0, sticky=W)

        self.cnv_compare_2_5 = Canvas(self.cnv_compare2, width=300, height=100)
        self.cnv_compare_2_5.grid(row=4, column=0, sticky=W)

        self.cnv_compare_2_6 = Canvas(self.cnv_compare2, width=300, height=100)
        self.cnv_compare_2_6.grid(row=5, column=0, sticky=W)

        self.cnv_compare_2_7 = Canvas(self.cnv_compare2, width=300, height=100)
        self.cnv_compare_2_7.grid(row=6, column=0, sticky=W)

        self.cnv_compare_2_8 = Canvas(self.cnv_compare2, width=300, height=100)
        self.cnv_compare_2_8.grid(row=7, column=0, sticky=W)

        self.cnv_compare_2_9 = Canvas(self.cnv_compare2, width=300, height=100)
        self.cnv_compare_2_9.grid(row=8, column=0, sticky=W)

        self.cnv_compare_2_10 = Canvas(self.cnv_compare2, width=300, height=100)
        self.cnv_compare_2_10.grid(row=9, column=0, sticky=W)

        self.cnv_compare_2_11 = Canvas(self.cnv_compare2, width=300, height=100)
        self.cnv_compare_2_11.grid(row=10, column=0, sticky=W)

        self.cnv_compare_2_12 = Canvas(self.cnv_compare2, width=300, height=100)
        self.cnv_compare_2_12.grid(row=11, column=0, sticky=W)

        self.txt_topspeed_2 = StringVar()
        self.txt_topspeed_2.set("0")
        Label(self.cnv_compare_2_1, image=self.icn_speed).pack(side=LEFT)
        Label(self.cnv_compare_2_1, text='Topspeed:',font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_compare_2_1, textvariable=self.txt_topspeed_2,font=('Arial', 15, 'bold')).pack(side=LEFT)
        Label(self.cnv_compare_2_1, text='km/h',font=('Arial', 15, 'bold')).pack(side=LEFT)

        self.txt_acceleration_2 = StringVar()
        self.txt_acceleration_2.set("0")
        Label(self.cnv_compare_2_2, image=self.icn_speed).pack(side=LEFT)
        Label(self.cnv_compare_2_2, text='Acceleration:',font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_compare_2_2, textvariable=self.txt_acceleration_2,font=('Arial', 15, 'bold')).pack(side=LEFT)
        Label(self.cnv_compare_2_2, text='s', font=('Arial', 15, 'bold')).pack(side=LEFT)

        self.txt_range_2 = StringVar()
        self.txt_range_2.set("0")
        Label(self.cnv_compare_2_3, image=self.icn_range).pack(side=LEFT)
        Label(self.cnv_compare_2_3, text='Range:',font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_compare_2_3, textvariable=self.txt_range_2,font=('Arial', 15, 'bold')).pack(side=LEFT)
        Label(self.cnv_compare_2_3, text='km', font=('Arial', 15, 'bold')).pack(side=LEFT)

        self.txt_efficiency_2 = StringVar()
        self.txt_efficiency_2.set("0")
        Label(self.cnv_compare_2_4, image=self.icn_effic).pack(side=LEFT)
        Label(self.cnv_compare_2_4, text='Efficiency:',font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_compare_2_4, textvariable=self.txt_efficiency_2,font=('Arial', 15, 'bold')).pack(side=LEFT)
        Label(self.cnv_compare_2_4, text='Wh/km',font=('Arial', 15, 'bold')).pack(side=LEFT)

        self.txt_fastcharging_2 = StringVar()
        self.txt_fastcharging_2.set("0")
        Label(self.cnv_compare_2_5, image=self.icn_fast).pack(side=LEFT)
        Label(self.cnv_compare_2_5, text='Fast charging:',font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_compare_2_5, textvariable=self.txt_fastcharging_2,font=('Arial', 15, 'bold')).pack(side=LEFT)
        Label(self.cnv_compare_2_5, text='km/h',font=('Arial', 15, 'bold')).pack(side=LEFT)

        self.txt_rapidcharging_2 = StringVar()
        self.txt_rapidcharging_2.set("0")
        Label(self.cnv_compare_2_6, image=self.icn_fast).pack(side=LEFT)
        Label(self.cnv_compare_2_6, text='Rapid charging:',font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_compare_2_6, textvariable=self.txt_rapidcharging_2,font=('Arial', 15, 'bold')).pack(side=LEFT)

        self.txt_powertrain_2 = StringVar()
        self.txt_powertrain_2.set("0")
        Label(self.cnv_compare_2_7, image=self.icn_drive).pack(side=LEFT)
        Label(self.cnv_compare_2_7, text='Power train:',font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_compare_2_7, textvariable=self.txt_powertrain_2,font=('Arial', 15, 'bold')).pack(side=LEFT)

        self.txt_plugtype_2 = StringVar()
        self.txt_plugtype_2.set("0")
        Label(self.cnv_compare_2_8, image=self.icn_plug).pack(side=LEFT)
        Label(self.cnv_compare_2_8, text='Plug type:',font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_compare_2_8, textvariable=self.txt_plugtype_2,font=('Arial', 15, 'bold')).pack(side=LEFT)

        self.txt_bodystyle_2 = StringVar()
        self.txt_bodystyle_2.set("0")
        Label(self.cnv_compare_2_9, image=self.icn_style).pack(side=LEFT)
        Label(self.cnv_compare_2_9, text='Body style:',font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_compare_2_9, textvariable=self.txt_bodystyle_2,font=('Arial', 15, 'bold')).pack(side=LEFT)

        self.txt_segment_2 = StringVar()
        self.txt_segment_2.set("0")
        Label(self.cnv_compare_2_10, image=self.icn_segment).pack(side=LEFT)
        Label(self.cnv_compare_2_10, text='Segment:',font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_compare_2_10, textvariable=self.txt_segment_2,font=('Arial', 15, 'bold')).pack(side=LEFT)

        self.txt_seats_2 = StringVar()
        self.txt_seats_2.set("0")
        Label(self.cnv_compare_2_11, image=self.icn_seat).pack(side=LEFT)
        Label(self.cnv_compare_2_11, text='Seats:',font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_compare_2_11, textvariable=self.txt_seats_2,font=('Arial', 15, 'bold')).pack(side=LEFT)

        self.txt_price_2 = StringVar()
        self.txt_price_2.set("0")
        Label(self.cnv_compare_2_12, image=self.icn_price).pack(side=LEFT)
        Label(self.cnv_compare_2_12, text='Price:',font=('Arial', 15)).pack(side=LEFT)
        Label(self.cnv_compare_2_12, textvariable=self.txt_price_2,font=('Arial', 15, 'bold')).pack(side=LEFT)
        Label(self.cnv_compare_2_12, text='euro', font=('Arial', 15, 'bold')).pack(side=LEFT)



    def range_car(self):
        self.server.send_message_to_server('{"request": "range", "query": "' + self.entry_range.get() + '"}')
        print('click')

    def search_car(self):
        self.server.send_message_to_server('{"request": "search", "query": "' + self.entry_search.get() + '"}')

    def disconnect_from_server(self):
        self.server.close_connection()
        self.master.switch_frame("start", None)

    def callback_cmb_car1(self, event):
        self.server.send_message_to_server('{"request": "compare", "query": { "name": "' + self.cmb_car1.get() + '", "combo": "1" }}')

    def callback_cmb_car2(self, event):
        self.server.send_message_to_server('{"request": "compare", "query": { "name": "' + self.cmb_car2.get() + '", "combo": "2" }}')

    def lst_callback(self, event):
        for i in self.lst_searchresult.curselection():
            car = self.selected_cars[i]

            self.txt_topspeed.set(car.topspeed)
            self.txt_acceleration.set(car.accel)
            self.txt_range.set(car.range)
            self.txt_efficiency.set(car.efficiency)
            self.txt_fastcharging.set(car.fastcharge)
            self.txt_rapidcharging.set(car.rapidcharge)
            self.txt_powertrain.set(car.powertrain)
            self.txt_plugtype.set(car.plugtype)
            self.txt_brand.set(car.brand)
            self.txt_model.set(car.model)
            self.txt_bodystyle.set(car.bodystyle)
            self.txt_segment.set(car.segment)
            self.txt_seats.set(car.seats)
            self.txt_price.set(car.priceeuro)

            decodeit = open('image.png', 'wb')
            decodeit.write(base64.b64decode(car.photo))
            decodeit.close()
            self.img = (Image.open("image.png"))
            # Resize the Image using resize method
            self.resized_image = self.img.resize((425, 250), Image.ANTIALIAS)
            self.img_car_data = ImageTk.PhotoImage(self.resized_image)
            self.img_car.configure(image=self.img_car_data)

    def receive_messages(self):
        print('start')
        while True:
            commando = self.server.s.makefile(
                mode='rw').readline().rstrip('\n')
            commando = jsonpickle.decode(commando)

            if commando['return'] == 'search':
                print(commando['data'])
                self.selected_cars = commando['data']

                self.lst_searchresult.delete(0, END)

                i = 0
                for car in commando['data']:
                    self.lst_searchresult.insert(i, car)
                    i += 1

            elif commando['return'] == 'all':
                print('all')
                self.selected_cars = commando['data']
                seen = set()
                i = 0
                self.brand = []
                for car in commando['data']:
                    self.lst_searchresult.insert(i, car)
                    self.brand.append(car.brand)

                    i += 1

                seen = set()
                for x in self.brand:
                    if x not in seen:
                        self.combo['values'] = tuple(list(self.combo['values']) + [str(x)])
                        seen.add(x)
                    i += 1

                lijst = []
                for car in commando['data']:
                    self.tree.insert(parent="",index=i,values=(car.model,car.brand,car.range,car.priceeuro))
                    i += 1
                    lijst.append(car)

                self.cmb_car1['values'] = lijst
                self.cmb_car2['values'] = lijst

            elif commando['return'] == 'graph':
                print('graph')
                print(commando['data'])

                self.decodeit = open('graph.png', 'wb')
                self.decodeit.write(base64.b64decode(commando['data']))
                self.decodeit.close()

                # decodeit = open('image.png', 'wb')
                # decodeit.write(base64.b64decode(car.photo))
                # decodeit.close()

                self.img_graph_data = ImageTk.PhotoImage(Image.open('graph.png'))
                #self.img_graph.configure(image=self.img_graph_data)

            elif commando['return'] == 'range':
                print('range')
                print(commando['data'])
                self.tree.delete(*self.tree.get_children())
                for car in commando['data']:
                    self.tree.insert(parent="", index=i, values=(car.model, car.brand, car.range, car.priceeuro))
                    i += 1



            elif commando['return'] == 'message':
                messagebox.showinfo('Message from server', commando['data'])

            elif commando['return'] == 'compare1':
                car = commando['data']
                self.txt_topspeed_1.set(car.topspeed)
                self.txt_acceleration_1.set(car.accel)
                self.txt_range_1.set(car.range)
                self.txt_efficiency_1.set(car.efficiency)
                self.txt_fastcharging_1.set(car.fastcharge)
                self.txt_rapidcharging_1.set(car.rapidcharge)
                self.txt_powertrain_1.set(car.powertrain)
                self.txt_plugtype_1.set(car.plugtype)
                #self.txt_brand_1.set(car.brand)
                #self.txt_model_1.set(car.model)
                self.txt_bodystyle_1.set(car.bodystyle)
                self.txt_segment_1.set(car.segment)
                self.txt_seats_1.set(car.seats)
                self.txt_price_1.set(car.priceeuro)

            elif commando['return'] == 'compare2':
                car = commando['data']
                self.txt_topspeed_2.set(car.topspeed)
                self.txt_acceleration_2.set(car.accel)
                self.txt_range_2.set(car.range)
                self.txt_efficiency_2.set(car.efficiency)
                self.txt_fastcharging_2.set(car.fastcharge)
                self.txt_rapidcharging_2.set(car.rapidcharge)
                self.txt_powertrain_2.set(car.powertrain)
                self.txt_plugtype_2.set(car.plugtype)
                #self.txt_brand_2.set(car.brand)
                #self.txt_model_2.set(car.model)
                self.txt_bodystyle_2.set(car.bodystyle)
                self.txt_segment_2.set(car.segment)
                self.txt_seats_2.set(car.seats)
                self.txt_price_2.set(car.priceeuro)
                
    def graphdata(self, event):
        brand = self.selected_brand.get()
        self.server.send_message_to_server('{"request": "graph", "query": "' + brand + '"}')