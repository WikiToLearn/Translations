#!/usr/bin/env python3

import wtl
import os
import sys
from subprocess import call

config = wtl.load_config(config_dir="/etc/translations/")
if config == None:
    print("Missing configuration file. Using defaults")
    config = {}

if not os.path.exists("/root/.ssh/"):
    os.makedirs("/root/.ssh/")
    os.chmod("/root/.ssh/", 0o600)

if 'ssh_private_key' in config:
    file_name_private = "/root/.ssh/{}".format(config['ssh_private_key']['file'])
    text_file_private = open(file_name_private, "w")
    text_file_private.write(config['ssh_private_key']['private'])
    text_file_private.close()
    os.chmod(file_name_private, 0o600)

    file_name_public = "/root/.ssh/{}.pub".format(config['ssh_private_key']['file'])
    text_file_public = open(file_name_public, "w")
    text_file_public.write(config['ssh_private_key']['public'])
    text_file_public.close()
    os.chmod(file_name_public, 0o640)

scripts = []
scripts.append("./01-download-from-git.py")
scripts.append("./02-make-pot.py")
scripts.append("./03-svn-ci.py")
scripts.append("./04-svn-co.py")
scripts.append("./05-make.py")

cmd = ["ssh","-o","BatchMode=yes","-o","StrictHostKeyChecking=no","svn.kde.org"]
ssh_svn_kde_org_exit_status = call(cmd)

if ssh_svn_kde_org_exit_status == 0:
    for dir_name in ["/srv/Tool-MW-json","/srv/Tool-WikiPages"]:
        try:
            print(dir_name)
            os.chdir(dir_name)
            for script in scripts:
                print(script)
                exit_status = call(script)
                if exit_status != 0:
                    raise Exception("{} {}".format(script, exit_status))
                    if 'gateway' in config:
                        wtl.send_notify({
                            "dir_name":dir_name,
                            "script":script,
                            "exit_status":exit_status
                            },"fail_script",config['gateway'])
        except Exception as e:
            print(e)
else:
    print("Failed to ssh into the svn.kde.org server")
    sys.exit(1)
