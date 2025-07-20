import os

class Library:
    """"""
    def __init__(self, library_path: str):
        self.library_path = library_path
        self.name = library_path

    def get_issue_dir(self, book_name: str, issue_name: str) -> str:
        return os.path.join(self.library_path, book_name, issue_name)

    def has(self, book_name: str, issue_name: str) -> bool:
        issue_dir = self.get_issue_dir(book_name, issue_name)
        return os.path.exists(issue_dir)