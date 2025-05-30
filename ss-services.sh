#!/bin/bash

if [[ "$1" = "start" ]]
then
    shift
    if [[ "$#" -eq 0 ]]
    then
        echo "Starting all containers"
        docker compose up
    else
        echo "Starting containers $*"
        docker compose up "$@"
    fi

elif [[ "$1" = "stop" ]]
then
    shift
    if [[ "$#" -eq 0 ]]
    then
        echo "Stopping all containers"
        docker compose down
    else
        echo "Stopping containers $*"
        docker compose down "$@"
    fi

elif [[ "$1" = "rebuild" ]]
then
    shift
    if [[ "$#" -eq 0 ]]
    then
        echo "Rebuilding all images"
        docker compose build
    else
        echo "Rebuilding images $*"
        docker compose build "$@"
    fi

elif [[ "$1" = "clear" ]]
then
    echo "Clearing database"
    docker compose down -v

elif [[ "$1" = "load" ]]
then
    echo "Loading latest database migration script"
    docker compose up -d db
    until [ "$(docker inspect --format='{{.State.Health.Status}}' $(docker compose ps -q db))" = "healthy" ]; do
        sleep 2
    done

    cd database && \
    alembic upgrade head

elif [[ "$1" = "migrate" ]]
then
    echo "Creating database migration script"
    echo "Specify a message:"
    read -r next_line && \

    docker compose up -d db
    until [ "$(docker inspect --format='{{.State.Health.Status}}' $(docker compose ps -q db))" = "healthy" ]; do
        sleep 2
    done

    cd database && \
    alembic revision --autogenerate -m "$next_line" && {
        docker compose down db
        echo "Please verify the generated script in database/alembic/versions"
    } || {
        docker compose down db
    }

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
    echo "Use this script to perform various development tasks"
    echo "usage: ./ss-services [start|stop|rebuild|clear|migrate|test]"
    echo
    echo "start <container_list> - creates and starts containers"
    echo "stop <container_list> - stops and removes containers"
    echo "rebuild <container_list> - rebuilds images (use after editing code)"
    echo "clear - clears database volume, removes all containers"
    echo "load - loads latest database migration script"
    echo "migrate - creates database migration script"
    echo "test [unit|int] - tests code"
fi