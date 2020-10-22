import requests
from bs4 import BeautifulSoup
import json
import sys

url = 'https://www.thecocktaildb.com/api/json/v1/1/lookup.php?iid='

import sqlite3

conn = sqlite3.connect('ingredient.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS ingredients (
    id INTEGER UNIQUE,
    name TEXT,
    type TEXT,
    alcohol TEXT,
    abv REAL)''')
c.execute('''CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER UNIQUE,
    name TEXT,
    tags, TEXT
    category TEXT,
    alcoholic TEXT,
    glass TEXT,
    drinkThumb TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS join_recipes_to_ingredients (
    id INTEGER UNIQUE,
    id_recipe INTEGER,
    id_ingredient INTEGER,
    amount TEXT)''')
conn.commit()

# Start gathering ingredients
for i in range(1,609-1):
    search_url = url + str(i)

    try:
        page = requests.get(search_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        ingr = json.loads(str(soup))
        list_of_ingredients = list(ingr["ingredients"])
        ingr_dict = dict(list_of_ingredients[0])
        print('Ingredient #: '+str(i)+' Success!')
        insrt = (ingr_dict["idIngredient"],
                 ingr_dict["strIngredient"],
                 ingr_dict["strType"],
                 ingr_dict["strAlcohol"],
                 ingr_dict["strABV"])
        c.execute('''INSERT INTO ingredients VALUES (?,?,?,?,?)''',insrt)
    except:
        print('Ingredient #: '+str(i)+' Failed!')
        print("Unexpected error:", sys.exc_info()[0])

conn.commit()
conn.close()
