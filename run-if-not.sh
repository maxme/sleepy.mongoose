#!/bin/bash

pid=$(ps x|grep "python"|grep "httpd.py"| grep -v grep |sed "s/^ *//"|cut -d " " -f 1)

if [ -z "$pid" ]; then
    echo "Start mongodb REST api"
    python /home/bbsrv/tipcode/sleepy.mongoose/httpd.py
fi


