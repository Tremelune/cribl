from collections.abc import Generator

from flask import Flask
from flask import request

import log_reader

# It seems like there should be one place where this is instantiated...
# and some random endpoint is not it. Look into how this should be done.
app = Flask(__name__)


@app.route("/logs", methods=['GET'])
def getLog():
    filename = request.args.get('filename')
    limit = request.args.get('limit')
    filter = request.args.get('filter')

    # At this point we should check for good input and respond with intelligent messages/codes to ensure
    # the caller knows exactly why the call failed...but for now we'll just explode and return whatever
    # error message our system bubbles up from the depths.

    limit = int(limit) if limit else None

    lines = log_reader.readLogs(filename, limit, filter)

    # Respond with text, as big as they want to handle
    return _addNewlines(lines), {"Content-Type": "text/plaintext"}


def _addNewlines(lines: Generator[str]) -> Generator[str]:
    for line in lines:
        yield line + "\n"


@app.route("/")
def root():
    return "<p>Hello, World!</p>"
