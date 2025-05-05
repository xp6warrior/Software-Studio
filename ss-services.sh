#!/bin/bash

if [[ "$1" = "start" ]]
then
    docker compose up
elif [[ "$1" = "stop" ]]
then
    docker compose down
else
    echo "ERROR: incorrect goal, must be [start|stop]"
fi