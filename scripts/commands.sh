#!/bin/sh
echo 'Running commands.sh'
# Shell will terminate the session when the command fail
set -e

wait_psql.sh
collectstatic.sh
migrate.sh
runserver.sh