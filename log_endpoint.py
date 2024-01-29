from collections.abc import Generator

from flask import Flask
from flask import request
from flask import jsonify

import log_reader

# It seems like there should be one place where this is instantiated...
# and some random endpoint is not it. Look into how this should be done.
app = Flask(__name__)

PREVIEW_MAX_LINES = 10  # Arbitrary but reasonable


@app.route("/logs/previews", methods=['GET'])
def getLogPreview():
    filename = request.args.get('filename')
    limit = request.args.get('limit')
    filter = request.args.get('filter')

    # At this point we should check for good input and respond with intelligent messages/codes to ensure
    # the caller knows exactly why the call failed...In addition, different types of failures should be handled
    # explicitly (file not found is different from a null pointer error). For this exercise we'll just explode and
    # return whatever error message our system bubbles up from the depths.

    # Limit preview results to a small set
    limit = min(int(limit), PREVIEW_MAX_LINES) if limit else PREVIEW_MAX_LINES

    lines = log_reader.readLogs(filename, limit, filter)
    response = jsonify(list(lines))
    response.headers.add('Access-Control-Allow-Origin', '*')  # Hack in CORS compliance...Don't do this...
    return response


@app.route("/logs", methods=['GET'])
def getLog():
    filename = request.args.get('filename')
    limit = request.args.get('limit')
    filter = request.args.get('filter')

    limit = int(limit) if limit else None

    lines = log_reader.readLogs(filename, limit, filter)

    # Respond with text, as big as they want to handle
    return _addNewlines(lines), {"Content-Type": "text/plaintext"}


def _addNewlines(lines: Generator[str]) -> Generator[str]:
    """Adds newline character on the fly, without breaking out of the generator stream..."""
    for line in lines:
        yield line + "\n"


@app.route("/")
def root():
    """derp derp"""
    return "<p>Hello, World!</p>"
