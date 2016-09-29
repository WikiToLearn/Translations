#!/bin/bash

LANG="it"
for L in $LANG; do
  cp ../guide/compiled/$L.mw dict.txt
  python pwb.py pagefromfile -start:xxxxxxSEPARATORBEGINxxxxxx -end:xxxxxxSEPARATORENDxxxxxx -notitle -force -lang:dev$L
done
