#!/bin/bash
if [ $1 == "runserver" ];then
    python manager.py runserver 0.0.0.0:${PORT}
fi

exec "$@"
