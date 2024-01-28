# Cribl Log Reader
```
(_(
/_/'_____/)
"  |      |
   |""""""|
```
## Deploying
In a terminal in the top of the project directory, run:

```
flask --app log_endpoint run
```
Some Macs have port 5000 occupied, so you might have to work around
that. The easiest way is by killing the Mac process:

https://stackoverflow.com/questions/72369320/why-always-something-is-running-at-port-5000-on-my-mac

There might be some user permission issues with /var/log, but the
app is usually deployed as a user that can read from that
directory (works on my machine!).

Note that a Python 3.9 interpreter is expected for this project.

## API

There are two endpoints that pull from the same data source.

Errors result in a HTTP status of 500 with an accompanying system
message. This is cludgy, but not critical...It's on my todo list,
I'll open a Jira ticket...

### GET /logs/previews
#### Input Params
**filename** - The full name of the logfile (relative to /var/log).
If you want to read from /var/log/system.log, you would pass in
"system.log".

**filter (optional)** - Text to filter the results through. If you
only want lines with "dog" in it, pass in "dog". Lines returned will
include "lovely doghouse" as well as "what's updog?"

**limit (optional)** - This limits the response to the number of
lines specified (*after* filtration), with a maximum of ten. If no
limit is specified, the default is 10.

#### Response
Response is a JSON list of lines.

### GET /logs
#### Input Params
**filename** - Same as /logs/previews

**filter (optional)** - Same as /logs/prviews

**limit (optional)** - This limits the response to the number of
lines specified (*after* filtration).

#### Response
Response is plaintext, with each log line separated by a newline
character.

## Architecture
I chose Python and Flask due to its popularity and simplicity.

Also for simplicity, all files are in one Python package. There just
weren't enough of them to bother organizing them. Conceptually,
they occupy three tiers:

- **API/UI** - Handles HTTP requests/responses as
well as routing and content type. This is where log_endpoint
belongs.
- **Business Logic** - Where most application logic
would live. Has  no knowledge of disks, databases, HTTP, or the
CLI. This is where log_reader belongs.
- **Data Access** - Where data is wrangeled. This is where disk
access is provided, as well as calls to datastores, queues, or
external APIs. disk_reader belongs here.

## Performance
Data is pulled directly from disk and sent in the response stream
while being processed. Regardless of how large the log file is, it
is only read into memory in chunks commensurate with how much data
has been transferred in the response.

Besides those that transfer many lines, the slowest requests are
those for which the log file is large, and the filter term is rare.
The app might go through a whole 2GB file just to find three lines
that match. I thought about trying to leverage a local grep
instance, but that opens the door to a lot more environmental
variables than I want in a take-home exercise...

I also considered pagination, but pagination is annoying for
everyone.

## Assumptions
- All log files are plain text UTF-8.
- If no limit is specified, clients are expected to handle
response sizes over a GB.
- Log lines are returned most-recent first, which means if you
request the entire log and write it to disk, the last line written
will be the first line read (the oldest).