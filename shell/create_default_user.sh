#!/bin/sh
curl -F name=若竹雅貴 -F mail=masaki.wakatake@smail.com -F password=testtest -F lang=en -F picture=@/Users/megustaelgato/Pictures/fb_profile/ascii_art.png http://localhost:8080/users/sign_in_with_email
echo "\n"
echo "S\n"
curl -F name=藤橋亮太 -F mail=aringre@shour.jp -F password=testtest -F lang=en http://localhost:8080/users/sign_in_with_email
echo "\n"
echo "Sh\n"
curl -F name=ちょん -F first_name=中田 -F last_name=雄太 -F mail=yuta.nakata@shour.jp -F password=testtest http://localhost:8080/users/sign_in_with_email
echo "\n"
echo "Sho\n"
curl -F name=かとまい -F first_name=加藤 -F last_name=舞子 -F mail=maiko.kato@shour.jp -F password=testtest http://localhost:8080/users/sign_in_with_email
echo "\n"
echo "Shou\n"
curl -F name=yamatw -F first_name=大和 -F last_name=渡辺 -F mail=yamatw@gmail.jp -F password=testtest http://localhost:8080/users/sign_in_with_email
echo "\n"
echo "Shour\n"
curl -F name=よしなりさん -F first_name=ゆうと -F last_name=吉成 -F mail=yuto@shour.jp -F password=testtest http://localhost:8080/users/sign_in_with_email
echo "\n"
echo "Shour！\n Creating default users is complete."