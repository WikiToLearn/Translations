#!/bin/bash

LANGS="it fr en es"

for L in $LANGS; do

  mkdir -p $L po-$L
  # Extract strings
  ini2po -P ini templates

  # Update translations
  pot2po -t po-$L/ templates/ po-$L/

  # Generate ini files
  po2ini -t ini po-$L $L

done

for L in $LANGS; do

  mkdir -p $L po-$L
  # Extract strings
  json2po -P json templates

  # Update translations
  pot2po -t po-$L/ templates/ po-$L/

  # Generate ini files
  po2json -t json po-$L $L

done
