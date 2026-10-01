# Mini URL Shortener (CLI)

This project is a command line tool, written in Python 3, that turns long URLs into short custom codes (or random ones) and resolves them back to the original URL. All the data is saved to a local file, so it persists between runs and also maintains the click count.

## Features

- Shorten a URL into a random 6-character code.
- Custom alias support with `--alias`.
- Resolve a short code back to its URL and opens it in the browser.
- Click count tracking: every `resolve` increases the counter.
- List all stored mappings with click counts and creation time.
- Persistent storage in `data.json`.
- Input checks: only `http` and `https` URLs are accepted, unknown codes give a clear error, and a corrupted data file is backed up instead of crashing the program.
- Uses only the Python standard library, with no external shortening APIs.

## Requirements

- Python 3 (no extra packages to install)

## How to run

1. Clone the repository and go into the folder:
```
git clone https://github.com/Ruhaan261/gdgtask1_url_shortener_cli.git
cd gdgtask1_url_shortener_cli
```
2. Run any command with `python3 main.py`:

`python3 main.py shorten <url>` => Creates a random short code
`python3 main.py shorten <url> --alias <name>` => Uses your own code
`python3 main.py resolve <code>` => Prints and opens the original URL
`python3 main.py list` => Shows all stored mappings

Running `python3 main.py` with no command shows the help text.

## Sample commands and output

Shorten a URL with a custom alias:
```
$ python3 main.py shorten https://www.wikipedia.org --alias wiki
Short code created: wiki
```

Resolve a code (also opens the URL in your browser and adds 1 to its click count):
```
$ python3 main.py resolve wiki
Resolved to: https://www.wikipedia.org
```

List everything:
```
$ python3 main.py list
Search_Engine-> https://google.com| clicks:2| created:2026-09-18 15:36:41
gh-> https://github.com| clicks:1| created:2026-09-18 18:08:26
insta-> https://www.instagram.com| clicks:1| created:2026-10-01 01:54:50
PwbUep-> https://example.com| clicks:0| created:2026-10-01 21:55:30
oRIcsb-> https://hello.com| clicks:0| created:2026-10-01 21:56:04
wiki-> https://www.wikipedia.org| clicks:1| created:2026-10-01 21:59:32
```

Invalid input is rejected:
```
$ python3 main.py shorten notaurl
Error: "notaurl" is not a valid URL.
```

## How it works

- Mappings are stored in `data.json` as a dictionary: the short code is the key, and the value holds the URL, click count and creation time.
- If no alias is given, a random code is generated from letters and digits. It is regenerated if it already exists.
- If an alias already exists, the tool asks before overwriting it.
- If `data.json` is corrupted, it is renamed to `data.json.corrupt` and the tool starts with an empty store.