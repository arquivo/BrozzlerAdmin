import argparse
import logging
import os

import yaml
from flask import Flask, g, render_template, request, flash, redirect
from jinja2 import Template

from brozzleradmin.database import DataBaseAccess
from brozzleradmin.forms import NewCrawlRequestForm
from brozzleradmin.forms import NewCustomJobForm
from brozzleradmin.forms import NewJobForm
from brozzleradmin.forms import NewScheduleJobForm
from brozzleradmin.launch_job import launch_job, launch_scheduled_job

app = Flask(__name__)
db = DataBaseAccess()


# TODO remake this
@app.route('/newschedulejob', methods=['GET', 'POST'])
def new_schedule_job():
    form = NewScheduleJobForm()
    if request.args.get('crawlrequest'):
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


def generate_job_template(job_id, job_type, crawl_request_name, crawl_request_prefix, seeds, ignore_robots):
    template_name = None
    if job_type[0] == '1':
        template_name = 'job_templates/template_single_page_crawl.yaml'
    elif job_type[0] == '2':
        template_name = 'job_templates/template_domain_crawl.yaml'
    elif job_type[0] == '3':
        template_name = 'job_templates/template_twitter_crawl.yaml'
    elif job_type[0] == '4':
        template_name = 'job_templates/template_1_hop_daily_crawl.yaml'
    elif job_type[0] == '5':
        template_name = 'job_templates/template_1_hopoff_crawl.yaml'

    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, template_name), mode='r') as file_template:
        job_template = Template(file_template.read())
        job_config = job_template.render(job_id=job_id, crawl_request_name=crawl_request_name,
                                         crawl_request_prefix=crawl_request_prefix, seeds=seeds.split(),
                                         ignore_robots=ignore_robots)
    return job_config


@app.route('/newjob', methods=['GET', 'POST'])
def new_job():
    form = NewJobForm()
    crawl_request_name = request.args.get('crawlrequest')
    if crawl_request_name:
        if form.validate_on_submit():
            job_id = db.generate_job_name(crawl_request_name)
            job_config = generate_job_template(job_id, form.job_template_config.data, crawl_request_name,
                                               form.job_warc_prefix.data, form.job_seeds.data, form.job_robots.data)

            launch_job(db, crawl_request_name, job_id, job_config)
            return redirect('/')
        else:
            job_name = request.args.get('crawlrequest')
            conf = db.get_last_job_configuration(request.args.get('crawlrequest'))
            if conf:
                conf['id'] = job_name
            else:
                conf = ''

            conf = yaml.dump(conf)
            form = NewJobForm(job_name=job_name, job_config=conf)

    return render_template('new_job_form.html', form=form)


@app.route('/newcustomjob', methods=['GET', 'POST'])
def new_custom_job():
    form = NewCustomJobForm()
    if request.args.get('crawlrequest'):
        if form.validate_on_submit():
            launch_job(request.args.get('crawlrequest'), form.job_name.data, form.job_config.data)
            return redirect('/')
        else:
            job_name = request.args.get('crawlrequest')
            conf = db.get_last_job_configuration(request.args.get('crawlrequest'))
            if conf:
                conf['id'] = job_name
            else:
                conf = ''

            conf = yaml.dump(conf)
            form = NewCustomJobForm(job_name=job_name, job_config=conf)

    return render_template('new_custom_job_form.html', form=form)


@app.route('/crawlrequest', methods=['GET', 'POST'])
def new_crawl_request():
    form = NewCrawlRequestForm()
    if form.validate_on_submit():
        db.new_crawl_request(form.crawl_request_name.data)
        return redirect('/')
    else:
        flash('Invalid crawl request parameters')
        logging.info('Invalid crawl request parameters')
    return render_template('new_crawl_request_form.html', form=form)


@app.route('/')
def list_crawl_requests():
    crawl_requests = db.list_crawlrequests()
    names = []
    for crawl_request in crawl_requests:
        names.append(crawl_request['name'])

    return render_template('index.html', crawl_requests=crawl_requests)


def main():
    logging.basicConfig(level=logging.INFO)

    # specify configuration file
    parser = argparse.ArgumentParser(epilog=(
        'You can specify a specific configuration using the following environment variables:\n\n'
        ' BROZZLER_ADMIN_CONFIGURATION  <path to config.py>'
    ))
    parser.add_argument('--host', default='localhost',
                        help='Setup host interface to listen. ( Setup 0.0.0.0 to bind all interfaces)')
    parser.add_argument('--port', default=5001, help='Specify port that app will listen.')
    parser.add_argument('--debug', action='store_true', help='Start in flask debug mode.')

    args = parser.parse_args()

    app.config.from_pyfile('config.py')
    app.config.from_envvar('BROZZLER_ADMIN_CONFIGURATION')
    app.run(debug=args.debug, port=args.port, host=args.host)


if __name__ == '__main__':
    main()
