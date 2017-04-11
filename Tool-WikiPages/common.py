#!/usr/bin/env python3
import os
mypath = "{}/".format(os.path.dirname(os.path.realpath(__file__)))

work_dir = "{}workdir/".format(mypath)
if not os.path.exists(work_dir):
    os.makedirs(work_dir)

output_pot_dir = "{}pot/".format(work_dir)
if not os.path.exists(output_pot_dir):
    os.makedirs(output_pot_dir)

output_mw_dir = "{}mw/".format(work_dir)
if not os.path.exists(output_mw_dir):
    os.makedirs(output_mw_dir)

tmp_dir = "{}tmp/".format(work_dir)
if not os.path.exists(tmp_dir):
    os.makedirs(tmp_dir)

tmp_output_po_dir = "{}po/".format(tmp_dir)
if not os.path.exists(tmp_output_po_dir):
    os.makedirs(tmp_output_po_dir)

tmp_git_dir = "{}git/".format(tmp_dir)
if not os.path.exists(tmp_git_dir):
    os.makedirs(tmp_git_dir)

tmp_mw_files = "{}mw-in-files/".format(tmp_dir)
if not os.path.exists(tmp_mw_files):
    os.makedirs(tmp_mw_files)
    
kde_svn_dir = "{}kde_svn/".format(work_dir)
if not os.path.exists(kde_svn_dir):
    os.makedirs(kde_svn_dir)

languages = ["ca", "fr", "es", "de", "it", "pt", "sv", "uk"]

git_repo = "https://github.com/WikiToLearn/WikiPages-en"
