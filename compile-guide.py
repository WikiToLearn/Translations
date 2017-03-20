#!/usr/bin/env python2

# usage: compile-guide.py <ini> <english ini> <language code>

import sys, codecs
import configparser, os
import re

p = re.compile(ur'<ref:([^>]*)>')

config = configparser.ConfigParser()
config.readfp(codecs.open(sys.argv[2],'r', 'utf8'))

enconfig = configparser.ConfigParser()
enconfig.readfp(codecs.open(sys.argv[1],'r', 'utf8'))

for identifier, string in config.items("messages"):
    output_path = sys.argv[4] + '/' + sys.argv[3] + '/' + string + '.mw'
    # print os.path.dirname(output_path)
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))
    output_file = open(output_path, 'w')

    if len(string) == 0:
       string = enconfig.get("messages", identifier)
    string = string.encode('utf-8')

    # print 'xxxxxxSEPARATORBEGINxxxxxx'
    # print "'''"+string+"'''"
    for line in open("guide/"+sys.argv[3]+'/'+identifier+".txt").readlines():
        raw_line = line.strip()
        for match in re.findall(p, raw_line):
            wstring = u'<ref:'+match+'>'
            tstring = config.get("messages", match)
            raw_line = codecs.decode(raw_line, 'utf8')
            raw_line.replace(wstring.decode('utf-8'), tstring)
            raw_line = raw_line.replace(wstring, tstring).encode('utf-8')
        output_file.write(raw_line+'\n')

    # print 'xxxxxxSEPARATORENDxxxxxx'
