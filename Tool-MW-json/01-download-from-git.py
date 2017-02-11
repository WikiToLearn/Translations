#!/usr/bin/env python3
import common

import git
import os
from subprocess import call
import polib
import time
import datetime

output_repo = git.Repo.init(common.output_pot_dir)

def output_snapshot():
    if len(output_repo.index.diff(None)) + len(output_repo.untracked_files) > 0:
        ts = time.time()
        output_repo.git.add('.')
        output_repo.index.commit("Snapshot {}".format(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))

output_snapshot()

for git_repo_label in common.git_repos:
    git_repo = common.git_repos[git_repo_label]
    print("Cloning git...")
    try:
        repo_obj = git.Repo(git_repo['path'])
    except:
        git.Git().clone(git_repo['url'], git_repo['path'])
        repo_obj = git.Repo(git_repo['path'])

    repo_obj.git.add(".")
    repo_obj.git.reset('--hard')
    origin = repo_obj.remotes.origin
    origin.pull(rebase=True)

    last_commit = repo_obj.git.log("-n1","--pretty=oneline").split(' ')[0]
    print("Git last commit: {}".format(last_commit))

    input_json_file = "{}/i18n/en.json".format(git_repo['path'])
    pot_lib_repo_key = None

    output_pot_file = "{}{}.pot".format(common.output_pot_dir,git_repo_label)
    project_id_version = "{} {}".format(git_repo_label,last_commit)
    gen_pot = True
    if os.path.exists(output_pot_file):
        pot = polib.pofile(output_pot_file)
        gen_pot = pot.metadata['Project-Id-Version'] != project_id_version

    if gen_pot:
        cmd = ["json2po","-P",input_json_file,output_pot_file]
        call(cmd)

        pot = polib.pofile(output_pot_file)
        pot.metadata['Project-Id-Version'] = project_id_version
        pot.save(output_pot_file)

output_snapshot()
