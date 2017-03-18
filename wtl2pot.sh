#!/bin/bash

if [ ! -d "locales/templates" ]; then
    echo "We couldn't find a working copy of the locales"
    echo "Please run either:"
    echo "  svn co svn://anonsvn.kde.org/home/kde/trunk/l10n-kf5/templates/messages/wikitolearn locales/templates"
    echo "  svn co svn+ssh://svn@svn.kde.org/home/kde/trunk/l10n-kf5/templates/messages/wikitolearn locales/templates"
    echo "depending on whether you have or not a KDE developer account"
    exit 1
fi

set -e

for b in txt2po ini2po json2po
do
    if ! which $b &> /dev/null
    then
        echo "Missing "$b
        exit 1
    fi
done

source config.sh

### Extract strings

for J in $TXT; do
  for L in $LANGS; do
    mkdir -p locales/$L locales/templates
    # Extract strings
    txt2po --progress=none -P $J/en locales/templates -x "*.ini" --flavour=mediawiki
    done
done

for J in $INI; do
  for L in $LANGS; do
    mkdir -p locales/$L locales/templates
    # Extract strings
    ini2po --progress=none -P $J/en.ini locales/templates/$J.pot

  done
done

for J in $JSON; do
  for L in $LANGS; do
    mkdir -p locales/$L
    # Extract strings
    json2po  --progress=none -P $J/en.json locales/templates/$J.pot
  done
done

echo "All done! New templates have been generated in locales/templates!"
