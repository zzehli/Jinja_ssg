# Jinja Generator
This is a python package that takes Jinja templates and output HTML files. Each input
files (templates, static files and config files) are contained in a folder that the program will read in as a directory. The program can render multiple templates at once. The config file is a list of json object that can specify variables in Jinaja templates, output directories and filenames.

## Install the package
To set up the static generator, first download the repo with `git clone`. Then create a python virtual environment with:
```
python3 -m venv env
```
Activate the environment:
```
source env/bin/activate
```
Install the package specified in the `pyproject.toml` file
```
python3 -m pip install jinjagenerator
```
## Run
Run with the example templates in the `hello_css` folder:
```
jinjagenerator hello_css
```