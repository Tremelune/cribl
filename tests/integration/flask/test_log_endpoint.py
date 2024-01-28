from tests.integration.flask import client  # This is needed, though not referenced


def testRoot(client):
    response = client.get("/")
    assert "<p>Hello, World!</p>" == response.text


def testGetLog(client):
    response = client.get("/logs", query_string={"filename": "system.log"})
    assert "__thr_AMMuxedDeviceDisconnected" in response.text


def testGetLog_limit(client):
    response = client.get("/logs", query_string={"filename": "system.log", "limit": 1})
    assert "__thr_AMMuxedDeviceDisconnected" in response.text
    split = response.text.split("\n")
    assert len(split) == 2


def testGetLog_filter(client):
    response = client.get("/logs", query_string={"filename": "system.log", "limit": 1, "filter": "syslogd"})
    assert "ASL Sender Statistics" in response.text
    split = response.text.split("\n")
    assert len(split) == 2


def testGetBigLog(client):
    response = client.get("/logs", query_string={"filename": "bigboy.log", "limit": 3})
    lines = response.text.split("\n")
    assert len(lines) == 4
    assert "067456160 This is line 67456160" == lines[0]
    assert "067456159 This is line 67456159" == lines[1]
    assert "067456158 This is line 67456158" == lines[2]


def testGetLogPreview(client):
    response = client.get("/logs/previews", query_string={"filename": "system.log"})
    assert "__thr_AMMuxedDeviceDisconnected" in response.json[0]


def testGetLogPreview_limit(client):
    response = client.get("/logs/previews", query_string={"filename": "system.log"})
    assert len(response.json) == 10


def testGetLogPreview_filter(client):
    response = client.get("/logs/previews", query_string={"filename": "system.log", "limit": 1, "filter": "syslogd"})
    assert "ASL Sender Statistics" in response.json[0]
