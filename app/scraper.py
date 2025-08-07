# app/scraper.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

BASE_URL = "https://books.toscrape.com/"
DATA_DIR = "/tmp"
CSV_PATH = os.path.join(DATA_DIR, "books.csv")

def extract_books(pages=1):
    books = []
    book_id = 1
    
    for page in range(pages):
        next_url = BASE_URL + (f"catalogue/page-{page+1}.html")    
        print(f"Extraindo página {page+1}: {next_url}")
        response = requests.get(next_url)
        if response.status_code != 200:
            raise Exception(f"Erro ao acessar a página: {next_url}")
        soup = BeautifulSoup(response.text, 'html.parser')

        articles = soup.select("article.product_pod")

        for article in articles:
            title = article.h3.a["title"]
            price = article.select_one(".price_color").text.strip()
            availability = article.select_one(".availability").text.strip()
            rating = article.p["class"][1]
            relative_url = article.h3.a["href"]
            url = f"https://books.toscrape.com/catalogue/{relative_url}"
            image_url = "https://books.toscrape.com/" + article.img["src"].replace("../", "")

            book_response = requests.get(url)
            book_soup = BeautifulSoup(book_response.text, "html.parser")
            category = book_soup.select("ul.breadcrumb li a")[-1].text.strip()
            disponibility = book_soup.select_one("table.table.table-striped tr:nth-child(6) td").text.strip()

            books.append({
                "id": book_id,
                "title": title,
                "price": price,
                "availability": availability,
                "rating": rating,
                "disponibility": disponibility,
                "category": category,
                "image": image_url,
            })
            book_id += 1

    os.makedirs(DATA_DIR, exist_ok=True)
    pd.DataFrame(books).to_csv(CSV_PATH, index=False)

