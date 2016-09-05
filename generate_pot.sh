#!/bin/bash

JSON="courseeditor"
INI="wtl-messages"
LANGS="it fr es"

mkdir -p locales

for J in $INI; do
  for L in $LANGS; do
    mkdir -p locales/$L locales/templates
    # Extract strings
    ini2po -P $J/en.ini locales/templates/$J.pot

    # Update translations
    pot2po -t locales/$L/$J.po locales/templates/$J.pot locales/$L/$J.po

    # Generate ini files
    po2ini -t $J/en.ini -i locales/$L/$J.po -o $J/$L.ini
  done
done

for J in $JSON; do
  for L in $LANGS; do
    mkdir -p locales/$L
    # Extract strings
    json2po -P $J/en.json locales/templates/$J.pot

    # Update translations
    pot2po -t locales/$L/$J.po locales/templates/$J.pot locales/$L/$J.po

    # Generate ini files
    po2json -t $J/en.json -i locales/$L/$J.po -o $J/$L.json
  done
done
