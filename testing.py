import os   # For gui2fg()
import sys  # For gui2fg()
import tkinter as tk
import tkinter.messagebox as tkmb
import tkinter.font as tkf
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from api import *
import numpy as np

import collections  # remove after finished testing
root = tkinter.Tk()
canvas = tkinter.Canvas(root)
canvas.pack()

def gui2fg():
    """Brings tkinter GUI to foreground on Mac
    Call gui2fg() after creating main window and before mainloop()
    start
    """
    if sys.platform == 'darwin':
        tmpl = 'tell application "System Events" to set frontmost of every process whose unix id is %d to true'
        os.system("/usr/bin/osascript -e '%s'" % (tmpl % os.getpid()))


def get_coordinates(event):
    canvas.itemconfigure(tag, text='({x}, {y})'.format(x=event.x, y=event.y))

canvas.bind('<Motion>', get_coordinates)
canvas.bind('<Enter>', get_coordinates)  # handle <Alt>+<Tab> switches between windows
tag = canvas.create_text(10, 10, text='', anchor='nw')

if __name__ == '__main__':
    root.mainloop()
    gui2fg()
    app.mainloop()
