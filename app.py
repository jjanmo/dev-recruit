from flask import Flask
from scrapper.wwr import extract_wwr_job
from scrapper.indeed import extract_indeed_job
from file import save_to_file

app = Flask(__name__)


@app.route('/')
def home():
    keyword = input("What do you want to search for?")

    wwr_jobs = extract_wwr_job(keyword)
    indeed_jobs = extract_indeed_job(keyword)
    jobs = wwr_jobs + indeed_jobs

    save_to_file(keyword, jobs)

    return 'hello world'


if __name__ == '__main__':
    app.run()
