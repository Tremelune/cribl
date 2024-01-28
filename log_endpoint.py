from collections.abc import Generator

from flask import Flask
from flask import request
from flask import jsonify

import log_reader

# It seems like there should be one place where this is instantiated...
# and some random endpoint is not it. Look into how this should be done.
app = Flask(__name__)

PREVIEW_MAX_LINES = 10  # Arbitrary but reasonable


# 403 FileNotFoundError: [Errno 2] No such file or directory: '/var/log/fill.log'
@app.route("/logs/previews", methods=['GET'])
def getLogPreview():
    filename = request.args.get('filename')
    limit = request.args.get('limit')
    filter = request.args.get('filter')

    # At this point we should check for good input and respond with intelligent messages/codes to ensure
    # the caller knows exactly why the call failed...but for now we'll just explode and return whatever
    # error message our system bubbles up from the depths.

    # Limit preview results to a small set
    limit = min(int(limit), PREVIEW_MAX_LINES) if limit else PREVIEW_MAX_LINES

    lines = log_reader.readLogs(filename, limit, filter)
    response = jsonify(list(lines))
    response.headers.add('Access-Control-Allow-Origin', '*')  # Hack in CORS compliance...
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
    for line in lines:
        yield line + "\n"


@app.route("/")
def root():
    return "<p>Hello, World!</p>"
