# TemplateMessages

Ideally, you first have to extract the strings:

``./generate_pot.sh``

and then you simply compile the strings, ready to be imported

`python compile.py`

## If you need to add a new language

Add your language to `$LANG` in `generate_pot.sh` and in the `languages` variable in `compile.py`

# Writing the guide

To write the guide, have a look at the folder `guide`. You can edit files in `guide/en`
and add the chapter names in `en.ini`. The `ini` file has the following structure:

```
[messages]
filename=Readable name of the chapter
```

The compiled files can then be uploaded to mediawiki using a configured `pywikibot-core`
by doing something like:
```
for L in "en it es"; do
  cp /path/to/guide/$L.mw dict.txt
  python pwb.py pagefromfile -start:xxxxxxSEPARATORBEGINxxxxxx -end:xxxxxxSEPARATORENDxxxxxx -notitle -force -lang:$L
done
```
