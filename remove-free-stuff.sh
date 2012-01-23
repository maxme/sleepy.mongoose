#!/bin/zsh

jscode="use tipcode;\ndb.freestuff.find();\n"
echo $jscode | mongo

echo "Enter ObjectId to remove"
read objid

jscode="use tipcode;\ndb.freestuff.remove({\"_id\":ObjectId(\"$objid\")});\n"
echo $jscode
echo $jscode | mongo


echo "Check if removed"
jscode="use tipcode;\ndb.freestuff.find();\n"
echo $jscode | mongo
