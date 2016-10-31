#!/bin/bash
if [ -n "$BASH_SOURCE" ] ; then
    cd $(dirname "$BASH_SOURCE")
elif [ $(basename -- "$0") = "svn-checkout.sh" ]; then
    cd $(dirname "$0")
else
    exit 1
fi

cd locales/

for lang in it de es fr pt sv ca
do
    echo "Update for "$lang"..."
    rm -Rf $lang
    svn co svn://anonsvn.kde.org/home/kde/trunk/l10n-kf5/$lang/messages/wikitolearn $lang
done
