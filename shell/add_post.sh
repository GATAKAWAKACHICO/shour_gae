#!/bin/sh
#user_idとfriend_idを変更して確認
#datetime="2015-12-20 18:00:00"
curl -F user_id=$1 -F password=$2 -F comment=$3 -F place_name=$4 -F start_time="2013-01-01 18:00:00" -F place_lat=35.670496 -F place_lng=139.707286 -F status_id=1 -F public_id=0 http://localhost:8080/posts/add
echo "\n"
echo "Event Posted.\n"