import requests

'''response = requests.post('http://127.0.0.1:8002/api/process', files={'image': open('pantry.png', 'rb')})
print(response.json())'''

import json

'''headers = {
    'Accent': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accent-Encodings': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Origin': 'https://cosylab.iiitd.edu.in',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'Sec-Fetch-Site': 'same-origin',
    'Referer': 'https://cosylab.iiitd.edu.in/recipedb/'
}
data = {
    'page': 1,
    'autocomplete_region': '',
    'autocomplete_cuisine': '',
    'autocomplete_recipe': ''
}
r = requests.post('https://cosylab.iiitd.edu.in/recipedb/search_recipe', headers=headers, data=data)

with open('test.html', 'w') as file:
    file.write(r.text)'''


'''data = json.loads(open('../database.json', 'r').read())

while True:
    i = input('> ')
    if i in data['Ingredients']:
        print([key for key in data['Ingredients'][i]])'''

data = json.loads(open('../data/0.json', 'r').read())
print(data['100017'])