from bs4 import BeautifulSoup
from requests import get

WWR_BASE_URL = 'https://weworkremotely.com'
REQUEST_URL = f'{WWR_BASE_URL}/remote-jobs/search?term='


def extract_jobs(keyword):
    response = get(f'{REQUEST_URL}{keyword}')
    results = []

    if response.status_code == 200:
        html_doc = response.text
        soup = BeautifulSoup(html_doc, 'html.parser')
        jobs = soup.find_all('section', class_='jobs')

        for job in jobs:
            job_items = job.find_all('li')
            for item in job_items:
                if 'view-all' in item['class']:
                    continue
                company, job_type, region = item.find_all('span', class_="company")
                position = item.find('span', class_="title").text
                link = item.find_all('a')[1].attrs['href']
                logo = None
                logo_elem = item.find_all('a')[0].find('div', class_="flag-logo")
                if logo_elem is not None:
                    logo = logo_elem['style'].split('(')[1].split(')')[0]

                result = {
                    'company': company.text,
                    'job_type': job_type.text,
                    'region': region.text,
                    'position': position,
                    'link': f'{WWR_BASE_URL}{link}',
                    'logo': logo
                }
                results.append(result)
    else:
        print('Can`t request website')

    return results
