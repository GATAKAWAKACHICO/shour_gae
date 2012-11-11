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
from shouruser import ShourUser

# 独自例外モジュール読み込み
err_dir = 'err'
sys.path.append(err_dir)
from shourapperror import ShourAppError

class ShourTempUser(db.Model):
    token = db.StringProperty(required=True)

    @classmethod
    def save_user_temporary(self, tmp_user, user):
        user.put()
        tmp_user.put()

    @classmethod
    def activate(self, token):
        if token:
            query = ShourTempUser.all()
            query.filter("token =", token)
            tmp_user = query.get()
            query2 = ShourUser.all()
            query2.filter('token =', token)
            user = query2.get()
        else:
            # アクティベートに失敗
            raise ShourAppError(10006)
        if tmp_user and user:
            # クロスグループトランザクションCross-Group (XG) Transactions有効化
            xg_on = db.create_transaction_options(xg=True)
            db.run_in_transaction_options(xg_on, ShourTempUser.activate_all, tmp_user, user)
        else:
            # アクティベートに失敗
            raise ShourAppError(10006)

    @classmethod
    def activate_all(self, tmp_user, user):
        db.delete(tmp_user)
        user.active = True
        user.put()

    @classmethod
    def is_duplicate_token(self, token):
        query = ShourUser.all(keys_only=True).filter('token', token)
        entity = query.get()
        if entity:
            return False
        else:
            return True