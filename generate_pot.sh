#!/bin/bash

JSON="courseeditor"
LANGS="it fr en es"

# for J in $JSON; do
#   mkdir -p $J
#   json2po -P $J
#   for L in $LANGS; do
#     /$L
#   done
# done

for L in $LANGS; do

  mkdir -p locales/$L locales/po-$L locales/templates
  # Extract strings
  ini2po -P ini locales/templates

  # Update translations
  pot2po -t locales/po-$L/ locales/templates/ locales/po-$L/

  # Generate ini files
  po2ini -t ini locales/po-$L locales/$L

done

for L in $LANGS; do

  mkdir -p locales/$L locales/po-$L
  # Extract strings
  json2po -P json locales/templates

  # Update translations
  pot2po -t locales/po-$L/ locales/templates/ locales/po-$L/

  # Generate ini files
  po2json -t json locales/po-$L locales/$L

done
