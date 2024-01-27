```
(_(
/_/'_____/)
"  |      |
   |""""""|
```
# Cribl Log Reader
## Deploying
In a terminal in the top of the project directory, run:

```
flask --app log_endpoint run
```
Some Macs have port 5000 occupied, so you might have to work around
that. The easiest way is by killing the Mac process:

https://stackoverflow.com/questions/72369320/why-always-something-is-running-at-port-5000-on-my-mac

There might be some user permission issues with /var/log, but at
on my machine, the app was deployed as the same user as the a user
that could read from the directory.

Note that a Python 3.9 interpreter is expected for this project!

## API

There is one endpoint:

### GET /logs
#### Input Params
**filename** - The full name of the logfile (relative to /var/log).
If you want to read from /var/log/system.log, you would pass in
"system.log" for the filename params.

**filter (optional)** - Text of filter the results through. If you want only
lines with "dog" in it, pass in "dog". Lines returned will include
"lovely doghouse" as well as "what's updog?"

**limit (optional)** - This limits the response to the number of
lines specified (*after* filtration).

#### Response
Response is plaintext, with each log line separated by a newline
character.

Errors result in a HTTP status of 500 with an accompanying system
message.

## Architecture
I chose Flask due to its popularity and simplicity.

Also for simplicity, all files are in one Python package. There just
weren't enough of them to bother organizing them. Conceptually,
they occupy three tiers:

- **API/UI** - Handles HTTP requests/responses as
well as routing and content type. This is where log_endpoint lives.
- **Business Logic** - Where most application logic
would live. Has  no knowledge of disks, databases, HTTP, or the
CLI. This is where log_reader lives.
- **Data Access** - Where data is wrangeled. This is where disk
access is provided, as well as calls to datastores, queues, or
external APIs. disk_reader lives here.

## Performance
Data is pulled directly from disk and sent in the response stream.
Regardless of how large the log file is, it is only read into
memory in chunks commensurate with how much data has been
transferred in the response.

Besides those that transfer many lines, the slowest requests are
those for which the log file is large, and the filter term is rare.
The app might go through a whole 2GB file just to find three lines
that match. I thought about trying to leverage a local grep
instance, but that opens the door to a lot more environmental
variables than I want in a take-home exercise...

I also considered pagination, but pagination is *annoying*.

## Assumptions
- All log files are plain text UTF-8.
- If no limit is specified, clients are expected to handle
response sizes over a GB.
- Log lines are returned most-recent first, which means if you
request the entire log and write it to disk, the last line written
will be the first line read (the oldest).