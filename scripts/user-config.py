# -*- coding: utf-8 -*-
#mylang='en'
family='wikitolearn'
console_encoding = 'utf-8'
password_file = "./passwordFile.txt"
#put_throttle=1
#maxthrottle=10
#usernames = {}
#usernames[family] = {}
for l in ['en', 'fr', 'it']:
    usernames[family][l] = u"WikiToBot"
    usernames[family]['dev'+l] = u"WikiToBot"

