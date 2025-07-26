from collections import defaultdict

from tqdm import tqdm

from src.misc import download_file_from_link, get_soup_from_link, pretty_print, clean_filename


class Source:
    """
    Abstract base class for comic sources (websites to download comics from).
    Handles metadata and downloading for comic issues.
    """
    HEADERS = {"User-Agent": f"Mozilla/5.0 (compatible; placeholder/placeholder)"}

    def __init__(self):
        """
        Initializes metadata dictionaries for books and issues.
        """
        # Maps book name to a list of issue names
        self.book_name_to_issue_names: dict[str, list[str]] = defaultdict(list)
        # Maps issue name to its homepage link
        self.issue_name_to_issue_homelink: dict[str, str] = {}
        # Maps issue name to a list of page file links
        self.issue_name_to_page_filelinks: dict[str, list[str]] = defaultdict(list)

    def update_book_metadata(self, book_name: str):
        """
        Update book-level metadata: populates issue names and their homepage links for a given book.
        Should be implemented by subclasses.
        """
        raise NotImplementedError()

    def update_issue_metadata(self, issue_name: str):
        """
        Update issue-level metadata: populates page file links for a given issue.
        Should be implemented by subclasses.
        """
        raise NotImplementedError()

    def download_issue(self, issue_name: str, write_directory: str):
        """
        Download all pages for a given issue to the specified directory.
        """
        issue_page_links = self.issue_name_to_page_filelinks[issue_name]
        for page_link in tqdm(issue_page_links, desc=f"Downloading {issue_name}"):
            download_file_from_link(page_link, write_directory, self.HEADERS)


class ReadComicsOnlineRu(Source):
    """
    Comic source for readcomicsonline.ru. Implements metadata extraction and page download logic.
    """
    URL_BASE = "https://readcomicsonline.ru/comic/"

    def update_book_metadata(self, book_name: str):
        """
        Populate issue names and homepage links for a book from readcomicsonline.ru.
        """
        book_link = self.URL_BASE + book_name
        book_soup = get_soup_from_link(book_link, self.HEADERS)
        for h5 in book_soup.find_all('h5', class_='chapter-title-rtl'):
            a_tag = h5.find('a')
            if a_tag and a_tag.get('href'):
                issue_name = clean_filename(h5.get_text(strip=True))
                issue_url = a_tag['href']
                self.book_name_to_issue_names[book_name].insert(0, issue_name)
                self.issue_name_to_issue_homelink[issue_name] = issue_url

    def update_issue_metadata(self, issue_name: str):
        """
        Populate page file links for an issue from readcomicsonline.ru.
        """
        issue_link = self.issue_name_to_issue_homelink[issue_name]
        issue_soup = get_soup_from_link(issue_link, self.HEADERS)
        div = issue_soup.find('div', id='all')
        assert div
        for img in div.find_all('img'):
            url = img.get('data-src').strip()
            self.issue_name_to_page_filelinks[issue_name].append(url)


class XOXOComicCom(Source):
    """
    Comic source for xoxocomic.com. Implements metadata extraction and page download logic.
    """
    URL_BASE = "https://xoxocomic.com/comic/"

    def update_book_metadata(self, book_name: str):
        """
        Populate issue names and homepage links for a book from xoxocomic.com.
        """
        book_link = self.URL_BASE + book_name
        book_soup = get_soup_from_link(book_link, self.HEADERS)
        for div in book_soup.find_all('div', class_='col-xs-9 chapter'):
            a_tag = div.find('a')
            if a_tag and a_tag.get('href'):
                issue_name = clean_filename(div.get_text(strip=True))
                issue_url = a_tag['href']
                self.book_name_to_issue_names[book_name].insert(0, issue_name)
                self.issue_name_to_issue_homelink[issue_name] = issue_url

    def update_issue_metadata(self, issue_name: str):
        """
        Populate page file links for an issue from xoxocomic.com.
        For each page, finds the image URL and appends it to the issue's file links.
        """
        issue_link = self.issue_name_to_issue_homelink[issue_name]
        issue_soup = get_soup_from_link(issue_link, self.HEADERS)
        select_tag = issue_soup.find('select', id='selectPage')
        assert select_tag
        for option in select_tag.find_all('option'):
            page_link = option.get('value')
            assert page_link
            page_soup = get_soup_from_link(page_link, self.HEADERS)
            div = page_soup.find('div', class_='page-chapter')
            assert div
            a = div.find("a")
            assert a
            img_tag = a.find('img', class_='single-page lazy')
            assert img_tag
            url = img_tag.get('data-original').strip()
            self.issue_name_to_page_filelinks[issue_name].append(url)


class SourceFactory:
    """
    Factory class to instantiate the correct Source subclass based on the source URL.
    """
    SOURCES = {
        "readcomicsonline.ru": ReadComicsOnlineRu,
        "xoxocomic.com": XOXOComicCom,
    }

    @classmethod
    def make_source(cls, source_url: str) -> Source:
        """
        Returns an instance of the appropriate Source subclass for the given source_url.
        Raises an exception if the source_url is not supported.
        """
        if source_url not in cls.SOURCES.keys():
            print("source_url must be one of the following:")
            pretty_print(list(cls.SOURCES.keys()))
            raise Exception
        return cls.SOURCES[source_url]()