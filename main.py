from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv

url = 'https://www.dafiti.com.br/roupas-masculinas/'

# Configure Selenium to use the Chrome WebDriver (you can change this to another browser)
driver_path = '/LATEST_RELEASE_116.0.5845'
driver = webdriver.Chrome()

# Open the webpage in the browser
driver.get(url)

# Create a list to store all product data from all pages
all_product_data = []

while True:
    # Define a function to scroll down the page and load more products
    def scroll_down():
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Adjust the delay as needed
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    # Perform scrolling to load all products
    scroll_down()

    # Get the HTML content of the fully loaded page
    html_content = driver.page_source

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all product boxes (assuming each product is contained within a "product-box" div)
    product_boxes = soup.find_all('div', class_='product-box')

    # Create a list to store the extracted product data from the current page
    page_product_data = []

    # Iterate through each product box and extract information
    for product_box in product_boxes:
        product_title = product_box.find('p', class_='product-box-title').text.strip()
        product_brand = product_box.find('div', class_='product-box-brand').find('span').text.strip()
        price_from = product_box.find('span', class_='product-box-price-from').text.strip()
        try:
            price_to = product_box.find('span', class_='product-box-price-to').text.strip()
        except:
            price_to = price_from

        image_url = product_box.find('a', class_='product-box-link').find('img')['data-original']

        page_product_data.append({
            'Product Title': product_title,
            'Product Brand': product_brand,
            'Price From': price_from,
            'Price To': price_to,
            'Image URL': image_url
        })

    # Add the product data from the current page to the list of all product data
    all_product_data.extend(page_product_data)

    try:
        # Wait for the "Next" button to be clickable
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.page.next a'))
        )

        # Dismiss the cookie consent banner if it exists
        cookie_banner = driver.find_elements(By.XPATH, '//div[contains(@class, "cc-banner")]')
        if cookie_banner:
            ActionChains(driver).move_to_element(cookie_banner[0]).click().perform()

        # Scroll to the "Next" button to ensure it's in the viewport
        driver.execute_script("arguments[0].scrollIntoView();", next_button)

        # Scroll up a bit more to make the button visible
        driver.execute_script("window.scrollBy(0, -100);")

        # Scroll back up to the top
        driver.execute_script("window.scrollTo(0, 0);")

        # Click on the "Next" button
        next_button.click()
    except TimeoutException:
        # If there is no "Next" button, break out of the loop
        break

# Close the browser
driver.quit()

# Specify the CSV file path where you want to save all the data
csv_file_path = 'dafiti_male_products.csv'

# Write all the data to the CSV file
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['Product Title', 'Product Brand', 'Price From', 'Price To', 'Image URL']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for product in all_product_data:
        writer.writerow(product)

print("Data saved to", csv_file_path)
