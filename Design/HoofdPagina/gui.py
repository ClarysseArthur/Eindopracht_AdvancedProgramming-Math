# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from PIL import Image
from PIL import ImageTk


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("951x633")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=633,
    width=951,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    699.5,
    379.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#E6E6E6",
    highlightthickness=0
)
entry_1.place(
    x=480.0,
    y=358.0,
    width=439.0,
    height=40.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    699.5,
    545.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#E6E6E6",
    highlightthickness=0
)
entry_2.place(
    x=480.0,
    y=524.0,
    width=439.0,
    height=40.0
)

canvas.create_text(
    481.0,
    526.0,
    anchor="nw",
    text="Testje 2132",
    fill="#000000",
    font=("Inter", 12 * -1)
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    699.5,
    489.5,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#E6E6E6",
    highlightthickness=0
)
entry_3.place(
    x=480.0,
    y=468.0,
    width=439.0,
    height=41.0
)

entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    699.5,
    434.0,
    image=entry_image_4
)
entry_4 = Entry(
    bd=0,
    bg="#E6E6E6",
    highlightthickness=0
)
entry_4.place(
    x=480.0,
    y=413.0,
    width=439.0,
    height=40.0
)

canvas.create_text(
    481.0,
    415.0,
    anchor="nw",
    text="Bepaalde tekst",
    fill="#000000",
    font=("Inter", 12 * -1)
)

entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    699.5,
    434.0,
    image=entry_image_4
)
entry_4 = Entry(
    bd=0,
    bg="#E6E6E6",
    highlightthickness=0
)
entry_4.place(
    x=480.0,
    y=413.0,
    width=439.0,
    height=40.0
)

canvas.create_text(
    481.0,
    415.0,
    anchor="nw",
    text="Bepaalde tekst",
    fill="#000000",
    font=("Inter", 12 * -1)
)

entry_5 = Entry(
    bd=0,
    bg="#E6E6E6",
    highlightthickness=0
)
entry_5.place(
    x=82.0,
    y=87.0,
    width=227.0,
    height=36.0
)


button_1 = Button(
    bg="#E6E6E9",
    text="Search",
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=140.3253173828125,
    y=139.80120849609375,
    width=110.81927490234375,
    height=22.427703857421875
)

entry_6 = Text(
    bd=0,
    bg="#E6E6E9",
    highlightthickness=0
)
entry_6.place(
    x=82.0,
    y=177.0,
    width=227.0,
    height=387.0
)


img = Image.open("assets/mercedes-benz-74-81a1eb.jpg")
img = img.resize((100,66), Image.ANTIALIAS)
photoImg1 = ImageTk.PhotoImage(img)

image_1 = canvas.create_image(
    882.0,
    45.0,
    image=photoImg1

)

img = Image.open("assets/Mercedes_EQA-01@2x.jpg")
img = img.resize((449,237), Image.ANTIALIAS)
photoImg = ImageTk.PhotoImage(img)

image_2 = canvas.create_image(
    699.0,
    209.0,
    image=photoImg
)

canvas.create_rectangle(
    391.9999694824219,
    0.0,
    392.0,
    633.0,
    fill="#000000",
    outline="")

canvas.create_text(
    475.0,
    26.0,
    anchor="nw",
    text="Car Brand",
    fill="#000000",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    512.0,
    50.0,
    anchor="nw",
    text="Car Model",
    fill="#000000",
    font=("Inter", 12 * -1)
)

canvas.create_text(
    130.0,
    38.0,
    anchor="nw",
    text="Electric Car",
    fill="#000000",
    font=("Inter", 24 * -1)
)

canvas.create_text(
    481.0,
    360.0,
    anchor="nw",
    text="Kilometer",
    fill="#000000",
    font=("Inter", 12 * -1)
)

canvas.create_text(
    481.0,
    470.0,
    anchor="nw",
    text="Zever man",
    fill="#000000",
    font=("Inter", 12 * -1)

)
window.resizable(False, False)
window.mainloop()
