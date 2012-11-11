#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
# アプリのカレントディレクトリを取得して独自モジュールを読み込む
import sys,os
apppath = os.path.dirname(os.path.abspath(__file__))
# モデルとコントローラのディレクトリのモジュール読み込み
controllers_dir = 'controllers'
models_dir = 'models'
sys.path.append(apppath+'/'+controllers_dir)
sys.path.append(apppath+'/'+models_dir)
# コントローラ
from shouruser_controller import ShourUserSignInEmail, ShourUserLoginEmail
from shourpost_controller import ShourPostAdd
from shourfriend_controller import ShourFriendGenereteRequest, ShourFriendNoticeRequest, ShourFriendRequestAccept, ShourFriendDestroy
from shouruserprofile_controller import ShourProfileShow
# モデル
from shouruser import ShourUser as shour_user

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.write("We're making shour bigger.")

# URLルートの設定
app = webapp.WSGIApplication([
    ('/', MainHandler),
    # /users
    ('/users/sign_in_with_email', ShourUserSignInEmail),
    ('/users/login_with_email', ShourUserLoginEmail),
    # /profile
    ('/profile/show', ShourProfileShow),
    # /posts
    ('/posts/add', ShourPostAdd),
    # /friends
    ('/friends/request', ShourFriendGenereteRequest),
    ('/friends/notice', ShourFriendNoticeRequest),
    ('/friends/accept', ShourFriendRequestAccept),
    ('/friends/delete', ShourFriendDestroy),
], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()