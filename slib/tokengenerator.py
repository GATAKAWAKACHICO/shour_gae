#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import string

class TokenGenerator:
    def generate_token(self):
        s = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz123456789"
        string = ""
        for i in range(16):
            x = random.randint(0,len(s)-1)
            string += s[x]
        return string