import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import requests
from urllib.request import urlopen
import io
from tkcalendar import Calendar
from datetime import datetime
import logging
import my_gui

HEIGHT = 720
WIDTH = 980

EERIE_BLACK="#0B1221"

NASA_KEY = "CHJFAY4XzXIc5LrO0MvAcB12XeHoAzHufVBR4AvV"

selectedDate = "{}".format(datetime.now().date())

logging.basicConfig(level=logging.DEBUG)

def GetDate():

    return selectedDate

def ShowDateSelect():
  
    def SetDate():
        selection = cal.selection_get()
        if type(selection) == datetime:
            selection = selection.date()
        if selection <= datetime.now().date():
            global selectedDate        
            selectedDate = "{}".format(selection)
            dateLabel.configure(text="Selected Date: " + selectedDate)
            top.Quit()
        else:
            cal.selection_set(datetime.strptime(selectedDate, "%Y-%m-%d"))

    top = my_gui.FloatingWindow(root)
    cal = Calendar(top, font=("Book Antiqua",15), selectmode="day", showothermonthdays=False, showweeknumbers=False)
    cal.selection_set(datetime.strptime(selectedDate, "%Y-%m-%d"))
    cal.pack(fill="both", expand=True)

    selectBtn = ttk.Button(top, text="Select", command=SetDate).pack()

#date is in format YYYY-MM-DD
def GetAPOD():

    dateF = GetDate()
    url = "https://api.nasa.gov/planetary/apod"
    params = {"api_key":NASA_KEY, "hd":True, "date":dateF}
    response = requests.get(url, params=params)
    apod = response.json()
    apodUrl = apod["url"]
    mediaType = apod["media_type"]
    if mediaType == "image":
        image_bytes = urlopen(apodUrl).read()
        data_stream = io.BytesIO(image_bytes)
        pil_image = Image.open(data_stream)
        tk_image = ImageTk.PhotoImage(pil_image)
        label.configure(image=tk_image)
        label.image = tk_image
        label.grid()
        label.pack()
    elif mediaType == "video":
        label.configure(text="video", image="")
        label.image = ""
        label.grid()
        label.pack()

root = tk.Tk()
root.title("Astronomy Picture of the Day")
root.configure(bg=EERIE_BLACK)

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg=EERIE_BLACK, highlightthickness=0)
canvas.pack()

frame = tk.Frame(root, bg=EERIE_BLACK)
frame.place(relx=0.5, rely=0.05, relwidth=0.9, anchor="n")

dateLabel = tk.Label(frame, font=("Book Antiqua",15), text="Selected Date: " + GetDate())
dateLabel.grid(row=1, column=1)

chooseDate = tk.Button(frame, text="Choose Date...", font=("Book Antiqua",15), command=lambda: ShowDateSelect())
chooseDate.grid(row=1, column=2)

submit = tk.Button(frame, text="Get APOD", font=("Book Antiqua",15), command=lambda: GetAPOD())
submit.grid(row=1, column=3)

lowerFrame = tk.Frame(root, bg=EERIE_BLACK)
lowerFrame.place(relx=0.5, rely=0.16, relwidth=0.9, relheight=0.8, anchor="n")

label = tk.Label(lowerFrame, text="TEST")
label.pack()
label.grid()
label.grid_remove()

root.mainloop()