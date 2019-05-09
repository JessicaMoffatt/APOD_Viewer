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
YELLOW="#ffe304"

DATE_FORMAT="%b %d, %Y"

NASA_KEY = "CHJFAY4XzXIc5LrO0MvAcB12XeHoAzHufVBR4AvV"

selectedDate = "{}".format(datetime.now().date().strftime(DATE_FORMAT))

pickingDate = False

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
            chooseDate.configure(text=selectedDate)
            pickingDate = False
            top.Quit()
        else:
            cal.selection_set(datetime.strptime(selectedDate, DATE_FORMAT))

    global pickingDate
    global top
    if not pickingDate:
        pickingDate = True

        top = my_gui.FloatingWindow(root)
        cal = Calendar(top, font=("Book Antiqua",15), selectmode="day", showothermonthdays=False, showweeknumbers=False)
        cal.selection_set(datetime.strptime(selectedDate, DATE_FORMAT))
        cal.pack(fill="both", expand=True)

        selectBtn = ttk.Button(top, text="Select", command=SetDate).pack()
    else:        
        top.lift()

#date is in format YYYY-MM-DD
def GetAPOD():

    dateF = datetime.strptime(GetDate(), DATE_FORMAT).date()
    url = "https://api.nasa.gov/planetary/apod"
    params = {"api_key":NASA_KEY, "hd":True, "date":dateF}
    response = requests.get(url, params=params)
    apod = response.json()
    if 'url' not in apod:
        label.configure(text="There is no picture for this day", image="")
        label.image = ""
        label.grid()

    else:
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
            label.configure(text="Video is not supported", image="")
            label.image = ""
            label.grid()

root = tk.Tk()
root.title("Astronomy Picture of the Day")
root.configure(bg=GUN_METAL)

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg=GUN_METAL, highlightthickness=0)
canvas.pack(fill="both", expand=1)

frame = tk.Frame(canvas, bg=GUN_METAL)
frame.place(relx=0.5, rely=0.05, relwidth=0.9, relheight=1, anchor="n")

dateLabel = tk.Label(frame, font=("Book Antiqua",20), text="Selected Date: ", bg=GUN_METAL, fg=IVORY)
dateLabel.place(relx=0, rely=0.01)

chooseDate = tk.Button(frame, text=GetDate(), font=("Book Antiqua",20), command=lambda: ShowDateSelect())
chooseDate.place(relx=0.5, rely=0.01, relwidth=0.5, relheight=0.05, anchor="nw")

submit = tk.Button(frame, text="Get APOD", font=("Book Antiqua",25), command=lambda: GetAPOD(), bg=IVORY, fg=GUN_METAL)
submit.place(relx=0.5, rely=0.09, relwidth=0.5, relheight=0.07, anchor="n")

lowerFrame = tk.Frame(canvas, bg=GUN_METAL)
lowerFrame.place(relx=0.5, rely=0.24, relwidth=0.9, relheight=0.7, anchor="n")
lowerFrame.bind("<Configure>", OnConfigure)

label = tk.Label(lowerFrame, font=("Book Antiqua",25), bg=GUN_METAL, fg=IVORY)
label.place(relwidth=1, relheight=1,)
label.grid()
label.grid_remove()

root.mainloop()