jscode="use tipcode;\ndb.freestuff.find()"
echo $jscode | mongo

echo "Enter ObjectId to remove"
read objid

jscode="use tipcode;\ndb.freestuff.remove({\"_id\":ObjectId(\"$objid\")});"
echo $jscode
echo $jscode | mongo


echo "Check if removed"
jscode="use tipcode;\ndb.freestuff.find()"
echo $jscode | mongo
