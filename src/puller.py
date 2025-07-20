import os
from urllib.parse import urlparse
from typing import Optional

from bs4 import BeautifulSoup
import requests
from tqdm import tqdm

import src.misc

HEADERS = {
    "User-Agent": f"Mozilla/5.0 (compatible; placeholder/placeholder)"
}

READ_COMICS_ONLINE = "https://readcomicsonline.ru/comic/"

class Puller:
    @staticmethod
    def get_soup_from_url(url: str):
        response = requests.get(url=url, headers=HEADERS)
        html = response.text
        code = response.status_code
        if code != 200:
            raise Exception(f"Got status code {code}")
        soup = BeautifulSoup(html, "html.parser")
        return soup

    @staticmethod
    def get_issue_names_and_links(volume_soup: BeautifulSoup):
        results = {}
        for h5 in volume_soup.find_all('h5', class_='chapter-title-rtl'):
            a_tag = h5.find('a')
            if a_tag and a_tag.get('href'):
                title = src.misc.clean_filename(h5.get_text(strip=True))
                url = a_tag['href']
                results[title] = url
        return results

    @staticmethod
    def get_page_names_and_links(issue_soup: BeautifulSoup):
        results = {}
        div = issue_soup.find('div', id='all')
        assert div
        for img in div.find_all('img'):
            name = src.misc.clean_filename(img.get('alt'))
            url = img.get('data-src').strip()
            results[name] = url
        return results

    @staticmethod
    def download_content_from_link(url, dir_out):
        response = requests.get(url)
        if response.status_code == 200:
            os.makedirs(dir_out, exist_ok=True)

            parsed = urlparse(url)
            filename_out = os.path.basename(parsed.path)

            path_out = os.path.join(dir_out, filename_out)
            with open(path_out, "wb") as f:
                f.write(response.content)
        else:
            print(f"Failed to fetch from {url}; did not write {filename_out}.")

    @staticmethod
    def pull(book_name: str, library: str, first_issue: int = 1, last_issue: Optional[int] = None):
        assert first_issue >= 1, "First issue should be specified as 1 or higher."
        if last_issue is not None:
            assert last_issue >= 1, "Last issue should be specified as 1 or higher."

        print(f"Checking online for available issues.")
        book_soup = Puller.get_soup_from_url(READ_COMICS_ONLINE + book_name)
        issue_links = Puller.get_issue_names_and_links(book_soup)
        issue_names = list(reversed(list(issue_links.keys())))

        if (last_issue is None) or (last_issue > len(issue_names)):
            last_issue = len(issue_names)
        issue_indices_to_check = range(first_issue-1, last_issue)

        # Figure out which issues we do not have.
        issue_names_to_pull = []
        for i in issue_indices_to_check:
            issue_name = issue_names[i]
            issue_dir = os.path.join(library, book_name, issue_name)

            if os.path.exists(issue_dir):
                print(f"{library} already has {issue_name}")
            else:
                print(f"{library} does not have {issue_name}")
                issue_names_to_pull.append(issue_name)
        num_issues_to_pull = len(issue_names_to_pull)

        if num_issues_to_pull == 0:
            print(f"{library} already has all requested issues from {book_name}.\nIf there are more issues, they are not available online.")
            return

        # Retrieve the missing issues
        print(f"Downloading missing issues now.")
        for i in range(num_issues_to_pull):
            issue_name = issue_names_to_pull[i]
            issue_dir = os.path.join(library, book_name, issue_name)

            issue_soup = Puller.get_soup_from_url(issue_links[issue_name])
            issue_page_links = Puller.get_page_names_and_links(issue_soup)

            for page_name, page_link in tqdm(issue_page_links.items(), desc=f"Downloading {issue_name}"):
                Puller.download_content_from_link(page_link, issue_dir)
            print(f"Downloaded {issue_name} to {library}")

        print(f"Done.")