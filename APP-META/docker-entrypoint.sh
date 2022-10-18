#!/bin/bash
if [ "$1" == "runserver" ];then
    sleep infinity
elif [ "$1" == "runserver"];then
    python manager.py runserver 0.0.0.0:${EXPOSE_PORT}
fi

exec "$@"
