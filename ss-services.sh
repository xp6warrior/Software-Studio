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
else
    echo "ERROR: incorrect goal, must be [start|stop]"
fi