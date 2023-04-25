"""
This file contains the code for fetching documentation from whatever necessary framework.

It contains an explicit mapping of URLs from frameworks. 
"""

import re
import requests
from bs4 import BeautifulSoup
from infra.cache  import get_cache, set_cache

framework_urls = {
    "Next13": {
        "base_url": "https://beta.nextjs.org/docs",
        "match": "https://beta.nextjs.org/docs",
    }
}

def get_absolute_link(url: str, link: str):
    # take a current url and get its base_url:
    base_url = re.match(r"(https?://[^/]+)", url).group(1)
    
    if link.startswith("http"):
        return link
    else:
        return base_url + link

def fetch_page_content(url: str, match: str, visited: set):
    # cached = get_cache(url)
    # if cached:
    #     return cached

    if url in visited:
        return []

    print("Visiting URL: " + url)
    visited.add(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.title.string
    content = soup.get_text(separator="\n", strip=True)

    docs = [{"url": url, "title": title, "content": content}]

    links = [get_absolute_link(url, a['href']) for a in soup.find_all('a', href=True) if match in get_absolute_link(url, a['href'])]

    for link in links:
        docs.extend(fetch_page_content(link, match, visited))

    return docs

def fetch_docs(framework: str):

    # if not, crawl and download
    base_url = framework_urls[framework]["base_url"]
    match = framework_urls[framework]["match"]

    visited = set()
    docs = fetch_page_content(base_url, match, visited)

    # # checks if embedded
    # for doc in docs:
    #     set_cache(doc['url'], docs)

    return docs