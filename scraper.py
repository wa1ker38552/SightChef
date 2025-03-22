import requests
import json
from bs4 import BeautifulSoup
import time

def get_recipe_data(page=0):
    response = requests.post("https://cosylab.iiitd.edu.in/recipedb/search_recipe",
                             {
                                'page': 1,
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
    
    with open("webpage.html", "w") as f:
        f.write(response.text)

def parse_recipe_data(filename: str):
    with open("webpage.html", "r") as f:
        text = f.read().encode().decode()

    soup = BeautifulSoup(text, 'html.parser')

    table = soup.find("table", attrs={"id": "myTable"})
    body = table.find("tbody")

    for button in body.find_all("button"):
        text = "{" + button['onclick'].split("handleInfoClick({")[1].split("})")[0] + "}"
        with open("test.json", "w") as f:
            f.write(json.dumps(json.loads(text), indent=2));

def parse_page():
    pass

if __name__ == "__main__":

    start_time = time.time()
    get_recipe_data()
    parse_recipe_data("webpage.html")
    print(time.time() - start_time)