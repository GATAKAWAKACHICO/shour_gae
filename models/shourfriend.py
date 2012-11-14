#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import sys
import logging

# モデルのモジュール読み込み
import sys,os
models_dir = 'models'
sys.path.append(os.pardir+'/'+models_dir)
from google.appengine.ext import db
from google.appengine.api.datastore_types import Key
from shouruser import ShourUser

# 独自例外モジュール読み込み
err_dir = 'err'
sys.path.append(err_dir)
from shourapperror import ShourAppError

class ShourFriend(db.Model):
    user_id = db.IntegerProperty(required=True)
    friend_id = db.IntegerProperty(required=True)
    status = db.IntegerProperty(required=True)
    user_reference = db.ReferenceProperty(ShourUser)
    created_at = db.DateTimeProperty(auto_now_add=True, required=True)

    @classmethod
    def is_requestable(self, user_id, friend_id):
        user = ShourUser.get_by_id(int(user_id))
        friend = ShourUser.get_by_id(int(friend_id))
        if not user:
            # 申請元が存在しない
            raise ShourAppError(20001)
        if not friend:
            # 相手方が存在しない
            raise ShourAppError(20002)
        else:
            # 申請元または相手方ユーザーが存在しない
            return [user, friend]

    @classmethod
    def is_duplicate_request(self, user_id, friend_id):
        # すでにリクエストしていないか
        query = ShourFriend.all(keys_only=True).filter("user_id =", int(user_id)).filter("friend_id =", int(friend_id))
        friend_request = query.get()
        if friend_request:
            # すでにリクエストしている
            raise ShourAppError(20003)
        # すでにリクエストされてないか
        query = ShourFriend.all(keys_only=True).filter("user_id =", int(friend_id)).filter("friend_id =", int(user_id))
        entity = query.get()
        if entity:
            # すでにリクエストされている
            raise ShourAppError(20004)

    @classmethod
    def request(self, user, friend):
        # 引数はShourUserオブジェクト
        friend_request = ShourFriend(user_id=user.key().id(), friend_id=friend.key().id(), status=1, user_reference=user.key())
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
        datas = []
        if friend_requests:
            for request in friend_requests:
                data = {
                "created_at":request.created_at, 
                "user":{
                "user_id":request.user_reference.key().id(),
                "name":request.user_reference.name,
                "picture_url":request.user_reference.picture_url
                }}
                datas.append(data)
        return datas

    @classmethod
    def is_acceptable(self, user_id, friend_id):
        user = ShourUser.get_by_id(int(user_id))
        friend = ShourUser.get_by_id(int(friend_id))
        if not user:
            # 申請元が存在しない
            raise ShourAppError(20001)
        if not friend:
            # 相手方が存在しない
            raise ShourAppError(20002)
        else:
            # 申請元または相手方ユーザーが存在しない
            return [user, friend]
    
    @classmethod
    def is_duplicate_accept(self, user_id, friend_id):
        # すでにリクエストしていないか
        query = ShourFriend.all()
        query.filter("user_id =", int(user_id))
        query.filter("friend_id =", int(friend_id))
        entity = query.get()
        if entity:
            # すでにリクエストしている
            raise ShourAppError(20003)

    @classmethod
    def accept(self, user, friend, friend_request, user_events, friend_events):
        user_id = user.key().id()
        friend_id = friend.key().id()
        # 祖先パスは/承認者(ShourUser)/ShourFriend
        friend_accept = ShourFriend(parent=user, user_id=user_id, friend_id=friend_id, status=2, user_reference=user.key())
        friend_request.status = 2
        # 一括保存用リスト(リクエスト承認データ、申請リクエストデータ)
        records = [friend_accept, friend_request]
        db.put(records)

    @classmethod
    def get_relation(self, user_id, friend_id):
        query = ShourFriend.all()
        query.filter("user_id =", int(user_id))
        query.filter("friend_id =", int(friend_id))
        entity = query.get()
        if entity:
            return entity
        else:
            # 友人関係が存在しない
            raise ShourAppError(20006)

    @classmethod
    def destroy(self, friendship):
        # エンティティの削除
        db.delete(friendship)

    @classmethod
    def show_all_friends(self, user_id):
        query = ShourFriend.all()
        query.filter("user_id =", int(user_id))
        query.filter("status =", 2)
        # 友達1000人まで
        friendships = query.fetch(1000)
        return friendships