#!/bin/bash

# List of directories with en.json to translate
JSON="courseeditor skin"
# List of directories with ini files to translate
INI="wtl-messages guide"

TXT="guide"

LANGS="it fr es"

mkdir -p locales

### Extract strings

for J in $TXT; do
  for L in $LANGS; do
    mkdir -p locales/$L locales/templates
    # Extract strings
    txt2po -P $J/en locales/templates -x "*.ini" --flavour=mediawiki
    done
done

for J in $INI; do
  for L in $LANGS; do
    mkdir -p locales/$L locales/templates
    # Extract strings
    ini2po -P $J/en.ini locales/templates/$J.pot

  done
done

for J in $JSON; do
  for L in $LANGS; do
    mkdir -p locales/$L
    # Extract strings
    json2po -P $J/en.json locales/templates/$J.pot
  done
done


### Merge strings
for L in $LANGS; do
  cd locales/templates
  FILELIST="$(ls -1 *.pot)"
  cd -
  for FILE in $FILELIST; do
    # Update translations
    pot2po -t locales/$L/${FILE%.pot}.po locales/templates/$FILE locales/$L/${FILE%.pot}.po
  done
done

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
    ./compile-guide.py $J/en.ini $J/$L.ini $L > $J/compiled/$L.mw
    done
done


mkdir -p wtl-messages/mediawiki/
for L in $LANGS; do
  ./compile.py wtl-messages/en.ini wtl-messages/$L.ini > wtl-messages/mediawiki/$L.mw
done

