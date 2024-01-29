# The Benedict Cribl Log Reader
```
(_(
/_/'_____/)
"  |      |
   |""""""|
```
## Deploying the Server
In a terminal in the top of the project directory, run:

```commandline
flask --app log_endpoint run
```
This will launch the server at http://127.0.0.1:5000/

Some Macs have port 5000 occupied, so you might have to work around
that. The easiest way is by killing the Mac process:

https://stackoverflow.com/questions/72369320/why-always-something-is-running-at-port-5000-on-my-mac

There might be some user permission issues with /var/log, but the
app is usually deployed as a user that can read from that
directory (works on my machine!).

Note that a Python 3.9 interpreter is expected for this server.

## UI
If you would like to use the (very) rudimentary React UI, it can
be deployed by running this in the root project directory:
```commandline
npm install
```
and once the packages are installed:
```commandline
npm start
```
This will launch a site at http://127.0.0.1:3000/ that will let
you hit the API. The "Get Preview" button gets up to 100 lines of
the specified log file. If you want the full file, a download link
is provided (and it will limit the resultset to what was specified
in the preview request).

Due to cross-origin shenanegans, the "download" attribute won't
force a file download, so you may want to right-click on that link
and choose "Save As..." Otherwise, your browser might try and
display a 2GB text file and explode if no limit has been specified.

This is also why you want to run the UI and API under 127.0.0.1
(instead of, say, localhost).

## API

There are two endpoints that pull from the same data source.

Errors are, ah, not handled with grace. I'll open a Jira ticket...

### GET /logs/previews
#### Input Params
**filename** - The full name of the logfile (relative to /var/log).
If you want to read from /var/log/system.log, you would pass in
"system.log".

**filter (optional)** - Text to filter the results through. If you
only want lines with "dog" in it, pass in "dog". Lines returned will
include "lovely doghouse" as well as "what's updog?"

**limit (optional)** - This limits the response to the number of
lines specified (*after* filtration), with a maximum of 100. If no
limit is specified, the default is 100.

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
I chose Python and Flask (as well as Node.js/React) due to their
popularity and simplicity.

Also for simplicity, all files are in one Python package. There
just weren't enough of them to bother organizing them.
Conceptually, they occupy three tiers:

- **API** - Handles HTTP requests/responses as
well as routing and content type. This is where log_endpoint
belongs.
- **Business Logic** - Where most application logic
would live. Has  no knowledge of disks, databases, HTTP, or the
CLI. This is where log_reader belongs.
- **Data Access** - Where data is wrangeled. This is where disk
access is provided, as well as calls to datastores, queues, or
external APIs. disk_reader belongs here.

Please forgive the munging of the UI React/Node.js code and API
Python/Flask code—they should probably be in their own directories
but things started breaking as I moved them around, so I stopped.

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

## Testing

There are unit tests and integration tests. I've been running them
from my IDE while building.

The unit tests can be run quickly on any environment. Many mock
out the disk reader to avoid having to have real files locally.

The integration tests rely on the existence of certain log files
on my local machine, but could be easily tweaked to account for any
files on another machine. That said, they exist to help me build
things, but if they were long-lived, I would take a different
approach (such as creating the files as part of the
test fixture).

One set of integration tests spins up a Flask instance and hits
the real endpoints. Mocking proved tricky, so they too hit the
disk looking for specific files in var.log.

## Proxy
I didn't get around to creating the proxy server for pulling log
files from other machines, but my approach would be something
like this:

Create a log_client (in the Data Access package) whose only job is
to hit other Benedict Cribl Log Reader instances.

It would have a map of server IDs to base URLs/IPs or something
to determine where to send the request.

Calls to log_client would simply return the response body
from the other servers as a Python generator (iterable) stream.
This would mean that any log reader instance could act as a proxy,
streaming the same log results from other servers in the same
format, also without having to pull the entire response into
memory at any point in the chain.

The API interface would be the same, with the exception of 
specifying a server ID in the initial request to the primary server
(which has the same code as all the secondary servers). If no ID
is specified, it behaves as normal, pulling from its own log disk.

## Assumptions
- All log files are plain text UTF-8.
- If no limit is specified, clients are expected to handle
response sizes over a GB.
- Log lines are returned most-recent first, which means if you
request the entire log and write it to disk, the last line written
will be the first line read (the oldest).
- Building profitable software on a team involves a lot more than
writing code, particularly if you want to enjoy doing it.
