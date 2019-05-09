import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image, ImageOps
import requests
from urllib.request import urlopen
import io
from tkcalendar import Calendar
from datetime import datetime
import my_gui
import logging

HEIGHT = 720
WIDTH = 720

GUN_METAL="#292f3c"
IVORY="#fffdf4"

DATE_FORMAT="%b %d, %Y"

NASA_KEY = "CHJFAY4XzXIc5LrO0MvAcB12XeHoAzHufVBR4AvV"

selectedDate = "{}".format(datetime.now().date().strftime(DATE_FORMAT))

logging.basicConfig(level=logging.DEBUG)

def OnConfigure(event):

    w = event.width
    h = event.height

    if hasattr(label,'image') and label.image != "":
        global pil_image
        hsize = CalculateHSize(w, pil_image.size[0], pil_image.size[1])
        new_image = pil_image.resize((w,hsize), Image.ANTIALIAS)
        tk_image = ImageTk.PhotoImage(new_image)
        label.image = ImageTk.PhotoImage(new_image)
        label.configure(image=tk_image)
        label.image = tk_image
        
def CalculateHSize(base, size0, size1):

     ratio = (base/float(size0))
     hsize = int((float(size1 * float(ratio))))
     return hsize

def GetDate():

    return selectedDate

def ShowDateSelect():
  
    def SetDate():
        selection = cal.selection_get()
        if type(selection) == datetime:
            selection = selection.date()
        if datetime(1995, 6, 16).date() <= selection <= datetime.now().date():
            global selectedDate        
            selectedDate = "{}".format(selection.strftime(DATE_FORMAT))
            dateLabel.configure(text="Selected Date: " + selectedDate)
            top.Quit()
        else:
            cal.selection_set(datetime.strptime(selectedDate, DATE_FORMAT))

    top = my_gui.FloatingWindow(root)
    cal = Calendar(top, font=("Book Antiqua",15), selectmode="day", showothermonthdays=False, showweeknumbers=False)
    cal.selection_set(datetime.strptime(selectedDate, DATE_FORMAT))
    cal.pack(fill="both", expand=True)

    selectBtn = ttk.Button(top, text="Select", command=SetDate).pack()

#date is in format YYYY-MM-DD
def GetAPOD():

    dateF = datetime.strptime(GetDate(), DATE_FORMAT).date()
    url = "https://api.nasa.gov/planetary/apod"
    params = {"api_key":NASA_KEY, "hd":True, "date":dateF}
    response = requests.get(url, params=params)
    apod = response.json()
    apodUrl = apod["url"]
    mediaType = apod["media_type"]
    if mediaType == "image":
        image_bytes = urlopen(apodUrl).read()
        data_stream = io.BytesIO(image_bytes)
        global pil_image
        pil_image = Image.open(data_stream)        
        hsize = CalculateHSize(lowerFrame.winfo_width(), pil_image.size[0], pil_image.size[1])
        new_image = pil_image.resize((lowerFrame.winfo_width(),hsize), Image.ANTIALIAS)

        tk_image = ImageTk.PhotoImage(new_image)
        
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
root.configure(bg=GUN_METAL)

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg=GUN_METAL, highlightthickness=0)
canvas.pack(fill="both", expand=1)

frame = tk.Frame(root, bg=GUN_METAL)
frame.place(relx=0.5, rely=0.05, relwidth=0.9, anchor="n")

dateLabel = tk.Label(frame, font=("Book Antiqua",15), text="Selected Date: " + GetDate(), bg=GUN_METAL, fg='white')
dateLabel.grid(row=1, column=1)

chooseDate = tk.Button(frame, text="Choose Date...", font=("Book Antiqua",15), command=lambda: ShowDateSelect())
chooseDate.grid(row=1, column=2)

submit = tk.Button(frame, text="Get APOD", font=("Book Antiqua",15), command=lambda: GetAPOD())
submit.grid(row=1, column=3)

lowerFrame = tk.Frame(root, bg=GUN_METAL)
lowerFrame.place(relx=0.5, rely=0.16, relwidth=0.9, relheight=0.8, anchor="n")
lowerFrame.bind("<Configure>", OnConfigure)

label = tk.Label(lowerFrame)
label.pack()
label.grid()
label.grid_remove()

root.mainloop()