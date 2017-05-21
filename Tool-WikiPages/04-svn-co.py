#!/usr/bin/env python3

import common

import glob
import shutil
import os
import os.path
import json
import git
import time
import datetime
from subprocess import call
from re import sub


en_reverse_placeholder_dict = {}
with open("{}pages_id.json".format(common.tmp_dir)) as pages_id_file:
    en_reverse_placeholder_dict = json.load(pages_id_file)
    pages_id_file.close()

expected_pos = []
for key in en_reverse_placeholder_dict.keys():
    expected_pos.append("{}.po".format(key))

for lang in common.languages:
    po_output = "{}{}".format(common.kde_svn_dir, lang)
    if os.path.exists(po_output):
        shutil.rmtree(po_output)
    cmd = ["svn","co", "svn://anonsvn.kde.org/home/kde/trunk/l10n-kf5/{}/messages/wikitolearn".format(lang), po_output]
    #print(cmd)
    call(cmd)
    out_path = "{}/{}".format(common.tmp_output_po_dir, lang)
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    shutil.copy2("{}/project_messages.po".format(po_output), "{}{}/project_messages.po".format(common.tmp_output_po_dir, lang))
    shutil.copy2("{}/pages_id.po".format(po_output), "{}{}/pages_id.po".format(common.tmp_output_po_dir, lang))

    for po in expected_pos:
        if po.startswith("FILE"):
            continue
        #print(["cp", "{}/{}".format(po_output, po), "{}/{}/{}".format(common.tmp_output_po_dir, lang, po)])
        shutil.copy2("{}/{}".format(po_output, po), "{}/{}/{}".format(common.tmp_output_po_dir, lang, po))
