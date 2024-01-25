def readLogs():
    file = open("/var/log/system.log", "r")
    try:
        return file.read()
    finally:
        file.close()

