from flask import Flask

from scrapper.wwr import extract_wwr_job
from scrapper.indeed import extract_indeed_job

app = Flask(__name__)


@app.route('/')
def hello_world():
    keyword = input("What do you want to search for?")

    wwr_jobs = extract_wwr_job(keyword)
    indeed_jobs = extract_indeed_job(keyword)

    return wwr_jobs + indeed_jobs


if __name__ == '__main__':
    app.run()
