#!/usr/bin/env python3

import wtl

config = wtl.load_config(config_dir="/etc/translations/")
if config == None:
    print("Missing configuration file. Using defaults")
    config = {}
