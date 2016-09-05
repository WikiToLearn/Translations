#!/bin/bash

JSON="courseeditor"
INI="wtl-messages"
LANGS="it fr es"

# for J in $JSON; do
#   mkdir -p $J
#   json2po -P $J
#   for L in $LANGS; do
#     /$L
#   done
# done


for J in $INI; do
  for L in $LANGS; do
    mkdir -p locales/po-$L
    # Extract strings
    ini2po -P $J/en.ini locales/templates/$J.pot

    # Update translations
    pot2po -t locales/po-$L/$J.po locales/templates/$J.pot locales/po-$L/$J.po

    # Generate ini files
    po2ini -t $J/en.ini -i locales/po-$L/$J.po -o $J/$L.ini
  done
done

for J in $JSON; do
  for L in $LANGS; do
    mkdir -p locales/po-$L
    # Extract strings
    json2po -P $J/en.json locales/templates/$J.pot

    # Update translations
    pot2po -t locales/po-$L/$J.po locales/templates/$J.pot locales/po-$L/$J.po

    # Generate ini files
    po2json -t $J/en.json -i locales/po-$L/$J.po -o $J/$L.json
  done
done
