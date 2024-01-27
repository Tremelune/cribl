from tests.unit.flask import client  # This is needed, though not referenced


def testRoot(client):
    response = client.get("/")
    assert "<p>Hello, World!</p>" == response.text
