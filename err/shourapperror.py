#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

class ShourAppError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)