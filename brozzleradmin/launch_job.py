import logging
from datetime import datetime, timedelta

import doublethink
import yaml
from brozzler import model, new_job
from brozzleradmin.utils import get_url_base


# TODO Add logging starting and scheduling jobs

def launch_scheduled_daily_job(scheduler, crawl_request_name, job_id, job_conf, date, hour, minutes):
    scheduled_time = datetime.strptime(date, '%m/%d/%Y') + timedelta(hours=int(hour), minutes=int(minutes))
    scheduler.add_job(launch_job, trigger='cron', id=job_id, start_date=scheduled_time, hour=hour, minute=minutes,
                      args=[crawl_request_name, job_id, job_conf])


def launch_scheduled_job(scheduler, crawl_request_name, job_id, job_conf, date, hour, minutes):
    scheduled_time = datetime.strptime(date, '%m/%d/%Y') + timedelta(hours=int(hour), minutes=int(minutes))
    scheduler.add_job(launch_job, 'date', id=job_id, run_date=scheduled_time,
                      args=[crawl_request_name, job_id, job_conf])


# save part at database
# id of the noob needs to be generated
def launch_job(db, crawl_request_name, job_id, job_conf):
    conf = yaml.full_load(job_conf)
    # the pre configured jobid is ignored
    conf['id'] = job_id
    frontier = db.get_frontier()

    try:
        new_job(frontier, conf)
        db.update_collection_joblist(crawl_request_name, job_id)
        logging.info('Launched a new job {} from collection {}'.format(job_id, crawl_request_name))
    except model.InvalidJobConf as e:
        logging.warning('Invalid job configuration: {}'.format(e))


# TODO add tests
def add_bulk_urls(db, job_id, urls):
    for url in urls:
        # dificil perceber quando temos um site objecto ou só uma representação
        # TODO mudar o naming para ser consistente
        site = db.get_site(job_id, get_url_base(url))

        logging.debug("adding page url: {} to site_id: {}".format(url, site['id']))
        db.add_page_to_site(site['id'], url)


def resume_job(db, job_id):
    frontier = db.get_frontier()
    job = db.get_job_by_name(job_id)
    frontier.resume_job(job)


def stop_job(db, job_id):
    db.stop_job(job_id)


# TODO remove this, and make it a pytest
if __name__ == '__main__':
    # test launch job
    rr = doublethink.Rethinker(servers=['localhost:28015'], db='brozzler_admin')
    crawl_request = list(rr.table('crawl_requests').filter({'name': 'VideoTesting'}).run())[0]
    job_prefix = crawl_request['job_prefix']

    # generate job_id
    job_list = crawl_request['job_list']

    with open('job_configuration.yaml') as f:
        job_conf = yaml.load(f)

    # increment id
    if len(job_list):
        id = int(job_list[-1].split('_')[-1]) + 1
    else:
        id = 0
    job_id = "%s_%s" % (job_prefix, id)
    launch_job('VideoTesting', job_id, job_conf)
