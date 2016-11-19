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

import commons

print("Starting real work...")

for lang in ["en", "it", "es", "ca"]:
    for template_json_file in glob.glob("{}/*/i18n/en.json".format(commons.tmp_git_dir)):
        i18n_dir = os.path.dirname(os.path.realpath(template_json_file))
        po_file = "{}{}/{}.po".format(commons.output_po_dir,lang,template_json_file[len(commons.tmp_git_dir):-len("/i18n/en.json")])
        output_json_file = "{}/{}.json".format(i18n_dir,lang)
        cmd = ["po2json","-t",template_json_file,po_file,output_json_file]
        call(cmd)

    input_po_file = "{}{}/templatedata_dict.po".format(commons.output_po_dir, lang)
    output_json_file = "{}templatedata_dict_{}.json".format(commons.tmp_dir, lang)
    cmd = ["po2json", "-t", "{}templatedata_dict.json".format(
        commons.tmp_dir), input_po_file, output_json_file]
    call(cmd)
    template_name_map = {}

    json_filename_ve_template_ext_en = "{}/i18n/en.json".format(commons.git_repos["WikiToLearnVETemplates"]["path"])
    json_filename_ve_template_ext_lang = "{}/i18n/{}.json".format(commons.git_repos["WikiToLearnVETemplates"]["path"],lang)

    with open(json_filename_ve_template_ext_en) as json_file_en:
        json_file_en_data = json.load(json_file_en)
        json_file_en.close()

        with open(json_filename_ve_template_ext_lang) as json_file_lang:
            json_file_lang_data = json.load(json_file_lang)
            json_file_lang.close()

            en_begin = json_file_en_data['wtlvet-env-begin']
            en_end = json_file_en_data['wtlvet-env-end']
            lang_begin = json_file_lang_data['wtlvet-env-begin']
            lang_end = json_file_lang_data['wtlvet-env-end']
            for key in json_file_en_data:
                if key[0:len("wtlvet-env-name-")] == "wtlvet-env-name-":
                    template_name_map[en_begin + json_file_en_data[key]] = lang_begin +json_file_lang_data[key]
                    template_name_map[en_end + json_file_en_data[key]] = lang_end + json_file_lang_data[key]

    with open(output_json_file) as json_data_file:
        templatedata_dict = json.load(json_data_file)
        json_data_file.close()

        template_files_prefix = "{}/struct-wikipages/en/Template:".format(
            commons.git_repos["WikiToLearn"]['path'])
        template_files = glob.glob("{}*".format(template_files_prefix))
        for file_name in template_files:
            template_name = file_name[
                len(template_files_prefix):]
            with open(file_name) as input_template_file:
                new_template_name = None
                if template_name in template_name_map:
                    new_template_name = template_name_map[template_name]
                else:
                    new_template_name = template_name
                output_file = "{}/struct-wikipages/{}/Template:{}".format(
                    commons.git_repos["WikiToLearn"]['path'],lang,new_template_name)

                input_data = input_template_file.read()
                templatedata_matchs = re.findall(
                    "<templatedata>(.*?)</templatedata>", input_data, re.DOTALL)
                if len(templatedata_matchs) == 1:
                    templatedata_old = templatedata_matchs[0]
                    templatedata_new = "\n{}\n".format(json.dumps(templatedata_dict[template_name.lower()], sort_keys=True, indent=4, separators=(',', ': ')))
                    output_data = input_data.replace(templatedata_old,templatedata_new)
                else:
                    output_data = input_data
                input_template_file.close()
                with open(output_file, "wb") as out_file:
                    out_file.write(output_data.encode('utf8'))
                    out_file.close()
