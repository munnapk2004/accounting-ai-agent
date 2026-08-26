import os
import requests
from bs4 import BeautifulSoup

# Define key IRS HTML publications to pull
PUBLICATIONS = {
    "irs_pub334.txt": "https://www.irs.gov/publications/p334",  # Tax Guide for Small Business
    "irs_pub535.txt": "https://www.irs.gov/publications/p535",  # Business Expenses
}

OUTPUT_DIR = "knowledge_base"

def fetch_irs_publications():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    for filename, url in PUBLICATIONS.items():
        try:
            response = requests.get(url, headers=headers, timeout=20)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extract main content body, discarding site navigation
            main_content = soup.find("article") or soup.find("main") or soup.find("body")
            
            filepath = os.path.join(OUTPUT_DIR, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"=== SOURCE: {url} ===\n\n")
                f.write(main_content.get_text(separator="\n", strip=True))
                
            print(f"Successfully updated {filename}")
        except Exception as e:
            print(f"Error fetching {url}: {e}")

if __name__ == "__main__":
    fetch_irs_publications()
