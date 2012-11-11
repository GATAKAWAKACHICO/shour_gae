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

# ライブラリのモジュール読み込み
lib_dir = 'slib'
sys.path.append(lib_dir)
import jsonencoder

# 独自例外モジュール読み込み
err_dir = 'err'
sys.path.append(err_dir)
from shourapperror import ShourAppError

class ShourProfileShow(webapp.RequestHandler):
    def post(self):
        self.response.content_type = "application/json; charset=utf-8"
        profile_id = self.request.get('profile_id')
        try:
            profile = ShourUser.show(profile_id)
            data = {"name": profile.name, "first_name": profile.first_name, "last_name": profile.last_name, "picture_url":profile.picture_url, "created_at":profile.created_at, "last_login":profile.last_login}
            data = jsonencoder.GqlEncoder().encode(data)
            self.response.out.write(data)
        except ShourAppError, e:
            data = {"message": False, "err":e.value}
            json.dump(data, self.response.out, ensure_ascii=False)