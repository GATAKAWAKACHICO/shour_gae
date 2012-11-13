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

class ShourPost(db.Model):
    user_id = db.IntegerProperty(required=True)
    friend_id = db.IntegerProperty(required=True)
    master= db.BooleanProperty(required=True)
    start_time = db.DateTimeProperty(auto_now_add=False, required=True)
    end_time = db.DateTimeProperty(auto_now_add=False)
    place_name = db.StringProperty(required=True)
    place_address = db.StringProperty()
    place_lat = db.StringProperty(required=True)
    place_lng = db.StringProperty(required=True)
    comment = db.StringProperty()
    status_id = db.IntegerProperty(required=True)
    public_id = db.IntegerProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)
    modified_at = db.DateTimeProperty(auto_now_add=False)
    deleted_at = db.DateTimeProperty(auto_now_add=False)

    @classmethod
    def set_offset(self, offset):
        if offset:
            return offset
        else:
            return 0

    @classmethod
    def get_feed_new(self, user_id, limit, offset):
        if offset == 0:
            offset = 0
        else:
            offset = limit * offset + 1
        query = ShourPost.all()
        query.filter("friend_id =", int(user_id))
        query.order("-created_at")
        feed = query.fetch(limit=limit, offset=offset)
        return feed

    @classmethod
    def get_feed_near(self, user_id, limit, offset):
        if offset == 0:
            offset = 0
        else:
            offset = limit * offset + 1
        query = ShourPost.all()
        query.filter("friend_id =", int(user_id))
        query.order("start_time")
        feed = query.fetch(limit=limit, offset=offset)
        return feed

    @classmethod
    def get_master_event(self, user_id):
        query = ShourPost.all()
        query.filter("user_id =", int(user_id))
        query.filter("master =", True)
        events = query.fetch(1000)
        return events