#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
import json
import datetime
import urllib

# モデルのモジュール読み込み
import sys,os
models_dir = 'models'
sys.path.append(os.pardir+'/'+models_dir)
from google.appengine.ext import db
from shouruser import ShourUser
from shourpost import ShourPost
from shourfriend import ShourFriend

# 独自例外モジュール読み込み
err_dir = 'err'
sys.path.append(err_dir)
from shourapperror import ShourAppError

class ShourPostAdd(webapp.RequestHandler):
    def post(self):
        self.response.content_type = "application/json"
        user_id = int(self.request.get('user_id'))
        password = self.request.get('password')
        start_time = datetime.datetime.strptime(urllib.unquote_plus(self.request.get('start_time')), '%Y-%m-%d %H:%M:%S')
        end_time = self.request.get('end_time')
        if end_time != "":
            end_time = datetime.datetime.strptime(urllib.unquote_plus(self.request.get('end_time')), '%Y-%m-%d %H:%M:%S')
        place_name = self.request.get('place_name')
        place_address = self.request.get('place_address')
        place_lat = self.request.get('place_lat')
        place_lng = self.request.get('place_lng')
        comment = self.request.get('comment')
        status_id = int(self.request.get('status_id'))
        public_id = int(self.request.get('public_id'))
        modified_at = datetime.datetime.now()
        try:
            ShourUser.shour_authorize(user_id, password)
        except ShourAppError, e:
            data = {"message": False, "err":e.value}
            json.dump(data, self.response.out, ensure_ascii=False)
            return
        friendships = ShourFriend.show_all_friends(user_id)
        shour_posts = []
        if friendships:
            # 友達いる場合
            # 自分用と友だち用のポストを作成する
            # 自分用のポスト
            shour_post = ShourPost(
                user_id=user_id,
                friend_id=user_id,
                master=True,
                start_time=start_time,
                end_time=end_time,
                place_name=place_name,
                place_address=place_address,
                place_lat=place_lat,
                place_lng=place_lng,
                comment=comment,
                status_id=status_id,
                public_id=public_id,
                modified_at=modified_at
            )
            # 自分用をリストに追加
            shour_posts.append(shour_post)
            for friend in friendships:
                # 友人閲覧用のポスト
                shour_post = ShourPost(
                    user_id=user_id,
                    friend_id=friend.friend_id,
                    master=False,
                    start_time=start_time,
                    end_time=end_time,
                    place_name=place_name,
                    place_address=place_address,
                    place_lat=place_lat,
                    place_lng=place_lng,
                    comment=comment,
                    status_id=status_id,
                    public_id=public_id,
                    modified_at=modified_at
                )
                # 友人用をリストに追加
                shour_posts.append(shour_post)
            db.put(shour_posts)
        else:
            # 友達なしの場合
            # 自分用のポスト
            shour_post = ShourPost(
                user_id=user_id,
                friend_id=user_id,
                master=True,
                start_time=start_time,
                end_time=end_time,
                place_name=place_name,
                place_address=place_address,
                place_lat=place_lat,
                place_lng=place_lng,
                comment=comment,
                status_id=status_id,
                public_id=public_id,
                modified_at=modified_at
            )
            db.put(shour_post)
        data = {"message": True}
        json.dump(data, self.response.out, ensure_ascii=False)
        #except:
        #    data = {"message": False, "err":50000}
        #    json.dump(data, self.response.out, ensure_ascii=False)