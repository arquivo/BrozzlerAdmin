docker run -d --rm --name test-rethinkdb -p "28015:28015" rethinkdb

# run pytests
pytest test_database.py

docker stop test-rethinkdb