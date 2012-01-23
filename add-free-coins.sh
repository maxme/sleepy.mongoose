#!/bin/zsh

if [ -z $2 ]; then
    echo "Usage:   $0 message coins [android|ios]"
    echo "Example: $0 \"Thanks to our partnership with OpenFeint Free Game Of The Day, you won 1 000 000 coins today\" 1000000 ios"
    exit 1
fi


jscode="use tipcode;\ndb.freestuff.insert({\"message\": \"$1\", \"coins\": $2, \"platform\":\"$3\"});"

echo $jscode
echo $jscode | mongo
