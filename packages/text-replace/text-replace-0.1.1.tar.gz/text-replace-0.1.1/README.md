# Text Replace
## Description
A python package that traverse files based on some regex pattern to select certain files and then update the text in these files using regex.

## Install
PyPI: `pip install text-replace`
Source: `git clone https://github.com/Salaah01/text-replace.git`

## Usage
```
usage: python -m text_replace [-h] [-d ROOT_DIR] [-f FILE_PATTERN] [-s] [-r] [-t TEXT_PATTERN] [-m {default,relative-url-prefixer}] [-n NEW_TEXT]

Search through files and replace text.

optional arguments:
  -h, --help            show this help message and exit
  -d ROOT_DIR, --root-dir ROOT_DIR
                        Root directory.
  -f FILE_PATTERN, --file-pattern FILE_PATTERN
                        Regex pattern to follow when searching for files.
  -s, --skip-check      Show a list of files that will potentially be changed before proceeding.
  -r, --recursive       Recursively search for files?
  -t TEXT_PATTERN, --text-pattern TEXT_PATTERN
                        Regex pattern for searching for text to replace.
  -m {default,relative-url-prefixer}, --mode {default,relative-url-prefixer}
  -n NEW_TEXT, --new-text NEW_TEXT
                        Next text to replace the old text with.
```
## Presets
Preset exist within `test_replace/presets` and they include helpful shortcuts
to perform certain replaces. These include:

* ### `relative_url_prefixer`
  Updates the relative URLs in your files to include a prefix.
  e.g: /about becomes iamsalaah.com/about where the prefix set is iamsalaah.com.
