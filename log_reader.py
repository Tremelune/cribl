BASE_DIR = "/var/log"


def readLogs(filename: str, lineCount: int, filter: str = None) -> str:
    # todo protect against directory traversal
    with open(f"{BASE_DIR}/{filename}", "r") as file: # Open for reading
        return file.read()
