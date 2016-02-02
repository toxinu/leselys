#!/bin/sh

CONFIG="/data/config.ini"

if [ ! -f "${CONFIG}" ]; then
	leselys init "${CONFIG}"
	sed -i -e 's|host = mongodb://localhost:27017|host = mongodb://mongo:27017|g' "${CONFIG}"
fi

exec "${@}"
