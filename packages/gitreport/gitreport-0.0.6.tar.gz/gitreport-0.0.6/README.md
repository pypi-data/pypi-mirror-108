# Git Report

## Installation
```shell
# recommend to avoid cached
pip install git+https://github.com/peelz/git-report
# or install from repository 
pip install gitreport
```

## Parameters

```shell
usage: cli.py [-h] --projects PROJECTS [PROJECTS ...] --authors AUTHORS --month MONTH --output-file OUTPUT_FILE

optional arguments:
  -h, --help            show this help message and exit
  --projects PROJECTS [PROJECTS ...], -p PROJECTS [PROJECTS ...]
                        project dir can be list
  --authors AUTHORS     author pattern name use for filter
  --month MONTH, -m MONTH
                        number month of year
  --output-file OUTPUT_FILE, -o OUTPUT_FILE
                        end date format dd/mm/yyyy

```

## Example 
```shell
# Unix
gireport -p ~/path/to/project -m 5 -a peelz -o ./output.xlsx
# Window
gireport -p C:\path\to\project -m 5 -a peelz -o output.xlsx
```