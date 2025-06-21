#!/bin/bash

if [[ "$1" = "start" ]]
then
    shift
    if [[ "$#" -eq 0 ]]
    then
        echo "Starting all services"
        docker compose up
    else
        echo "Starting services $*"
        docker compose up "$@"
    fi

elif [[ "$1" = "stop" ]]
then
    shift
    if [[ "$#" -eq 0 ]]
    then
        echo "Stopping all services"
        docker compose down
    else
        echo "Stopping services $*"
        docker compose down "$@"
    fi

elif [[ "$1" = "build" ]]
then
    shift
    if [[ "$#" -eq 0 ]]
    then
        echo "Building all images"
        docker compose build
    else
        echo "Building images $*"
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
        sleep 1
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
        sleep 1
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
        echo "Running webapp unit tests..."
        docker run \
            --name ss-webapp-test \
            --volume ./webapp/test/results:/webapp/webapp/test/results \
            -e IMAGE_STORE_PATH=/webapp/webapp/test/results \
            --rm \
            software-studio-webapp \
            python3 -m unittest discover -s test -p unit_*.py

    elif [[ "$2" = "int" ]]
    then
        echo "Running webapp integration tests..."
        docker compose -f docker-compose-test.yaml up db -d
        
        until [ "$(docker inspect --format='{{.State.Health.Status}}' ss-postgres-test)" = "healthy" ]; do
            sleep 1
        done

        cd database && alembic upgrade head && cd .. && \
        docker compose -f docker-compose-test.yaml up --abort-on-container-exit
        docker compose -f docker-compose-test.yaml down

    else
        echo "usage: ./ss-services test [unit|int]"
    fi

else
    echo "Use this script to perform various development tasks"
    echo "usage: ./ss-services [start|stop|rebuild|clear|migrate|test]"
    echo
    echo "start <service_list> - creates and starts services"
    echo "stop <service_list> - stops and removes services"
    echo "build <service_list> - builds images (use after editing code)"
    echo "clear - clears database volume, removes all containers"
    echo "load - loads latest database migration script"
    echo "migrate - creates database migration script"
    echo "test [unit|int] - runs test code"
fi