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

# 独自例外モジュール読み込み
err_dir = 'err'
sys.path.append(err_dir)
from shourapperror import ShourAppError

class ShourUserSignInEmail(webapp.RequestHandler):
    def post(self):
        self.response.content_type = "application/json"
        name = self.request.get('name')
        password = self.request.get('password')
        mail = self.request.get('mail')
        try:
            ShourUser.sign_up_check(mail)
        except ShourAppError, e:
            data = {"message": False, "err":e.value}
            json.dump(data, self.response.out, ensure_ascii=False)
            return
        rsa = ShourUser.generate_rsa_pub_and_private_key(password)
        shour_user = ShourUser(name=name, rsa_pub_key=rsa[0], password=rsa[1], mail=mail)
        try:
            shour_user.put()
            data = {"message": True}
            json.dump(data, self.response.out, ensure_ascii=False)
        except ShourAppError, e:
            data = {"message": False, "err":e.value}
            json.dump(data, self.response.out, ensure_ascii=False)

class ShourUserLoginEmail(webapp.RequestHandler):
    def post(self):
        self.response.content_type = "application/json"
        mail = self.request.get('mail')
        password = self.request.get('password')
        try:
            user_id = ShourUser.login_check(mail, password)
            data = {"user_id": user_id}
            json.dump(data, self.response.out, ensure_ascii=False)
        except ShourAppError, e:
            data = {"message": False, "err":e.value}
            json.dump(data, self.response.out, ensure_ascii=False)