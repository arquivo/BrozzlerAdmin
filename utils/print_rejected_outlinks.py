import doublethink
from argparse import ArgumentParser

parser = ArgumentParser(description="Utility to print all outlinks from a job.")
parser.add_argument('job_id',help="job_id we want to print the rejected outlinks")
parser.add_argument('--rethinkdb_server', default="localhost:28015", help="RethinkDB server")
args = parser.parse_args()

rr = doublethink.Rethinker([args.rethinkdb_server], 'brozzler')
links = rr.table('pages').filter({'job_id': args.job_id })['outlinks']['rejected'].run()

for link in links:
    for e in link:
     print(e)
