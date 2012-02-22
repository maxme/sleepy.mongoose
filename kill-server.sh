#!/bin/bash

ps x|grep "python"|grep "httpd.py"| grep -v grep |sed "s/^ *//"|cut -d " " -f 1|xargs kill
