from tests.integration.flask import client  # This is needed, though not referenced


def testRoot(client):
    response = client.get("/")
    assert "<p>Hello, World!</p>" == response.text


def testGetLog(client):
    response = client.get("/logs", query_string={"filename": "system.log"})
    assert response.status_code == 200
    assert "__thr_AMMuxedDeviceDisconnected" in response.text


def testGetLog_limit(client):
    response = client.get("/logs", query_string={"filename": "system.log", "limit": 1})
    assert response.status_code == 200
    lines = response.json
    assert len(lines) == 1
    assert "__thr_AMMuxedDeviceDisconnected" in response.text


def testGetLog_filter(client):
    response = client.get("/logs", query_string={"filename": "system.log", "limit": 1, "filter": "syslogd"})
    assert response.status_code == 200
    lines = response.json
    assert len(lines) == 1
    assert "ASL Sender Statistics" in response.text


def testGetBigLog(client):
    response = client.get("/logs", query_string={"filename": "bigboy.log", "limit": 1})
    assert response.status_code == 200
    # assert "[" not in response.text
    assert "067456160 This is line 67456160" in response.text
    lines = response.text.split("\n")
    assert len(lines) == 2
