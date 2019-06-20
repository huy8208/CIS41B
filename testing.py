import collections
from api import *

BASE_URL = "https://trackapi.nutritionix.com/v2"                # URL for Nutritionix API calls
HEADERS = {'x-app-id': "d43b95b0",
           'x-app-key': "ccc1f54d0392398034fcda2a489c3522",
           "Content-Type": "application/json"}

x = brandItemSearch("5a66df14df2fd71d72e5ed29", BASE_URL, HEADERS)
print(x)
for k, v in x.items():
    print(k, v)


"""
{'Apple (Common)': None, 'Apples (Common)': None, 'Apple Pie (Common)': None, 'Applepear (Common)': None, 'Appletini (Common)': None, 'Gala Apple (Common)': None, 'Applejacks (Common)': None, 'Applejuice (Common)': None, 'Applesauce (Common)': None, 'Apple Cider (Common)': None, 'Apple Sauce (Common)': None, 'Apple Juice (Common)': None, 'Applebutter (Common)': None, 'Green Apple (Common)': None, 'Applefritter (Common)': None, 'Apple Oatmeal (Common)': None, 'Apple Strudel (Common)': None, 'Apple Cider Vinegar (Common)': None, 'Unsweetened Applesauce (Common)': None, 'Evans Apples Green Apples (Common)': None, 'Bite Size Dry Salami, Spicy': '5aa0e0ebfc2eb0e754513df6', 'Cheddar Cheese, Minis': '591d48c38dc161941ddebb90', 'Mini Wafers, Vanilla': '599fcc623486467f3a8210b8', 'Organic Chicken & Maple Breakfast Sausage': '57c4fd949ce6c17244a22237', 'Organic Uncured Beef Hot Dog': '58e3470d4d6d23825ac0216f', 'Pork Carnitas, Seasoned & Seared': '59c608bc7bbbe596167a518f', 'Sparkling Apple Juice': '5a28e75263c33ab62319fe3d', 'Turkey Breast, Oven Roasted': '5a66df14df2fd71d72e5ed29', 'Uncured Black Forest Ham': '51c36add97c3e69de4b0758a', 'Uncured Thick Cut Bacon, Hickory Smoked': '57f0472c8458302154168dd0', 'Oatmeal Bar, Chocolate': '54e43f972348c2ed72bd9ab7', 'The Great Uncured Chicken Hot Dog, Organic': '557b215a7ba850e50f3d2ed7', 'Organic Apple Snack, No Sugar Added': '57f30663f495154d6a481077', 'Apple & Strawberry Fruit Snack': '5ca855705673df464273bfe9', 'Apple & Strawberry Snack': '5a8e6c7557cdcb2b74c8739a', 'Applesauce with Peaches': '55082bd9d51a79c5575dd4a7', 'Applesauce, Unsweetened': '5937a6ae189f473117d27803', 'Chicken & Maple Breakfast Sausage': '51c36af597c3e69de4b07630', 'Herb Turkey Breast': '51c36ae197c3e69de4b075a8', 'Hot Dog, Uncured Beef': '51c36af897c3e69de4b07644'}


Apple (Common) None
Apples (Common) None
Apple Pie (Common) None
Applepear (Common) None
Appletini (Common) None
Gala Apple (Common) None
Applejacks (Common) None
Applejuice (Common) None
Applesauce (Common) None
Apple Cider (Common) None
Apple Sauce (Common) None
Apple Juice (Common) None
Applebutter (Common) None
Green Apple (Common) None
Applefritter (Common) None
Apple Oatmeal (Common) None
Apple Strudel (Common) None
Apple Cider Vinegar (Common) None
Unsweetened Applesauce (Common) None
Evans Apples Green Apples (Common) None
Bite Size Dry Salami, Spicy 5aa0e0ebfc2eb0e754513df6
Cheddar Cheese, Minis 591d48c38dc161941ddebb90
Mini Wafers, Vanilla 599fcc623486467f3a8210b8
Organic Chicken & Maple Breakfast Sausage 57c4fd949ce6c17244a22237
Organic Uncured Beef Hot Dog 58e3470d4d6d23825ac0216f
Pork Carnitas, Seasoned & Seared 59c608bc7bbbe596167a518f
Sparkling Apple Juice 5a28e75263c33ab62319fe3d
Turkey Breast, Oven Roasted 5a66df14df2fd71d72e5ed29
Uncured Black Forest Ham 51c36add97c3e69de4b0758a
Uncured Thick Cut Bacon, Hickory Smoked 57f0472c8458302154168dd0
Oatmeal Bar, Chocolate 54e43f972348c2ed72bd9ab7
The Great Uncured Chicken Hot Dog, Organic 557b215a7ba850e50f3d2ed7
Organic Apple Snack, No Sugar Added 57f30663f495154d6a481077
Apple & Strawberry Fruit Snack 5ca855705673df464273bfe9
Apple & Strawberry Snack 5a8e6c7557cdcb2b74c8739a
Applesauce with Peaches 55082bd9d51a79c5575dd4a7
Applesauce, Unsweetened 5937a6ae189f473117d27803
Chicken & Maple Breakfast Sausage 51c36af597c3e69de4b07630
Herb Turkey Breast 51c36ae197c3e69de4b075a8
Hot Dog, Uncured Beef 51c36af897c3e69de4b07644
"""



"""
{'food_name': 'Turkey Breast, Oven Roasted', 'brand_name': 'Applegate', 'id': '5a66df14df2fd71d72e5ed29', 'brand_id': '51db37b5176fe9790a8988b3', 'serving_qty': 2, 'serving_unit': 'oz', 'photo': {'thumb': 'https://d1r9wva3zcpswd.cloudfront.net/5a66df18df2fd71d72e5ed2a.jpeg', 'highres': None, 'is_user_uploaded': False}, 'ingredients': None, 'calories': 50, 'total_fat': 0, 'sat_fat': 0, 'cholesterol': 30, 'sodium': 400, 'total_carbs': 0, 'fiber': 0, 'sugar': 0, 'protein': 12}


food_name Turkey Breast, Oven Roasted
brand_name Applegate
id 5a66df14df2fd71d72e5ed29
brand_id 51db37b5176fe9790a8988b3
serving_qty 2
serving_unit oz
photo {'thumb': 'https://d1r9wva3zcpswd.cloudfront.net/5a66df18df2fd71d72e5ed2a.jpeg', 'highres': None, 'is_user_uploaded': False}
ingredients None
calories 50
total_fat 0
sat_fat 0
cholesterol 30
sodium 400
total_carbs 0
fiber 0
sugar 0
protein 12
"""
