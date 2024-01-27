from typing import Optional

import disk_reader
import fnmatch


BASE_DIR = "/var/log"


def readLogs(filename: str, lineLimit: int = 100, filterToken: str = None) -> list:
    if not filename:
        raise Exception("Filename cannot be blank")

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
