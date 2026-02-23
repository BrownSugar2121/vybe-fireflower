import requests
from bs4 import BeautifulSoup
import json
import time
import requests
from bs4 import BeautifulSoup
import json
import time

BASE = "https://fireandflower.com/shop/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_product_links(category_url):
    res = requests.get(category_url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    links = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/shop/product/" in href:
            if href.startswith("/"):
                href = "https://fireandflower.com" + href
            links.add(href)

    return list(links)

def scrape_product(url):
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    text = soup.get_text()

    meta_title = soup.find("meta", property="og:title")
    name = meta_title["content"].strip() if meta_title else None

    # Price
    price_tag = soup.find("span", class_="price")
    price = price_tag.text.strip() if price_tag else None

    # Check for THC/CBD info if available
    thc_match = None
    cbd_match = None

    return {
        "name": name,
        "price": price,
        "thc": thc_match,
        "cbd": cbd_match,
        "in_stock": True,
        "url": url
    }

all_products = []

print("Scraping main shop page...")
links = get_product_links(BASE)

for link in links:
    try:
        product = scrape_product(link)
        all_products.append(product)
        print("Scraped:", product["name"])
        time.sleep(0.5)
    except Exception as e:
        print("Error:", link, e)

with open("menu.json", "w") as f:
    json.dump(all_products, f, indent=2)

print("Done. Saved to fireflower_menu.json")
