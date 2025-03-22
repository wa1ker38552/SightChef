from flask import request
from flask import Flask

app = Flask(__name__)
version = '0.0.0'

@app.route('/')
def app_index():
    return f'v{version}'

app.run(host='0.0.0.0', port=8002)