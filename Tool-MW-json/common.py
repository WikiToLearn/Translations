#!/usr/bin/env python3
import os
mypath = "{}/".format(os.path.dirname(os.path.realpath(__file__)))

work_dir = "{}workdir/".format(mypath)
if not os.path.exists(work_dir):
    os.makedirs(work_dir)

output_pot_dir = "{}pot/".format(work_dir)
if not os.path.exists(output_pot_dir):
    os.makedirs(output_pot_dir)

output_json_dir = "{}json/".format(work_dir)
if not os.path.exists(output_json_dir):
    os.makedirs(output_json_dir)

tmp_dir = "{}tmp/".format(work_dir)
if not os.path.exists(tmp_dir):
    os.makedirs(tmp_dir)

tmp_output_po_dir = "{}po/".format(tmp_dir)
if not os.path.exists(tmp_output_po_dir):
    os.makedirs(tmp_output_po_dir)

tmp_git_dir = "{}git/".format(tmp_dir)
if not os.path.exists(tmp_git_dir):
    os.makedirs(tmp_git_dir)

kde_svn_dir = "{}kde_svn/".format(work_dir)
if not os.path.exists(kde_svn_dir):
    os.makedirs(kde_svn_dir)

languages = ["ca", "fr", "es", "de", "it", "pt", "sv", "uk"]

git_repos = {}
git_repos["WikiToLearnSkin"] = {
    "url": "https://github.com/WikiToLearn/WikiToLearnSkin",
    "path": "{}WikiToLearnSkin/".format(tmp_git_dir)
}
git_repos["WikiToLearnVETemplates"] = {
    "url": "https://github.com/WikiToLearn/WikiToLearnVETemplates",
    "path": "{}WikiToLearnVETemplates/".format(tmp_git_dir)
}
git_repos["CourseEditor"] = {
    "url": "https://github.com/WikiToLearn/CourseEditor",
    "path": "{}CourseEditor/".format(tmp_git_dir)
}
git_repos["SpeechToText"] = {
    "url":"https://github.com/WikiToLearn/SpeechToText",
    "path":"{}SpeechToText/".format(tmp_git_dir)
}
