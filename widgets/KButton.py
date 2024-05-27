
import sys
import tkinter
from tkinter import ttk
from engine import DrawingEngine

class KButton(ttk.Frame):

    def __init__(self, parent, text, background, onHoverBackground, column, row, onClick=None,columnspan=1, rowspan=1, textfill='white', type='rounded', frameColor='white', *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.text = text
        self.background = background
        self.onHoverBackground = onHoverBackground
        self.onClick = onClick
        self.column = column
        self.row = row
        self.columnspan = columnspan
        self.rowspan = rowspan
        self.textfill = textfill
        self.type = type
        self.frameColor = frameColor
        self.cache = {}

        self.draw()
        self.configureButtonInteractivity()
        self.grid(column=self.column, row=self.row, columnspan=self.columnspan, rowspan=self.rowspan)

    def __onHover(self, event):
        self.canvas.itemconfig("Frame", fill=self.onHoverBackground)

    def __onLeave(self, event):
        self.canvas.itemconfig("Frame", fill=self.background)

    def __onClick(self, event):
        self.onClick()

    def configureButtonInteractivity(self):
        self.canvas.bind("<Enter>", lambda e: self.__onHover(e))
        self.canvas.bind("<Leave>", lambda e: self.__onLeave(e))
        self.canvas.bind("<Button-1>", lambda e: self.__onClick(e))
        self.cache["onHover"] = lambda e : self.__onHover(e)
        self.cache["onLeave"] = lambda e : self.__onLeave(e)
        self.cache["onClick"] = self.onClick

    def draw(self):
        #canvasBD = -2 if sys.platform == "win32" else -3 
        self.canvas = tkinter.Canvas(
            self,
            height=self['height'],
            width=self['width'],
            background=self.frameColor,
            bd=0,
            highlightthickness=0,
            cursor="hand2",
        )

        if self.type == 'rect':
            DrawingEngine().drawRectangle(
                canvas=self.canvas,
                x1=0,
                x2=self['width'],
                y1=0,
                y2=self['height'],
                borderFill=self.onHoverBackground,
                fill=self.background,
                tags=("Frame"),
            )
        
        if self.type == 'rounded':
            DrawingEngine().drawRoundedRect(
                canvas=self.canvas,
                x1=0,
                x2=self['width'],
                y1=0,
                y2=self['height'],
                radius=10,
                fill=self.background,
                tags=("Frame"),
        )
        #self.canvas.itemconfig("Frame", fill=self.background)

        self.canvas.create_text(self['width'] * 0.5, self['height'] * 0.5, text=self.text, fill=self.textfill)
        self.canvas.grid(column=self.column, row=self.row, columnspan=self.columnspan, rowspan=self.rowspan)

    def __str__(self):
        return self.text
