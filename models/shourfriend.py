#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import sys

# モデルのモジュール読み込み
import sys,os
models_dir = 'models'
sys.path.append(os.pardir+'/'+models_dir)
from google.appengine.ext import db
from shouruser import ShourUser

# 独自例外モジュール読み込み
err_dir = 'err'
sys.path.append(err_dir)
from shourapperror import ShourAppError

class ShourFriend(db.Model):
    user_id = db.IntegerProperty(required=True)
    friend_id = db.IntegerProperty(required=True)
    status = db.IntegerProperty(required=True)
    created_at = db.DateTimeProperty(auto_now_add=True, required=True)

    @classmethod
    def is_requestable(self, user_id, friend_id):
        if ShourUser.is_exist(user_id) == False:
            # 申請元ユーザーが存在しない
            raise ShourAppError(20001)
        if ShourUser.is_exist(friend_id) == False:
            # 申請先ユーザーが存在しない
            raise ShourAppError(20002)
        ShourFriend.is_duplicate_request(user_id, friend_id)

    @classmethod
    def is_duplicate_request(self, user_id, friend_id):
        # すでにリクエストしていないか
        query = ShourFriend.all()
        query.filter("user_id =", int(user_id))
        query.filter("friend_id =", int(friend_id))
        entity = query.get()
        if entity:
            # すでにリクエストしている
            raise ShourAppError(20003)
        # すでにリクエストされてないか
        query = ShourFriend.all()
        query.filter("user_id =", int(friend_id))
        query.filter("friend_id =", int(user_id))
        entity = query.get()
        if entity:
            # すでにリクエストされている
            raise ShourAppError(20004)

    @classmethod
    def request(self, user_id, friend_id):
        friend_request = ShourFriend(user_id=int(user_id), friend_id=int(friend_id), status=1)
        try:
            friend_request.put()
        except:
            # フレンド申請を登録できなかった
            raise ShourAppError(20005)

    @classmethod
    def notice(self, user_id):
        # 友達リクエストの確認
        query = ShourFriend.all()
        query.filter("friend_id =", int(user_id))
        query.filter("status =", 1)
        friend_requests = query.fetch(5)
        return friend_requests

    @classmethod
    def is_acceptable(self, user_id, friend_id):
        if ShourUser.is_exist(user_id) == False:
            # 申請元ユーザーが存在しない
            raise ShourAppError(20001)
        if ShourUser.is_exist(friend_id) == False:
            # 申請先ユーザーが存在しない
            raise ShourAppError(20002)
        # すでにリクエストしていないか
        query = ShourFriend.all()
        query.filter("user_id =", int(user_id))
        query.filter("friend_id =", int(friend_id))
        entity = query.get()
        if entity:
            # すでにリクエストしている
            raise ShourAppError(20003)

    @classmethod
    def accept(self, user_id, friend_id, friend_request):
        friend_accept = ShourFriend(user_id=int(user_id), friend_id=int(friend_id), status=2)
        friend_accept.put()
        friend_request.status = 2
        friend_request.put()

    @classmethod
    def get_relation(self, user_id, friend_id):
        query = ShourFriend.all()
        query.filter("user_id =", int(user_id))
        query.filter("friend_id =", int(friend_id))
        entity = query.get()
        if entity:
            return entity
        else:
            return None

    @classmethod
    def destroy(self, friendship):
        # エンティティの削除
        db.delete(friendship)