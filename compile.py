#!/usr/bin/env python2

import sys, codecs
import configparser, os

config = configparser.ConfigParser()
config.readfp(codecs.open(sys.argv[2],'r','utf8'))

enconfig = configparser.ConfigParser()
enconfig.readfp(codecs.open(sys.argv[1],'r','utf8'))

for identifier, string in config.items("messages"):
    if len(string) == 0:
       string = enconfig.get("messages", identifier)

    out = "<section begin=" + identifier
    out += " />" + string
    out += "<section end=" + identifier +  " /> "
    print out.encode('utf8')
#     outarr.append(out)
# outfile = open('mediawiki/'+f+'.mw', 'w')
# outfile.write('\n'.join(outarr)+'\n')
