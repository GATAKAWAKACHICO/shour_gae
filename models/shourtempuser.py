#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import sys
import random
import string

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

class ShourTempUser(db.Model):
    # Tokenが使われたかどうか
    used = db.BooleanProperty(required=True)
    created_at = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def save_user_temporary(self, tmp_user, user):
        user.put()
        tmp_user.put()

    @classmethod
    def activate(self, token, tmp_user_id, user_id):
        if token:
            # tパラメータで渡されたキー(トークン)をKeyオブジェクトに変換
            tmp_user_key = Key(encoded=token)
            tmp_user = db.get(tmp_user_key)
            user_key = db.Key.from_path('ShourTempUser', int(tmp_user_id), 'ShourUser', int(user_id))
            user = db.get(user_key)
            #query = ShourTempUser.all()
            #query.filter("token =", token)
            #tmp_user = query.get()
            #query2 = ShourUser.all()
            #query2.filter('token =', token)
            #user = query2.get()
        else:
            # アクティベートに失敗
            raise ShourAppError(10006)
        if tmp_user and user:
            if tmp_user.used == True:
                # アクティベートに失敗
                raise ShourAppError(10006)
            elif user.active == True:
                # アクティベートに失敗
                raise ShourAppError(10006)
            # クロスグループトランザクションCross-Group (XG) Transactions有効化
            #xg_on = db.create_transaction_options(xg=True)
            #db.run_in_transaction_options(xg_on, ShourTempUser.activate_all, tmp_user, user)
            db.run_in_transaction(ShourTempUser.activate_all, tmp_user, user)
        else:
            # アクティベートに失敗
            raise ShourAppError(10006)

    @classmethod
    def activate_all(self, tmp_user, user):
        tmp_user.used = True
        user.active = True
        db.put([tmp_user, user])

    @classmethod
    def is_duplicate_token(self, token):
        query = ShourUser.all(keys_only=True).filter('token', token)
        entity = query.get()
        if entity:
            return False
        else:
            return True