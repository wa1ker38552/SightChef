import requests
import json
from bs4 import BeautifulSoup
from threading import Thread
import time

def get_recipe_data(page):
    response = requests.post("https://cosylab.iiitd.edu.in/recipedb/search_recipe",
    {
        'page': page,
        "autocomplete_region": "" ,
        "autocomplete_cuisine": "",
        "autocomplete_recipe": "", 
    }, headers={
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Length": "69",
        "Content-Type": "application/x-www-form-urlencoded",
        "Dnt": "1",
        "Host": "cosylab.iiitd.edu.in",
        "Origin": "https://cosylab.iiitd.edu.in",
        "Referer": "https://cosylab.iiitd.edu.in/recipedb/",
        "Sec-Ch-Ua": f'"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "Windows",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    })
    
    text = response.text.encode().decode()
    soup = BeautifulSoup(text, 'html.parser')
    table = soup.find("table", attrs={"id": "myTable"})
    body = table.find("tbody")

    for button in body.find_all("button"):
        text = "{" + button['onclick'].split("handleInfoClick({")[1].split("})")[0] + "}"
    return json.loads(text)

def worker(i, chunk):
    data = {}
    for c in chunk:
        print(i, c)
        d = get_recipe_data(c)
        data[d['Recipe_id']] = d
        with open(f'data/{i}.json', 'w') as file:
            file.write(json.dumps(data))

pages = list(range(5908))
THREADS = 25
chunks = [pages[i::25] for i in range(25)]

for i, c in enumerate(chunks):
    Thread(target=lambda: worker(i, c)).start()