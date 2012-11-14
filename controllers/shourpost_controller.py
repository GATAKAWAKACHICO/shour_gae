#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
import json
import datetime
import urllib
import logging

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
        # ここはint()が必要。
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
        user = ShourUser.get_by_id(int(user_id))
        shour_post = ShourPost(
        user_id=user_id,
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
        modified_at=modified_at,
        user_reference=user.key()
        )
        db.put(shour_post)
        data = {"message": True}
        json.dump(data, self.response.out, ensure_ascii=False)

class ShourPostEdit(webapp.RequestHandler):
    def post(self):
        self.response.content_type = "application/json"
        user_id = self.request.get('user_id')
        password = self.request.get('password')
        event_id = self.request.get('event_id')
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
            event = ShourPost.get_event(int(event_id))
        except ShourAppError, e:
            data = {"message": False, "err":e.value}
            json.dump(data, self.response.out, ensure_ascii=False)
            return
        event.start_time = start_time
        event.end_time = end_time
        event.place_name = place_name
        event.place_address = place_address
        event.place_lat = place_lat
        event.place_lng = place_lng
        event.comment = comment
        event.public_id = public_id
        db.put(event)

class ShourPostDelete(webapp.RequestHandler):
    def post(self):
        self.response.content_type = "application/json"
        user_id = self.request.get('user_id')
        password = self.request.get('password')
        event_id = self.request.get('event_id')
        try:
            ShourUser.shour_authorize(user_id, password)
        except ShourAppError, e:
            data = {"message": False, "err":e.value}
            json.dump(data, self.response.out, ensure_ascii=False)
            return
        ShourPost.destroy_all(event_id)
        
        