import requests
from urllib.parse import urlparse, urljoin
import re

def get_robots_url(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}/robots.txt"

def fetch_robots_content(robots_url):
    try:
        response = requests.get(robots_url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException:
        return None

def is_allowed_by_robots(url, user_agent='*'):
    robots_url = get_robots_url(url)
    content = fetch_robots_content(robots_url)
    if not content:
        return True  # If robots.txt is not found, assume allowed
    parsed = urlparse(url)
    path = parsed.path
    if not path:
        path = '/'
    lines = content.splitlines()
    allow_rules = []
    disallow_rules = []
    current_agent = None
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = re.split(r':\s*', line, 1)
        if len(parts) != 2:
            continue
        key, value = parts
        key = key.lower()
        if key == 'user-agent':
            current_agent = value
        elif key == 'allow' and current_agent in (user_agent, '*'):
            allow_rules.append(value)
        elif key == 'disallow' and current_agent in (user_agent, '*'):
            disallow_rules.append(value)
    for rule in disallow_rules:
        if path.startswith(rule):
            return False
    for rule in allow_rules:
        if path.startswith(rule):
            return True
    return True  