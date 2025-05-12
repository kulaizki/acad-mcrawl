# Acad Mailcrawl

A specialized web scraper designed to extract publicly available academic and research email addresses from university and research institution websites while adhering to ethical crawling practices.

## Features

- Extracts email addresses from academic and research institution websites
- Respects robots.txt directives and implements polite crawling practices
- Configurable crawling depth and rate limiting
- Handles various academic website structures
- Exports results in a structured format
- Supports both single URL and batch processing
- Organized output with detailed results and consolidated email lists

## Project Structure

```
acad-mcrawl/
├── data/
│   └── urls.txt           # List of academic/research URLs to scrape, one per line
├── output/                # Directory containing scraping results
│   └── run_YYYYMMDD_HHMMSS/  # Each run creates a timestamped folder
│       ├── detailed_results.json  # Full results with URLs and emails
│       └── all_emails.txt        # Consolidated list of unique emails
├── scraper/
│   ├── __init__.py
│   └── scraper.py         # Core scraping logic with rate limiting and robots.txt compliance
├── main.py                # Entry point for running the scraper
├── requirements.txt       # Python dependencies
└── .gitignore
```

## How to Use

1. **Add URLs to Scrape:**
   - Edit `data/urls.txt` and paste academic/research institution URLs, one per line
   - Lines starting with `#` are treated as comments and ignored
   - Example URLs:
     ```
     https://cs.stanford.edu/people/
     https://www.cs.cornell.edu/people/faculty/
     https://www.csail.mit.edu/people
     ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Scraper:**
   ```bash
   python3 main.py
   ```
   - The script will process each URL and extract email addresses
   - Results are displayed in the console
   - Two output files are created in a timestamped folder:
     - `detailed_results.json`: Contains full mapping of URLs to emails
     - `all_emails.txt`: Contains a consolidated list of unique emails

## Output Structure

Each run of the scraper creates a new folder in the `output` directory with the format `run_YYYYMMDD_HHMMSS`. Inside this folder:

1. **detailed_results.json**
   - Contains the complete scraping results
   - Maps each URL to its found email addresses
   - Example:
     ```json
     {
       "https://example.edu/faculty": [
         "prof1@example.edu",
         "prof2@example.edu"
       ],
       "https://example.edu/researchers": [
         "researcher1@example.edu"
       ]
     }
     ```

2. **all_emails.txt**
   - Contains a consolidated list of all unique emails found
   - One email address per line
   - Sorted alphabetically
   - Example:
     ```
     prof1@example.edu
     prof2@example.edu
     researcher1@example.edu
     ```

## Ethical Considerations

- **Robots.txt Compliance:** The scraper automatically checks and respects robots.txt directives
- **Rate Limiting:** Implements polite crawling with configurable delays between requests
- **Data Usage:** Only extracts publicly available email addresses
- **Privacy:** Respects website terms of service and privacy policies
- **Responsible Use:** Intended for legitimate academic and research purposes only

## Best Practices

1. Always verify the website's robots.txt before scraping
2. Use appropriate delays between requests to avoid server overload
3. Only collect publicly available information
4. Respect website terms of service and privacy policies
5. Use the collected data responsibly and ethically
6. Consider implementing user-agent identification
7. Monitor and respect server response codes

## Notes

- The tool is designed specifically for academic and research institution websites
- Results may vary based on website structure and accessibility
- Some websites may block automated access
- Always ensure compliance with local laws and regulations regarding data collection

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 