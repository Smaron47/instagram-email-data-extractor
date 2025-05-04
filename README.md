**Google Search Results Scraper — Extended Documentation**

---

## 1. Project Overview

This project is a Python-based automation tool built using Selenium WebDriver. Its primary purpose is to perform Google search queries (specifically targeting Instagram profiles) and extract structured data such as profile URLs, usernames (detected as `@username`), and email addresses (like `example@gmail.com`) from the search results. The tool uses controlled browser automation, dynamic scrolling, and pagination to reveal and capture extended search result data. Extracted data is saved into a CSV file for easy review or further processing.

### 1.1 Core Functionalities

* **Search Automation**: Navigate to Google, perform a predefined query, and iterate through results.
* **Dynamic Content Handling**: Use keyboard simulation and button interactions to load more data.
* **Data Extraction**: Identify and capture URLs, snippet content, usernames, and email addresses.
* **Regex Parsing**: Isolate usernames and email addresses from free text using regular expressions.
* **CSV Export**: Store the cleaned data in a structured CSV format.
* **Robust Browser Session**: Cleanly handles session lifecycle with exception management.

---

## 2. File & Directory Structure

```plaintext
/ (project root)
│
├─ scraper_google.py        # Primary script for scraping logic
├─ requirements.txt         # Python dependencies
├─ output.csv               # Output file storing results
└─ README.md                # Project documentation
```

---

## 3. Environment Setup

### 3.1 Prerequisites

* **Python**: Version 3.7 or higher
* **Google Chrome**: Installed and updated on your system
* **Chromedriver**: Matching your Chrome version; should be added to system PATH

### 3.2 Installation

Run the following command to install the necessary Python package:

```bash
pip install selenium
```

### 3.3 Optional Setup

If you wish to run the browser in headless mode (no GUI), add the following line in your script setup:

```python
chrome_options.add_argument('--headless')
```

---

## 4. Script Components (`scraper_google.py`)

### 4.1 Imports

```python
import csv
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
```

### 4.2 Helper Functions

#### `extract_username(text)`

Extracts an Instagram-style username using regex:

```python
def extract_username(text):
    match = re.search(r'@(\w+)', text)
    return match.group(1) if match else None
```

#### `extract_email(text)`

Extracts email addresses from text:

```python
def extract_email(text):
    match = re.search(r'(\S+@\S+)', text)
    return match.group(1) if match else None
```

---

### 4.3 Main Function — `scrape_google_search_results(url, output_file)`

This function orchestrates the web scraping session:

```python
def scrape_google_search_results(url, output_file):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--lang=en')
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)
        time.sleep(2)

        for _ in range(5):
            for __ in range(15):
                ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
                time.sleep(1)
            try:
                more = driver.find_element(By.XPATH, '//a[@class="T7sFge sW9g3e VknLRd"]')
                more.click()
            except Exception:
                break  # Stop if button not found

        links = [e.get_attribute('href') for e in driver.find_elements(By.XPATH, '//a[@jsname="UWckNb"]')]
        snippets = [e.text for e in driver.find_elements(By.XPATH, '//div[@class="kb0PBd cvP2Ce"]')]
        usernames = [extract_username(txt) for txt in snippets]
        emails = [extract_email(txt) for txt in snippets]

        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['Link','Username','Email'])
            writer.writeheader()
            for link, user, mail in zip(links, usernames, emails):
                writer.writerow({'Link': link, 'Username': user, 'Email': mail})

    except Exception as err:
        print(f"Error: {err}")
    finally:
        driver.quit()
```

### Workflow Summary

1. **Initialization**: Launch Chrome in incognito mode.
2. **Query Execution**: Load the provided Google search URL.
3. **Scrolling & Expansion**: Use simulated keypresses to scroll; click "More results" if available.
4. **Content Parsing**: Gather all visible links and snippets.
5. **Regex Application**: Filter out usernames and emails from text.
6. **Data Export**: Save as CSV.
7. **Cleanup**: Ensure browser is closed regardless of success/failure.

---

## 5. Usage Guide

### 5.1 Basic Steps

1. **Open** `scraper_google.py` in your editor.
2. **Edit** the `google_search_url` to reflect your desired search:

   ```python
   google_search_url = "https://www.google.com/search?q=site%3Ainstagram.com+%22model%22+%22bangladesh%22+%22%40gmail.com%22"
   ```
3. **Run** the script using:

   ```bash
   python scraper_google.py
   ```
4. **Output** will be available in `output.csv`

---

## 6. Error Handling

* **Element Not Found**: Script uses `try/except` to prevent crashing when UI elements like the "More results" button are missing.
* **Graceful Shutdown**: The browser always closes via `finally` block.
* **Print Trace**: Console logging of errors for troubleshooting.

---

## 7. Extensions & Improvements

* **Headless Browsing**: Add `--headless` to avoid GUI loading.
* **Smart Pagination**: Dynamically detect end of results instead of fixed scroll count.
* **User-Agent Spoofing**: Set custom user-agent via `chrome_options.add_argument()`.
* **Proxy Support**: Add proxy routing for anonymity or regional targeting.
* **Database Output**: Store output in SQLite/PostgreSQL instead of CSV.
* **Parallel Execution**: Use `concurrent.futures` for multi-query processing.
* **UI Frontend**: Create a web GUI for non-technical users.

---

## 8. Debugging Tips

* **Check Selectors**: Use Chrome DevTools to verify XPaths.
* **Test Regex Separately**: Validate regex patterns in an online tester.
* **Sleep Times**: Adjust `time.sleep()` to account for internet speed.
* **Avoid CAPTCHA**: Excessive scraping might trigger CAPTCHA. Throttle frequency.

---

## 9. SEO Keywords

```plaintext
google scraper selenium python
selenium scroll scraper
instagram email data extractor
profile username crawler
regex parser python scraper
selenium google search automation
scrape instagram links from Google
python automation csv export
```

---

*© 2025 Smarom Biswas. Licensed under MIT.*
