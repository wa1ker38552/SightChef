import json
import time
import tqdm

def work(recipes: list):

    for recipe in recipes:

        database["recipes"][recipe["Recipe_id"]] = recipe

        for ingredient in recipe["ingredients"]:
            name = (ingredient["ingredient_name"]).strip().lower()
            if database["ingredients"][name] != None:
                #Database indexed by ingredients, containing a dictionary with all 
                #of the recipes that can be made with that ingredient 
                database["ingredients"][name][recipe["Recipe_id"]] = True
            else:
                database["ingredients"][name] = {
                    recipe["Recipe_id"]: True
                }

if __name__ == "__main__":
    database = {"recipes": {}, "ingredients": {}}
    for num in range(25):
        with open(f"data/{num}.json", "r") as f:
            recipes = json.loads(f.read())
            work(recipes)