#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.api import mail
import json

# モデルのモジュール読み込み
import sys,os
models_dir = 'models'
sys.path.append(os.pardir+'/'+models_dir)
from google.appengine.ext import db
from shouruser import ShourUser
from shourtempuser import ShourTempUser

# ライブラリのモジュール読み込み
lib_dir = 'slib'
sys.path.append(lib_dir)
import jsonencoder
from tokengenerator import TokenGenerator

# 独自例外モジュール読み込み
err_dir = 'err'
sys.path.append(err_dir)
from shourapperror import ShourAppError

class ShourUserSignInEmail(webapp.RequestHandler):
    def post(self):
        self.response.content_type = "application/json"
        name = self.request.get('name')
        password = self.request.get('password')
        email = self.request.get('mail')
        try:
            ShourUser.sign_up_check(email)
        except ShourAppError, e:
            data = {"message": False, "err":e.value}
            json.dump(data, self.response.out, ensure_ascii=False)
            return
        try:
            tg = TokenGenerator()
            token = tg.generate_token()
            while ShourTempUser.is_duplicate_token(token) == False:
                tg = TokenGenerator()
                token = tg.generate_token()
            tmp_user = ShourTempUser(token=token)
        except ShourAppError, e:
            data = {"message": False, "err":e.value}
            json.dump(data, self.response.out, ensure_ascii=False)
            return
        rsa = ShourUser.generate_rsa_pub_and_private_key(password)
        shour_user = ShourUser(name=name, rsa_pub_key=rsa[0], password=rsa[1], mail=email, active=False, token=token)
        try:
            # クロスグループトランザクションCross-Group (XG) Transactions有効化
            xg_on = db.create_transaction_options(xg=True)
            db.run_in_transaction_options(xg_on, ShourTempUser.save_user_temporary, tmp_user, shour_user)
            data = {"message": True}
            json.dump(data, self.response.out, ensure_ascii=False)
        except ShourAppError, e:
            data = {"message": False, "err":e.value}
            json.dump(data, self.response.out, ensure_ascii=False)
            return
        # アカウントアクティベート用のメールを送信する
        if not mail.is_email_valid(email):
            return
        mail.send_mail(sender="webmaster@shour.jp",
              to=email,
              subject="Welcome to Shour",
              body="Shourにあなたのメールアドレスが仮登録され、アカウントが発行されました。下記のURLからアカウントを有効化してください。  https://sh-hringhorni.appspot.com/activate?t=" + token + "  このメールに覚えがない場合は削除してください。"
              )

class ShourUserLoginEmail(webapp.RequestHandler):
    def post(self):
        self.response.content_type = "application/json"
        email = self.request.get('mail')
        password = self.request.get('password')
        try:
            user_id = ShourUser.login_check(email, password)
            data = {"user_id": user_id}
            json.dump(data, self.response.out, ensure_ascii=False)
        except ShourAppError, e:
            data = {"message": False, "err":e.value}
            json.dump(data, self.response.out, ensure_ascii=False)

class ShourUserActivate(webapp.RequestHandler):
    def get(self):
        token = self.request.get('t')
        try:
            ShourTempUser.activate(token)
            self.redirect("tel:")
        except ShourAppError, e:
            self.response.out.write('<script>alert("エラーが発生しました");</script>')