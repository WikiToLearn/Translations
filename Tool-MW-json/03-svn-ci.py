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


templates_dir = "{}/templates".format(common.kde_svn_dir)
if os.path.exists(templates_dir):
    shutil.rmtree(templates_dir)
cmd = ["svn","co", "svn+ssh://svn@svn.kde.org/home/kde/trunk/l10n-kf5/templates/messages/wikitolearn", templates_dir]
call(cmd)

for pot_file in glob.glob("{}*.pot".format(common.output_pot_dir)):
    shutil.copy2(pot_file, "{}/{}".format(templates_dir, os.path.basename(pot_file)))

old_cwd = os.getcwd()
os.chdir(templates_dir)

# Uncomment the following to add the files automatically
# NOTE: this behiavour is not suggested
# for pot_file in glob.glob("*.pot"):
#     cmd = ["svn","add",pot_file]
#     call(cmd)
cmd = ["svn","status"]
#cmd = ["svn","ci", "-m='Update templates'"]
call(cmd)

os.chdir(old_cwd)
