import logging
import sys
import rethinkdb as r
import yaml
from apscheduler.jobstores.rethinkdb import RethinkDBJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, g, render_template, abort, request, flash, redirect, current_app

sys.path.append(".")
from forms import NewCollectionForm
from forms import NewJobForm
from forms import NewScheduleJobForm
from launch_job import launch_job, launch_scheduled_job

import brozzleradmin.database as db

app = Flask(__name__)
app.config.from_object('config')

rdb = r.RethinkDB()

def db_setup():

    connection = rdb.connect(app.config['RETHINKDB_SERVER'], app.config['RETHINKDB_PORT'])
    try:
        rdb.db_create(app.config['DATABASE']).run(connection)
        rdb.db(app.config['DATABASE']).table_create(app.config['TABLE_COLLECTIONS']).run(connection)
    except rdb.RqlRuntimeError:
        logging.info("Database already exist")
    finally:
        connection.close()


@app.before_request
def before_request():
    try:
        # TODO this is needed?
        sched = BackgroundScheduler()
        sched.add_jobstore(RethinkDBJobStore())
        sched.start()

        g.scheduler = sched
        g.database_conn = rdb.connect("localhost", 28015)
    except rdb.RqlDriverError:
        logging.critical("No database connection could be established.")
        abort(503, "No database connection could be established.")


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
            launch_scheduled_job(g.scheduler, request.args.get('collection'), form.job_name.data, form.job_config.data,
                                 form.job_schedule.data, form.job_hour.RethinkDB.data, form.job_minutes.data)
            return redirect('/')
        else:
            # get job_name
            job_name = db.generate_job_name(request.args.get('collection'))

            conf = db.get_last_job_configuration(request.args.get('collection'))
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
    if request.args.get('collection'):
        if form.validate_on_submit():
            launch_job(request.args.get('collection'), form.job_name.data, form.job_config.data)
            return redirect('/')
        else:
            # get job_name
            job_name = db.generate_job_name(request.args.get('collection'))

            conf = db.get_last_job_configuration(request.args.get('collection'))
            if conf:
                conf['id'] = job_name
            else:
                conf = ''

            conf = yaml.dump(conf)
            form = NewJobForm(job_name=job_name, job_config=conf)

    return render_template('new_job_form.html', form=form)


@app.route('/newcollection', methods=['GET', 'POST'])
def new_collection():
    form = NewCollectionForm()
    if form.validate_on_submit():
        db.new_collection(form.collection_name.data, form.collection_prefix.data)
        return redirect('/')
    else:
        flash('Invalid collection parameters')
        logging.info('Invalid collection parameters')
    return render_template('new_collection_form.html', form=form)


@app.route('/')
def list_collections():
    collections = list(
        rdb.db(current_app.config['DATABASE']).table(current_app.config['TABLE_COLLECTIONS']).run(g.database_conn))
    names = []
    for collection in collections:
        names.append(collection['name'])

    return render_template('index.html', collections=collections)


if __name__ == '__main__':
    logging.basicConfig(filename='heaven.log', level=logging.INFO)
    db_setup()
    app.run(debug=True, port=5001)
