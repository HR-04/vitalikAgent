import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://vitalik.eth.limo"

response = requests.get(f"{BASE_URL}/index.html")
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')

blog_links = []

for link in soup.find_all('a', href=True):
    href = link['href']
    if href.endswith('.html') and href != "index.html":
        full_url = BASE_URL + '/' + href
        blog_links.append(full_url)

print(f"Found {len(blog_links)} blog posts.")

data = []

for url in blog_links:
    try:
        blog_response = requests.get(url)
        blog_response.raise_for_status()
        blog_soup = BeautifulSoup(blog_response.text, 'html.parser')

        title_tag = blog_soup.find('h1')
        if not title_tag:
            title_tag = blog_soup.find('title')
        
        title = title_tag.text.strip() if title_tag else "No Title"

        paragraphs = blog_soup.find_all('p')
        content = "\n\n".join([p.get_text(strip=True) for p in paragraphs])

        data.append({
            'Title': title,
            'Content': content
        })

        print(f"Scraped: {title}")

        time.sleep(1)

    except Exception as e:
        print(f"Failed to scrape {url}: {e}")

df = pd.DataFrame(data)
df.to_excel('vitalik_blogs.xlsx', index=False)

print("Saved all blogs to vitalik_blogs.xlsx")
