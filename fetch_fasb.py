import os
import xml.etree.ElementTree as ET
import requests

RSS_URL = "https://www.fasb.org/rss/asu"  # FASB Update Feed
OUTPUT_FILE = "knowledge_base/fasb_updates.txt"

def update_fasb_data():
    # Create knowledge_base folder if it doesn't exist
    os.makedirs("knowledge_base", exist_ok=True)
    try:
        response = requests.get(RSS_URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("=== FASB RECENT ACCOUNTING STANDARDS UPDATES ===\n\n")
            for item in root.findall(".//item"):
                title = item.find("title").text if item.find("title") is not None else ""
                desc = item.find("description").text if item.find("description") is not None else ""
                f.write(f"TITLE: {title}\nSUMMARY: {desc}\n{'-'*40}\n")
        print("FASB knowledge updated successfully.")
    except Exception as e:
        print(f"Error fetching FASB RSS: {e}")

if __name__ == "__main__":
    update_fasb_data()
