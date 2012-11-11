#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db

class ShourPost(db.Model):
    user_id = db.IntegerProperty(required=True)
    start_time = db.DateTimeProperty(auto_now_add=False, required=True)
    end_time = db.DateTimeProperty(auto_now_add=False)
    place_name = db.StringProperty(required=True)
    place_address = db.StringProperty()
    place_lat = db.StringProperty(required=True)
    place_lng = db.StringProperty(required=True)
    comment = db.StringProperty()
    status_id = db.IntegerProperty(required=True)
    public_id = db.IntegerProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)
    modified_at = db.DateTimeProperty(auto_now_add=False)
    deleted_at = db.DateTimeProperty(auto_now_add=False)