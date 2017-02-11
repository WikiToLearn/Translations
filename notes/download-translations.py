#!/usr/bin/env python3
import os
import os.path
import glob
import polib

mypath = "{}/".format(os.path.dirname(os.path.realpath(__file__)))

pot_files = glob.glob("{}/pot/*".format(mypath))
for pot_file in pot_files:
    if not os.path.exists(mypath + "/po/en/" ):
        os.makedirs(mypath + "/po/en/" )
    po_file = mypath + "/po/en/" + pot_file[len(mypath) + 5:-4] + ".po"
    pot = polib.pofile(pot_file)
    pot.metadata['Report-Msgid-Bugs-To'] = "info@wikitolearn.org"
    pot.metadata['Language-Team'] = "info@wikitolearn.org"
    pot.metadata['Last-Translator'] = "info@wikitolearn.org"
    pot.metadata['PO-Revision-Date'] = pot.metadata['POT-Creation-Date']
    for e in pot:
        e.msgstr = e.msgid
    pot.save(po_file)
