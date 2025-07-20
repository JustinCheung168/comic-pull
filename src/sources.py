from collections import defaultdict

from tqdm import tqdm

import src.misc

class Source:
    """"""
    HEADERS = {"User-Agent": f"Mozilla/5.0 (compatible; placeholder/placeholder)"}
    def __init__(self):
        """"""
        # Book-level metadata
        self.book_name_to_issue_names: dict[str, list[str]] = defaultdict(list)
        self.issue_name_to_issue_homelink: dict[str, str] = {}

        # Issue-level metadata
        self.issue_name_to_page_filelinks: dict[str, list[str]] = defaultdict(list)

    def update_book_metadata(self, book_name: str):
        """
        Update book-level metadata (i.e. each issue's name, and links to issue sites for each issue in the book)
        """
        raise NotImplementedError()

    def update_issue_metadata(self, issue_name: str):
        """
        Update issue-level metadata (i.e. links to page files for each page in the issue)
        """
        raise NotImplementedError()
    
    def download_issue(self, issue_name: str, write_directory: str):
        issue_page_links = self.issue_name_to_page_filelinks[issue_name]
        for page_link in tqdm(issue_page_links, desc=f"Downloading {issue_name}"):
            src.misc.download_file_from_link(page_link, write_directory, self.HEADERS)

class ReadComicsOnlineRu(Source):
    """"""
    URL_BASE = "https://readcomicsonline.ru/comic/"
    def update_book_metadata(self, book_name: str):
        book_link = self.URL_BASE + book_name
        book_soup = src.misc.get_soup_from_link(book_link, self.HEADERS)
        for h5 in book_soup.find_all('h5', class_='chapter-title-rtl'):
            a_tag = h5.find('a')
            if a_tag and a_tag.get('href'):
                issue_name = src.misc.clean_filename(h5.get_text(strip=True))
                issue_url = a_tag['href']

                self.book_name_to_issue_names[book_name].insert(0, issue_name)
                self.issue_name_to_issue_homelink[issue_name] = issue_url

    def update_issue_metadata(self, issue_name: str):
        issue_link = self.issue_name_to_issue_homelink[issue_name]
        issue_soup = src.misc.get_soup_from_link(issue_link, self.HEADERS)
        div = issue_soup.find('div', id='all')
        assert div
        for img in div.find_all('img'):
            url = img.get('data-src').strip()

            self.issue_name_to_page_filelinks[issue_name].append(url)

SOURCES = {
    "readcomicsonline.ru": ReadComicsOnlineRu,
}