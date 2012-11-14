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
from shouruser import ShourUser
from shourfriend import ShourFriend

# 独自例外モジュール読み込み
err_dir = 'err'
sys.path.append(err_dir)
from shourapperror import ShourAppError

class ShourPost(db.Model):
    user_id = db.IntegerProperty(required=True)
    user_reference = db.ReferenceProperty(reference_class=ShourUser)
    master= db.BooleanProperty(required=True)
    start_time = db.DateTimeProperty(auto_now_add=False, required=True)
    end_time = db.DateTimeProperty(auto_now_add=False)
    place_name = db.StringProperty(required=True)
    place_address = db.StringProperty()
    place_lat = db.StringProperty(required=True)
    place_lng = db.StringProperty(required=True)
    comment = db.StringProperty()
    # 1が通常、2がclose、3がfix
    status_id = db.IntegerProperty(required=True)
    # 0が公開、1が非公開
    public_id = db.IntegerProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)
    modified_at = db.DateTimeProperty(auto_now_add=False)
    deleted_at = db.DateTimeProperty(auto_now_add=False)

    @classmethod
    def get_event(self, event_id):
        event = ShourPost.get_by_id(int(event_id))
        if event:
            return event
        else:
            # イベントが存在しない
            raise ShourAppError(30001)
    
    @classmethod
    def set_offset(self, offset):
        if offset:
            return offset
        else:
            return 0
    
    @classmethod
    def refresh_feed_new(self, user_id):
        query = ShourPost.all()
        query.filter("user_id =", int(user_id))
        query.order("-created_at")
        events = query.fetch(1000)
        datas = []
        for event in events:
            dec = datetime.datetime.now() - event.start_time
            if dec >= 24:
                # 3は非公開、ShourPostのPropertyのコメント参照
                event.status_id = 3
                datas.append(event)
        if len(datas) > 0:
            db.put(datas)
    
    @classmethod
    def get_feed_new(self, user_id, limit, offset):
        if offset == 0:
            offset = 0
        else:
            offset = limit * offset + 1
        logging.info("友人検索")
        friends = ShourFriend.show_all_friends(user_id)
        for friend in friends:
            query = ShourPost.all()
            logging.info(friend.friend_id)
            query.filter("user_id =", friend.friend_id)
            # 公開のものを取得
            query.filter("public_id =", 0)
            #query.order("-created_at")
            events = query.fetch(limit=limit, offset=offset)
            datas = []
            for event in events:
                data = {
                "event": {
                "event_id": event.key().id(),
                "comment:": event.comment,
                "created_at": event.created_at,
                "end_time": event.end_time,
                "master": event.master,
                "modified_at": event.modified_at,
                "place_address": event.place_address,
                "place_lat": event.place_lat,
                "place_lng": event.place_lng,
                "place_name": event.place_name,
                "public_id": event.public_id,
                "start_time": event.start_time,
                "status_id": event.status_id
                },
                "user":{
                "user_id":event.user_reference.key().id(),
                "name":event.user_reference.name,
                "picture_url":event.user_reference.picture_url
                }}
                datas.append(data)
        # 投稿が新しい順にソート
        sorted(datas, key=lambda data: data["event"]["event_id"], reverse=True)
        return datas

    @classmethod
    def get_feed_near(self, user_id, limit, offset):
        if offset == 0:
            offset = 0
        else:
            offset = limit * offset + 1
        logging.info("友人検索")
        friends = ShourFriend.show_all_friends(user_id)
        for friend in friends:
            query = ShourPost.all()
            logging.info(friend.friend_id)
            query.filter("user_id =", friend.friend_id)
            # 公開のものを取得
            query.filter("public_id =", 0)
            #query.order("started_at")
            events = query.fetch(limit=limit, offset=offset)
            datas = []
            for event in events:
                data = {
                "event": {
                "event_id": event.key().id(),
                "comment:": event.comment,
                "created_at": event.created_at,
                "end_time": event.end_time,
                "master": event.master,
                "modified_at": event.modified_at,
                "place_address": event.place_address,
                "place_lat": event.place_lat,
                "place_lng": event.place_lng,
                "place_name": event.place_name,
                "public_id": event.public_id,
                "start_time": event.start_time,
                "status_id": event.status_id
                },
                "user":{
                "user_id":event.user_reference.key().id(),
                "name":event.user_reference.name,
                "picture_url":event.user_reference.picture_url
                }}
                datas.append(data)
        return datas

    @classmethod
    def get_master_event(self, user_id):
        query = ShourPost.all()
        query.filter("user_id =", int(user_id))
        query.filter("master =", True)
        events = query.fetch(1000)
        return events
    
    @classmethod
    def destroy_all(self, event_id):
        return None