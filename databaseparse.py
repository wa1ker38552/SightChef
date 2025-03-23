import json

data = json.loads(open('database_1.json', 'r').read())
with open('database_1.json', 'w') as file:
    file.write(json.dumps(data))