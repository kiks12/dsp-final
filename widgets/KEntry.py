
import tkinter
from constants import Constants

from engine import DrawingEngine


class KEntry(tkinter.Frame):

    def __init__(self, parent, background, textvariable, type, state='normal', frameColor=Constants().windowBackgroundColor,borderColor='gray', *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.background = background
        self.textvariable = textvariable
        self.type = type
        self.state = state
        self.border = borderColor
        self.frameColor = frameColor

        self.draw()
    
    def draw(self):
        self.canvas = tkinter.Canvas(
            self,
            background=self.frameColor,
            height=self['height'],
            width=self['width'],
            bd=0,
            highlightthickness=0
        )
        self.entry = tkinter.Entry(
            self,
            background=self.background,
            width=30,
            textvariable=self.textvariable,
            relief=tkinter.FLAT,
            show= "*" if self.type == 'password' else None,
            state=self.state
        )
        DrawingEngine().drawRoundedRect(
            self.canvas,
            x1=0,
            y1=0,
            x2=self['width'],
            y2=self['height'],
            radius=10,
            fill=self.background if self.state != 'disabled' else '#F0F0F0'
        )
        DrawingEngine().drawRoundedRectangle(
            self.canvas, 
            x=0,
            y=0,
            w=self['width'] -1,
            h=self['height'] - 1,
            c=5,
            fill=self.border,
        )
        self.entry.grid(column=0, row=0, padx=10, pady=5, sticky=tkinter.NSEW)
        self.canvas.grid(column=0, row=0, sticky=tkinter.NSEW)
