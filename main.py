"""
CIS 41B (01Y)
Final Project - main.py
~ Offers the user the ability to search food(s) to see calories and nutritional data

Imported Files:
- api.py

bind Enter key
add note why there isn't a status check
lower limit for graphs (choice 3) due to API limits


@author Huy Nguyen, Minhduc Cao
@version 1.0
@date 2019.06.14
"""
import os   # For gui2fg()
import sys  # For gui2fg()
import tkinter as tk
import tkinter.messagebox as tkmb
import tkinter.font as tkFont
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from api import *

import collections  # remove after finished testing

BASE_URL = "https://trackapi.nutritionix.com/v2"                # URL for Nutritionix API calls
HEADERS = {'x-app-id': "2713eda2",                              # Headers for Nutritionix API calls
           'x-app-key': "2f3f23571397305a0df5759ce0da0f2e",
           "Content-Type": "application/json"}

def gui2fg():
    """Brings tkinter GUI to foreground on Mac
    Call gui2fg() after creating main window and before mainloop()
    start
    """
    if sys.platform == 'darwin':
        tmpl = 'tell application "System Events" to set frontmost of every process whose unix id is %d to true'
        os.system("/usr/bin/osascript -e '%s'" % (tmpl % os.getpid()))


class MainWin(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Food Search")
        self.resizable(False, False)
        tk.Button(self, text="Search and display food label", command=self.searchAndDisplay).grid(padx=10, pady=10)
        tk.Button(self, text="Calculate total calorie count for foods", command=self.totalCalories).grid(padx=10, pady=10)
        tk.Button(self, text="Display calorie count graph of food", command= lambda : ChoiceThree(self)).grid(padx=10, pady=10)
        tk.Button(self, text="Show food label of restaurant menu item", command = lambda : ChoiceFour(self)).grid(padx=10, pady=10)        # Remove if not possible

    def searchAndDisplay(self):
        SingleFoodPrompt(self)

    def totalCalories(self):
        pass

    def calorieGraph(self):
        pass


class SingleFoodPrompt(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Search and display food label")
        self.resizable = (False, False)
        self.grab_set()

        self.textField = tk.StringVar()
        tk.Label(self, text="Enter an food item to be searched. Press <Enter> to search:").grid(pady=10, sticky="e")
        tk.Entry(self, textvariable=self.textField).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self, text="Print Label", command=self.getSelection).grid(row=2)
        self.bind("<Return>", self.search)

        self.scroll = tk.Scrollbar(self)
        self.scroll.grid(row=2, column=1, sticky="nsw")                     # Grids scrollbar in 2nd column next to listbox
        self.LB = tk.Listbox(self, height=15, width=50, selectmode="single", yscrollcommand=self.scroll.set)
        self.LB.grid(row=2, padx=5, pady=10)
        self.scroll.config(command=self.LB.yview)                   # Allows scrollbar to work with listbox y-scrolling

        self.results = {}       # To store search results

    def search(self, event):
        query = self.textField.get()
        self.LB.delete(0, tk.END)                       # Clears listbox for new search
        self.results = genSearch(query, BASE_URL, HEADERS)
        if len(self.results) == 0:      # If query doesn't return any results
            tkmb.showinfo("Search Results", "Your search query has returned 0 results. Please double check for spelling errors or try with a different food item.")
        else:           # Inserts results into listbox -- since API isn't massive, display all results
            for food in self.results:
                self.LB.insert(tk.END, food)

    def getSelection(self):
        index = self.LB.curselection()
        if index is ():         # If user presses "Print Label" before searching anything
            tkmb.showerror("Error", "Please search for and select one food item before pressing \'Print Label\'.")
        else:
            foodItem = self.LB.get(self.LB.curselection())
            if self.results[foodItem] is None:  # Checks if food item is a common item
                foodData = commonItemSearch(foodItem.replace("(Common)", ""), BASE_URL, HEADERS)
            else:       # Runs if food item is a branded food item
                foodData = brandItemSearch(self.results[foodItem], BASE_URL, HEADERS)
            print(foodData)
            NutritionLabel(self, foodData)      # Creates nutrition label window


class NutritionLabel(tk.Toplevel):
    DAILY_VALUES = {"total_fat": 65, "sat_fat": 20, "cholesterol": 300}


    def __init__(self, master, data):
        super().__init__(master)
        self.title("Nutritional Facts")
        self.resizable = (False, False)

        self.fontTitle = tkFont.Font(family="Arial", size=30, weight="bold")
        self.fontSubTitle = tkFont.Font(family="Arial", size=12, weight="bold")

        tk.Label(self, text=data["food_name"]).grid(padx=10, pady=10, columnspan=2)
        tk.Label(self, text="Nutrition Facts", font=self.fontTitle).grid(padx=10, sticky="w", columnspan=2)
        tk.Label(self, text="Serving Size " + str(int(data["serving_qty"])) + " " + data["serving_unit"], font=self.fontSubTitle).grid(padx=10, sticky="w", columnspan=2)
        tk.Label(self, background="black").grid(sticky="we", columnspan=2)

        tk.Label(self, text="Amount per Serving", font=tkFont.Font(weight="bold")).grid(padx=10, sticky="w")
        tk.Label(self, background="black").grid(sticky="we", columnspan=2)
        tk.Label(self, text="Calories " + str(data["calories"])).grid(sticky="w", columnspan=2)
        tk.Label(self, text="% Daily Values").grid(sticky="e", column=1)
        tk.Label(self, text="Total Fat " + str(data["total_fat"])).grid(sticky="w", column=0) # row 8
        tk.Label(self, text="")



        for k, v in data.items():
            print(k, v)


class ChoiceFour(tk.Toplevel):
    def __init__(self,master):
        super().__init__(master)
        self.title("Nearby Restaurants")
        # self.resizable(False,False)

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
        for restaurant in self.data['locations']:
            self.LB.insert(tk.END, restaurant['name'])

        # # TEST
        # self.data = json.dumps(self.data,indent = 4)
        # print(self.data)

class ChoiceThree(tk.Toplevel):
    def __init__(self,master):
        super().__init__(master)
        self.title("Nutrition Graph")
        self.resizable = (False, False)
        self.grab_set()

        textField = tk.StringVar()
        tk.Label(self, text="Enter an food item to be graphed:").grid(pady=10, sticky="e")
        E = tk.Entry(self, textvariable=textField)
        E.grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self, text="Search", command=lambda: self.search(textField.get())).grid(row=1, column=1)
        E.bind("<Return>", lambda: self.search(textField.get()))

    def search(self,query):
        print(query)
        data = genSearch(query,BASE_URL,HEADERS)
        print("This is all the branded items: ")
        rangeY = []
        for item,nix_item_id in data.items(): # Loop and do work with branded foods only.
            if nix_item_id == None:
                continue
            else:
                try:
                    data = brandItemSearch(nix_item_id,BASE_URL,HEADERS)
                    # rangeY.append(data['calories'])
                    # print("This is calories: ",data['calories'])
                except requests.exceptions.RequestException as e:
                    print("Request exception: ", e)


if __name__ == '__main__':
    app = MainWin()
    gui2fg()
    app.mainloop()
