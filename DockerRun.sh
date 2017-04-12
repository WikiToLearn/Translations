#!/bin/bash
docker build -t wikitolearn/translations .
docker container run \
  -ti \
  --rm \
  wikitolearn/translations
