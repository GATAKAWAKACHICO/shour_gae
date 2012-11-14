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

# ライブラリのモジュール読み込み
lib_dir = 'slib'
sys.path.append(lib_dir)
import jsonencoder

# 独自例外モジュール読み込み
err_dir = 'err'
sys.path.append(err_dir)
from shourapperror import ShourAppError

class ShourFeedShowNew(webapp.RequestHandler):
    def post(self):
        self.response.content_type = "application/json"
        user_id = self.request.get('user_id')
        password = self.request.get('password')
        offset = self.request.get('offset')
        # オフセットを初期化（パラメータが無ければoffset=0）
        offset = ShourPost.set_offset(offset)
        try:
            user = ShourUser.shour_authorize(user_id, password)
        except ShourAppError, e:
            data = {"message": False, "err":e.value}
            json.dump(data, self.response.out, ensure_ascii=False)
            return
        # 2番目引数はlimit
        feed = ShourPost.get_feed_new(user_id, 10, int(offset))
        data = jsonencoder.GqlEncoder().encode(feed)
        self.response.out.write(data)

class ShourFeedShowNear(webapp.RequestHandler):
    def post(self):
        self.response.content_type = "application/json"
        user_id = int(self.request.get('user_id'))
        password = self.request.get('password')
        offset = self.request.get('offset')
        # オフセットを初期化（パラメータが無ければoffset=0）
        offset = ShourPost.set_offset(offset)
        try:
            user = ShourUser.shour_authorize(user_id, password)
        except ShourAppError, e:
            data = {"message": False, "err":e.value}
            json.dump(data, self.response.out, ensure_ascii=False)
            return
        # 2番目引数はlimit
        feed = ShourPost.get_feed_near(user_id, 10, int(offset))
        data = jsonencoder.GqlEncoder().encode(feed)
        self.response.out.write(data)

class ShourFeedRefreshShowNew(webapp.RequestHandler):
    def post(self):
        self.response.content_type = "application/json"
        user_id = self.request.get('user_id')
        password = self.request.get('password')
        # オフセットいらない？
        # offset = self.request.get('offset')
        # オフセットを初期化（パラメータが無ければoffset=0）
        # offset = ShourPost.set_offset(offset)
        try:
            user = ShourUser.shour_authorize(user_id, password)
        except ShourAppError, e:
            data = {"message": False, "err":e.value}
            json.dump(data, self.response.out, ensure_ascii=False)
            return
        ShourPost.refresh_feed_new(user_id)
        data = {"message": True}
        json.dump(data, self.response.out, ensure_ascii=False)
        