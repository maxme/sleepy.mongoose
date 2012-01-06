#!/bin/bash

pid=$(ps x|grep "python"|grep "httpd.py"| grep -v grep |sed "s/^ *//"|cut -d " " -f 1)

if [ -n "$pid" ]; then
    echo "kill $pid"
    kill $pid
fi
