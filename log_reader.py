from typing import Optional

import disk_reader
import fnmatch


BASE_DIR = "/var/log"


def readLogs(filename: str, lineLimit: int, filterToken: str = None) -> list:
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

    if lineLimit < 1:
        raise Exception(f"Line limit must be positive!")


# Modifies lines
def _addFilteredLine(lines: list, line: str, filterToken: str):
    if filterToken:
        match = fnmatch.fnmatch(line, f"*{filterToken}*")
        if match:
            lines.append(line)
    else:
        lines.append(line)
