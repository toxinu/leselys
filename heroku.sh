#!/bin/bash
cat >heroku.ini <<EOL
[webserver]
host = 0.0.0.0
port = ${PORT}
debug = false

[backend]
type = mongodb
host = ${MONGOHQ_URL}
EOL