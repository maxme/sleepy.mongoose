#!/usr/bin/zsh

echo "use tipcode;\ndb.tokens.find().forEach(printjson);\n" | mongo|grep -i '"token" :'|cut -d ":" -f2| sed "s/[^a-z0-9]//g"
