"Foodie" - CIS 41B Final Project
Instructor Clare Nguyen
June 23, 2019
Team Members: Duc Huy Nguyen, Minhduc Cao

// What does it do?
This program provides users with nutritional values information from common foods and
various food brands for the purpose of improving their eating habits. The program has four functions, which are:
querying a food data API (Nutritionix.com) based on user-input to show nutritional label for a single food item,
calculating total calories counts from up to 4 different food items, displaying a graph of average calories
based on user input item and display nutritional labels for menu items from nearby restaurants.


>>> IMPORTANT <<<
Our program requires the use of an external Python module called 'geocoder', specifically for api.py.
It is documented here: https://pypi.org/project/geocoder/

If you already have pip installed, please skip this part:
    1. To install pip, go to this link https://www.liquidweb.com/kb/install-pip-windows/ and download get-pip.py
    2. Open a command prompt and navigate to the folder containing get-pip.py.
    3. Run the following command: python get-pip.py
    4. Pip is now installed, you can run >>> pip --version and >>> python -m pip install --upgrade pip

Please install the module via command line by executing the following line without quotes:
'pip install geocoder'

If the installation fails, please let one of us know so we can remove code that deals with the module.

In addition, the API we're using has data restrictions on searching items which prompted us to add limits on
pull data from the API. However, in the case of excessive testing, we have included multiple keys that you can
swap from by changing the value of 'API_KEY_SET' from 0 to 1, 2, or 3 in the case that api.py throws a KeyError
exception.


// What does it contain? - main.py
main.py runs the GUI windows with the 4 choices (listed above) using imported functions from api.py to
pull data from the API and display it to the user.


// What does it contain? - api.py
api.py contains functions to pull data from the API to perform a general search, specific branded item search,
common item search, and a local restaurant search based on current location.


// Project Requirements - Topics
Data Analysis / Visualization - main.py with plotting graphs to show calorie count with as well as an average
GUI - main.py with the use of tkinter windows
Web Access - api.py with the use of functions to pull data from the Nutritionix API
Multiprocessing - main.py with the use of multithreading to pull data from the API based on multiple queries
