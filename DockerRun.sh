#!/bin/bash
if test ! -f translations.yaml
then
  touch translations.yaml
fi

docker build -t wikitolearn/translations .
docker container run \
  --net=host \
  -v `pwd`/translations.yaml:/etc/translations/config.yaml \
  -v wikitolearn-translations-root:/root/ \
  -v wikitolearn-translations-mw-json:/srv/Tool-MW-json/workdir/ \
  -v wikitolearn-translations-wikiPages:/srv/Tool-WikiPages/workdir/ \
  -ti \
  --rm \
  wikitolearn/translations
