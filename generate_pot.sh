#!/bin/bash

LANGS="it fr"

for L in $LANGS; do

  mkdir -p $L po-$L
  # Extract strings
  ini2po -P ini templates

  # Update translations
  pot2po -t po-$L/ templates/ po-$L/

  # Generate ini files
  po2ini -t ini po-$L $L
done
