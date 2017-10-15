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


lang_en = "{}en/".format(common.tmp_output_po_dir)
if not os.path.exists(lang_en):
    os.makedirs(lang_en)

expected_pos = []
for pot_file in glob.glob("{}*.pot".format(common.output_pot_dir)):
    expected_pos.append(os.path.basename(pot_file)[:-4]+".po")

for lang in common.languages:
    po_output = "{}{}".format(common.kde_svn_dir, lang)
    if os.path.exists(po_output):
        shutil.rmtree(po_output)
    cmd = ["svn","co", "svn://anonsvn.kde.org/home/kde/trunk/l10n-kf5/{}/messages/wikitolearn".format(lang), po_output]
    call(cmd)
    out_path = "{}/{}".format(common.tmp_output_po_dir, lang)
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    for po in expected_pos:
        source_po = "{}/{}".format(po_output, po)
        # Skip missing translations gracefully
        if not os.path.exists(source_po):
            continue
        shutil.copy2(source_po, "{}/{}/{}".format(common.tmp_output_po_dir, lang, po))
