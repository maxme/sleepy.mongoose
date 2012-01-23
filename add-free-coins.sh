#!/bin/zsh

if [ -z $2 ]; then
    echo "Usage:   $0 message coins"
    echo "Example: $0 \"Thanks to our partnership with OpenFeint Free Game Of The Day, you won 1 000 000 coins today\" 1000000"
    exit 1
fi

jscode="use tipcode;\ndb.freestuff.insert({\"message\": \"$1\", \"coins\": $2});"

echo $jscode
echo $jscode | mongo
