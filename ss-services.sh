#!/bin/bash

if [[ "$1" = "start" ]]
then
    docker compose up
elif [[ "$1" = "stop" ]]
then
    docker compose down
elif [[ "$1" = "restart" ]]
then
    docker compose down -v
elif [[ "$1" = "test" ]]
then
    cd webapp
    echo "Running webapp unit tests..."
    python3 -m unittest discover -s test -p unit_*.py

    if [[ $? -eq 0 ]]
    then
        cd ..
        echo "Running webapp integration tests..."
        docker compose -f docker-compose.test.yaml up --abort-on-container-exit --exit-code-from test-webapp
        docker compose -f docker-compose.test.yaml down --volumes --remove-orphans
    fi
else
    echo "ERROR: incorrect goal, must be [start|stop|restart|test]"
fi