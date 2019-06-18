import requests
import json
import sys  # For gui2fg()
import os
import tkinter as tk
import tkinter.messagebox as tkmb
import tkinter.filedialog as tkfd
import threading
from api import GETnearbyRestaurants

# TEST LATER
# url = "https://trackapi.nutritionix.com/v2/locations?ll=37.321949,-122.048889&distance=1mi&limit=20&brand_id=513fbc1283aa2dc80c00001f"

# Note: when combining all the files together, just replace rename MainWin to a topWin object.

def gui2fg():
    """Brings tkinter GUI to foreground on Mac
       Call gui2fg() after creating main window and before mainloop() start
    """
    if sys.platform == 'darwin':
        tmpl = 'tell application "System Events" to set frontmost of every process whose unix id is %d to true'
        os.system("/usr/bin/osascript -e '%s'" % (tmpl % os.getpid()))

def windowBeautify(window,x,y,width,height):
    """Change window size and location on screen, set x to 250 and y to 150 if we want window to be
    at the middle of the screen. """
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()
    xCoordinate = (screenWidth/2) - x
    yCoordinate = (screenHeight/2) - y
    window.geometry("%sx%s+" % (width,height) + str(int(xCoordinate))+ "+" + str(int(yCoordinate)))




class MainWin(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Foodie")
        # self.resizable(False,False)

        windowBeautify(self,250,150,480,250)
        # List box
        self.scroll = tk.Scrollbar(self)
        self.LB = tk.Listbox(self, height=10, width=50, selectmode="multiple", yscrollcommand=self.scroll.set)
        self.LB.grid(padx = 10, pady = 10,row=0,column=0)
        self.scroll.grid(column=1, sticky="ns")
        tk.Button(self, text="Find nearby restaurants", command= self.insertToListBox).grid(row=1,column=0)
        self.scroll.config(command=self.LB.yview)      # Allows scrollbar to work with listbox y-scrolling

        # Json structure
        self.data = {}
    def insertToListBox(self):
        self.data = GETnearbyRestaurants()
        brand_id_list = []
        for restaurant in self.data['locations']:
            self.LB.insert(tk.END, restaurant['name'])

        # # TEST
        self.data = json.dumps(self.data,indent = 4)
        print(self.data)

if __name__ == "__main__":
    app = MainWin()
    gui2fg()
    app.mainloop()

print('SOMETHING')
print('aisjdkla')
print('alsjdlak')
