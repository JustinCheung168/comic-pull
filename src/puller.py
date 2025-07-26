from typing import Optional

from src.sources import SourceFactory
from src.library import Library


class Puller:
    """
    Main interface for pulling comic issues from a source into a local library.
    """
    @staticmethod
    def pull(book_name: str, library_path: str, source_url: str, first_issue: int = 1, last_issue: Optional[int] = None):
        """
        Download missing comic issues for a given book from a specified source into the library.

        Args:
            book_name (str): Name of the comic book to pull.
            library_path (str): Path to the local library directory.
            source_url (str): URL identifier for the comic source.
            first_issue (int, optional): First issue index to pull (1-based, default: 1).
            last_issue (int, optional): Last issue index to pull (inclusive, default: last available).
        """
        # Validate input arguments
        assert first_issue >= 1, "First issue should be specified as 1 or higher."
        if last_issue is not None:
            assert last_issue >= 1, "Last issue should be specified as 1 or higher."

        # Create the source object for the given URL
        source = SourceFactory.make_source(source_url)

        print(f"Checking {source_url} for available issues.")
        source.update_book_metadata(book_name)
        issue_names = source.book_name_to_issue_names[book_name]

        # Determine the last issue index if not specified or out of range
        if (last_issue is None) or (last_issue > len(issue_names)):
            last_issue = len(issue_names)

        # Initialize the library object
        lib = Library(library_path)

        # Select the range of issues to check
        issue_names_to_check = issue_names[(first_issue-1):last_issue]

        # Figure out which issues we do not have in the library
        issue_names_to_pull = []
        for issue_name in issue_names_to_check:
            if lib.has(book_name, issue_name):
                print(f"{lib.name} already has {issue_name}")
            else:
                print(f"{lib.name} does not have {issue_name}")
                issue_names_to_pull.append(issue_name)

        if len(issue_names_to_pull) == 0:
            print(f"{lib.name} already has all requested issues from {book_name}.")
            print(f"If there are more issues, they are not available at {source_url}.")
            return

        # Retrieve the missing issues
        print(f"Downloading missing issues now.")
        for issue_name in issue_names_to_pull:
            source.update_issue_metadata(issue_name)
            source.download_issue(issue_name, lib.get_issue_dir(book_name, issue_name))

        print(f"Done.")