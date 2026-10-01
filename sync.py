import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://cdn.iptvboss.pro/logos/"
OUTPUT_ROOT = "logos"

# Add or uncomment countries here to expand your backup.
# Folder names must match the server path exactly (case-sensitive).
TARGET_COUNTRIES = [
    "USA",
    "Canada",
    # "UK",
]

def sync_country(country):
    source_url = urljoin(BASE_URL, f"{country.strip('/')}/")
    country_dir = os.path.join(OUTPUT_ROOT, country)

    if not os.path.exists(country_dir):
        os.makedirs(country_dir)

    print(f"\n--- Syncing category: {country} ---")
    try:
        response = requests.get(source_url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch {source_url}: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')
    valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp')

    for link in links:
        href = link.get('href')
        if not href or href.startswith('?') or href in ('../', '/'):
            continue
            
        if href.lower().endswith(valid_extensions):
            file_url = urljoin(source_url, href)
            file_name = href.split('/')[-1]
            file_path = os.path.join(country_dir, file_name)

            if not os.path.exists(file_path):
                print(f"Downloading [{country}]: {file_name}")
                try:
                    img_data = requests.get(file_url).content
                    with open(file_path, 'wb') as f:
                        f.write(img_data)
                except Exception as e:
                    print(f"Failed to download {file_url}: {e}")

def main():
    for country in TARGET_COUNTRIES:
        sync_country(country)

if __name__ == "__main__":
    main()
