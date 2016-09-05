# TemplateMessages

Ideally, you first have to extract the strings:

``./generate_pot.sh``

and then you simply compile the strings, ready to be imported

`python compile.py`

## If you need to add a new language

Add your language to `$LANG` in `generate_pot.sh` and in the `languages` variable in `compile.py`
