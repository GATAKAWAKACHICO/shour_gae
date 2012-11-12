#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.api import mail
from google.appengine.api import files
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
from mailbody import MailBody

# 独自例外モジュール読み込み
err_dir = 'err'
sys.path.append(err_dir)
from shourapperror import ShourAppError

class ShourUserSignInEmail(webapp.RequestHandler):
    def post(self):
        self.response.content_type = "application/json"
        name = self.request.get('name')
        first_name = self.request.get('first_name')
        last_name = self.request.get('last_name')
        picture = self.request.get('picture')
        #picture = self.request.body_file.vars['picture']
        password = self.request.get('password')
        email = self.request.get('mail')
        lang = self.request.get('lang')
        # メールが重複して登録されていないか
        try:
            ShourUser.sign_up_check(email)
        except ShourAppError, e:
            data = {"message": False, "err":e.value}
            json.dump(data, self.response.out, ensure_ascii=False)
            return
        # 本登録用トークンの生成
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
        # 画像が送られてきたかどうかで分岐
        if picture:
            # バイナリの画像データがある場合
            body_file_name = self.request.body_file.vars['picture'].filename.decode("utf8")
            root_, ext_ = os.path.splitext(body_file_name)
            #header = self.request.body_file.vars['picture'].headers['content-type']
            try:
                header = ShourUser.get_header(ext_)
            except ShourAppError, e:
                data = {"message": False, "err":e.value}
                json.dump(data, self.response.out, ensure_ascii=False)
                return
            # DB保存用のurl
            picture_url = "http://commondatastorage.googleapis.com/sh_avatar/user/" + token + ext_
            # Google Cloud Storage用url
            READ_PATH = '/gs/sh_avatar/user/' + token + ext_
            write_path = files.gs.create(READ_PATH, mime_type=header, acl='public-read')
            with files.open(write_path, 'a') as fp:
                fp.write(picture)
            files.finalize(write_path)
        else:
            # 無ければデフォルトの画像を設定
            picture_url = "http://commondatastorage.googleapis.com/sh_avatar/default/default_avater.png"
        # 公開鍵作成
        rsa = ShourUser.generate_rsa_pub_and_private_key(password)
        # POSTされたユーザデータをモデルに変換
        shour_user = ShourUser(
        name=name, first_name=first_name, last_name=last_name, picture_url=picture_url, rsa_pub_key=rsa[0], password=rsa[1], mail=email, active=False, token=token)
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
        # メール本文言語対応
        mabd = MailBody()
        body = mabd.thank_after_registered(name, token, lang)
        mail.send_mail(sender="webmaster@shour.jp",
              to=email,
              subject="Welcome to Shour",
              body=body
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