#!/bin/bash
DATABASE=$(echo ${MONGOHQ_URL} | cut -d"/" -f4)
cat >heroku.ini <<EOL
[webserver]
host = 0.0.0.0
port = ${PORT}
debug = false

[backend]
type = mongodb
host = ${MONGOHQ_URL}
database = ${DATABASE}
EOL