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

for J in $INI; do
  for L in $LANGS; do
    mkdir -p $J/mediawiki

    # Generate ini files
    po2ini -t $J/en.ini -i locales/$L/$J.po -o $J/$L.ini
  done
done

for J in $JSON; do
  for L in $LANGS; do
    # Generate ini files
    po2json -t $J/en.json -i locales/$L/$J.po -o $J/$L.json
    # po2json -i locales/$L/$J.po -o $J/$L.json
  done
done

for J in $TXT; do
  for L in $LANGS; do
    # Generate txt files
    po2txt -t $J/en -i locales/$L -o $J/$L
    done
done
# We also want to compile files for english:
LANGS="$LANGS en"
for J in $TXT; do
  mkdir -p $J/compiled
  for L in $LANGS; do
    python2 ./compile-guide.py $J/en.ini $J/$L.ini $L > $J/compiled/$L.mw
    done
done

mkdir -p wtl-messages/mediawiki/
for L in $LANGS; do
  python2 ./compile.py wtl-messages/en.ini wtl-messages/$L.ini > wtl-messages/mediawiki/$L.mw
done
