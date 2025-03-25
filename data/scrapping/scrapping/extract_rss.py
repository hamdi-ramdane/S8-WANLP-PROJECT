import requests
from bs4 import BeautifulSoup
import csv
import sys

# Force UTF-8 encoding for stdout
sys.stdout.reconfigure(encoding='utf-8')

rss_feeds = ["https://feeds.feedburner.com/aps-algerie-ar", 
        "http://feeds.aps.dz/aps-economie-ar",
        "http://feeds.aps.dz/aps-monde-ar",
        "http://feeds.aps.dz/aps-sport-ar",
        "http://feeds.aps.dz/aps-societe-ar",
        "http://feeds.aps.dz/aps-culture-ar",
        "http://feeds.aps.dz/aps-regions-ar",

        "https://www.ennaharonline.com/feed",

        "https://www.caert.org.dz/feed/",

        "https://www.alyaum.com/rssFeed/1005",
        "https://www.alyaum.com/rssFeed/1005/92",
        "https://www.alyaum.com/rssFeed/1005/93",
        "https://www.alyaum.com/rssFeed/1005/94",
        "https://www.alyaum.com/rssFeed/1005/95",
        "https://www.alyaum.com/rssFeed/1005/96"
]

def get_rss_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors

        text = response.text
        # save to xml file
        with open(f"scrapping/data/xml/{url.split("/")[-1]}.xml", "w", encoding="utf-8") as file:
            file.write(text)    
        return text
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def extract_xml_data(text):
    soup = BeautifulSoup(text, "xml")
    items = soup.find_all("item")
    news_data = []
    for item in items:
        title = item.find("title").get_text(strip=True) if item.find("title") else "N/A"
        author = item.find("author").get_text(strip=True) if item.find("author") else "N/A"
        link = item.find("link").get_text(strip=True) if item.find("link") else "N/A"
        pub_date = item.find("pubDate").get_text(strip=True) if item.find("pubDate") else "N/A"
        category = item.find("category").get_text(strip=True) if item.find("category") else "N/A"

        description = "N/A"
        desc_tag = item.find("description")
        if desc_tag:
            # Get raw text with HTML
            raw_desc = desc_tag.get_text(strip=True)
            # Parse the CDATA HTML content separately
            desc_soup = BeautifulSoup(raw_desc, "html.parser")
            # Get all <p> tags
            paragraphs = desc_soup.find_all("p")
            # Take only the first <p> (main content), exclude the "The post..." part
            if paragraphs:
                description = paragraphs[0].get_text(strip=True)
        news_item = {
            "title": title,
            "author": author,
            "category": category ,
            "pub_date": pub_date,
            "link": link,
            "description": description
        }
        news_data.append(news_item)
    return news_data 

def extract_rss():
    all_data = []
    for url in rss_feeds:
        text = get_rss_text(url)
        extracted_data = extract_xml_data(text)
        all_data.extend(extracted_data)

    # Write to CSV
    fieldnames = ["title", "author","category", "pub_date", "link", "description"]
    with open(f"scrapping/data/rss_data.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_data)

    print(f"RSS: {len(all_data)} Items saved to rss_data.csv")
    return all_data 

if __name__ == "__main__":
    extract_rss()



