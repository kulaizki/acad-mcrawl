from scraper import scrape_emails_from_urls

DATA_FILE = "data/urls.txt"

def load_urls_from_file(filepath):
    urls = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                urls.append(line)
    return urls

if __name__ == "__main__":
    url_list = load_urls_from_file(DATA_FILE)
    print(f"Attempting to find emails on {len(url_list)} URLs from {DATA_FILE}")
    print("---")
    print("IMPORTANT REMINDERS:")
    print("1. Check the website's 'robots.txt' and Terms of Service before running this for real.")
    print("2. This script is a basic example and might need changes for the specific website.")
    print("3. Use any found emails responsibly and ethically.")
    print("---")

    results = scrape_emails_from_urls(url_list)
    for url, emails in results.items():
        print(f"\nURL: {url}")
        if emails:
            print("Found potential email addresses:")
            for email in emails:
                print(email)
        else:
            print("No email addresses found or an error occurred.")