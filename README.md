# comic-pull

## Usage:

### First-time

You will need to install Python 3. (https://www.python.org/)
Confirm that you have it:
```bash
python3 --version
# Should see a version of Python print out.
```

Clone this repository.
```bash
git clone git@github.com:JustinCheung168/comic-pull.git
```

In your command line:
```bash
cd comic-pull
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Set the DEFAULT_LIBRARY_PATH variable in config.py to the path on your system that you want to download to by default.

### Pulling a comic

First:
```bash
source env/bin/activate
```

To download all of a comic:
```bash
./pull.py superman-smashes-the-klan-2019
```

#### More options

To download the 2nd through the 4th issue of a comic:
```bash
./pull.py absolute-green-lantern-2025 --first-issue 2 --last-issue 4
```

To download the first 3 issues of a comic:
```bash
./pull.py absolute-superman-2024 --last-issue 3
```

To download the 5th issue of a comic onward:
```bash
./pull.py supergirl-woman-of-tomorrow-2021 --first-issue 5
```

### Setting up a pull list

You can save a list of pull commands in `pull_list.sh`. 

To run all of them:
```bash
./pull_list.sh
```
