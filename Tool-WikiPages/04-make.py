#!/usr/bin/env python3
import common

import glob
import os
import os.path
import json
import git
import time
import datetime
from subprocess import call
from re import sub

output_repo = git.Repo.init(common.output_mw_dir)

def output_snapshot():
    if len(output_repo.index.diff(None)) + len(output_repo.untracked_files) > 0:
        ts = time.time()
        output_repo.git.add('.')
        output_repo.index.commit("Snapshot {}".format(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')))

output_snapshot()

for lang_path in glob.glob("{}*".format(common.tmp_output_po_dir)):
    lang_code = os.path.basename(lang_path)

    # read the templatedata_dict file
    input_po_file = "{}/pages_id.po".format(lang_path)
    output_json_file = "{}pages_id_{}.json".format(common.tmp_dir, lang_code)
    cmd = ["po2json", "-t", "{}pages_id.json".format(common.tmp_dir), input_po_file, output_json_file]
    call(cmd)


    en_placeholder_dict = {}
    en_reverse_placeholder_dict = {}
    with open("{}pages_id.json".format(common.tmp_dir)) as pages_id_file:
        en_reverse_placeholder_dict = json.load(pages_id_file)
        pages_id_file.close()
        for k in en_reverse_placeholder_dict:
            en_placeholder_dict[en_reverse_placeholder_dict[k]] = k

    lang_placeholder_dict = {}
    lang_reverse_placeholder_dict = {}
    with open(output_json_file) as pages_id_file:
        lang_reverse_placeholder_dict = json.load(pages_id_file)
        pages_id_file.close()
        for k in lang_reverse_placeholder_dict:
            lang_placeholder_dict[lang_reverse_placeholder_dict[k]] = k

    mw_en_pages_dir = "{}pages/".format(common.tmp_git_dir)
    mw_en_pages_files = {}

    for root, directories, filenames in os.walk(mw_en_pages_dir):
        for filename in filenames:
            file_full_name = os.path.join(root, filename)
            page_title = file_full_name[len(mw_en_pages_dir):-3]
            mw_en_pages_files[page_title] = file_full_name


    def evaluate(match):
        link_to = str(match.group(1))
        link_label = None
        placeholder = None

        if match.group(3) != None:
            link_label = str(match.group(3))

        reverse_placeholder = lang_reverse_placeholder_dict[link_to]

        return_val = "[[" + reverse_placeholder
        if link_label != None:
            return_val = return_val + "|" + link_label
        return_val = return_val + "]]"
        return return_val

    mw_lang_tmp_output_dir = common.tmp_dir + "mw-output/" + lang_code
    mw_lang_output_dir = common.output_mw_dir + lang_code
    for mw_en_title in mw_en_pages_files:
        mw_lang_tmp_output_file = "{}/{}.mw".format(mw_lang_tmp_output_dir, lang_reverse_placeholder_dict[en_placeholder_dict[mw_en_title]] ,".mw")
        mw_lang_tmp_output_file_dir = os.path.dirname(os.path.realpath(mw_lang_tmp_output_file))
        mw_lang_output_file = "{}/{}.mw".format(mw_lang_output_dir, lang_reverse_placeholder_dict[en_placeholder_dict[mw_en_title]] ,".mw")
        mw_lang_output_file_dir = os.path.dirname(os.path.realpath(mw_lang_output_file))


        pot_file = "{}/{}.mw".format(common.tmp_mw_files, en_placeholder_dict[mw_en_title])
        po_file = "{}{}/{}.po".format(common.tmp_output_po_dir, lang_code, en_placeholder_dict[mw_en_title])
        if not os.path.exists(mw_lang_tmp_output_file_dir):
            os.makedirs(mw_lang_tmp_output_file_dir)
        if not os.path.exists(mw_lang_output_file_dir):
            os.makedirs(mw_lang_output_file_dir)
        cmd = ["po2txt","-t",pot_file,po_file,mw_lang_tmp_output_file]
        call(cmd)


        with open(mw_lang_tmp_output_file, 'r') as content_file:
            content = content_file.read()
            # this regex uses
            # https://www.mediawiki.org/wiki/Manual:$wgLegalTitleChars
            new_content = sub(r'\[{2}(.[^\[\]\{\}\|\#\<\>\%\+\?]+)(\|(.[^\[\]\{\}\|\#\<\>\%\+\?]+)){0,1}\]{2}', evaluate, content)

            with open(mw_lang_output_file, "wb") as out_file:
                out_file.write(new_content.encode('utf8'))
                out_file.close()

    project_messages_tinput_po_file = "{}/project_messages.po".format(lang_path)
    project_messages_output_json_file = "{}project_messages_{}.json".format(common.tmp_dir, lang_code)
    cmd = ["po2json", "-t", "{}project_messages.json".format(common.tmp_dir), project_messages_tinput_po_file, project_messages_output_json_file]
    call(cmd)

    with open(project_messages_output_json_file) as project_messages_obj:
        with open("{}/Project:Messages".format(mw_lang_tmp_output_dir),'wb') as output_file:
            project_messages_data_k_v = json.load(project_messages_obj)
            for key in project_messages_data_k_v:
                output_file.write("<section begin={key} />{value}<section end={key} />\n".format(key=key,value=project_messages_data_k_v[key]).encode('utf8'))
            project_messages_obj.close()
            output_file.close()

output_snapshot()
