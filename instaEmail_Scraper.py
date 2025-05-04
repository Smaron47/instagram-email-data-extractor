import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import re
def extract_username(text):
    # Extract username using regex
    username_match = re.search(r'@(\w+)', text)
    username = username_match.group(1) if username_match else None
    return username
def extract_email(text):
    # Extract email using regex
    email_match = re.search(r'(\S+@\S+)', text)
    email = email_match.group(1) if email_match else None

    return email




def scrape_google_search_results(url, output_file):
    # Specify the path to your webdriver
    webdriver_path = '/path/to/your/chromedriver'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--lang=en')
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Open the provided URL
        driver.get(url)
        time.sleep(2)

        # Perform scrolling
        for _ in range(5):
            for _ in range(15):
                ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
                time.sleep(1)

            # Click on "More results"
            more_results_button = driver.find_element(By.XPATH, '//a[@class="T7sFge sW9g3e VknLRd"]')
            more_results_button.click()

        # # Perform additional scrolling
        # for _ in range(30):
        #     ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
        #     time.sleep(1)

        # Extract data
        links = [link.get_attribute('href') for link in driver.find_elements(By.XPATH, '//a[@jsname="UWckNb"]')]
        details = [detail.text for detail in driver.find_elements(By.XPATH, '//div[@class="kb0PBd cvP2Ce"]')]
        usernames = [extract_username(i.text) for i in driver.find_elements(By.XPATH, '//a[@jsname="UWckNb"]')]
        emails = [extract_email(i) for i in details]

        # Save data to CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Link', 'Username', 'Email']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write header
            writer.writeheader()

            # Write data
            for link, detail, username, email in zip(links, details, usernames, emails):
                writer.writerow({'Link': link, 'Username': username, 'Email': email})

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    google_search_url = "https://www.google.com/search?q=site%3Ainstagram.com+%22model%22+%22bangladesh%22+%22%40gmail.com%22&sca_esv=594611910&sxsrf=AM9HkKmQWIPaTvaFUgez6DwMQIiCQwWdhg%3A1703954031924&source=hp&ei=b0aQZYPAMP7S2roPqaegsAw&oq=&gs_lp=EhFtb2JpbGUtZ3dzLXdpei1ocCIAKgIIADIHECMY6gIYJzINECMYgAQYigUY6gIYJzINECMYgAQYigUY6gIYJzINECMYgAQYigUY6gIYJzIHECMY6gIYJzINECMYgAQYigUY6gIYJzIHECMY6gIYJzIHECMY6gIYJzIHECMY6gIYJzINECMYgAQYigUY6gIYJzIHECMY6gIYJzINECMYgAQYigUY6gIYJzINECMYgAQYigUY6gIYJzINECMYgAQYigUY6gIYJzINECMYgAQYigUY6gIYJ0iHJlAAWABwAXgAkAEAmAEAoAEAqgEAuAEByAEAqAIP&sclient=mobile-gws-wiz-hp#ip=1"
    output_csv_file = "output.csv"
    scrape_google_search_results(google_search_url, output_csv_file)
    