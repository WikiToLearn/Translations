#!/usr/bin/env python3
import common

import git

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
