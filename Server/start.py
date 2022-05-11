import logging
import threading
from tkinter import *

from gui_server import ServerWindow

logging.basicConfig(level=logging.CRITICAL)

def callback():
    logging.debug("Active threads:")
    for thread in threading.enumerate():
        logging.debug(f">Thread name is {thread.getName()}.")
    root.destroy()

root = Tk()
root.geometry("600x500")
gui_server = ServerWindow(root)
root.protocol("WM_DELETE_WINDOW", callback)
root.mainloop()

