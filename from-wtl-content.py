#!/usr/bin/env python3
import requests
import os
import os.path
import git
import sys
import mwapiutils
from re import sub
from pprint import pprint
import json

# this is the file where is stored the key-value for filenames (mainly MediaWiki pages titles)
source_for_pot_placeholder_dict_file = "placeholder_dict.json"

# this is the directory where the content will be downloaded
download_dir = "input/"
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# this is the directory there wikipages will be downloaded
wikipages_download_dir = "{}wikipages/".format(download_dir)
if not os.path.exists(wikipages_download_dir):
    os.makedirs(wikipages_download_dir)

# this is the directory where the content is placed after the pre-parsing
source_for_pot = "source_for_pot/"
if not os.path.exists(source_for_pot):
    os.makedirs(source_for_pot)
# this is the directory where the wikitext is placed when ready to be templated as pot
source_for_pot_wikitext = "{}wikitext/".format(source_for_pot)
if not os.path.exists(source_for_pot_wikitext):
    os.makedirs(source_for_pot_wikitext)

# this dic is [<mnemonic name>] = <en.json url>
i18n_json_files_urls = {}
i18n_json_files_urls[
    'WikiToLearnSkin'] = "https://raw.githubusercontent.com/WikiToLearn/WikiToLearnSkin/master/i18n/en.json"
i18n_json_files_urls[
    'CourseEditor'] = "https://raw.githubusercontent.com/WikiToLearn/CourseEditor/master/i18n/en.json"
i18n_json_files_urls[
    'WikiToLearnVETemplates'] = "https://raw.githubusercontent.com/WikiToLearn/WikiToLearnVETemplates/master/i18n/en.json"

# this is the location of the main repo
wikitolearn_main_git_repo = "https://github.com/WikiToLearn/WikiToLearn"
wikitolearn_main_git_repo_download_dir = "{}/WikiToLearn".format(download_dir)

# api entrypoint used to download pages
root_website_api_for_wikipages = "https://en.wikitolearn.org/api.php"

# list pages to be downloaded
root_page_for_user_manual = "Manual"
single_pages_title_to_be_downloaded = [
    'About',
    'Hacker',
    'Student',
    'Teacher',
    'Project:Messages'
]

print("List page for: Manual")
guide_pages_title = mwapiutils.list_page_and_subpages(
    root_website_api_for_wikipages, root_page_for_user_manual)
for page_title in guide_pages_title:
    single_pages_title_to_be_downloaded.append(page_title)

for page_title in single_pages_title_to_be_downloaded:
    print("Download for: {}".format(page_title))
    mwapiutils.download_wikipage(
        root_website_api_for_wikipages, page_title, wikipages_download_dir)

print("Download for: Json")
for json_name in i18n_json_files_urls:
    response = requests.get(i18n_json_files_urls[json_name])
    text_file = open("{}{}.json".format(download_dir, json_name), "wb")
    text_file.write(response.content)
    text_file.close()

print("Download for: Git repo")
if not os.path.exists(wikitolearn_main_git_repo_download_dir):
    git.Git().clone(wikitolearn_main_git_repo, wikitolearn_main_git_repo_download_dir)
else:
    repo = git.Repo(wikitolearn_main_git_repo_download_dir)
    repo.git.add(".")
    repo.git.reset('--hard')
    origin = repo.remotes.origin
    origin.pull(rebase=True)

print("Addidional steps...")
mw_pages_files = []
for root, directories, filenames in os.walk(wikipages_download_dir):
    for filename in filenames:
        mw_pages_files.append(os.path.join(root, filename))

for mw_page_file in mw_pages_files:
    if mw_page_file not in ["{}{}.mw".format(wikipages_download_dir, mw_page_title) for mw_page_title in single_pages_title_to_be_downloaded]:
        os.remove(mw_page_file)

placeholder_dict = {}
if os.path.isfile(source_for_pot_placeholder_dict_file):
    with open(source_for_pot_placeholder_dict_file) as data_file:
        placeholder_dict = json.load(data_file)
        data_file.close()

def get_placeholder(link):
    if link not in placeholder_dict:
        placeholder = None
        retry_counter = 0
        while placeholder == None or placeholder in placeholder_dict.values():
            placeholder = "FILE_{}".format(
                len(placeholder_dict) + retry_counter)
            retry_counter = retry_counter + 1

        placeholder_dict[link] = placeholder

    return placeholder_dict[link]

new_file_content = {}


def evaluate(match):
    link_to = str(match.group(1))
    link_label = None
    placeholder = None

    if match.group(3) != None:
        link_label = str(match.group(3))

    placeholder = get_placeholder(link_to)

    return_val = "[[" + placeholder
    if link_label != None:
        return_val = return_val + "|" + link_label
    return_val = return_val + "]]"
    return return_val

for mw_page_file in mw_pages_files:
    get_placeholder(mw_page_file[len(wikipages_download_dir):-3])

for mw_page_file in mw_pages_files:
    with open(mw_page_file, 'r') as content_file:
        content = content_file.read()
        # this regex uses
        # https://www.mediawiki.org/wiki/Manual:$wgLegalTitleChars
        new_file_content[mw_page_file[len(wikipages_download_dir):-3]] = sub(
            r'\[{2}(.[^\[\]\{\}\|\#\<\>\%\+\?]+)(\|(.[^\[\]\{\}\|\#\<\>\%\+\?]+)){0,1}\]{2}', evaluate, content)

for k in placeholder_dict:
    if k in new_file_content:
        output_filename = "{}{}.mw".format(
            source_for_pot_wikitext, placeholder_dict[k])
        text_file = open(output_filename, "wb")
        text_file.write(new_file_content[k].encode('utf8'))
        text_file.close()

with open(source_for_pot_placeholder_dict_file, 'w') as outfile:
    json.dump(placeholder_dict, outfile, sort_keys=True, indent=4)
    outfile.close()
