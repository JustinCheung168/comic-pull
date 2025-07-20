import os
import re
import json

def clean_filename(filename: str) -> str:
    # Get forbidden characters for the current OS
    if os.name == 'posix': # Mac
        forbidden = r':/'
    else:
        raise NotImplementedError()
    return re.sub(f'[{re.escape(forbidden)}]', '', filename)

def pretty_print(d: dict):
    print(json.dumps(d, indent=2))