#!/bin/bash

set -e

for b in po2txt po2ini po2json
do
    if ! which $b &> /dev/null
    then
        echo "Missing "$b
        exit 1
    fi
done

source config.sh

echo "-----"
echo "Warnings of the following kind are expected and to be ignored:"
echo "po2txt: WARNING: No template at None. Skipping guide.po."
echo "po2txt: WARNING: No template at None. Skipping courseeditor.po."
echo "po2txt: WARNING: No template at None. Skipping skin.po."
echo "po2txt: WARNING: No template at None. Skipping wtl-messages.po."
echo "-----"

for J in $INI; do
  for L in $LANGS; do
    mkdir -p $J/mediawiki

    # Generate ini files
    po2ini --progress=none -t $J/en.ini -i locales/$L/$J.po -o $J/$L.ini
  done
done

for J in $JSON; do
  for L in $LANGS; do
    # Generate ini files
    po2json --progress=none -t $J/en.json -i locales/$L/$J.po -o $J/$L.json
    # po2json -i locales/$L/$J.po -o $J/$L.json
  done
done

for J in $TXT; do
  for L in $LANGS; do
    # Generate txt files
    po2txt --progress=none -t $J/en -i locales/$L -o $J/$L
    done
done
# We also want to compile files for english:
LANGS="$LANGS en"
for J in $TXT; do
  mkdir -p $J/compiled
  for L in $LANGS; do
    mkdir -p $J/compiled/$L
    python2 ./compile-guide.py $J/en.ini $J/$L.ini $L $J/compiled
    done
done

mkdir -p wtl-messages/mediawiki/
for L in $LANGS; do
  python2 ./compile.py wtl-messages/en.ini wtl-messages/$L.ini > wtl-messages/mediawiki/$L.mw
done
echo "-----"
echo "All done!"
