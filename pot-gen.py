#!/usr/bin/env python3
import os
import os.path
import git
import glob
import re
import json
import yaml
from re import sub
from subprocess import call
import polib
import time
import datetime

# directory where the script is
mypath = "{}/".format(os.path.dirname(os.path.realpath(__file__)))

# directory where all pot file must to be
output_pot_dir = "{}pot/".format(mypath)
if not os.path.exists(output_pot_dir):
    os.makedirs(output_pot_dir)

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
    "url":"https://github.com/WikiToLearn/WikiToLearn",
    "path":"{}WikiToLearn/".format(tmp_git_dir)
}
git_repos["WikiToLearnSkin"] = {
    "url":"https://github.com/WikiToLearn/WikiToLearnSkin",
    "path":"{}WikiToLearnSkin/".format(tmp_git_dir)
}
git_repos["WikiToLearnVETemplates"] = {
    "url":"https://github.com/WikiToLearn/WikiToLearnVETemplates",
    "path":"{}WikiToLearnVETemplates/".format(tmp_git_dir)
}
git_repos["CourseEditor"] = {
    "url":"https://github.com/WikiToLearn/CourseEditor",
    "path":"{}CourseEditor/".format(tmp_git_dir)
}
git_repos["WikiPages-en"] = {
    "url":"https://github.com/WikiToLearn/WikiPages-en",
    "path":"{}WikiPages-en/".format(tmp_git_dir)
}

# GIT repo is used to version pot files
output_repo = git.Repo.init(output_pot_dir)

def output_snapshot():
    if len(output_repo.index.diff(None)) + len(output_repo.untracked_files) > 0:
        ts = time.time()
        output_repo.git.add('.')
        output_repo.index.commit("Snapshot {}".format(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))

output_snapshot()

# this procedure downloads all git repos to last commit
print("Download for: Git repo")
for key in git_repos:
    print("Cloning {}".format(key))
    local_dir = git_repos[key]['path']
    repo = git_repos[key]['url']
    if not os.path.exists(local_dir):
        git.Git().clone(repo, local_dir)
    repo_obj = git.Repo(local_dir)

    git_repos[key]['last_commit'] = repo_obj.git.log("-n1","--pretty=oneline").split(' ')[0]

    repo_obj.git.add(".")
    repo_obj.git.reset('--hard')
    origin = repo_obj.remotes.origin
    origin.pull(rebase=True)

print("Starting real work...")
# extracting templatedata json data and build a dict to translate all templatedata in one file
templatedata_dict = {}
template_files_prefix = "{}/struct-wikipages/en/Template:".format(git_repos["WikiToLearn"]['path'])
template_files = glob.glob("{}*".format(template_files_prefix))
for file_name in template_files:
    template_name = file_name[
        len(template_files_prefix):]
    with open(file_name) as data_file:
        templatedata_matchs=re.findall("<templatedata>(.*?)</templatedata>",data_file.read(),re.DOTALL)
        if len(templatedata_matchs) == 1:
            templatedata = json.loads(templatedata_matchs[0])
            del templatedata['params']['title']['type']
            templatedata_dict[template_name.lower()] = templatedata
        data_file.close()

# write templatedata_dict.json file and make the templatedata_dict.pot
with open("{}templatedata_dict.json".format(tmp_git_dir), 'w') as outfile:
    json.dump(templatedata_dict, outfile)
    outfile.close()

    pot_lib_repo_key = "WikiToLearn"
    output_pot_file = "{}templatedata_dict.pot".format(output_pot_dir)
    project_id_version = "{} {}".format(pot_lib_repo_key,git_repos[pot_lib_repo_key]['last_commit'])
    gen_pot = True
    if os.path.exists(output_pot_file):
        pot = polib.pofile(output_pot_file)
        gen_pot = pot.metadata['Project-Id-Version'] != project_id_version

    if gen_pot:
        cmd = ["json2po","-P","{}templatedata_dict.json".format(tmp_git_dir),output_pot_file]
        call(cmd)
        pot = polib.pofile(output_pot_file)
        pot.metadata['Project-Id-Version'] = project_id_version
        pot.save(output_pot_file)

