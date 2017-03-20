#!/bin/bash

LANG="devpt"
for L in $LANG; do
  cp ../guide/compiled/$L.mw dict.txt
  python2 pwb.py pagefromfile -begin:xxxxxxSEPARATORBEGINxxxxxx -end:xxxxxxSEPARATORENDxxxxxx -notitle -force -lang:$L -summary:Maintainance
done
