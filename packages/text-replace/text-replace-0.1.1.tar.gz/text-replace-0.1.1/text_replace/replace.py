"""Replaces text in a file using regex."""

import re
import traceback


def replace(filePath, pattern, newText, breakOnFail: True) -> bool:
    """Replaces text in a file using regex.

    Args:
        filePath - (str) File path.
        pattern - (str) Regex pattern to search for text to replace.
        newText - (str) Replacement text.
        silentFail - (bool) Should the function break and raise an exception on
            fail?

    Returns:
        bool - Was the update successful.
    """

    try:
        if not isinstance(pattern, str):
            raise ValueError('`pattern` must be regex string.')

        if not isinstance(newText, str):
            raise ValueError('`newText` must be defined.')

        with open(filePath, 'r') as f:
            content = f.read()

        with open(filePath, 'w') as f:
            f.write(re.sub(pattern, newText, content))

        return True

    except IOError:
        if breakOnFail:
            raise IOError(traceback.format_exc())
        else:
            print(f'\033[91mFailed updating {filePath}.\033[0m')
            return False
