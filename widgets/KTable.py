
import tkinter
from tkinter import ttk

from Model.account import Account
from constants import Constants

class KTable(ttk.Frame):

    def __init__(self, parent, headers, data, currentData, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.rows = []
        self.currentData = currentData
        self.headers = headers
        self.data = data
        self.draw()

    def drawHeader(self):
        self.headerCanvas = tkinter.Canvas(
            self,
            height=self['height'] * 0.09,
            width=self['width'] * 0.97,
            background="white",
            bd=0,
            highlightthickness=0
        )
        self.headerCanvas.bind("<Button-1>", lambda x: print("click"))

        for idx, val in enumerate(self.headers):
            if idx == 4: continue
            self.headerCanvas.create_text(
                self['width'] - ((self['width'] // 5) * (4.4-idx)),
                self['height'] *0.1 * 0.4,
                text=val,
                fill=Constants().buttonAccentColor,
                font=("Century Gothic Bold", 11)
            )

        self.headerCanvas.pack()

    def __manageDataWidgetsBackground(self, widget):
        for idx, canvas in enumerate(self.rows):
            if canvas == widget:
                continue
            canvas.configure(background=Constants().evenRowColor if idx % 2 == 0 else Constants().oddRowColor)
    
    def setCurrentData(self, event, row, widget : tkinter.Canvas):
        self.currentData = Account(list(row))
        widget.configure(background=Constants().creamButtonAccentColor)

        self.__manageDataWidgetsBackground(widget)

    def drawData(self):
        for idx, row in enumerate(self.data):
            dataCanvas = tkinter.Canvas(
                self,
                height=self['height'] * 0.07,
                width=self['width'] * 0.97,
                background=Constants().evenRowColor if idx % 2 == 0 else Constants().oddRowColor,
                bd=0,
                highlightthickness=0
            )

            dataCanvas.bind('<Button-1>', lambda event, row=row, widget=dataCanvas : self.setCurrentData(event, row, widget))

            for jdx, val in enumerate(row):
                if jdx == 4: continue
                dataCanvas.create_text(
                    self['width'] - ((self['width'] // 5) * (4.4-jdx)),
                    self['height'] * 0.1 * 0.3,
                    text=val,
                    fill="black",
                )

            self.rows.append(dataCanvas)
            dataCanvas.pack()

    def draw(self):
        self.drawHeader()
        self.drawData()
    
    def redraw(self):
        for child in self.winfo_children():
            child.destroy()
        self.rows = []
        self.draw()

