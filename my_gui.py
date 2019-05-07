import tkinter as tk
from tkinter import ttk

class FloatingWindow(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.overrideredirect(True)

        self.grip = tk.Label(self)
        self.grip.pack(side="top", fill="x")

        self.grip.bind("<ButtonPress-1>", self.StartMove)
        self.grip.bind("<ButtonRelease-1>", self.StopMove)
        self.grip.bind("<B1-Motion>", self.OnMotion)
        cancelBtn = CloseButton(self.grip, text="X", height=25, width=25, command=self.Quit).pack(side="right")

    def Quit(self):

        self.destroy()

    def StartMove(self, event):

        self.x = event.x
        self.y = event.y

    def StopMove(self, event):

        self.x = None
        self.y = None

    def OnMotion(self, event):

        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry("+%s+%s" % (x, y))

class CloseButton(ttk.Frame):
    def __init__(self, parent, height=None, width=None, text="", command=None, style=None):
        ttk.Frame.__init__(self, parent, height=height, width=width, style="CloseButton.TFrame")

        self.pack_propagate(0)
        self._btn = ttk.Button(self, text=text, command=command, style=style)
        self._btn.pack(fill=tk.BOTH, expand=1)
