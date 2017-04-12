import os

# directory where the script is
mypath = "{}/".format(os.path.dirname(os.path.realpath(__file__)))

# directory where all pot file must to be
output_pot_dir = "{}pot/".format(mypath)
if not os.path.exists(output_pot_dir):
    os.makedirs(output_pot_dir)

# directory where all po file must to be
output_po_dir = "{}po/".format(mypath)
if not os.path.exists(output_po_dir):
    os.makedirs(output_po_dir)

# directory where place tmp files
tmp_dir = "{}tmp/".format(mypath)
if not os.path.exists(tmp_dir):
    os.makedirs(tmp_dir)

tmp_git_dir = "{}git-repos/".format(tmp_dir)
if not os.path.exists(tmp_git_dir):
    os.makedirs(tmp_git_dir)


tmp_mw_files = "{}mw-files/".format(tmp_dir)
if not os.path.exists(tmp_mw_files):
    os.makedirs(tmp_mw_files)

# dict for all git repos used
git_repos = {}
git_repos["WikiToLearn"] = {
    "url": "https://github.com/WikiToLearn/WikiToLearn",
    "path": "{}WikiToLearn/".format(tmp_git_dir)
}
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
git_repos["WikiPages-en"] = {
    "url": "https://github.com/WikiToLearn/WikiPages-en",
    "path": "{}WikiPages-en/".format(tmp_git_dir)
}
git_repos["SpeechToText"] = {
    "url":"https://github.com/WikiToLearn/SpeechToText",
    "path":"{}SpeechToText/".format(tmp_git_dir)
}
