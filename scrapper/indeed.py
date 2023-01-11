from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

INDEED_BASE_URL = 'https://kr.indeed.com'
REQUEST_URL = f'{INDEED_BASE_URL}/jobs?q='


def get_source(keyword, query_string=''):
    options = Options()
    options.add_experimental_option("detach", True)  # prevent auto-Off
    driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
    driver.get(f'{REQUEST_URL}{keyword}{query_string}')
    source = driver.page_source

    return source, driver


def get_page_count(keyword):
    source, driver = get_source(keyword)
    soup = BeautifulSoup(source, 'html.parser')
    page_nav = soup.find('nav', attrs={'role': 'navigation'})

    if page_nav is None:
        return 1
    else:
        pages = list(page_nav.children)
        last_page = pages[-1].find('a')['data-testid']

        if last_page == 'pagination-page-next':
            return len(pages) - 1
        else:
            return len(pages)

    driver.close()


def extract_indeed_job(keyword):
    page_count = get_page_count(keyword)

    results = []
    for i in range(page_count):
        source, driver = get_source(keyword, f'&start={i * 10}')
        soup = BeautifulSoup(source, 'html.parser')
        job_list = soup.find('ul', class_='jobsearch-ResultsList')
        jobs = job_list.find_all('li', recursive=False)

        for job in jobs:
            zone = job.find('div', class_='mosaic-zone')
            if zone is None:
                anchor = job.select_one('h2 a')
                title = anchor['aria-label']
                link = anchor['href']
                company = job.find('span', class_='companyName')
                location = job.find('div', class_='companyLocation')

                result = {
                    'company': company.string,
                    'location': location.string,
                    'position': title,
                    'link': f'{INDEED_BASE_URL}{link}'
                }
                results.append(result)

        driver.close()

    return results
