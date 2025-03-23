from flask_cors import CORS
from flask import request
from flask import Flask
from PIL import Image
import base64
import json
import io

db = json.loads(open('../database.json', 'r').read())
app = Flask(__name__)
CORS(app)
version = '0.0.0'

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
    img.show()
    return {'success': True}

app.run(host='0.0.0.0', port=8002)