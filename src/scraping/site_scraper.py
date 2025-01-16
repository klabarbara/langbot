import requests
from bs4 import BeautifulSoup
import os
import json

def scrape_website(url, output_file="data/raw/website_content.json"):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # http error exception

        soup = BeautifulSoup(response.content, "lxml")

        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
        headers = [h.get_text(strip=True) for h in soup.find_all(["h1", "h2", "h3"])]

        content = {"url": url, "headers": headers, "paragraphs": paragraphs}

        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(content, f, ensure_ascii=False, indent=4)

        print(f"Scraped content saved to {output_file}")
    except Exception as e:
        print(f"Error scraping {url}: {e}")

if __name__ == "__main__":
    scrape_website("https://zh.wikipedia.org")
