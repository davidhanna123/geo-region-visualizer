import requests
from bs4 import BeautifulSoup
import csv
import time

def get_bishop_details(profile_url):
    response = requests.get(profile_url)
    soup = BeautifulSoup(response.content, "html.parser")

    details = {
        "title": "",
        "monasticism": "",
        "episcopate": "",
        "patriarchate": "",
        "metropolitan": "",
        "birthdate": ""
    }

    items = soup.select("li.elementor-icon-list-item .elementor-icon-list-text")

    for item in items:
        text = item.get_text(strip=True)
        lower = text.lower()

        if not details["title"] and any(t in lower for t in ["pope", "bishop", "metropolitan"]):
            details["title"] = text

        if "patriarchate" in lower:
            details["patriarchate"] = text.split(":")[-1].strip()
        elif "episcopate" in lower:
            details["episcopate"] = text.split(":")[-1].strip()
        elif "monasticism" in lower:
            details["monasticism"] = text.split(":")[-1].strip()
        elif "metropolitan" in lower:
            details["metropolitan"] = text.split(":")[-1].strip()
        elif "birthdate" in lower:
            details["birthdate"] = text.split(":")[-1].strip()

    return details

def main():
    url = "https://copticorthodox.church/en/holysynod/synod-members/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    bishop_cards = soup.find_all("div", class_="dce-post-item")
    all_bishops = []

    for card in bishop_cards:
        name_tag = card.find("h4", class_="dce-post-title")
        name = name_tag.get_text(strip=True) if name_tag else ""

        if name.startswith("Fr."):
            continue
        
        profile_url = name_tag.find("a")["href"] if name_tag and name_tag.find("a") else ""
        img_tag = card.find("img")
        img_url = img_tag["src"] if img_tag else ""

        print(f"Scraping {name}...")
        bishop = {
            "name": name,
            "profile_url": profile_url,
            "image_url": img_url
        }

        if profile_url:
            profile_data = get_bishop_details(profile_url)
            bishop.update(profile_data)
            time.sleep(1)  

        all_bishops.append(bishop)

    keys = [
    "name", "title", "patriarchate", "metropolitan",
    "episcopate", "monasticism", "birthdate",
    "profile_url", "image_url"
    ]

    with open("data/bishops.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(all_bishops)

    print("✅ Saved bishop data to data/bishops.csv")

if __name__ == "__main__":
    main()
