import rethinkdb as r
import rethinkstuff

DATABASE = 'brozzler_controller'
TABLE_COLLECTIONS = 'collections'


# TODO handle better the connections to database

def db_setup(connection):
    try:
        r.db_create(DATABASE).run(connection)
        r.db(DATABASE).table_create(TABLE_COLLECTIONS, primary_key='name').run(connection)
    except r.RqlRuntimeError:
        print("Database already exist")
    finally:
        connection.close()


def get_services():
    r = rethinkstuff.Rethinker(servers=['localhost:28015'], db='brozzler')
    services = list(r.db('brozzler').table('services').run())
    return services


def update_collection_joblist(collection_name, job_id):
    r = rethinkstuff.Rethinker(servers=['localhost:28015'], db='brozzler_controller')
    # be sure that the table is indexed with name
    job_list = list(r.db(DATABASE).table(TABLE_COLLECTIONS).filter({'name': collection_name}).run())[0][
        'job_list']
    if job_list:
        job_list.append(job_id)
    else:
        job_list = [job_id]

    r.db(DATABASE).table(TABLE_COLLECTIONS).filter({'name': collection_name}).update({'job_list': job_list}).run()


def get_last_job_configuration(collection_name):
    r = rethinkstuff.Rethinker(servers=['localhost:28015'], db='brozzler_controller')
    job_list = list(r.db(DATABASE).table(TABLE_COLLECTIONS).filter({'name': collection_name}).run())[0][
        'job_list']
    if job_list:
        last_job_id = job_list[-1]
        conf = list(r.db('brozzler').table('jobs').filter({'id': last_job_id}).run())[0]['conf']
        return conf
    else:
        # TODO generera default job schema
        return None


def generate_job_name(collection_name):
    r = rethinkstuff.Rethinker(servers=['localhost:28015'], db='brozzler_controller')
    job_prefix = list(r.table(TABLE_COLLECTIONS).filter({'name': collection_name}).run())[0]['job_prefix']
    job_list = list(r.db(DATABASE).table(TABLE_COLLECTIONS).filter({'name': collection_name}).run())[0][
        'job_list']
    if not job_list:
        job_name = '{}'.format(job_prefix)
    elif len(job_list) == 1:
        job_name = '{}_{}'.format(job_prefix, '1')
    else:
        job_number = int(job_list[-1].split('_')[1]) + 1
        job_name = '{}_{}'.format(job_prefix, job_number)
    return job_name


def new_collection(collection_name, prefix_name):
    r = rethinkstuff.Rethinker(servers=['localhost:28015'], db='brozzler_controller')
    r.table(TABLE_COLLECTIONS).insert({
        'name': collection_name,
        'job_prefix': prefix_name,
        'job_list': ''
    }).run()


if __name__ == '__main__':
    connection = r.connect("localhost", 28015)
    db_setup(connection)
    new_collection('VideoTesting', 'VideoTesting')
    # update_collection_joblist(connection, 'teste1', 'video_testing')
    # r.table('comments').index_create('post_id').run(conn)
