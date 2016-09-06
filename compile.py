#!/usr/bin/env python

import configparser, os

languages = ["it", "en", "fr", "es"]

config = configparser.ConfigParser()

enconfig = configparser.ConfigParser()
enconfig.readfp(open("wtl-messages/en.ini",'r'))

for f in languages:
    config.readfp(open("wtl-messages/"+f+".ini",'r'))
    outarr = []
    for identifier, string in config.items("messages"):
        if len(string) == 0:
           string = enconfig.get("messages", identifier)

        out = "<section begin=" + identifier
        out += " />" + string
        out += "<section end=" + identifier +  " /> "
        outarr.append(out)
    outfile = open('mediawiki/'+f+'.mw', 'w')
    outfile.write('\n'.join(outarr)+'\n')
