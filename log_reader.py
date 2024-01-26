import disk_reader

BASE_DIR = "/var/log"


def readLogs(filename: str, lineLimit: int, filterToken: str = None) -> list:
    # todo protect against directory traversal
    with open(f"{BASE_DIR}/{filename}", "r") as file: # Open for reading
        lines = []
        # todo Offset ain't work yet!
        for line in disk_reader.reverseRead(f"{BASE_DIR}/{filename}", 0, lineLimit):
            if len(lines) >= lineLimit:  # Could remove this calc by incrementing an i variable
                return lines

            # todo This may squash blank lines, which we don't want
            filtered = filterLine(line, filterToken)
            if filtered:
                lines.append(filtered)

        return lines


def filterLine(line: str, filterToken: str) -> str:
    return line
