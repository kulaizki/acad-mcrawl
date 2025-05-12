import requests
from bs4 import BeautifulSoup
import re

def find_emails_on_page(url):
    """
    Attempts to find email addresses on a single web page.

    DISCLAIMERS:
    1. This is a conceptual script and may need significant adaptation for any specific website.
    2. Always check the website's 'robots.txt' (e.g., url + '/robots.txt') and Terms of Service before scraping.
       Automated scraping may be against their terms.
    3. This script may not find emails that are obfuscated (e.g., using JavaScript, images, or [at] instead of @).
    4. Ethical use of any extracted email addresses is paramount. Contact individuals respectfully and for relevant purposes.
    5. Ensure you have a legitimate reason aligned with the purpose for which the email was made public.
    """
    emails_found = set() 

    try:
        # Add headers to mimic a browser visit
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Raises an exception for bad status codes (4XX or 5XX)

        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. Look for mailto links
        mailto_links = soup.select('a[href^="mailto:"]')
        for link in mailto_links:
            email = link['href'].replace('mailto:', '').split('?')[0] # Remove "mailto:" and any parameters
            if email:
                emails_found.add(email.strip())

        # 2. Look for email patterns in the visible text of the page
        email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        
        # Search in the whole text content
        page_text = soup.get_text(separator=' ') 
        found_in_text = re.findall(email_regex, page_text)
        for email in found_in_text:
            emails_found.add(email.strip())
            
        return list(emails_found)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

if __name__ == "__main__":
    target_publication_url = "https://pmc.ncbi.nlm.nih.gov/articles/PMC10402187/" 

    print(f"Attempting to find emails on: {target_publication_url}")
    print("---")
    print("IMPORTANT REMINDERS:")
    print("1. Check the website's 'robots.txt' and Terms of Service before running this for real.")
    print("2. This script is a basic example and might need changes for the specific website.")
    print("3. Use any found emails responsibly and ethically.")
    print("---")
    
    retrieved_emails = find_emails_on_page(target_publication_url)

    if retrieved_emails:
        print("\nFound potential email addresses:")
        for email in retrieved_emails:
            print(email)
    else:
        print("\nNo email addresses found or an error occurred.")