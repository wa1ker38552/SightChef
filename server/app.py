from flask_cors import CORS
from flask import request
from flask import Flask
from PIL import Image
import base64
import json
import io
import sys
sys.path.append(r"C:\Users\walke\Downloads\VSCode\SightChef")

from model.main import get_ingredients  

db = json.loads(open("database.json", "r").read())
app = Flask(__name__)
CORS(app)
version = '0.0.0'

def match_recipes_from_ingredients(ingredients: list[str]):
    for i in range(len(ingredients)):
        ingredients[i] = ingredients[i].lower().strip()

    all_recipes = []
    possible_recipes = []

    for ingredient in ingredients:
        recipes = db['Ingredients'][ingredient]
        for recipe in (list(recipes.keys())):
            if recipe not in all_recipes:
                all_recipes.append(recipe)

    for recipe in all_recipes:
        recipe = db["Recipes"][recipe]
        count = 0
        for ingredient in recipe['Ingredients']:
            if ingredient['ingredient_name'].lower().strip() in ingredients:
                count += 1
            
        if (count/len(recipe['Ingredients']) > 0.2 and recipe not in possible_recipes):
            possible_recipes.append([recipe, count/len(recipe['Ingredients'])])

    return possible_recipes

def match_recipes(image):
    ingredients = get_ingredients(image)
    return {
        'ingredients': ingredients,
        'recipes': match_recipes_from_ingredients(ingredients)
    }

@app.route('/')
def app_index():
    return f'v{version}'

@app.route('/api/search')
def api_search():
    i = request.args.get('ingredient')
    ingredients = db['Ingredients']
    if i in ingredients:
        return {
            'success': True,
            'data': [{
                'name': db['Recipes'][recipe]['Recipe_title'],
                'image': db['Recipes'][recipe]['img_url'],
                'url': db['Recipes'][recipe]['url']
            } for recipe in ingredients[i]]
        }
    return {'success': False}

@app.route('/api/process', methods=['POST'])
def api_process():
    ct = request.headers.get('Content-Type')
    if 'json' in ct:
        data = request.json
        data['image'] = data['image'].replace('data:image/jpeg;base64,', '')
        img = Image.open(io.BytesIO(base64.b64decode(data['image'])))
    else:
        img = Image.open(request.files['image'])
    return {'success': True, 'data': match_recipes(img)}

app.run(host='0.0.0.0', port=8002)