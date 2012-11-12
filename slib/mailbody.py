#!/usr/bin/env python
# -*- coding: utf-8 -*-

class MailBody:
    def thank_after_registered(self, name, token, lang):
        body = name + u"さん、\nShourへようこそ。\n\nShourにあなたのメールアドレスが仮登録され、アカウントが発行されました。下記のURLをクリックしてアカウントを有効化してください。\nhttps://sh-hringhorni.appspot.com/activate?t=" + token + u"\n\nShourは、ちょっとした時間を親しい間柄の人との楽しいひと時に変える新感覚予定共有アプリです。\n\n「今度お茶しよう」\n「久しぶりに会いたいね」\n「また語りましょう」\nそんな友達との約束を、Shourで是非実現してみてください。\n\n日々の生活の中にあるスキマ時間が、シャワータイムのようなリフレッシュのひと時になるよう、Shourはお手伝いします。\n\nShour開発チーム一同\n\n※このメールに覚えがない場合、誤って送信された可能性がございます。大変お手数ですが、破棄してください。"
        if lang:
            if lang == "en":
                body = u"Hi," + name +".\nYou are the newest member of \"Shour\".\n\nClick here to verify your email address. \nhttps://sh-hringhorni.appspot.com/activate?t=" + token + u"\n\nWith shour, you can enjoy a pleasant time with your close friends in your spare time. Shour will help you spent refreshing moments like shower time. Please just try it! We hope you enjoy \"SHaring your hOUR\"!! \n\nDevelopment team of Shour\n\nNotice: If you do not know any idea about this email, this may be miscarriaged to wrong email address. We appologize for this inconvenience and thank you for delete this email."
        return body