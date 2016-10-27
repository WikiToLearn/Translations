#!/bin/bash
if [ -n "$BASH_SOURCE" ] ; then
    cd $(dirname "$BASH_SOURCE")
elif [ $(basename -- "$0") = "download-en-json-for-skin-and-courseeditor.sh" ]; then
    cd $(dirname "$0")
else
    echo "Can't cd to the current working dir"
    exit 1
fi
cd skin
wget -N https://raw.githubusercontent.com/WikiToLearn/WikiToLearnSkin/master/i18n/en.json
cd ..
cd courseeditor
wget -N https://raw.githubusercontent.com/WikiToLearn/CourseEditor/master/i18n/en.json
cd ..
