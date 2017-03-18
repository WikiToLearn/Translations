#!/bin/bash
if [ -n "$BASH_SOURCE" ] ; then
    cd $(dirname "$BASH_SOURCE")
elif [ $(basename -- "$0") = "svn-checkout.sh" ]; then
    cd $(dirname "$0")
else
    exit 1
fi

source config.sh

cd locales/

for lang in $LANGS
do
    echo "Checking out "$lang"..."
    rm -Rf $lang
    svn co $SVN_BASE/$lang/messages/wikitolearn $lang
done
