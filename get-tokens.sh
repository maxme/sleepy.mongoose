#!/bin/sh

echo "use tipcode;\ndb.tokens.find();\n"|mongo|grep -i '"token" :'|cut -d ":" -f3| sed "s/[^a-z0-9]//g"
