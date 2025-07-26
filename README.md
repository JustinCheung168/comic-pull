# comic-pull

`comic-pull` is a command-line tool for downloading comic book issues from supported online sources into your own organized library.

## Features
- Download all or a range of issues for a comic series
- Supports multiple comic sources (see `src/sources.py` for supported sites)
- Maintains a local library and avoids duplicate downloads
- Batch download via a pull list script

## Quick Start

### 1. Prerequisites
- A recent version of Python 3 ([Download Python](https://www.python.org/))
- `git` (for cloning the repository)

Check your Python version:
```bash
python3 --version
# Should see a version of Python print out.
```

### 2. Installation
Clone this repository and set up a virtual environment:
```bash
git clone git@github.com:JustinCheung168/comic-pull.git
cd comic-pull
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### 3. Configuration
Edit `config.py` and set the `DEFAULT_LIBRARY_PATH` variable to the directory where you want comics to be saved by default.

You can leave `DEFAULT_SOURCE_URL` alone - this is the default website you will download comics from.

## Usage

### Activating the Environment
Before running any commands, activate your Python virtual environment:
```bash
source env/bin/activate
```

### Downloading Comics
The following command will download all issues of a comic:
```bash
./pull.py superman-smashes-the-klan-2019
```

The format used for comic names depends on the format used by the website defined in `DEFAULT_SOURCE_URL`.
<p align="center">
  <img src="docs/example_url.png" alt="Example comic URL format" width="500"/>
</p>

#### More options
You can use the `--first-issue` and `--last-issue` flags to specify the range of comic issues you want to download.

For example, if you only want the 2nd through the 4th issues:
```bash
./pull.py absolute-green-lantern-2025 --first-issue 2 --last-issue 4
```

To download all issues up to the 3rd issue:
```bash
./pull.py absolute-superman-2024 --last-issue 3
```

To download all issues starting from the 5th issue onward:
```bash
./pull.py supergirl-woman-of-tomorrow-2021 --first-issue 5
```

#### Custom Library Path
You can use `--library-path` to download a comic to a different location on your computer other than `DEFAULT_LIBRARY_PATH`, in case you want to keep multiple collections:
```bash
./pull.py <comic-name> --library-path /path/to/your/comics
```

#### Custom Source URL
If you want to specify a different source to download comics from (see supported sources in `src/sources.py`):
```bash
./pull.py <comic-name> --source-url xoxocomic.com
```

### Batch Download with a Pull List
You can save a list of pull commands in `pull_list.sh` (one per line):
```bash
./pull.py superman-smashes-the-klan-2019
./pull.py supergirl-woman-of-tomorrow-2021
```
Run all of them at once:
```bash
./pull_list.sh
```

This is an easy way to keep up with the latest issues of your favorite comics. Simply rerun `./pull_list.sh` every so often, and any new available issues will be downloaded.

Issues which you already have will not be redownloaded.

## Project Structure

```
comic-pull/
├── config.py              # Configuration (set your DEFAULT_LIBRARY_PATH here)
├── pull.py                # Main script to pull comics
├── pull_list.sh           # Example batch script for multiple pulls
├── src/
│   ├── library.py         # Library management
│   ├── misc.py            # Utility functions
│   ├── puller.py          # Puller logic
│   ├── sources.py         # Source site logic
│   └── __init__.py        # Package marker
└── ...
```
