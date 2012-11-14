#!/bin/sh
curl -F user_id=$1 -F friend_id=$2 -F password=testtest http://localhost:8080/friends/request
echo "\n"
echo "An request sended.\n"
curl -F user_id=$2 -F friend_id=$1 -F password=testtest http://localhost:8080/friends/accept
echo "\n"
echo "Perhaps the request accepted.\n"
echo "If an error occured, check user_id or friend_id,\n"
echo "Or check the account is active.\n"