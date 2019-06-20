"""
CIS 41B (01Y)
Final Project - main.py
~ Offers the user the ability to search food(s) to see calories and nutritional data

Imported Files:
- api.py

Imported Modules:
- geocoder (requires command line installation)

add note why there isn't a status check
lower limit for graphs (choice 3) due to API limits

TO DO LIST:
1. Choice 2
    2a. Do everything
2. Choice 3
3. Choice 4

All Keys:
>> MDC Key:
2713eda2
2f3f23571397305a0df5759ce0da0f2e

>> MDC Key 2: (FOR DEMO)
d5b800e9
d95b0fdcdf5ac259b8a7b80b40200519

>> Huy Key:
a6db4eec
dd88c3b6ece495fd91ed7bb18bb133a2

>> Huy Key 2:
d43b95b0
ccc1f54d0392398034fcda2a489c3522

@author Huy Nguyen, Minhduc Cao
@version 1.3
@date 2019.06.19
"""
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

import collections  # remove after finished testing

BASE_URL = "https://trackapi.nutritionix.com/v2"                # URL for Nutritionix API calls
HEADERS = {"x-app-id": "d43b95b0",                              # Headers for Nutritionix API calls
           "x-app-key": "ccc1f54d0392398034fcda2a489c3522",
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
        """Initializes main window to display all four choices to deal with using Nutritionix API"""
        super().__init__()
        self.title("Food Search")
        self.resizable(False, False)
        tk.Button(self, text="Search and display food label", command=lambda: ChoiceOne(self)).grid(padx=10, pady=10)
        tk.Button(self, text="Calculate total calorie count for foods", command=lambda: ChoiceTwo(self)).grid(padx=10, pady=10)
        tk.Button(self, text="Display calorie count graph of food", command=lambda: ChoiceThree(self)).grid(padx=10, pady=10)
        tk.Button(self, text="Show food label of restaurant menu item", command=lambda: ChoiceFour(self)).grid(padx=10, pady=10)


class ChoiceOne(tk.Toplevel):
    def __init__(self, master):
        """Initializes window to prompt user to search for a food item and print a corresponding food label

        Arguments:
            master (MainWin class): links to MainWindow window
        """
        super().__init__(master)
        self.title("Search and display food label")
        self.resizable = (False, False)
        self.grab_set()

        self.textField = tk.StringVar()                             # Stores text field for Entry widget
        tk.Label(self, text="Enter an food item to be searched. Press <Enter> to search:").grid(pady=10, sticky="e")
        tk.Entry(self, textvariable=self.textField).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(self, text="Once you've searched for an item, select one to print nutritional label for.").grid(row=1, column=0, padx=10, pady=10)
        tk.Button(self, text="Print Label", command=self.printLabel).grid(row=1, column=1, padx=10, pady=10)
        self.bind("<Return>", self.search)                          # Binds enter key to search

        self.scroll = tk.Scrollbar(self)
        self.scroll.grid(row=2, column=1, sticky="nsw")             # Grids scrollbar in 2nd column next to listbox
        self.LB = tk.Listbox(self, height=15, width=50, selectmode="single", yscrollcommand=self.scroll.set)
        self.LB.grid(row=2, padx=5, pady=10)
        self.scroll.config(command=self.LB.yview)                   # Allows scrollbar to work with listbox y-scrolling

        self.results = {}                                           # To store search results

    def search(self, event):
        """Searches user query and inputs results into listbox

        Arguments:
            event (tkinter.Event): tkinter Event object storing event bind data
        """
        self.LB.delete(0, tk.END)               # Clears listbox for new search
        self.results = genSearch(self.textField.get(), BASE_URL, HEADERS)
        if len(self.results) == 0:              # If query doesn't return any results
            tkmb.showinfo("Search Results", "Your search query has returned 0 results. Please double check for spelling errors or try with a different food item.")
        else:                                   # Inserts results into listbox -- since API isn't massive, display all results
            for food in self.results:
                self.LB.insert(tk.END, food)

    def printLabel(self):
        """Checks user selection and calls Nutrition Label class to print nutrition label for food selection"""
        index = self.LB.curselection()
        if index is ():                         # If user presses "Print Label" before searching anything
            tkmb.showerror("Error", "Please search for and select one food item before pressing \'Print Label\'.")
        else:
            foodItem = self.LB.get(self.LB.curselection())
            if self.results[foodItem] is None:  # Checks if food item is a common item
                foodData = commonItemSearch(foodItem.replace("(Common)", ""), BASE_URL, HEADERS)
            else:                               # Runs if food item is a branded food item
                foodData = brandItemSearch(self.results[foodItem], BASE_URL, HEADERS)
            NutritionLabel(self, foodData)      # Creates nutrition label window


class NutritionLabel(tk.Toplevel):
    # FDA daily value nutrient amounts for a 2000 calorie diet
    DAILY_NUTRIENTS = ["total_fat", "sat_fat", "cholesterol", "sodium", "total_carbs", "fiber", "sugar", "protein"]
    DAILY_VALUES = [65, 20, 300, 2400, 300, 25, None, 50]

    def __init__(self, master, data):
        """Initializes nutrition label window to display food data

        Arguments:
            master (MainWin class): links to MainWindow window
            data (dictionary): nutritional information for a specified food item
        """
        print(data)
        super().__init__(master)
        self.title("Nutritional Facts")
        self.resizable = (False, False)

        # Sets up fonts for formatting
        self.titleFont = tkf.Font(size=30, weight="bold")
        self.bigBold = tkf.Font(size=15, weight="bold")
        self.bold = tkf.Font(weight="bold")
        self.tinyBold = tkf.Font(size=10, weight="bold")

        tk.Label(self, text="Nutrition Facts", font=self.titleFont).grid(row=0, columnspan=2, sticky="nw")
        tk.Label(self, text=data["food_name"]).grid(row=1, columnspan=2, sticky="nw")
        tk.Label(self, text="Serving Size " + str(data["serving_qty"]) + " " + data["serving_unit"], font=self.bigBold).grid(row=2, columnspan=2, sticky="w")
        tk.Label(self, background="black").grid(row=3, columnspan=2, sticky="we")

        tk.Label(self, text="Amount Per Serving      ", font=self.tinyBold).grid(row=4, columnspan=2, sticky="w")
        tk.Label(self, background="black").grid(row=5, columnspan=2, sticky="we")

        tk.Label(self, text="Calories " + str(data["calories"]), font=self.bigBold).grid(row=6, column=0, sticky="w")
        tk.Label(self, text="% Daily Value", font=self.bigBold).grid(row=6, column=1, sticky="e")

        # Creating nutritional facts lines with percentages and correct data assignment
        nutrientLabels = ["Total Fat", "Saturated Fat", "Cholesterol", "Sodium", "Total Carbohydrate", "Dietary Fiber", "Sugars", "Protein"]
        units = ["g", "g", "mg", "mg", "g", "g", "g", "g"]
        vals = [data[key] for key in self.DAILY_NUTRIENTS]          # List of nutrient values for the specified food
        foodVals = [0 if val is None else val for val in vals]      # Changes 'None' to 0 in nutrient values for the specified food

        for i in range(len(nutrientLabels)):
            label = tk.Label(self, text=nutrientLabels[i] + " " + str(int(foodVals[i])) + units[i])
            if nutrientLabels[i] == "Saturated Fat" or nutrientLabels[i] == "Dietary Fiber" or nutrientLabels[i] == "Sugars":
                label.grid(row=7+i, column=0, sticky="w", padx=20)      # Indents these lines as sub-labels for 'Total Fat' and "Total Carbohydrates'
            else:
                label.grid(row=7+i, column=0, sticky="w")
                label.config(font=self.bold)

            if nutrientLabels[i] != "Sugars":      # Skips sugar since it doesn't have a recommended daily value
                tk.Label(self, text=str(round((foodVals[i] / self.DAILY_VALUES[i]) * 100)) + "%", font=self.bold).grid(row=7+i, column=1, sticky="e")
        tk.Label(self, background="black").grid(columnspan=2, sticky="we")


class ChoiceTwo(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)


class ChoiceThree(tk.Toplevel):
    def __init__(self, master):
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
        # data = genSearchV2(query,BASE_URL,HEADERS) comment out for not to exceed api limits


        rangeY = [100, 80, 120, 120, 110, 220, 143.55, 50, 70, 50, 140, 70, 40, 40, 50, 90, 70, 110, 50, 70]
        rangeX = ['Bite Size Dry Salami, Spicy', 'Cheddar Cheese, Minis', 'Mini Wafers, Vanilla', 'Organic Chicken & Maple Breakfast Sausage', 'Organic Uncured Beef Hot Dog', 'Pork Carnitas, Seasoned & Seared', 'Sparkling Apple Juice', 'Turkey Breast, Oven Roasted', 'Uncured Black Forest Ham', 'Uncured Thick Cut Bacon, Hickory Smoked', 'Oatmeal Bar, Chocolate', 'The Great Uncured Chicken Hot Dog, Organic', 'Organic Apple Snack, No Sugar Added', 'Apple & Strawberry Fruit Snack', 'Apple Strawberry Snack', 'Applesauce with Peaches', 'Applesauce, Unsweetened', 'Chicken & Maple Breakfast Sausage', 'Herb Turkey Breast', 'Hot Dog, Uncured Beef']
        # for item in data['branded']:
        #     rangeY.append(round(item["nf_calories"],4))
        #     rangeX.append(item["food_name"])

        init = CaloriesWindow(self, lambda: self.plotCaloriesGraph(rangeX,rangeY))

    def plotCaloriesGraph(self, rangeX, rangeY):
        plt.bar(rangeX,rangeY,width=0.5,label='YEAHHH',color= '#7189bf')
        plt.xlabel("Tuition and fee for the year ")
        plt.ylabel("Undergraduate Budget")
        plt.title("Pathway Recommendation")
        plt.legend(loc="best")


class CaloriesWindow(tk.Toplevel):
    def __init__(self,master, plotgraph):
        super().__init__(master)
        fig = plt.figure(figsize=(10,7))
        plotgraph()
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().grid()
        canvas.draw()


class ChoiceFour(tk.Toplevel):
    def __init__(self, master):
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
        self.data = getNearbyRestaurants(BASE_URL, HEADERS)
        for restaurant in self.data['locations']:
            self.LB.insert(tk.END, restaurant['name'])

        # # TEST
        # self.data = json.dumps(self.data,indent = 4)
        # print(self.data)


if __name__ == '__main__':
    app = MainWin()
    gui2fg()
    app.mainloop()
