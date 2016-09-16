#!/usr/bin/env python

# usage: compile-guide.py <ini> <english ini> <language code>

import sys
import configparser, os
import re

p = re.compile(ur'<ref:([^>]*)>')

config = configparser.ConfigParser()
config.readfp(open(sys.argv[2],'r'))

enconfig = configparser.ConfigParser()
enconfig.readfp(open(sys.argv[1],'r'))

for identifier, string in config.items("messages"):
    if len(string) == 0:
       string = enconfig.get("messages", identifier)

    print 'xxxxxxSEPARATORBEGINxxxxxx'
    print "''"+string+"''"
    for line in open("guide/"+sys.argv[3]+'/'+identifier+".txt").readlines():
        raw_line = line.strip()
        for match in re.findall(p, raw_line):
            raw_line = raw_line.replace('<ref:'+match+'>', config.get("messages", match))
        print raw_line

    print 'xxxxxxSEPARATORENDxxxxxx'
