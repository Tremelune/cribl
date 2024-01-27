import pytest as pytest
from flask import Flask

import log_endpoint


# One could argue that hitting a Flask app with an HTTP text fixture client qualifies it as an
# integration test, but since it all happens in-memory and requires no external resources or
# setup, I'm inclined to put them here and treat them as such.
@pytest.fixture
def client():
    app = log_endpoint.app
    app.config.update({"TESTING": True})
    client = app.test_client()
    yield client
