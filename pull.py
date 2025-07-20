#!/usr/bin/env python3
import argparse

import src.puller
import config

def main():
    parser = argparse.ArgumentParser(
        description="Download comic issues using Puller."
    )
    parser.add_argument(
        "book_name",
        type=str,
        help=f"Name of the comic book (e.g. 'absolute-martian-manhunter-2025'. Format is the one in the URLs at {src.puller.READ_COMICS_ONLINE})"
    )
    parser.add_argument(
        "--library",
        type=str,
        default=config.LIBRARY,
        help=f"Path to the library directory where issues will be saved (default: {config.LIBRARY})."
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
        library=args.library,
        first_issue=args.first_issue,
        last_issue=args.last_issue
    )

if __name__ == "__main__":
    main()
