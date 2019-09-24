import brozzler
import doublethink
from brozzler import Job

DATABASE = 'brozzler_admin'
TABLE_CRAWLREQUESTS = 'crawl_requests'


# TODO put in a config file the database endpoint
def get_services():
    rr = doublethink.Rethinker(servers=['localhost:28015'], db='brozzler')
    services = list(rr.table('services').run())
    return services


# TODO get database values from config file instead of hardcoding them
def get_frontier():
    rr = doublethink.Rethinker(servers=['localhost:28015'], db='brozzler')
    return brozzler.RethinkDbFrontier(rr)


def update_collection_joblist(crawl_request_name, job_id):
    rr = doublethink.Rethinker(servers=['localhost:28015'], db=DATABASE)
    job_list = list(rr.table(TABLE_CRAWLREQUESTS).filter({'name': crawl_request_name}).run())[0][
        'job_list']
    if job_list:
        job_list.append(job_id)
    else:
        job_list = [job_id]

    rr.table(TABLE_CRAWLREQUESTS).filter({'name': crawl_request_name}).update({'job_list': job_list}).run()


def get_job_by_name(job_id):
    rr = doublethink.Rethinker(servers=[], db='brozzler')
    job = Job.load(rr, job_id)
    if job:
        return job


def get_last_job_configuration(crawl_request_name):
    rr = doublethink.Rethinker(servers=['localhost:28015'], db=DATABASE)
    job_list = list(rr.table(TABLE_CRAWLREQUESTS).filter({'name': crawl_request_name}).run())[0]['job_list']
    if job_list:
        last_job_id = job_list[-1]
        conf = list(rr.db('brozzler').table('jobs').filter({'id': last_job_id}).run())[0]['conf']
        return conf
    else:
        # TODO genererate default job schema
        return None


def generate_job_name(crawl_request_name):
    rr = doublethink.Rethinker(servers=['localhost:28015'], db=DATABASE)
    job_list = list(rr.table(TABLE_CRAWLREQUESTS).filter({'name': crawl_request_name}).run())[0]['job_list']
    if not job_list:
        job_name = '{}_1'.format(crawl_request_name)
    else:
        job_number = int(job_list[len(job_list) - 1].split('_')[1]) + 1
        job_name = '{}_{}'.format(crawl_request_name, job_number)
    return job_name


def new_crawl_request(crawl_request_name, prefix_name):
    rr = doublethink.Rethinker(servers=['localhost:28015'], db=DATABASE)
    rr.table(TABLE_CRAWLREQUESTS).insert({
        'name': crawl_request_name,
        'job_warc_prefix': prefix_name,
        'job_list': ''
    }).run()


# TODO refactor all this mess
def get_all_outlinks(job_id):
    rr = doublethink.Rethinker(servers=["localhost:28015"], db='brozzler')
    cursor = list(rr.table('pages').filter({'job_id': job_id, 'brozzle_count': 1}).run())
    for document in cursor:
        print("Rejected:\n")
        for url in document['outlinks']['rejected']:
            print(url)
        print("Accepted:\n")
        for url in document['outlinks']['accepted']:
            print(url)
        print("Blocked:\n")
        for url in document['outlinks']['blocked']:
            print(url)
