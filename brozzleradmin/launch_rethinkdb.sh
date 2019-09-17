cd /home/dbicho/Documents/CrawlingReplayEnvironment
docker run --name rethinkdb -v "$PWD:/data/" --net=host -d rethinkdb