#!/usr/bin/env python3
import common

import os
import os.path
import git
import yaml
import json
import polib
import time
import datetime
from subprocess import call
from re import sub

try:
    repo_obj = git.Repo(common.tmp_git_dir)
except:
    raise

last_commit = repo_obj.git.log("-n1","--pretty=oneline").split(' ')[0]
print("Git last commit: {}".format(last_commit))


output_repo = git.Repo.init(common.output_pot_dir)

def output_snapshot():
    if len(output_repo.index.diff(None)) + len(output_repo.untracked_files) > 0:
        ts = time.time()
        output_repo.git.add('.')
        output_repo.index.commit("Snapshot {}".format(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))

output_snapshot()

# convert pages_id to a json that can be converted to pot
pages_id_file = "{}pages_id.yml".format(common.tmp_git_dir)
placeholder_dict = {}
reverse_placeholder_dict = {}
if os.path.isfile(pages_id_file):
    with open(pages_id_file) as data_file:
        reverse_placeholder_dict = yaml.load(data_file)
        for k in reverse_placeholder_dict:
            placeholder_dict[reverse_placeholder_dict[k]] = k
        data_file.close()

# convert pages_id to pot
with open("{}pages_id.json".format(common.tmp_dir), 'w') as outfile:
    json.dump(reverse_placeholder_dict, outfile)
    outfile.close()
    pot_lib_repo_key = "WikiPages-en"
    output_pot_file = "{}pages_id.pot".format(common.output_pot_dir)
    project_id_version = "{} {}".format(pot_lib_repo_key,last_commit)
    gen_pot = True
    if os.path.exists(output_pot_file):
        pot = polib.pofile(output_pot_file)
        gen_pot = pot.metadata['Project-Id-Version'] != project_id_version

    if gen_pot:
        cmd = ["json2po","-P","{}pages_id.json".format(common.tmp_dir),output_pot_file]
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

mw_en_pages_dir = "{}pages/".format(common.tmp_git_dir)
mw_en_pages_files = {}
mw_tmp_content = {}

for root, directories, filenames in os.walk(mw_en_pages_dir):
    for filename in filenames:
        file_full_name = os.path.join(root, filename)
        page_title = file_full_name[len(mw_en_pages_dir):-3]
        mw_en_pages_files[page_title] = file_full_name

# create a meta-wikipage with link replaced with the placeholder
for mw_page_title in mw_en_pages_files:
    mw_page_file = mw_en_pages_files[mw_page_title]
    with open(mw_page_file, 'r') as content_file:
        content = content_file.read()
        # this regex uses
        # https://www.mediawiki.org/wiki/Manual:$wgLegalTitleChars
        mw_tmp_content[mw_page_title]  = sub(r'\[{2}(.[^\[\]\{\}\|\#\<\>\%\+\?]+)(\|(.[^\[\]\{\}\|\#\<\>\%\+\?]+)){0,1}\]{2}', evaluate, content)

# writing meta-wikipage to file and creating pot file
old_cwd = os.getcwd()
os.chdir(common.tmp_mw_files)
for mw_page_title in mw_en_pages_files:
    mw_tmp_file = "{}.mw".format(placeholder_dict[mw_page_title])

    with open(mw_tmp_file, "wb") as out_file:
        out_file.write(mw_tmp_content[mw_page_title].encode('utf8'))
        out_file.close()

    pot_lib_repo_key = "WikiPages-en"
    output_pot_file = "{}{}.pot".format(common.output_pot_dir,placeholder_dict[mw_page_title])
    project_id_version = "{} {}".format(pot_lib_repo_key,last_commit)
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
