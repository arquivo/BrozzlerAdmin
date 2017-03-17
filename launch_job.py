from datetime import datetime, timedelta

import brozzler
import rethinkstuff
import yaml

import database


def launch_scheduled_job(scheduler, collection_name, job_id, job_conf, date, hour, minutes):
    scheduled_time = datetime.strptime(date, '%m/%d/%Y') + timedelta(hours=int(hour), minutes=int(minutes))
    scheduler.add_job(launch_job, 'date', id=job_id, run_date=scheduled_time, args=[collection_name, job_id, job_conf])


# save part at database
# id of the noob needs to be generated
def launch_job(collection_name, job_id, job_conf):
    conf = yaml.load(job_conf)
    # the pre configured jobid is ignored
    conf['id'] = job_id
    r = rethinkstuff.Rethinker(servers=['localhost:28015'], db='brozzler')
    frontier = brozzler.RethinkDbFrontier(r)

    try:
        brozzler.new_job(frontier, conf)
        database.update_collection_joblist(collection_name, job_id)
    except brozzler.job.InvalidJobConf as e:
        # TODO log this
        print('Invalid job')


if __name__ == '__main__':
    # test launch job
    r = rethinkstuff.Rethinker(servers=['localhost:28015'], db='brozzler_controller')
    collection = list(r.table('collections').filter({'name': 'VideoTesting'}).run())[0]
    job_prefix = collection['job_prefix']

    # generate job_id
    job_list = collection['job_list']

    with open('job_configuration.yaml') as f:
        job_conf = yaml.load(f)

    # increment id
    if len(job_list):
        id = int(job_list[-1].split('_')[-1]) + 1
    else:
        id = 0
    job_id = "%s_%s" % (job_prefix, id)
    launch_job('VideoTesting', job_id, job_conf)
