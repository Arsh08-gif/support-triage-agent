import requests
from bs4 import BeautifulSoup
import os
import time

CORPUS_DIR = "corpus"

SOURCES = {
    "hackerrank": {
        "base_url": "https://support.hackerrank.com",
        "start_urls": ["https://support.hackerrank.com/hc/en-us"],
        "allowed_path": "/articles"
    },
    "claude": {
        "base_url": "https://support.claude.com",
        "start_urls": ["https://support.claude.com/en/"],
        "allowed_path": "/en/"
    },
    "visa": {
        "base_url": "https://www.visa.co.in",
        "start_urls": [
            "https://www.visa.co.in/support.html",
            "https://www.visa.co.in/support/consumer/lost-stolen-card.html",
            "https://www.visa.co.in/support/consumer/travel-support.html",
            "https://www.visa.co.in/contact-us.html",
        ],
        "allowed_path": "/support"
    }
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; SupportBot/1.0)"
}

def scrape_page(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        # Remove junk
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        text = soup.get_text(separator="\n")
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        return "\n".join(lines), soup
    except Exception as e:
        print(f"  Failed: {url} → {e}")
        return "", None

def get_links(soup, base_url, allowed_path):
    """Extract all links from a page that belong to the same support site."""
    links = set()
    if not soup:
        return links
    for a in soup.find_all("a", href=True):
        href = a["href"]
        # Build full URL if relative
        if href.startswith("/"):
            href = base_url + href
        # Only keep links within the allowed path
        if allowed_path in href and href.startswith(base_url):
            links.add(href.split("?")[0])  # strip query params
    return links

def crawl(company, config):
    base_url = config["base_url"]
    allowed_path = config["allowed_path"]

    visited = set()
    to_visit = set(config["start_urls"])
    all_text = []

    print(f"\nCrawling {company}...")

    while to_visit:
        url = to_visit.pop()
        if url in visited:
            continue
        visited.add(url)

        print(f"[{len(visited)}] {url}")
        text, soup = scrape_page(url)

        if text:
            all_text.append(f"--- SOURCE: {url} ---\n{text}")

        # Find new links to follow
        new_links = get_links(soup, base_url, allowed_path)
        for link in new_links:
            if link not in visited:
                to_visit.add(link)

        time.sleep(0.5)  # be polite

        # Safety cap — don't crawl forever
        if len(visited) >= 100:
            print(f"  Reached 100 page limit for {company}, stopping.")
            break

    return all_text

def build_corpus():
    os.makedirs(CORPUS_DIR, exist_ok=True)

    for company, config in SOURCES.items():
        all_text = crawl(company, config)

        out_path = os.path.join(CORPUS_DIR, f"{company}.txt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n\n".join(all_text))

        print(f"  Saved {len(all_text)} pages to {out_path}")

if __name__ == "__main__":
    build_corpus()
    print("\nDone! Corpus built successfully.")