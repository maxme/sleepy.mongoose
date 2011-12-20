#!/bin/bash

pid=$(ps x|grep "python"|grep "httpd.py"| grep -v grep |sed "s/^ *//"|cut -d " " -f 1)

if [ -z "$pid" ]; then
    echo "Start mongodb REST api"
    python /home/bbsrv/tipcode/sleepy.mongoose/httpd.py 2> /dev/null > /dev/null &
    # wait for the server to start
    sleep 5
    # connect to mongodb
    curl --data server=mongodb://localhost:27017 'http://localhost:27080/_connect'
fi
