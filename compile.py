import configparser, os

languages = ["en"]

for f in languages:
    config = configparser.ConfigParser()
    config.readfp(open(f+".ini"))
    outarr = []
    for identifier, string in config.items("messages"):
        out = "<section begin=" + identifier
        out += " />" + string
        out += "<section end=" + identifier +  " /> "
        outarr.append(out)
    outfile = open(f+'.mw', 'w')
    outfile.write('\n'.join(outarr)+'\n')

# config.read(['site.cfg', os.path.expanduser('~/.myapp.cfg')])
