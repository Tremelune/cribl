from flask import Flask
from flask import request

import log_reader

# It seems like there should be one place where this is instantiated...and some random endpoint is not
# it. Look into how this should be done.
app = Flask(__name__)

MAX_LINES = 100  # Arbitrary but reasonable


@app.route("/logs", methods=['GET'])
def getLog():
    filename = request.args.get('filename')
    limit = request.args.get('limit')
    filter = request.args.get('filter')

    # At this point we should check for good input and respond with intelligent messages/codes to ensure
    # the caller knows exactly why the call failed...but for now we'll just explode and return whatever
    # error message our system bubbles up from the depths.
    limit = int(limit) if limit else MAX_LINES

    res = log_reader.readLogs(filename, limit, filter)
    # Pull the whole resultset and respond with JSON of a list of lines.
    # This is fine because we know we have a reasonable number of lines to pull into memory.
    return list(res)


@app.route("/")
def root():
    return "<p>Hello, World!</p>"
