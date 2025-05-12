import requests
from bs4 import BeautifulSoup
import re

def find_emails_on_page(url):
    emails_found = set()
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        mailto_links = soup.select('a[href^="mailto:"]')
        for link in mailto_links:
            email = link['href'].replace('mailto:', '').split('?')[0]
            if email:
                emails_found.add(email.strip())
        email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        page_text = soup.get_text(separator=' ')
        found_in_text = re.findall(email_regex, page_text)
        for email in found_in_text:
            emails_found.add(email.strip())
        return list(emails_found)
    except requests.exceptions.RequestException:
        return []
    except Exception:
        return []

def scrape_emails_from_urls(url_list):
    results = {}
    for url in url_list:
        results[url] = find_emails_on_page(url)
    return results 