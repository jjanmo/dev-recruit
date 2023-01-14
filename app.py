from flask import Flask, render_template, request
from scrapper.wwr import extract_wwr_job
from scrapper.indeed import extract_indeed_job
from file import save_to_file

app = Flask(__name__)

fake_db = {}


@app.route('/')
def home():
    # save_to_file(keyword, jobs)

    return render_template('home.html')


@app.route('/result')
def result():
    keyword = request.args.get('keyword')

    if keyword not in fake_db:
        wwr_jobs = extract_wwr_job(keyword)
        indeed_jobs = extract_indeed_job(keyword)
        jobs = wwr_jobs + indeed_jobs

        fake_db[keyword] = jobs
    else:
        jobs = fake_db[keyword]

    return render_template(
        'result.html', keyword=keyword,
        jobs=jobs,
        total_count=len(jobs)
    )


if __name__ == '__main__':
    app.run(debug=True)
