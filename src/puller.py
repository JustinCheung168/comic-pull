from typing import Optional

from src.misc import pretty_print
from src.sources import SOURCES
from src.library import Library

class Puller:
    @staticmethod
    def pull(book_name: str, library_path: str, source_url: str, first_issue: int = 1, last_issue: Optional[int] = None):
        # Validate inputs.
        assert first_issue >= 1, "First issue should be specified as 1 or higher."
        if last_issue is not None:
            assert last_issue >= 1, "Last issue should be specified as 1 or higher."
        if source_url not in SOURCES.keys():
            print("source_url must be one of the following:")
            pretty_print(SOURCES.keys())
            raise Exception
        
        source = SOURCES[source_url]()
        
        print(f"Checking {source_url} for available issues.")
        source.update_book_metadata(book_name)
        issue_names = source.book_name_to_issue_names[book_name]

        if (last_issue is None) or (last_issue > len(issue_names)):
            last_issue = len(issue_names)

        lib = Library(library_path)

        issue_names_to_check = issue_names[(first_issue-1):last_issue]
        # Figure out which issues we do not have.
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