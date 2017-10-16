import argparse
import logging
import os
import sys

import doublethink

import brozzler
import brozzleradmin.database as db


def add_common_options(arg_parser, argv=None):
    argv = argv or sys.argv
    arg_parser.add_argument(
        '-q', '--quiet', dest='log_level', action='store_const',
        default=logging.INFO, const=logging.WARN, help=(
            'quiet logging, only warnings and errors'))
    arg_parser.add_argument(
        '-v', '--verbose', dest='log_level', action='store_const',
        default=logging.INFO, const=logging.DEBUG, help=(
            'verbose logging'))


def add_rethinkdb_options(arg_parser):
    arg_parser.add_argument(
        '--rethinkdb-servers', dest='rethinkdb_servers',
        default=os.environ.get('BROZZLER_RETHINKDB_SERVERS', 'localhost'),
        help=(
            'rethinkdb servers, e.g. '
            'db0.foo.org,db0.foo.org:38015,db1.foo.org (default is the '
            'value of environment variable BROZZLER_RETHINKDB_SERVERS)'))
    arg_parser.add_argument(
        '--rethinkdb-db', dest='rethinkdb_db',
        default=os.environ.get('BROZZLER_RETHINKDB_DB', 'brozzler'),
        help=(
            'rethinkdb database name (default is the value of environment '
            'variable BROZZLER_RETHINKDB_DB)'))


def resume_job(argv=None):
    argv = argv or sys.argv
    arg_parser = argparse.ArgumentParser(description='Resume stopped Brozzler Job')
    arg_parser.add_argument('-j', '--job-id', dest='job_id', default=None)
    add_common_options(arg_parser, argv)
    add_rethinkdb_options(arg_parser)

    args = arg_parser.parse_args(args=argv[1::])
    rr = doublethink.Rethinker(servers=args.rethinkdb_servers, db=args.rethinkdb_db)
    frontier = brozzler.RethinkDbFrontier(rr)
    job = db.get_job_by_name(args.job_id)
    if job:
        frontier.resume_job(job)


def get_job_queue(argv=None):
    argv = argv or sys.argv
    arg_parser = argparse.ArgumentParser(description='Print all pages queued to crawl in a job')
    arg_parser.add_argument('-j', '--job-id', dest='job_id', default=None)
    add_common_options(arg_parser, argv)
    add_rethinkdb_options(arg_parser)

    args = arg_parser.parse_args(args=argv[1::])
    rr = doublethink.Rethinker(servers=args.rethinkdb_servers, db=args.rethinkdb_db)
    cursor = list(rr.table('pages').filter({'job_id': args.job_id, 'brozzle_count': 0}).run())
    for document in cursor:
        print(document['url'])

def get_all_outlinks(argv=None):
    argv = argv or sys.argv
    arg_parser = argparse.ArgumentParser(description='Print all outlinks from a Brozzler Job')
    arg_parser.add_argument('-j', '--job-id', dest='job_id', default=None)
    arg_parser.add_argument('-r', '--rejected', dest='rejected', action='store_true')
    arg_parser.add_argument('-b', '--blocked', dest='blocked', action='store_true')
    arg_parser.add_argument('-a', '--accepted', dest='accepted', action='store_true')

    add_common_options(arg_parser, argv)
    add_rethinkdb_options(arg_parser)

    args = arg_parser.parse_args(args=argv[1::])
    rr = doublethink.Rethinker(servers=args.rethinkdb_servers, db=args.rethinkdb_db)
    cursor = list(rr.table('pages').filter({'job_id': args.job_id, 'brozzle_count': 1}).run())
    for document in cursor:
        if args.rejected:
            print("Rejected:")
            for url in document['outlinks']['rejected']:
                print(url)

        if args.accepted:
            print("Accepted:")
            for url in document['outlinks']['accepted']:
                print(url)

        if args.blocked:
            print("Blocked:")
            for url in document['outlinks']['blocked']:
                print(url)


if __name__ == '__main__':
    resume_job()
