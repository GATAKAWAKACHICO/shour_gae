#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db
from google.appengine.api.datastore_types import ByteString
import datetime
import sys

# 独自例外モジュール読み込み
err_dir = 'err'
sys.path.append(err_dir)
from shourapperror import ShourAppError

try:
    import Crypto.PublicKey.RSA as RSA
    Crypto_AVAILABLE = True
except ImportError:
    Crypto_AVAILABLE = False

class ShourUser(db.Model):
    name = db.StringProperty(required=True)
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    password = db.BlobProperty(required=True)
    rsa_pub_key = db.BlobProperty(required=True)
    mail = db.EmailProperty(required=True)
    picture_url = db.StringProperty()
    facebook_id = db.StringProperty()
    twitter_id = db.StringProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)
    last_login = db.DateTimeProperty(auto_now_add=False)
    active = db.BooleanProperty(required=True)
    token = db.StringProperty(required=True)

    @classmethod
    def sign_up_check(self, mail):
        query = ShourUser.all(keys_only=True).filter('mail', mail)
        entity = query.get()
        if entity:
            # 新規登録ユーザーがすでにいる
            raise ShourAppError(10000)

    @classmethod
    def login_check(self, mail, password):
        query = ShourUser.all(keys_only=False).filter('mail', mail)
        entity = query.get()
        if entity:
            if entity.password == ShourUser.encrypt_password(entity.rsa_pub_key, password):
                if entity.active == True:
                    entity.last_login = datetime.datetime.now()
                    db.put(entity)
                    return entity.key().id()
                else:
                    # 認証失敗：アカウントがアクティベートされていない
                    raise ShourAppError(10005)
            else:
                # 認証失敗：パスワードが異なる
                raise ShourAppError(10001)
        else:
            # 認証失敗：メールアドレスが異なる
            raise ShourAppError(10002)

    @classmethod
    def shour_authorize(self, user_id, password):
        if user_id and password:
            entity = ShourUser.get_by_id(int(user_id))
            if entity:
                if entity.password == ShourUser.encrypt_password(entity.rsa_pub_key, password):
                    if entity.active == True:
                        entity.last_login = datetime.datetime.now()
                        db.put(entity)
                        return entity.key().id()
                    else:
                        # 認証失敗：アカウントがアクティベートされていない
                        raise ShourAppError(10005)
                else:
                    # 認証失敗：パスワードが異なる
                    raise ShourAppError(10001)
            else:
                # 認証失敗：メールアドレスが異なる
                raise ShourAppError(10002)
        else:
            # 認証失敗：その他の理由
            raise ShourAppError(10004)

    @classmethod
    def generate_rsa_pub_and_private_key(self, password):
        if Crypto_AVAILABLE:
            rsa = RSA.generate(2048)
            #公開鍵
            rsa_pub_key = rsa.publickey()
            #暗号化したパスワード
            encrypto = rsa_pub_key.encrypt( bytes(password), "" )
            return [rsa_pub_key.exportKey('PEM'), encrypto[0]];
        else:
            rsa_pub_key = bytes(password)
            encrypto = bytes(password)
            return [rsa_pub_key, encrypto];
            
    @classmethod
    def encrypt_password(self, rsa_pub_key, password):
        if Crypto_AVAILABLE:
            rsa_pub_key = RSA.importKey(rsa_pub_key)
            encrypto = rsa_pub_key.encrypt( bytes(password), "" )
            return encrypto[0]
        else:
            encrypto = bytes(password)
            return encrypto

    @classmethod
    def is_exist(self, user_id):
        entity = ShourUser.get_by_id(int(user_id))
        if entity:
            return True
        else:
            return False

    @classmethod
    def show(self, profile_id):
        entity = ShourUser.get_by_id(int(profile_id))
        if entity:
            return entity
        else:
            # プロフィール（アカウント）が見つからない
            raise ShourAppError(10003)
