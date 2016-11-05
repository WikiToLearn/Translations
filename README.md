## This is a WIP for a new Translation system

To use this you have to install python3 and `pip`.

You have to install `pip install -r requirements.txt`

the script `./from-wtl-content.py` downloads data from the production system.

Is downloaded:
* `Manual` and all subpages
* `About`
* `Hacker`
* `Student`
* `Teacher`
* `Project:Messages`

Needs to be added (this will require some trick):
* All templates listed in `WikiToLearn/struct-wikipages/en`

It also downloads the `en.json` file (MediaWiki translation format) for:
* WikiToLearnSkin
* CourseEditor
* WikiToLearnVETemplates
