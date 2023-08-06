"""Locates files based on regex patterns."""

from typing import Iterable
import os
import re


def search_files(root: str, pattern: str,
                 recursive: bool = False) -> Iterable[str]:
    """Locates files based on regex patterns.

    Args:
        root - (str) Root directory.
        pattern - (str) Regex search pattern.
        recursive - (bool) Recursively search sub folders?

    Returns:
        Generator of files paths.
    """

    if recursive:
        for path, subdirs, files in os.walk(root):
            for fileName in files:
                if re.search(pattern, os.path.join(path, fileName)):
                    yield os.path.join(path, fileName)

    else:
        for fileName in os.listdir(root):
            if re.search(pattern, os.path.join(root, fileName)):
                yield os.path.join(root, fileName)
