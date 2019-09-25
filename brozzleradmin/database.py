import brozzler
import doublethink
from brozzler import Job


class DataBaseAccess(object):

    def __init__(self, database='brozzler_admin', rethinkdb_server='localhost', rethinkdb_port='28015',
                 table_crawlrequests='crawl_request'):
        self.DATABASE = database
        self.RETHINKDB_SERVER = rethinkdb_server
        self.RETHINKDB_PORT = rethinkdb_port
        self.TABLE_CRAWLREQUESTS = table_crawlrequests
        self._ensure_tables()

    def _ensure_tables(self):
        rr = doublethink.Rethinker(servers=['{}:{}'.format(self.RETHINKDB_SERVER, self.RETHINKDB_PORT)],
                                   db=self.DATABASE)
        dbs = rr.db_list().run()
        if self.DATABASE not in dbs:
            rr.db_create(self.DATABASE).run()

        tables = rr.table_list().run()
        if self.TABLE_CRAWLREQUESTS not in tables:
            rr.table_create(self.TABLE_CRAWLREQUESTS).run()

    def list_crawlrequests(self):
        rr = doublethink.Rethinker(servers=['{}:{}'.format(self.RETHINKDB_SERVER, self.RETHINKDB_PORT)],
                                   db=self.DATABASE)
        crawl_requests = list(rr.table(self.TABLE_CRAWLREQUESTS).run())
        return crawl_requests

    def get_services(self):
        rr = doublethink.Rethinker(servers=['{}:{}'.format(self.RETHINKDB_SERVER, self.RETHINKDB_PORT)], db='brozzler')
        services = list(rr.table('services').run())
        return services

    def get_frontier(self):
        rr = doublethink.Rethinker(servers=['{}:{}'.format(self.RETHINKDB_SERVER, self.RETHINKDB_PORT)], db='brozzler')
        return brozzler.RethinkDbFrontier(rr)

    def update_collection_joblist(self, crawl_request_name, job_id):
        rr = doublethink.Rethinker(servers=['{}:{}'.format(self.RETHINKDB_SERVER, self.RETHINKDB_PORT)],
                                   db=self.DATABASE)
        job_list = list(rr.table(self.TABLE_CRAWLREQUESTS).filter({'name': crawl_request_name}).run())[0][
            'job_list']
        if job_list:
            job_list.append(job_id)
        else:
            job_list = [job_id]

        rr.table(self.TABLE_CRAWLREQUESTS).filter({'name': crawl_request_name}).update({'job_list': job_list}).run()

    def get_job_by_name(self, job_id):
        rr = doublethink.Rethinker(servers=['{}:{}'.format(self.RETHINKDB_SERVER, self.RETHINKDB_PORT)], db='brozzler')
        job = Job.load(rr, job_id)
        if job:
            return job

    def get_last_job_configuration(self, crawl_request_name):
        rr = doublethink.Rethinker(servers=['{}:{}'.format(self.RETHINKDB_SERVER, self.RETHINKDB_PORT)],
                                   db=self.DATABASE)
        job_list = list(rr.table(self.TABLE_CRAWLREQUESTS).filter({'name': crawl_request_name}).run())[0]['job_list']
        if job_list:
            last_job_id = job_list[-1]
            conf = list(rr.db('brozzler').table('jobs').filter({'id': last_job_id}).run())[0]['conf']
            return conf
        else:
            # TODO genererate default job schema
            return None

    def generate_job_name(self, crawl_request_name):
        rr = doublethink.Rethinker(servers=['{}:{}'.format(self.RETHINKDB_SERVER, self.RETHINKDB_PORT)],
                                   db=self.DATABASE)
        job_list = list(rr.table(self.TABLE_CRAWLREQUESTS).filter({'name': crawl_request_name}).run())[0]['job_list']
        if not job_list:
            job_name = '{}_1'.format(crawl_request_name)
        else:
            job_number = int(job_list[len(job_list) - 1].split('_')[1]) + 1
            job_name = '{}_{}'.format(crawl_request_name, job_number)
        return job_name

    def new_crawl_request(self, crawl_request_name, prefix_name):
        rr = doublethink.Rethinker(servers=['{}:{}'.format(self.RETHINKDB_SERVER, self.RETHINKDB_PORT)],
                                   db=self.DATABASE)
        rr.table(self.TABLE_CRAWLREQUESTS).insert({
            'name': crawl_request_name,
            'job_warc_prefix': prefix_name,
            'job_list': ''
        }).run()

    # TODO refactor all this mess
    def get_all_outlinks(self, job_id):
        rr = doublethink.Rethinker(servers=['{}:{}'.format(self.RETHINKDB_SERVER, self.RETHINKDB_PORT)], db='brozzler')
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
