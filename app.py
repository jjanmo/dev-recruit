from flask import Flask

from scrapper.wwr import extract_jobs

app = Flask(__name__)


@app.route('/')
def hello_world():
    jobs = extract_jobs('python')
    return jobs


if __name__ == '__main__':
    app.run()
