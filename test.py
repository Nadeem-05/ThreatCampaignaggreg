from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from bs4 import BeautifulSoup
import re
import time

brave_options = ChromeOptions()
brave_options.binary_location = '/usr/bin/brave-browser'  # Path to Brave binary
brave_options.add_argument("--headless")  # Ensure GUI is off

driver = webdriver.Chrome(options=brave_options)

url = "https://otx.alienvault.com/pulse/65f3218a873a7f237e5bc3b5"

driver.get(url)

time.sleep(5)  
page_source = driver.page_source

driver.quit()

soup = BeautifulSoup(page_source, "html.parser")

text_content = soup.get_text()

cleaned_text = re.sub(r'\s+', ' ', text_content)

print(cleaned_text.strip()) 
