#!/bin/sh

mongo < mongo-count-usage.js|grep '"count" : '
