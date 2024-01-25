from flask import Flask

app = Flask(__name__)


@app.route("/logs")
def get_log():
    return "2:15p tuesday - Finished the whole sandwich and am just over the moon about it!"


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
