#!/usr/bin/env python3
import common

import git

print("Cloning git...")
try:
    repo_obj = git.Repo(common.tmp_git_dir)
except:
    git.Git().clone(common.git_repo, common.tmp_git_dir)
    repo_obj = git.Repo(common.tmp_git_dir)

repo_obj.git.add(".")
repo_obj.git.reset('--hard')
origin = repo_obj.remotes.origin
origin.pull(rebase=True)
