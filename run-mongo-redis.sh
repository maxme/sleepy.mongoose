mongod --dbpath db 2>/dev/null > /dev/null &
redis-server /usr/local/etc/redis.conf > /dev/null 2> /dev/null &

