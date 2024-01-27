from typing import Optional

import disk_reader
import fnmatch


BASE_DIR = "/var/log"
MAX_LINES = 100  # Arbitrary but reasonable


def readLogs(filename: str, lineLimit: int = MAX_LINES, filterToken: str = None) -> list:
    # These exceptions could be more specific, but the important bit is to explode
    if not filename:
        raise Exception("Filename cannot be blank!")

    # Not the best approach to security, but it's something!
    if "/" in filename:
        raise Exception("Directories cannot be traversed!")

    if lineLimit < 1 or lineLimit > MAX_LINES:
        raise Exception(f"Line limit must be between 1 and {MAX_LINES}!")

    lines = []
    for line in disk_reader.reverseRead(f"{BASE_DIR}/{filename}"):
        filtered = _filterLine(line, filterToken)
        # Explicit None check, because an empty string (blank line) we want to include
        if filtered is not None:
            lines.append(filtered)
        else:
            lines.append(line)

        if len(lines) >= lineLimit:
            return lines

    return lines


def _filterLine(line: Optional[str], filterToken: Optional[str]) -> Optional[str]:
    if not filterToken:
        return line

    if fnmatch.fnmatch(line, f"*{filterToken}*"):
        return line

    return None
