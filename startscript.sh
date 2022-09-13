#!/bin/bash

myscript(){
    python3 manage.py runserver 0.0.0.0:80
}

until myscript; do 
    echo "'myscript' crashed with exit code $?. Restarting ... " >&2
    sleep 1
done