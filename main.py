"""
CIS 41B (01Y)
Final Project - main.py
~ Offers the user the ability to search food(s) to see calories and nutritional data

Imported Files:
- api.py

NOTE: Excessive testing may go over the API search limit. You can change to a different set of API keys by
changing API_KEY_SET from 0, 1, 2, 3 if api.py raises a KeyError exception.

@author Duc Huy Nguyen (Choice 3-4), Minhduc Cao (Choice 1-2)
@version 1.4
@date 2019.06.23
"""
import os   # For gui2fg()
import sys  # For gui2fg()
import tkinter as tk
import tkinter.messagebox as tkmb
import tkinter.font as tkf
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import threading
import queue
from api import *
import numpy as np

BASE_URL = "https://trackapi.nutritionix.com/v2"                # URL for Nutritionix API calls
API_KEY_SET = 1                                                 # Change from 0, 1, 2, 3 if api.py raises a KeyError exception (due to API limits)
API_IDS = ["2713eda", "d5b800e9", "a6db4eec", "d43b95b0"]
API_KEYS = ["2f3f23571397305a0df5759ce0da0f2e", "d95b0fdcdf5ac259b8a7b80b40200519",
            "dd88c3b6ece495fd91ed7bb18bb133a2", "ccc1f54d0392398034fcda2a489c3522"]
HEADERS = {"x-app-id": API_IDS[API_KEY_SET],                              # Headers for Nutritionix API calls
           "x-app-key": API_KEYS[API_KEY_SET],
           "Content-Type": "application/json"}


