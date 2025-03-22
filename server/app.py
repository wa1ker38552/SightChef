from flask import request
from flask import Flask
from PIL import Image


app = Flask(__name__)
version = '0.0.0'

@app.route('/')
def app_index():
    return f'v{version}'

@app.route('/api/process', methods=['POST'])
def api_process():
    img = Image.open(request.files['image'])
    return {'success': True}

app.run(host='0.0.0.0', port=8002)