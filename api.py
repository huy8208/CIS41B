"""
CIS 41B (01Y)
Final Project - api.py
~ Module storing all functions related to pulling data from the Nutritionix API

TO DO LIST:
1. Check if ATTRIBUTES and NEW_ATTRIBUTES work properly

@author Huy Nguyen, Minhduc Cao
@version 1.2
@date 2019.06.19
"""
import json
import requests
import geocoder  # Custom installed Python module to get current latitude and longtitude

ATTRIBUTES = ['food_name', 'nix_brand_name', 'nix_item_id', 'nix_brand_id', 'serving_qty', 'serving_unit', 'photo', 'nf_ingredient_statement', 'nf_calories', 'nf_total_fat', 'nf_saturated_fat', 'nf_cholesterol', 'nf_sodium', 'nf_total_carbohydrate', 'nf_dietary_fiber', 'nf_sugars', 'nf_protein']
NEW_ATTRIBUTES = ['food_name', 'brand_name', 'id', 'brand_id', 'serving_qty', 'serving_unit', 'photo', 'ingredients', 'calories', 'total_fat', 'sat_fat', 'cholesterol', 'sodium', 'total_carbs', 'fiber', 'sugar', 'protein']


def genSearch(query: str, baseURL: str, headers: dict) -> dict:
    """Does a general search on the Nutritionix API and returns common and branded food results and their ids

    Arguments:
        query (string): food item to be looked up
        baseURL (string): Nutritionix API URL without additional endpoints
        headers (dictionary): headers to request data from API, includes API keys
    Returns:
        itemDict (dictionary): contains common and branded food items and their item ids (if any)
    """
    url = baseURL + "/search/instant?query=" + query
    try:
        response = requests.get(url, headers=headers)
        data = json.loads(response.content.decode('utf-8'))

        results = {}
        for commonItem in data["common"]:           # Common items have '(Common)' attached to the key and a value of None for item id
            results[commonItem['food_name'].title() + " (Common)"] = None
        for brandItem in data["branded"]:           # Branded items are assigned their nix_brand_id for later searching
            results[brandItem["food_name"]] = brandItem["nix_item_id"]
        return results
    except requests.exceptions.HTTPError as err:
        print("HTTP Error:", str(err))
    except requests.exceptions.ConnectionError as err:
        print("Error Connecting:", str(err))
    except requests.exceptions.Timeout as err:
        print("Timeout Error:", str(err))
    except requests.exceptions.RequestException as err:     # Catch-all for any other Request exceptions
        print("Request Exception:", str(err))


def brandItemSearch(id: str, baseURL: str, headers: dict) -> dict:
    """Does an individual search for an branded item using the item id to return nutrient data

    Arguments:
        id (string): Nutritionix item id for branded food item to be searched
        baseURL (string): Nutritionix API URL without additional endpoints
        headers (dictionary): headers to request data from API, includes API keys
    Returns:
        itemDict (dictionary): contains nutrient and identification for a specified branded food item
    """
    url = baseURL + "/search/item?nix_item_id=" + id
    try:
        response = requests.get(url, headers=headers)
        data = json.loads(response.content.decode('utf-8'))

        itemDict = {}
        for i in range(len(ATTRIBUTES)):
            itemDict[NEW_ATTRIBUTES[i]] = data['foods'][0].get(ATTRIBUTES[i], None)
        return itemDict
    except requests.exceptions.HTTPError as err:
        print("HTTP Error:", str(err))
    except requests.exceptions.ConnectionError as err:
        print("Error Connecting:", str(err))
    except requests.exceptions.Timeout as err:
        print("Timeout Error:", str(err))
    except requests.exceptions.RequestException as err:     # Catch-all for any other Request exceptions
        print("Request Exception:", str(err))


def commonItemSearch(query: str, baseURL: str, headers: dict) -> dict:
    """Does an individual search for a common item using the item name to return nutrient data

    Arguments:
        query (string): Nutritionix common food item name to be searched
        baseURL (string): Nutritionix API URL without additional endpoints
        headers (dictionary): headers to request data from API, includes API keys
    Returns:
        itemDict (dictionary): contains nutrient and identification for a specified common food item
    """
    url = baseURL + "/natural/nutrients"
    try:
        response = requests.post(url, headers=headers, json={"query": query})
        data = json.loads(response.content.decode('utf-8'))

        itemDict = {}
        for i in range(len(ATTRIBUTES)):
            itemDict[NEW_ATTRIBUTES[i]] = data['foods'][0].get(ATTRIBUTES[i], None)
        return itemDict
    except requests.exceptions.HTTPError as err:
        print("HTTP Error:", str(err))
    except requests.exceptions.ConnectionError as err:
        print("Error Connecting:", str(err))
    except requests.exceptions.Timeout as err:
        print("Timeout Error:", str(err))
    except requests.exceptions.RequestException as err:     # Catch-all for any other Request exceptions
        print("Request Exception:", str(err))


def getNearbyRestaurants(baseURL: str, headers: dict) -> dict:
    """Gets a dictionary of nearby restaurants based on current location from Nutritionix API

    Arguments:
        baseURL (string): Nutritionix API URL without additional endpoints
        headers (dictionary): headers to request data from API, includes API keys
    Returns:
        json.loads... (dictionary): contains data and ID of nearby restaurants within a span of 2 miles
    """
    myloc = geocoder.ip('me')   # Get current latitude and longitude based on IP address
    url = baseURL + "/locations?ll=%s,%s&distance=2mi&limit=20" % (myloc.latlng[0], myloc.latlng[1])
    try:
        response = requests.get(url, headers=headers, timeout=30)
        return json.loads(response.content.decode('utf-8'))
    except requests.exceptions.HTTPError as err:
        print("HTTP Error:", str(err))
    except requests.exceptions.ConnectionError as err:
        print("Error Connecting:", str(err))
    except requests.exceptions.Timeout as err:
        print("Timeout Error:", str(err))
    except requests.exceptions.RequestException as err:     # Catch-all for any other Request exceptions
        print("Request Exception:", str(err))
