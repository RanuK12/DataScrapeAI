"""Module for scraping web pages."""

import random
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

from .utils import USER_AGENTS, extract_text, sanitize_filename


def scrape_url(url: str, timeout: int = 30) -> dict:
    """Fetch a URL, extract text, and return a data dictionary.

    Args:
        url: The web page URL to scrape.
        timeout: Request timeout in seconds.

    Returns:
        dict with keys: url, title, text, timestamp.
    """
    headers = {"User-Agent": random.choice(USER_AGENTS)}

    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Error fetching {url}: {e}") from e

    html = resp.text
    title = None
    soup = BeautifulSoup(html, "html.parser")
    if soup.title and soup.title.string:
        title = soup.title.string.strip()

    text = extract_text(html)

    data = {
        "url": url,
        "title": title,
        "text": text,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    return data
