#!/bin/bash
# Installed heroku deps
pip install redis
pip install pymongo
pip install gunicorn

# Create heroku configuration file
DATABASE=$(echo ${MONGOHQ_URL} | cut -d"/" -f4)
cat >heroku.ini <<EOL
[webserver]
host = 0.0.0.0
port = ${PORT}
debug = false

[storage]
type = mongodb
host = ${MONGOHQ_URL}
database = ${DATABASE}

[session]
type = redis
uri = ${REDISTOGO_URL}
EOL
