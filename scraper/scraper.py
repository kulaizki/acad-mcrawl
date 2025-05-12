import requests
from bs4 import BeautifulSoup
import re
import io
try:
    from PyPDF2 import PdfReader
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False

def clean_email(email):
    """Clean up email addresses that might have extra characters after standard TLDs."""
    standard_tlds = ['.com', '.edu', '.org', '.net', '.gov', '.mil', '.int', '.io', '.co', '.ac', '.uk', '.ca', '.de', '.jp', '.fr', '.au', '.ru', '.ch', '.it', '.nl', '.se', '.no', '.es', '.in']
    
    email = email.strip()
    for tld in standard_tlds:
        tld_pos = email.lower().find(tld)
        if tld_pos > 0:
            return email[:tld_pos + len(tld)]
    return email  

def find_emails_on_page(url):
    emails_found = set()
    page_text = None
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30) # Increased timeout to 30s
        response.raise_for_status()

        content_type = response.headers.get('content-type', '').lower()

        if 'application/pdf' in content_type and PYPDF2_AVAILABLE:
            # Handle PDF
            try:
                pdf_file = io.BytesIO(response.content)
                reader = PdfReader(pdf_file)
                text_parts = [page.extract_text() for page in reader.pages if page.extract_text()]
                page_text = ' '.join(text_parts)
            except Exception as pdf_err:
                print(f"Error processing PDF {url}: {pdf_err}") # Added specific PDF error log
                return [] # Return empty list on PDF processing error
        elif 'html' in content_type:
            # Handle HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            mailto_links = soup.select('a[href^="mailto:"]')
            for link in mailto_links:
                email = link['href'].replace('mailto:', '').split('?')[0]
                if email:
                    emails_found.add(clean_email(email.strip()))
            page_text = soup.get_text(separator=' ')
        else:
            # Handle other content types or cases where PyPDF2 is not installed
            # Try to decode as text, might work for plain text files
            try:
                page_text = response.text
            except Exception:
                 print(f"Non-HTML/PDF content type encountered for {url}: {content_type}. Skipping text extraction.")
                 # We might still have mailto links if we could parse somehow, but unlikely.
                 # If we have emails from mailto links already, keep them. Otherwise return empty.
                 return list(emails_found) if emails_found else []


        # Common processing for text extracted from HTML or PDF
        if page_text:
            # Use a broader regex to catch potential emails, then clean them
            email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,20}'
            found_in_text = re.findall(email_regex, page_text)
            for email in found_in_text:
                emails_found.add(clean_email(email.strip()))

        return list(emails_found)
    except requests.exceptions.Timeout:
        print(f"Timeout occurred while fetching {url}")
        return []
    except requests.exceptions.RequestException as req_err:
        print(f"Request error for {url}: {req_err}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred for {url}: {e}")
        return []

def scrape_emails_from_urls(url_list):
    results = {}
    if not PYPDF2_AVAILABLE:
        print("Warning: PyPDF2 not installed. PDF processing will be skipped. Run 'pip install PyPDF2'")
    for url in url_list:
        results[url] = find_emails_on_page(url)
    return results 