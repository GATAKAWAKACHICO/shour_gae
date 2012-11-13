#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
import json

# モデルのモジュール読み込み
import sys,os
models_dir = 'models'
sys.path.append(os.pardir+'/'+models_dir)
from google.appengine.ext import db
from shouruser import ShourUser
from shourfriend import ShourFriend
from shourpost import ShourPost

# ライブラリのモジュール読み込み
lib_dir = 'slib'
sys.path.append(lib_dir)
import jsonencoder

# 独自例外モジュール読み込み
err_dir = 'err'
sys.path.append(err_dir)
from shourapperror import ShourAppError

class ShourFriendGenereteRequest(webapp.RequestHandler):
    def post(self):
        self.response.content_type = "application/json; charset=utf-8"
        user_id = self.request.get('user_id')
        friend_id = self.request.get('friend_id')
        try:
            ShourFriend.is_requestable(user_id, friend_id)
            ShourFriend.request(user_id, friend_id)
            data = {"message": True}
            json.dump(data, self.response.out, ensure_ascii=False)
        except ShourAppError, e:
            data = {"message": False, "err":e.value}
            json.dump(data, self.response.out, ensure_ascii=False)

class ShourFriendNoticeRequest(webapp.RequestHandler):
    def post(self):
        self.response.content_type = "application/json; charset=utf-8"
        user_id = self.request.get('user_id')
        friend_requests = ShourFriend.notice(user_id)
        data = jsonencoder.GqlEncoder().encode(friend_requests)
        self.response.out.write(data)

class ShourFriendRequestAccept(webapp.RequestHandler):
    def post(self):
        self.response.content_type = "application/json; charset=utf-8"
        user_id = int(self.request.get('user_id'))
        friend_id = int(self.request.get('friend_id'))
        try:
            ShourFriend.is_acceptable(user_id, friend_id)
            # リクエストされていたデータ
            friend_request = ShourFriend.get_relation(friend_id, user_id)
            # 友人リクエスト承認者の投稿したイベント
            user_events = ShourPost.get_master_event(user_id)
            # 友人リクエスト申請者の投稿したイベント
            friend_events = ShourPost.get_master_event(friend_id)
            # クロスグループトランザクションCross-Group (XG) Transactions有効化
            xg_on = db.create_transaction_options(xg=True)
            db.run_in_transaction_options(xg_on, ShourFriend.accept, user_id, friend_id, friend_request, user_events, friend_events)
            data = {"message": True}
            json.dump(data, self.response.out, ensure_ascii=False)
        except ShourAppError, e:
            data = {"message": False, "err":e.value}
            json.dump(data, self.response.out, ensure_ascii=False)

class ShourFriendDestroy(webapp.RequestHandler):
    def post(self):
        self.response.content_type = "application/json; charset=utf-8"
        user_id = self.request.get('user_id')
        friend_id = self.request.get('friend_id')
        try:
            friendship_from_me = ShourFriend.get_relation(user_id, friend_id)
            friendship_from_you = ShourFriend.get_relation(friend_id, user_id)
            if friendship_from_me:
                ShourFriend.destroy(friendship_from_me)
            if friendship_from_you:
                ShourFriend.destroy(friendship_from_you)
            data = {"message": True}
            json.dump(data, self.response.out, ensure_ascii=False)
        except ShourAppError, e:
            data = {"message": False, "err":e.value}
            json.dump(data, self.response.out, ensure_ascii=False)