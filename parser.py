import json
import time
import tqdm

def work(recipes: list):

    for recipe in recipes:

        database["Recipes"][recipe["Recipe_id"]] = recipe

        for ingredient in recipe["Ingredients"]:
            name = (ingredient["ingredient_name"]).strip().lower()
            if name in database["Ingredients"]:
                #Database indexed by ingredients, containing a dictionary with all 
                #of the recipes that can be made with that ingredient 
                database["Ingredients"][name][recipe["Recipe_id"]] = ""
            else:
                database["Ingredients"][name] = {
                    recipe["Recipe_id"]: ""
                }

if __name__ == "__main__":
    database = {"Recipes": {}, "Ingredients": {}}
    for num in tqdm.tqdm(range(25)):
        with open(f"data/{num}.json", "r") as f:
            recipes = json.loads(f.read()).values()
        work(recipes)

        with open("database_1.json", "w") as f:
            f.write(json.dumps(database, indent=2))
