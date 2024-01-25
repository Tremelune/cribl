import disk_reader

BASE_DIR = "/var/log"


def readLogs(filename: str, lineLimit: int, filterToken: str = None) -> list:
    # todo protect against directory traversal
    with open(f"{BASE_DIR}/{filename}", "r") as file: # Open for reading
        lines = []
        for line in disk_reader.reverseRead(f"{BASE_DIR}/{filename}"):
            if len(lines) >= lineLimit:  # Could remove this calc by incrementing an i variable
                return lines

            filtered = filterLine(line, filterToken)
            if filtered:
                lines.append(filtered)

        return lines


def filterLine(line: str, filterToken: str) -> str:
    return line
