#!/usr/bin/env python3
import argparse
import os
import sys

import config
import src.puller

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def main():
    parser = argparse.ArgumentParser(
        description="Download comic issues using Puller."
    )
    parser.add_argument(
        "book_name",
        type=str,
        help=f"Name of the comic book (e.g. 'absolute-martian-manhunter-2025'. Format is the one in the URLs at {config.DEFAULT_SOURCE_URL})"
    )
    parser.add_argument(
        "--library-path",
        type=str,
        default=config.DEFAULT_LIBRARY_PATH,
        help=f"Path to the library directory where issues will be saved (default: {config.DEFAULT_LIBRARY_PATH})."
    )
    parser.add_argument(
        "-s",
        "--source-url",
        type=str,
        default=config.DEFAULT_SOURCE_URL,
        help=f"URL to get comics from (default: {config.DEFAULT_SOURCE_URL})."
    )
    parser.add_argument(
        "-f",
        "--first-issue",
        type=int,
        default=1,
        help="First issue to pull (default: 1)."
    )
    parser.add_argument(
        "-l",
        "--last-issue",
        type=int,
        default=None,
        help="Stop index of issues to pull (inclusive, default: last issue)"
    )
    args = parser.parse_args()

    src.puller.Puller.pull(
        book_name=args.book_name,
        library_path=args.library_path,
        source_url=args.source_url,
        first_issue=args.first_issue,
        last_issue=args.last_issue
    )

if __name__ == "__main__":
    main()
