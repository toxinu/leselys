#!/bin/bash

# Create heroku configuration file
cat >heroku.ini <<EOL
[webserver]
host = 0.0.0.0
port = ${PORT}
debug = false

[storage]
type = mongodb
uri = ${MONGOHQ_URL}

[session]
type = redis
uri = ${REDISTOGO_URL}

[worker]
broker = ${MONGOHQ_URL}
interval = 20
EOL