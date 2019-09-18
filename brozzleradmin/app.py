import logging
import sys

import yaml
from flask import Flask, g, render_template, request, flash, redirect, current_app
import doublethink

sys.path.append(".")
from forms import NewCrawlRequestForm
from forms import NewJobForm
from forms import NewScheduleJobForm
from launch_job import launch_job, launch_scheduled_job

import brozzleradmin.database as db

app = Flask(__name__)
app.config.from_object('config')

@app.teardown_request
def teardown_request(exception):
    try:
        g.database_conn.close()
    except AttributeError:
        logging.warning("Some problems occurred closing the database connection")


@app.route('/newschedulejob', methods=['GET', 'POST'])
def new_schedule_job():
    job_name = ''
    conf = ''
    form = NewScheduleJobForm()
    if request.args.get('collection'):
        if form.validate_on_submit():
            launch_scheduled_job(g.scheduler, request.args.get('crawlrequest'), form.job_name.data,
                                 form.job_config.data,
                                 form.job_schedule.data, form.job_hour.RethinkDB.data, form.job_minutes.data)
            return redirect('/')
        else:
            # get job_name
            job_name = db.generate_job_name(request.args.get('crawlrequest'))

            conf = db.get_last_job_configuration(request.args.get('crawlrequest'))
            if conf:
                conf['id'] = job_name
            else:
                conf = ''

            conf = yaml.dump(conf)
            form = NewScheduleJobForm(job_name=job_name, job_config=conf)

    return render_template('new_scheduled_job_form.html', form=form)


@app.route('/newjob', methods=['GET', 'POST'])
def new_job():
    job_name = ''
    conf = ''
    form = NewJobForm()
    if request.args.get('crawlrequest'):
        if form.validate_on_submit():
            launch_job(request.args.get('crawlrequest'), form.job_name.data, form.job_config.data)
            return redirect('/')
        else:
            # get job_name
            job_name = db.generate_job_name(request.args.get('crawlrequest'))

            conf = db.get_last_job_configuration(request.args.get('crawlrequest'))
            if conf:
                conf['id'] = job_name
            else:
                conf = ''

            conf = yaml.dump(conf)
            form = NewJobForm(job_name=job_name, job_config=conf)

    return render_template('new_job_form.html', form=form)


@app.route('/crawlrequest', methods=['GET', 'POST'])
def new_crawl_request():
    form = NewCrawlRequestForm()
    if form.validate_on_submit():
        db.new_crawl_request(form.crawl_request_name.data, form.crawl_request_prefix.data)
        return redirect('/')
    else:
        flash('Invalid crawl request parameters')
        logging.info('Invalid crawl request parameters')
    return render_template('new_crawl_request_form.html', form=form)


@app.route('/')
def list_collections():
    rr = doublethink.Rethinker(servers=['localhost:28015'], db=current_app.config['DATABASE'])
    crawl_requests = list(rr.table(current_app.config['TABLE_CRAWLREQUESTS']).run())
    names = []
    for crawl_request in crawl_requests:
        names.append(crawl_request['name'])

    return render_template('index.html', crawl_requests=crawl_requests)


if __name__ == '__main__':
    logging.basicConfig(filename='brozzleradmin.log', level=logging.INFO)
    app.run(debug=True, port=5001)
