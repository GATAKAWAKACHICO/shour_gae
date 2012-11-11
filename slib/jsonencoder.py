#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import time
import json
from google.appengine.ext import db 

class GqlEncoder(json.JSONEncoder):
    def default(self, obj): 
        if hasattr(obj, '__json__'): 
            return getattr(obj, '__json__')() 

        if isinstance(obj, db.GqlQuery): 
            return list(obj) 

        elif isinstance(obj, db.Model): 
            properties = obj.properties().items() 
            output = {} 
            for field, value in properties: 
                output[field] = getattr(obj, field) 
            return output 

        elif isinstance(obj, datetime.datetime): 
            output = {} 
            fields = ['day', 'hour', 'microsecond', 'minute', 'month', 'second', 
            'year'] 
            methods = ['ctime', 'isocalendar', 'isoformat', 'isoweekday', 
            'timetuple'] 
            for field in fields: 
                output[field] = getattr(obj, field) 
            for method in methods: 
                output[method] = getattr(obj, method)() 
            output['epoch'] = time.mktime(obj.timetuple()) 
            return output 

        elif isinstance(obj, time.struct_time): 
            return list(obj)

        return json.JSONEncoder.default(self, obj)