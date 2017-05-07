#!/usr/bin/env python3
import common

import git
import glob
import os
from subprocess import call
import time
import datetime

output_repo = git.Repo.init(common.output_json_dir)

def output_snapshot():
    if len(output_repo.index.diff(None)) + len(output_repo.untracked_files) > 0:
        ts = time.time()
        output_repo.git.add('.')
        output_repo.index.commit("Snapshot {}".format(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))

output_snapshot()


#for lang_path in glob.glob("{}*".format(common.tmp_output_po_dir)):
    #lang_code = os.path.basename(lang_path)
for lang_code in common.languages:
    lang_path = "{}/{}".format(common.tmp_output_po_dir, lang_code)
    #print(lang_path)
    for po_file in glob.glob("{}/*".format(lang_path)):
        git_repo_label  = os.path.basename(po_file)[:-3]
        directory = "{}/{}".format(common.output_json_dir, git_repo_label)
        if not os.path.exists(directory):
            os.makedirs(directory)

        template_json_file = "{}i18n/en.json".format(common.git_repos[git_repo_label]['path'])
        output_json_file = "{}/{}.json".format(directory, lang_code)

        cmd = ["po2json","--progress=none","-t", template_json_file, po_file, output_json_file]
        call(cmd)

output_snapshot()
