import requests
import json

url = "https://trackapi.nutritionix.com/v2/locations?ll=37.321949,-122.048889&distance=1mi&limit=20"

# Add with brand_id
#url = "https://trackapi.nutritionix.com/v2/locations?ll=37.321949,-122.048889&distance=1mi&limit=20&brand_id=513fbc1283aa2dc80c00001f"

headers = {'x-app-id': "2713eda2",
           'x-app-key': "2f3f23571397305a0df5759ce0da0f2e",
           "Content-Type": "application/json"}


try:
    response = requests.get(url, headers=headers, timeout=30)
    data = json.loads(response.content.decode('utf-8'))
    data = json.dumps(data,indent = 4)
    pythonOb = json.loads(data) # Convert back to python object to get total number of restaurants
    print("Total number of restaurants: ",len(pythonOb["locations"]))
    print(data)
except requests.exceptions.HTTPError as e:
    print ("HTTP Error:", e)
except requests.exceptions.ConnectionError as e:
    print ("Error Connecting:", e)
except requests.exceptions.Timeout as e:
    print ("Timeout Error:", e)
except requests.exceptions.RequestException as e:
    print ("Request exception: ", e)
