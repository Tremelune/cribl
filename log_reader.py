from collections.abc import Generator
from typing import Optional

import disk_reader
import fnmatch


BASE_DIR = "/var/log"


def readLogs(filename: str, lineLimit: Optional[int], filterToken: str = None) -> Generator[str]:
    _checkInputs(filename, lineLimit)

    lineCount = 0
    for line in disk_reader.reverseRead(f"{BASE_DIR}/{filename}"):
        if filterToken:
            match = fnmatch.fnmatch(line, f"*{filterToken}*")
            if match:
                yield line
                lineCount += 1
        else:
            yield line
            lineCount += 1

        if lineLimit and lineCount >= lineLimit:
            return
            yield line


def _checkInputs(filename: str, lineLimit: Optional[int]):
    # These exceptions could be more specific, but the important bit is to explode
    if not filename:
        raise Exception("Filename cannot be blank!")

    # Not the best approach to security, but it's something!
    if "/" in filename:
        raise Exception("Directories cannot be traversed!")

    if lineLimit and lineLimit < 1:
        raise Exception(f"Line limit must be positive!")
