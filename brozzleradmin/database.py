import uuid

import doublethink
import rethinkdb as r

from brozzler import Job

DATABASE = 'brozzler_controller'
TABLE_COLLECTIONS = 'collections'


def db_setup(connection):
    try:
        r.db_create(DATABASE).run(connection)
        r.db(DATABASE).table_create(TABLE_COLLECTIONS, primary_key='name').run(connection)
    except r.RqlRuntimeError:
        print("Database already exist")
    finally:
        connection.close()


def get_services():
    rr = doublethink.Rethinker(servers=['localhost:28015'], db='brozzler')
    services = list(rr.table('services').run())
    return services


def update_collection_joblist(collection_name, job_id):
    rr = doublethink.Rethinker(servers=['localhost:28015'], db='brozzler_controller')
    job_list = list(rr.table(TABLE_COLLECTIONS).filter({'name': collection_name}).run())[0][
        'job_list']
    if job_list:
        job_list.append(job_id)
    else:
        job_list = [job_id]

    rr.table(TABLE_COLLECTIONS).filter({'name': collection_name}).update({'job_list': job_list}).run()


def get_job_by_name(job_id):
    rr = doublethink.Rethinker(servers=['localhost:28015'], db='brozzler')
    job = Job.load(rr, job_id)
    if job:
        return job


def get_last_job_configuration(collection_name):
    rr = doublethink.Rethinker(servers=['localhost:28015'], db='brozzler_controller')
    job_list = list(rr.table(TABLE_COLLECTIONS).filter({'name': collection_name}).run())[0]['job_list']
    if job_list:
        last_job_id = job_list[-1]
        conf = list(rr.db('brozzler').table('jobs').filter({'id': last_job_id}).run())[0]['conf']
        return conf
    else:
        # TODO genererate default job schema
        return None


def generate_job_name(collection_name):
    rr = doublethink.Rethinker(servers=['localhost:28015'], db='brozzler_controller')
    job_prefix = list(rr.table(TABLE_COLLECTIONS).filter({'name': collection_name}).run())[0]['job_prefix']
    job_list = list(rr.table(TABLE_COLLECTIONS).filter({'name': collection_name}).run())[0][
        'job_list']
    if not job_list:
        job_name = '{}'.format(job_prefix)
    else:
        job_name = '{}_{}'.format(job_prefix, str.upper(uuid.uuid1().urn[9:17]))
    return job_name


def new_collection(collection_name, prefix_name):
    rr = doublethink.Rethinker(servers=['localhost:28015'], db='brozzler_controller')
    rr.table(TABLE_COLLECTIONS).insert({
        'name': collection_name,
        'job_prefix': prefix_name,
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


if __name__ == '__main__':
    connection = r.connect("localhost", 28015)
    db_setup(connection)
    get_all_outlinks("Teste")
    # job = get_job_by_name("MundoNaEscola_2")
    # print("done")
    # new_collection('VideoTesting', 'VideoTesting')
    # update_collection_joblist(connection, 'teste1', 'video_testing')
    # r.table('comments').index_create('post_id').run(conn)
