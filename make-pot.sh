#!/bin/bash
set -e
if test ! -d pot
then
  mkdir pot
fi
if test -d pot/wikitext
then
  rm -Rf pot/wikitext
fi

mkdir pot/wikitext
txt2po -P source_for_pot/wikitext/ pot/wikitext --flavour=mediawiki

for json_file in source_for_pot/*.json
do
  FILENAME=`basename $json_file`
  # the '.json' string is 5 chars, I can use a substring
  FILENAME_EXT_FREE=${FILENAME::-5}
  json2po -P $json_file pot/$FILENAME_EXT_FREE.pot
done

json2po -P placeholder_dict.json pot/placeholder_dict.pot
