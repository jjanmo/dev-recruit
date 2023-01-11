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
job_list = soup.find('ul', class_='jobsearch-ResultsList')
jobs = job_list.find_all('li', recursive=False)

results = []
for job in jobs:
    zone = job.find('div', class_='mosaic-zone')
    if zone is None:
        anchor = job.select_one('h2 a')
        title = anchor['aria-label']
        link = anchor['href']
        company = job.find('span', class_='companyName')
        location = job.find('div', class_='companyLocation')
        job_type = job.find('span', class_='jobsearch-JobMetadataHeader-item')

        result = {
            'company': company.string,
            'location': location.string,
            'position': title,
            'link': f'{INDEED_BASE_URL}{link}'
        }
        results.append(result)

        for result in results:
            print(result)
            print('/////')
