from typing import Optional

import disk_reader
import fnmatch


BASE_DIR = "/var/log"
MAX_LINES = 100  # Arbitrary but reasonable


def readLogs(filename: str, lineLimit: int = MAX_LINES, filterToken: str = None) -> list:
    _checkInputs(filename, lineLimit)

    lines = []
    for line in disk_reader.reverseRead(f"{BASE_DIR}/{filename}"):
        _addFilteredLine(lines, line, filterToken)

        if len(lines) >= lineLimit:
            return lines

    return lines


def _checkInputs(filename: str, lineLimit: int):
    # These exceptions could be more specific, but the important bit is to explode
    if not filename:
        raise Exception("Filename cannot be blank!")

    # Not the best approach to security, but it's something!
    if "/" in filename:
        raise Exception("Directories cannot be traversed!")

    if lineLimit < 1 or lineLimit > MAX_LINES:
        raise Exception(f"Line limit must be between 1 and {MAX_LINES}!")


# Modifies lines
def _addFilteredLine(lines: list, line: str, filterToken: str):
    if filterToken:
        match = fnmatch.fnmatch(line, f"*{filterToken}*")
        if match:
            lines.append(line)
    else:
        lines.append(line)
