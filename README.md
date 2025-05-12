# Neuromail Scraper

## Project Structure

```
neuromail-scraper/
├── data/
│   └── urls.txt           # List of URLs to scrape, one per line
├── scraper/
│   ├── __init__.py
│   └── scraper.py         # Scraper logic
├── main.py                # Entry point for running the scraper
├── requirements.txt       # Python dependencies
└── .gitignore
```

## How to Use

1. **Add URLs to Scrape:**
   - Edit `data/urls.txt` and paste your URLs, one per line. Lines starting with `#` are ignored.

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Scraper:**
   ```bash
   python main.py
   ```
   - The script will print found email addresses for each URL.

## Notes
- Always check the website's `robots.txt` and Terms of Service before scraping.
- Use any found emails responsibly and ethically. 