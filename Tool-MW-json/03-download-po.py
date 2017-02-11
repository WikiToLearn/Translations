#!/usr/bin/env python3
import common

import os
import glob
import polib

lang_en = "{}en/".format(common.tmp_output_po_dir)
if not os.path.exists(lang_en):
    os.makedirs(lang_en)

for pot_file in glob.glob("{}*.pot".format(common.output_pot_dir)):
    en_po_file = "{}{}".format(lang_en, os.path.basename(pot_file)[:-4]+".po")
    pot = polib.pofile(pot_file)
    pot.metadata['Report-Msgid-Bugs-To'] = "info@wikitolearn.org"
    pot.metadata['Language-Team'] = "info@wikitolearn.org"
    pot.metadata['Last-Translator'] = "info@wikitolearn.org"
    pot.metadata['PO-Revision-Date'] = pot.metadata['POT-Creation-Date']
    for e in pot:
        e.msgstr = e.msgid
    pot.save(en_po_file)


for l in ["it","de"]: # dummy content, just for test
    lang_dummy = "{}{}/".format(common.tmp_output_po_dir,l)
    if not os.path.exists(lang_dummy):
        os.makedirs(lang_dummy)

    for pot_file in glob.glob("{}*.pot".format(common.output_pot_dir)):
        dummy_po_file = "{}{}".format(lang_dummy, os.path.basename(pot_file)[:-4]+".po")
        pot = polib.pofile(pot_file)
        pot.metadata['Report-Msgid-Bugs-To'] = "info@wikitolearn.org"
        pot.metadata['Language-Team'] = "info@wikitolearn.org"
        pot.metadata['Last-Translator'] = "info@wikitolearn.org"
        pot.metadata['PO-Revision-Date'] = pot.metadata['POT-Creation-Date']
        for e in pot:
            e.msgstr = l + e.msgid
        pot.save(dummy_po_file)
