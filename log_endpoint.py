from flask import Flask
from flask import request

import log_reader

app = Flask(__name__)


@app.route("/logs", methods=['GET'])
def get_log():
    filename = request.args.get('filename')
    limit = request.args.get('limit')
    filter = request.args.get('filter')

    # At this point we should check for good input and respond with intelligent messages/codes to ensure
    # the caller knows exactly why the call failed...but for now we'll just explode and return whatever
    # error message our system bubbles up from the depths.
    limit = int(limit) if limit else log_reader.MAX_LINES

    return log_reader.readLogs(filename, limit, filter)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
