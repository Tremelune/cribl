```
(_(
/_/'_____/)
"  |      |
   |""""""|
```
# cribl
A Python 3.9 interpreter is expected for this project!

```
flask --app log_endpoint run
```
Some Macs have port 5000 occupied, so you have to work around it.

There might be some user permission issues with /var/log...

Assumptions
All files are plain text UTF-8

### Performance
Pretty quick, and doesn't load everythign into memory.
Slowest requests are for giant files where you're trying to match
on something that is rare. Might go through whole 2GB file just
to find three lines with the matches...
