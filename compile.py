#!/usr/bin/env python

import sys
import configparser, os

config = configparser.ConfigParser()
config.readfp(open(sys.argv[2],'r'))

enconfig = configparser.ConfigParser()
enconfig.readfp(open(sys.argv[1],'r'))

for identifier, string in config.items("messages"):
    if len(string) == 0:
       string = enconfig.get("messages", identifier)

    out = "<section begin=" + identifier
    out += " />" + string
    out += "<section end=" + identifier +  " /> "
    print out
#     outarr.append(out)
# outfile = open('mediawiki/'+f+'.mw', 'w')
# outfile.write('\n'.join(outarr)+'\n')
