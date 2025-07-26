import os


class Library:
    """
    Represents a folder of comics on your computer,
    providing methods to check for and locate issues you have.
    """
    def __init__(self, library_path: str):
        """
        Initialize the Library with a root path.
        Args:
            library_path (str): Path to the root of the comic library.
        """
        self.library_path = library_path
        self.name = library_path

    def get_issue_dir(self, book_name: str, issue_name: str) -> str:
        """
        Get the directory path for a specific issue of a book.
        Args:
            book_name (str): Name of the comic book.
            issue_name (str): Name of the issue.
        Returns:
            Path to the issue's directory.
        """
        return os.path.join(self.library_path, book_name, issue_name)

    def has(self, book_name: str, issue_name: str) -> bool:
        """
        Check if the library already contains the specified issue.
        Args:
            book_name (str): Name of the comic book.
            issue_name (str): Name of the issue.
        Returns:
            True if the issue exists, False otherwise.
        """
        issue_dir = self.get_issue_dir(book_name, issue_name)
        return os.path.exists(issue_dir)