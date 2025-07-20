import os
import re
import json

from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests

def pretty_print(obj):
    """Pretty-print the JSON-serializable object `obj`."""
    print(json.dumps(obj, indent=2))

def clean_filename(filename: str) -> str:
    """Remove characters which are forbidden in `filename` for the current OS."""
    if os.name == 'posix': # Mac
        forbidden = r':/'
    else:
        raise NotImplementedError()
    return re.sub(f'[{re.escape(forbidden)}]', '', filename)

def download_file_from_link(url: str, dir_out: str, headers: dict):
    """Download from a file `url`."""
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        os.makedirs(dir_out, exist_ok=True)

        parsed = urlparse(url)
        filename_out = os.path.basename(parsed.path)

        path_out = os.path.join(dir_out, filename_out)
        with open(path_out, "wb") as f:
            f.write(response.content)
    else:
        print(f"Failed to fetch from {url}; did not write {filename_out}.")

def get_soup_from_link(url: str, headers: dict):
    """Get parsed HTML content from a webpage `url`."""
    response = requests.get(url=url, headers=headers)
    html = response.text
    code = response.status_code
    if code != 200:
        raise Exception(f"Got status code {code}")
    soup = BeautifulSoup(html, "html.parser")
    return soup
