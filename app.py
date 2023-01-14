from flask import Flask, render_template, request, redirect, send_file
from scraper.wwr import extract_wwr_job
from scraper.indeed import extract_indeed_job
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
    if keyword == '' or keyword is None:
        return redirect('/')

    if keyword in fake_db:
        jobs = fake_db[keyword]
    else:
        wwr_jobs = extract_wwr_job(keyword)
        indeed_jobs = extract_indeed_job(keyword)
        jobs = wwr_jobs + indeed_jobs
        fake_db[keyword] = jobs

    return render_template(
        'result.html', keyword=keyword,
        jobs=jobs,
        total_count=len(jobs)
    )


@app.route('/export')
def export():
    keyword = request.args.get('keyword')
    if keyword is None:
        return redirect('/')
    if keyword not in fake_db:
        return redirect(f'/result?keyword={keyword}')

    save_to_file(keyword, fake_db[keyword])
    return send_file(f'{keyword}.csv', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
