mongod --dbpath db 2>/dev/null > /dev/null &
redis-server /etc/redis/redis.conf > /dev/null 2> /dev/null &