# make pot file from en.json
for input_json_file in glob.glob("{}/*/i18n/en.json".format(tmp_git_dir)):
    pot_lib_repo_key = None
    for repo_check_key in git_repos:
        if input_json_file.startswith(git_repos[repo_check_key]['path']):
            pot_lib_repo_key = repo_check_key
    output_pot_file = "{}{}.pot".format(output_pot_dir,input_json_file[len(tmp_git_dir):-len("/i18n/en.json")])
    project_id_version = "{} {}".format(pot_lib_repo_key,git_repos[pot_lib_repo_key]['last_commit'])
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

# convert pages_id to a json that can be converted to pot
pages_id_file = "{}pages_id.yml".format(git_repos['WikiPages-en']['path'])
placeholder_dict = {}
if os.path.isfile(pages_id_file):
    with open(pages_id_file) as data_file:
        reverse_placeholder_dict = yaml.load(data_file)
        for k in reverse_placeholder_dict:
            placeholder_dict[reverse_placeholder_dict[k]] = k
        data_file.close()

# convert pages_id to pot
with open("{}pages_id.json".format(tmp_git_dir), 'w') as outfile:
    json.dump(placeholder_dict, outfile)
    outfile.close()
    pot_lib_repo_key = "WikiPages-en"
    output_pot_file = "{}pages_id.pot".format(output_pot_dir)
    project_id_version = "{} {}".format(pot_lib_repo_key,git_repos[pot_lib_repo_key]['last_commit'])
    gen_pot = True
    if os.path.exists(output_pot_file):
        pot = polib.pofile(output_pot_file)
        gen_pot = pot.metadata['Project-Id-Version'] != project_id_version

    if gen_pot:
        cmd = ["json2po","-P","{}pages_id.json".format(tmp_git_dir),output_pot_file]
        call(cmd)

        pot = polib.pofile(output_pot_file)
        pot.metadata['Project-Id-Version'] = project_id_version
        pot.save(output_pot_file)

def evaluate(match):
    link_to = str(match.group(1))
    link_label = None
    placeholder = None

    if match.group(3) != None:
        link_label = str(match.group(3))

    placeholder = placeholder_dict[link_to]

    return_val = "[[" + placeholder
    if link_label != None:
        return_val = return_val + "|" + link_label
    return_val = return_val + "]]"
    return return_val

mw_pages_dir = "{}pages/".format(git_repos["WikiPages-en"]['path'])
mw_pages_files = {}
mw_tmp_content = {}

for root, directories, filenames in os.walk(mw_pages_dir):
    for filename in filenames:
        file_full_name = os.path.join(root, filename)
        page_title = file_full_name[len(mw_pages_dir):-3]
        mw_pages_files[page_title] = file_full_name

# create a meta-wikipage with link replaced with the placeholder
for mw_page_title in mw_pages_files:
    mw_page_file = mw_pages_files[mw_page_title]
    with open(mw_page_file, 'r') as content_file:
        content = content_file.read()
        # this regex uses
        # https://www.mediawiki.org/wiki/Manual:$wgLegalTitleChars
        mw_tmp_content[mw_page_title]  = sub(r'\[{2}(.[^\[\]\{\}\|\#\<\>\%\+\?]+)(\|(.[^\[\]\{\}\|\#\<\>\%\+\?]+)){0,1}\]{2}', evaluate, content)

# writing meta-wikipage to file and creating pot file
old_cwd = os.getcwd()
os.chdir(tmp_mw_files)
for mw_page_title in mw_pages_files:
    mw_tmp_file = "{}.mw".format(placeholder_dict[mw_page_title])

    with open(mw_tmp_file, "wb") as out_file:
        out_file.write(mw_tmp_content[mw_page_title].encode('utf8'))
        out_file.close()

    pot_lib_repo_key = "WikiPages-en"
    output_pot_file = "{}{}.pot".format(output_pot_dir,placeholder_dict[mw_page_title])
    project_id_version = "{} {}".format(pot_lib_repo_key,git_repos[pot_lib_repo_key]['last_commit'])
    gen_pot = True
    if os.path.exists(output_pot_file):
        pot = polib.pofile(output_pot_file)
        gen_pot = pot.metadata['Project-Id-Version'] != project_id_version

    if gen_pot:
        cmd = ["txt2po","--flavour=mediawiki","-P",mw_tmp_file,output_pot_file]
        call(cmd)
        pot = polib.pofile(output_pot_file)
        pot.metadata['Project-Id-Version'] = project_id_version
        pot.save(output_pot_file)

os.chdir(old_cwd)

output_snapshot()
