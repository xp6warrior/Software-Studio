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
    if [[ "$2" = "unit" ]]
    then
        cd webapp
        echo "Running webapp unit tests..."
        python3 -m unittest discover -s test -p unit_*.py
    elif [[ "$2" = "int" ]]
    then
        echo "Running webapp integration tests..."
        docker compose -f docker-compose.test.yaml up --abort-on-container-exit --exit-code-from test-webapp
        docker compose -f docker-compose.test.yaml down --volumes --remove-orphans
    else
        echo "usage: ./ss-services test [unit|int]"
    fi
else
    echo "usage: ./ss-services [start|stop|restart|test]"
fi