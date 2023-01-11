from flask import Flask

from scrapper.wwr import extract_wwr_job
from scrapper.indeed import extract_indeed_job

app = Flask(__name__)


@app.route('/')
def hello_world():
    keyword = input("What do you want to search for?")

    wwr_jobs = extract_wwr_job(keyword)
    indeed_jobs = extract_indeed_job(keyword)
    jobs = wwr_jobs + indeed_jobs

    file = open(f'{keyword}.csv', 'w')
    file.write('Position, Company, Location, Link \n')

    for job in jobs:
        file.write(f'{job["position"]}, {job["company"]}, {job["location"]}, {job["link"]} \n')
    file.close()

    return 'hello world'


if __name__ == '__main__':
    app.run()
