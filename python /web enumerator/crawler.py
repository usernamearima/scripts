import requests
from urllib.parse import urljoin


def fetch_robots(base_url):
    robots_url = urljoin(base_url, "/robots.txt")
    try:
        response = requests.get(robots_url, timeout=5)
        if response.status_code == 200:
            return response.text.splitlines()
    except requests.RequestException:
        pass
    return []


def fetch_sitemap(base_url):
    sitemap_url = urljoin(base_url, "/sitemap.xml")
    links = []

    try:
        response = requests.get(sitemap_url, timeout=5)
        if response.status_code == 200:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.content, "xml")
            for loc in soup.find_all("loc"):
                links.append(loc.text)
    except requests.RequestException:
        pass

    return links
