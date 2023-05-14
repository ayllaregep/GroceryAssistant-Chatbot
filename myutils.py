import googlemaps
import requests
import random
import json

GMAPS_API_KEY = 'AIzaSyAqZbfo0-AbD_t0ef5uZIzHt6QSOaxbiY4'

gmaps = googlemaps.Client(key=GMAPS_API_KEY)


def load_recipes_from_file(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

recipes = load_recipes_from_file("./database/recipes.json")

def get_nearby_stores(user_location, search_radius):
    places = gmaps.places_nearby(
        location=user_location,
        radius=search_radius,
        type='grocery_or_supermarket'
    )

    nearby_stores = []
    for place in places['results']:
        store_name = place['name']
        store_address = place['vicinity']
        nearby_stores.append((store_name, store_address))

    return nearby_stores

def get_recipe_by_keyword(shopping_list):
    if len(shopping_list) == 0:
        return None, None 

    random_item = random.choice(shopping_list).lower()

    matching_recipes = [recipe for recipe in recipes if random_item in recipe["ingredients"]]

    if len(matching_recipes) == 0:
        return None, None

    selected_recipe = random.choice(matching_recipes)
    return selected_recipe["name"], selected_recipe["ingredients"]