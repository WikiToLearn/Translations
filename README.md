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
* All templates listed in `WikiToLearn/struct-wikipages/en`

It also downloads the `en.json` file (MediaWiki translation format) for:
* WikiToLearnSkin
* CourseEditor
* WikiToLearnVETemplates

After the `./from-wtl-content.py` you have to run `./make-pot.sh` to create actual pot files in the `./pot/` directory using as source the `./source_for_pot/` directory
