#!/bin/sh
#user_idとfriend_idを変更して確認
curl -F user_id=39 -F password=testtest -F comment=hogehoge -F start_time="2015-10-20 15:00:00" -F place_name=渋谷 -F place_lat=35.670496 -F place_lng=139.707286 -F status_id=1 -F public_id=0 http://localhost:8080/posts/add
echo "\n"
echo "Event Posted.\n"