import os
import xml.etree.ElementTree as ET
import requests

# GASB News / Pronouncements Feed
RSS_URL = "https://www.gasb.org/rss/gasb_news"
OUTPUT_FILE = "knowledge_base/gasb_updates.txt"

def update_gasb_data():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        response = requests.get(RSS_URL, headers=headers, timeout=15)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("=== GASB PRONOUNCEMENTS & GOVERNMENTAL ACCOUNTING UPDATES ===\n\n")
            for item in root.findall(".//item"):
                title = item.find("title").text if item.find("title") is not None else ""
                desc = item.find("description").text if item.find("description") is not None else ""
                pub_date = item.find("pubDate").text if item.find("pubDate") is not None else ""
                
                f.write(f"DATE: {pub_date}\n")
                f.write(f"TITLE: {title}\n")
                f.write(f"SUMMARY: {desc}\n")
                f.write(f"{'-'*50}\n")
                
        print("GASB knowledge updated successfully.")
    except Exception as e:
        print(f"Error fetching GASB RSS feed: {e}")
        # Write fallback header if feed structure changes
        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write("\nNote: GASB RSS feed update attempted.\n")

if __name__ == "__main__":
    update_gasb_data()
