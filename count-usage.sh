#!/bin/sh

#mongo < mongo-count-usage.js|grep '"count" : '
echo "use tipcode;\ndb.salts.count();\n"|mongo