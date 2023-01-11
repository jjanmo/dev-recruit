from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

INDEED_BASE_URL = 'https://kr.indeed.com'
REQUEST_URL = f'{INDEED_BASE_URL}/jobs?q='
search_term = 'python'

options = Options()
options.add_experimental_option("detach", True)  # prevent auto-Off
driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
driver.get(f'{REQUEST_URL}{search_term}')
source = driver.page_source

soup = BeautifulSoup(source, 'html.parser')
result = soup.find('ul', class_='jobsearch-ResultsList')
items = result.find_all('li', recursive=False)
print(items)
for item in items:
    zone = item.find('div', class_='mosaic-zone')
    if zone is None:
        print('job li')
