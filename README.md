# TemplateMessages

To generate, update, create the files to be exported, you simply need to:
```
./generate_pot.sh
```
## Translators!

This repository is experimental. Before translating anything, please ask on #translations if the file is ready and really not done.


## If you need to add a new language

Add your language to `$LANG` in `generate_pot.sh`.

# Writing the guide

To write the guide, have a look at the folder `guide`. You can edit files in `guide/en`
and add the chapter names in `en.ini`. The `ini` file has the following structure:

```
[messages]
filename=Readable name of the chapter
```
To insert links, use the following syntax anywhere in your file: `<ref:filename>`

The compiled files can then be uploaded to mediawiki using a configured `pywikibot-core`
by doing something like:
```
for L in "en it es"; do
  cp /path/to/guide/$L.mw dict.txt
  python pwb.py pagefromfile -start:xxxxxxSEPARATORBEGINxxxxxx -end:xxxxxxSEPARATORENDxxxxxx -notitle -force -lang:$L
done
```