def gui2fg():
    """Brings tkinter GUI to foreground on Mac
    Call gui2fg() after creating main window and before mainloop() start
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
        tk.Button(self, text="Show nearby restaurants", command=lambda: ChoiceFour(self)).grid(padx=10, pady=10)

        self.protocol("WM_DELETE_WINDOW", self.closeWin)

    def closeWin(self):
        """Closes all plot windows if main window is closed"""
        plt.close('all')
        self.destroy()


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
        """Initializes window to prompt user to search for multiple food items and calculate total calories of selected foods

        Arguments:
            master (MainWin class): links to MainWindow window
        """
        super().__init__(master)
        self.title("Search and display food label")
        self.resizable = (False, False)
        self.grab_set()

        # Create tk variables to store entry field ata
        self.fieldOne = tk.StringVar()
        self.fieldTwo = tk.StringVar()
        self.fieldThree = tk.StringVar()
        self.fieldFour = tk.StringVar()
        self.fields = [self.fieldOne, self.fieldTwo, self.fieldThree, self.fieldFour]

        tk.Label(self, text="Enter up to 4 food items to calculate total calories.\nPress \'Search Items\' when ready.\n\nWhen food items have shown up, "
                            "select up to 10 items\nthat you want to find the total calories for.\nPress \'Calculate\' when ready.").grid(padx=10, sticky="w")
        tk.Entry(self, textvariable=self.fieldOne).grid(row=1, padx=25, sticky="we")
        tk.Entry(self, textvariable=self.fieldTwo).grid(row=2, padx=25, sticky="we")
        tk.Entry(self, textvariable=self.fieldThree).grid(row=3, padx=25, sticky="we")
        tk.Entry(self, textvariable=self.fieldFour).grid(row=4, padx=25, sticky="we")
        tk.Button(self, text="Search Items", command=self.search).grid(row=5, padx=10)
        tk.Button(self, text="Calculate", command=self.calculate).grid(row=5, column=1, padx=10)

        self.scroll = tk.Scrollbar(self)
        self.scroll.grid(row=0, column=2, sticky="nsw", rowspan=5)             # Grids scrollbar in 2nd column next to listbox
        self.LB = tk.Listbox(self, height=15, width=50, selectmode="multiple", yscrollcommand=self.scroll.set)
        self.LB.grid(row=0, column=1, padx=5, pady=10, rowspan=5)
        self.scroll.config(command=self.LB.yview)                   # Allows scrollbar to work with listbox y-scrolling

        self.statusVar = tk.StringVar()
        self.statusVar.set("")
        self.status = tk.Label(self, textvariable=self.statusVar).grid(padx=10, pady=5)

        self.calorieVar = tk.StringVar()
        self.calorieVar.set("")
        self.calories = tk.Label(self, textvariable=self.calorieVar).grid(row=6, column=1, padx=10, pady=5)

        self.results = {}                                           # Stores search results from queries
        self.LB.bind("<<ListboxSelect>>", self.listboxLimit)        # Binds any listbox selection to callback function
        self.queue = queue.Queue()

    def listboxLimit(self, event):
        """Clears user selection if user selects more than 10 food items to calculate total calories

        Arguments:
            event (tkinter.Event): tkinter Event object storing event bind data, unused
        """
        if len(self.LB.curselection()) > 10:
            for i in range(len(self.results)):
                self.LB.selection_clear(i)
            tkmb.showwarning("Warning", "You have selected more than 10 items to be searched. Please choose 10 or less food items.")

    def search(self):
        """Checks user input and starts threads to search API for food items"""
        queries = []
        for field in self.fields:
            query = field.get()
            if query.strip() != "":                         # Adds non-empty fields as queries
                queries.append(query)
        if len(queries) == 0:
            tkmb.showerror("Error", "Please enter at least 1 search term in any of the four search fields.")
        else:
            self.statusVar.set("Searching for " + str(len(queries)) + " food(s)")
            self.update()
            self.LB.delete(0, tk.END)                       # Clears listbox for new data
            self.results = {}                               # Clears results for new data

            tList = []
            for query in queries:                           # Starts threads for API lookup
                tList.append(threading.Thread(target=self.searchAPI, args=(query, )))
            for t in tList:
                t.start()
            n = 0
            for t in tList:
                data = self.queue.get()
                n += 1
                self.statusVar.set("Finished " + str(n) + "/" + str(len(tList)) + " searches.")
                self.update()                               # Updates GUI to reflect # of searches completed
                self.results = {**self.results, **data}     # Merges existing results and new data into new results dict

            if len(self.results) == 0:
                tkmb.showinfo("No Results", "No results found. Double-check your search queries or try a new search.")
            else:
                for food in self.results:                       # Insert results into listbox
                    self.LB.insert(tk.END, food)

    def searchAPI(self, query):
        """Threaded method to search API for food item and put it in the queue

        Arguments:
            query (string): food item to lookup in API
        """
        response = genSearch(query, BASE_URL, HEADERS)
        self.queue.put(response)

    def calculate(self):
        """Checks listbox selection for food items and calculates total calories of the selected food items"""
        indexes = self.LB.curselection()
        if indexes is ():                           # If user presses "Print Label" before searching anything
            tkmb.showerror("Error", "Please search for and select at least one food item before pressing \'Calculate\'.")
        else:
            foodItems = {}
            for index in indexes:
                foodName = self.LB.get(index)
                foodItems[foodName] = self.results[foodName]
            total = 0
            for item, foodID in foodItems.items():
                if foodID is None:                  # Checks if item is common, runs itemSearches based on food type (common or not)
                    total += commonItemSearch(item.replace("(Common)", ""), BASE_URL, HEADERS)["calories"]
                else:
                    total += brandItemSearch(foodID, BASE_URL, HEADERS)["calories"]
            self.calorieVar.set("Total Calories for " + str(len(indexes)) + " selected food(s): " + str(total))
            self.update()                           # Updates GUI to reflect total calories calculation


class ChoiceThree(tk.Toplevel):
    def __init__(self, master):
        """Initializes window for user to search a food item and display a calorie graph of top 10 results

        Arguments:
            master (MainWin class): links to MainWindow window
        """
        super().__init__(master)
        self.title("Nutrition Graph")
        self.resizable = (False, False)
        self.grab_set()

        self.userText = tk.StringVar()
        tk.Label(self, text="Enter an food item to be graphed:").grid(pady=10, sticky="e")
        E = tk.Entry(self, textvariable=self.userText)
        E.grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self, text="Search Branded Food Items", command=self.search).grid(row=1, column=1)

    def search(self):
        """Checks user input and searches API for top 10 branded food items, sends data to be plotted"""
        foodName = self.userText.get().strip()
        if foodName == "":          # Show error window if user input is blank
            tkmb.showerror("Error", "Query cannot be blank. Please a food item in the entry field.")
        else:
            data = genSearch(foodName, BASE_URL, HEADERS)
            if len(data) <= 1:      # Show error window if results are too limited
                tkmb.showerror("Error", "Less than 2 results were returned from your query. Double-check your query's spelling or try another search.")
            else:
                yRange = []
                xRange = []
                datapoints = 0      # Limits data points to 10 to prevent going over API limit
                for food, foodID in data.items():
                    if foodID is not None and datapoints <= 10:
                        foodData = brandItemSearch(foodID, BASE_URL, HEADERS)
                        yRange.append(round(foodData["calories"]))
                        xRange.append(foodData["food_name"])
                        datapoints += 1

                minVal = min(yRange)
                maxVal = max(yRange)
                avgVal = np.mean(yRange)
                minPos = [i for i, x in enumerate(yRange) if x == minVal]       # Finds positions of min/max values to remove from data set for separate plotting
                maxPos = [i for i, x in enumerate(yRange) if x == maxVal]
                minLabels = [xRange[i] for i in minPos]
                maxLabels = [xRange[i] for i in maxPos]

                for i in sorted(minPos + maxPos, reverse=True):     # Removes min and max values to be plotted separately
                    yRange.pop(i)
                yRange = sorted(yRange)

                # Plotting lowest calories, highest calories, rest of data as bar graphs, average calories as line separately
                self.plotCaloriesGraph(yRange, minVal, maxVal, avgVal, minLabels, maxLabels, foodName)

    def plotCaloriesGraph(self, yRange, minVal, maxVal, avgVal, minLabels, maxLabels, food):
        """Plots a bar graph displaying calorie count for a specified food item

        Arguments:
            yRange (list): calorie count for food items (excluding min and max)
            minVal (int): smallest calorie out of specified food items
            maxVal (int): largest calorie out of specified food items
            avgVal (float): average calories out of specified food items
            minLabels (list): contains labels for food item(s) with smallest calorie amount
            maxLabels (list): contains labels for food item(s) with largest calorie amount
            food (string): name of specified food item
        """
        # Plots bar graphs for smallest, largest, and remaining foods separately to add identifying colors
        plt.bar(minLabels, minVal, width=0.9, label="Lowest Calories: " + str(minVal), color="yellow")
        plt.bar(np.linspace(len(minLabels), len(yRange), len(yRange)), yRange, width=0.9, color="blue")
        plt.bar(np.linspace(len(yRange) + 1, len(yRange + maxLabels), len(maxLabels)), maxVal, width=0.9, label="Highest Calories: " + str(maxVal), color="orange")
        plt.plot([0, len(yRange) + 1], [avgVal, avgVal], label="Average Calories: " + str(round(float(avgVal), 2)), color="black")
        plt.xlabel("Branded Food Items")
        plt.ylabel("Amount of Calories")
        plt.title("Calories Graph for " + food)
        plt.legend(loc="best")
        plt.xticks([])      # Hide x-axis labels since food names would be crowded
        plt.show()


class ChoiceFour(tk.Toplevel):
    def __init__(self, master):
        """Initializes window for user to search a food item and display a calorie graph of top 10 results

        Arguments:
            master (MainWin class): links to MainWindow window
        """
        super().__init__(master)
        self.title("Nearby Restaurants")
        self.resizable(False, False)

        # List box with scroll bar.
        self.scroll = tk.Scrollbar(self)
        self.LB = tk.Listbox(self, height=10, width=50, selectmode="single", yscrollcommand=self.scroll.set)
        self.LB.grid(padx=10, row=0, column=0)
        self.scroll.grid(row=0, column=1, sticky="ns")
        tk.Button(self, text="Find nearby restaurants", command=self.insertToListBox).grid(row=1,column=0)
        self.scroll.config(command=self.LB.yview)      # Allows scrollbar to work with listbox y-scrolling
        # A list contains dictionaries of nearby restaurants.
        self.data = []
        # Queue to store user's chosen restaurants data
        self.queue = queue.Queue()
    def insertToListBox(self):
        """Insert all restaurant's names to the listbox"""
        tk.Button(self, text="View restaurant detail",command = self.checkValid).grid(row=2,column=0,sticky="ns")
        self.data = getNearbyRestaurants(BASE_URL, HEADERS)
        for restaurant in self.data['locations']:
            self.LB.insert(tk.END,restaurant['name'])

    def checkValid(self):
        """Check if user select at most 3 choices, using processes to call ShowRestaurantsWindow to display
        multiple restaurants' information"""
        curSelected = self.LB.curselection()
        threads = []
        menu = self.searchAPI(self.data,*curSelected)
        resWindow = ShowRestaurantsWindow(self,self.data,*curSelected,list(menu.values()),list(menu.keys()))

        for k,v in menu.items():
            resWindow.LB.insert(tk.END,k)


    def searchAPI(self, restaurantList,index):
        """Input chosen restaurant to api genSearch to return food menu.

        Arguments:
            restaurantList: a dictionary of all nearby restaurants contained in a list.
            index: chosen index number from listbox current selection from ChoiceFour window.
        """
        response = genSearch(restaurantList['locations'][index]['name'], BASE_URL, HEADERS)
        return response

