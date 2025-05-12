from scraper import scrape_emails_from_urls, is_allowed_by_robots
import json
from datetime import datetime
import os

DATA_FILE = "data/urls.txt"
OUTPUT_DIR = "output"

def load_urls_from_file(filepath):
    urls = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                urls.append(line)
    return urls

def save_results_to_file(results):
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Generate timestamp for the run folder
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_folder = os.path.join(OUTPUT_DIR, f"run_{timestamp}")
    os.makedirs(run_folder, exist_ok=True)
    
    # Save detailed results to JSON file
    detailed_file = os.path.join(run_folder, "detailed_results.json")
    with open(detailed_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Save consolidated emails to text file
    emails_file = os.path.join(run_folder, "all_emails.txt")
    all_emails = set()  
    for emails in results.values():
        all_emails.update(emails)
    
    with open(emails_file, 'w') as f:
        for email in sorted(all_emails):  # Sort emails for consistent output
            f.write(f"{email}\n")
    
    return run_folder

if __name__ == "__main__":
    url_list = load_urls_from_file(DATA_FILE)
    print(f"Attempting to find emails on {len(url_list)} URLs from {DATA_FILE}")
    print("---")
    print("IMPORTANT REMINDERS:")
    print("1. Check the website's 'robots.txt' and Terms of Service before running this for real.")
    print("2. This script is a basic example and might need changes for the specific website.")
    print("3. Use any found emails responsibly and ethically.")
    print("---")

    results = {}
    for url in url_list:
        print(f"Processing URL: {url} ...")
        if is_allowed_by_robots(url):
            results[url] = scrape_emails_from_urls([url])[url]
        else:
            print(f"\nURL: {url}")
            print("WARNING: This URL is not allowed to be scraped according to robots.txt. Skipping.")
            results[url] = []

    # Print results to console
    for url, emails in results.items():
        print(f"\nURL: {url}")
        if emails:
            print("Found potential email addresses:")
            for email in emails:
                print(email)
        else:
            print("No email addresses found or an error occurred.")

    # Save results to files
    output_folder = save_results_to_file(results)
    print(f"\nResults have been saved to folder: {output_folder}")
    print("Files created:")
    print(f"- {os.path.join(output_folder, 'detailed_results.json')}")
    print(f"- {os.path.join(output_folder, 'all_emails.txt')}")