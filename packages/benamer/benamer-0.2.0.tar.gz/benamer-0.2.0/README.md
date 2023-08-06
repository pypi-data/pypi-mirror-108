# benamer
Bulk renamer with intuitive (no regex) options.

## Getting Started

In order to run this software, you need Python, it does not matter what version (provided it is updated enough), benamer will only run in Python 3.


## Installation

You can use pip in order to retrieve the package from PyPI: `sudo pip install benamer`

## Usage

`benamer.py [-h] [-d DIR] [-as RPREFX] [-ac START] [-rs RSUFX] [-ap RPREFX] [-rp RPREFX] [-fe FILTER_EXT] [-fp FILTER_PREFIX] [-fs FILTER_SUFFIX] [-st SUST] [-e EXT] [-rsp] [-s] [-p] [-jd] [-jf] [-u] [-l] [-v]`

Use `benamer -h` to get a complete list of available options. The availabe operations at the time of writing are:

-    -h, --help show this help message and exit
-    -d DIR, --dir DIR set the directory to work with
-    -as RPREFX, --add-suffix RPREFX add suffix to name
-    -ac START, --add-count START add count suffix to name
-    -rs RSUFX, --remove-suffix RSUFX remove suffix in name
-    -ap RPREFX, --add-prefix RPREFX add prefix to name
-    -rp RPREFX, --remove-prefix RPREFX remove prefix in name
-    -fe FILTER_EXT, --filter_by_ext FILTER_EXT filter by extension
-    -fp FILTER_PREFIX, --filter_by_prefix FILTER_PREFIX filter by prefix
-    -fs FILTER_SUFFIX, --filter_by_suffix FILTER_SUFFIX filter by suffix
-    -st SUST, --sust SUST substitute string
-    -e EXT, --ext EXT substitute extension
-    -rsp, --replace-spaces replace spaces in files with underscores
-    -s, --sort sort files before renaming
-    -p, --print do nothing, just show renamings
-    -jd, --directories rename only directories
-    -jf, --files rename only files
-    -u, --upper uppercase file names
-    -l, --lower lowercase file names
-    -v, --verbose describe what I am doing

## Examples

### Adding a prefix

    The following command will show the effects of adding a prefix to all files in the current directory. Nothing will be actually changed

    `benamer -p -ap file_`

    `benamer --print --add-prefix file_`

### Adding a prefix

    The following command will add a prefix to all files in the current directory.

    `benamer -ap file_`

    `benamer --add-prefix file_`
    
### Adding a count suffix

    The following command will add a suffix with a count to all files in the sub subdirectory.

    `benamer -ac 1 -d sub`

    `benamer --add-count 1 --directory sub`
    
### Replacing a part of the name

    The following command will replace all "er" with "ar" in all files of the current directory.

    `benamer -st er/ar`

    `benamer --sust er/ar`
    
### Replacing the whole file name

    The following command will replace the whole file name with "f" in all files of the current directory.

    `benamer -st /f`

    `benamer --sust /f`

### Remove a part of the file name

    The following command will remove the "er" part of the file name in all files of the current directory.

    `benamer -st er/`

    `benamer --sust er/`