class ShowRestaurantsWindow(tk.Toplevel):
    def __init__(self, master, restaurant, i,menuID,dishesName):
        """Initializes window to display restaurant's name, address, website and phone number.

        Arguments:
            master (MainWin class): links to MainWindow window
            restaurant: a dictionary of all nearby restaurants contained in a list.
            i : index of selected restaurant (listbox) from ChoiceFour
            menuID: a list of all dishes ID of user's chosen restaurant.
            dishesName: a list of all dishes name of user's chosen restaurant.
        """
        super().__init__(master)
        self.title("Restaurant(s) Information")
        self.font = tkf.Font(size=30, weight="bold")
        tk.Label(self, text=restaurant['locations'][i]['name'], font=self.font).grid(row=0, columnspan=2, sticky="nw")
        tk.Label(self, background="black").grid(row=1,columnspan=2,sticky="we")
        tk.Label(self, text='Address: ' + restaurant['locations'][i]['address']).grid(row=2, columnspan=2, sticky="nw")
        tk.Label(self, text='Website: ' + restaurant['locations'][i]['website']).grid(row=3, columnspan=2, sticky="nw")

        # Fixing phone number displaying blank.
        for res in restaurant['locations']:
            if not res['phone']:
                res['phone'] = 'unavailable'
        tk.Label(self, text='Contact number: ' + restaurant['locations'][i]['phone']).grid(row=4, columnspan=2, sticky="nw")

        # Adding restaurants menus in listbox
        tk.Label(self, text='Menu').grid(row=5, columnspan=2, sticky="n")
        self.scroll = tk.Scrollbar(self)
        self.scroll.grid(row=6, column=1, sticky="nsw")             # Grids scrollbar in 2nd column next to listbox
        self.LB = tk.Listbox(self, height=15, width=50, selectmode="multiple", yscrollcommand=self.scroll.set)
        self.LB.grid(row=6, padx=5, pady=10)
        self.scroll.config(command=self.LB.yview)


        tk.Button(self, text="Get menu",command = lambda : self.getMenu(menuID,dishesName)).grid(row=7,column=0,sticky="ns")

        self.resizable = (False, False)
        self.grab_set()

    def getMenu(self,menuID,dishesName):
        """Display nutritional values of selected dishes, which then is fetched from brandItemSearch and display it
        using NutritionLabel class.
        Arguments:
            menuID: a list of all food item IDs.
        """
        selectedMenu = self.LB.curselection()
        if selectedMenu is ():
            tkmb.showerror("Error", "Please select at least one food item.")
        elif not 0 < len(selectedMenu) <= 3:
            tkmb.showerror("Error", "Please choose up to 3 food items.")
        else:
            for index in selectedMenu:
                if menuID[index] is None:  # Checks if food item is a common item
                    foodData = commonItemSearch(dishesName[index].replace("(Common)", ""), BASE_URL, HEADERS)
                else:
                    foodData = brandItemSearch(menuID[index], BASE_URL, HEADERS)
                NutritionLabel(self, foodData)

if __name__ == '__main__':
    app = MainWin()
    gui2fg()            # For Mac
    app.mainloop()
