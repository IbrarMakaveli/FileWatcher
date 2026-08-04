# FileWatcher

[![Python versions](https://img.shields.io/badge/python-3.9%2B-blue?style=flat-square)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)

FileWatcher launches a shell command when a file is received in a watched path, with optional settings:

- Minimum file size
- Waiting time before launching the command
- File name must match a regex

The configuration is stored in local YAML files (inside FileWatcher).

## Requirements

- Python 3.9+
- Linux / macOS (the daemon uses `fork`)

## Installation

```bash
pip install .
python -m filewatcher.config.installer_config
```

Or for development:

```bash
pip install -r requirements.txt
pip install -e .
python -m filewatcher.config.installer_config
```

## Usage

Once installed, the `filewatcher` command is available (you can also use `python -m filewatcher`):

```bash
# Add a path to watch : run a command when a file arrives
filewatcher add /path/to/watch "echo new file received"

# With options : regex match, minimum size, waiting time
filewatcher add /path/to/watch "./process.sh" -regex ".*\.csv$" -minsize 10MB -timewait 00:05:00

# List watched paths
filewatcher list

# Modify a watched path
filewatcher modify /path/to/watch -command "./other.sh" -minsize 1KB

# Delete a watched path
filewatcher delete /path/to/watch

# Start the daemon (10 workers by default)
filewatcher start
filewatcher start --force        # restart if already started
filewatcher start -worker 20     # custom number of workers

# Daemon status / stop
filewatcher status
filewatcher stop

# Follow the logs
filewatcher log                  # live stream (tail -F)
filewatcher log --all            # all logs of the current day
filewatcher log -date 2026-08-01 # logs of a given day
```

## How it works

- `filewatcher start` daemonizes and watches every configured path with [watchdog](https://github.com/gorakhargosh/watchdog).
- When a file is created, it waits until the file stops growing, checks the size/regex rules, waits `timewait` if configured, then runs the command.
- Watched-path configurations are YAML files stored in the `data/` folder; the daemon restarts its observers automatically when they change.
- Logs are rotated daily in the `logs/` folder.

## License

MIT
