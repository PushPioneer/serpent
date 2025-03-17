# Serpent

Serpent is a lightweight task scheduling and automation tool that allows you to run Python scripts, shell scripts, and binary executables at specified intervals. It runs as a system service and provides a simple command-line interface for management.

## Features

- Run Python scripts, shell scripts, and binary executables
- Schedule tasks with configurable intervals (seconds, minutes, hours, days)
- Enable/disable tasks without removing them
- Persistent task storage using SQLite
- System service integration
- Simple command-line interface

## Installation

1. Clone this repository or download the source files
2. Run the installation script as root:
```bash
sudo ./install.sh
```

This will:
- Install the CLI tool to `/bin/serpent`
- Set up the runner script in `/usr/serpent/`
- Create necessary directories and database
- Install and enable the system service

## Usage

### Creating a New Task

To create a new task, use the `create` command with the following options:

```bash
serpent create -n <name> -p <path> -d <delay> -t <type>
```

Options:
- `-n, --name`: Name of your task (must be unique)
- `-p, --path`: Path to the script/executable
- `-d, --delay`: Time interval between runs (e.g., "30s", "5m", "1h", "2d")
- `-t, --type`: File type ("py" for Python, "sh" for shell scripts, "bin" for binaries)

Example:
```bash
serpent create -n backup -p /home/user/backup.sh -d 1h -t sh
```

### Managing Tasks

Enable a task:
```bash
serpent enable -n <task_name>
```

Disable a task:
```bash
serpent disable -n <task_name>
```

Remove a task:
```bash
serpent remove -n <task_name>
```

### Service Management

Start the service:
```bash
serpent start
```

Stop the service:
```bash
serpent stop
```

Restart the service (required after enabling new tasks):
```bash
serpent restart
```

## Supported File Types

- `py`: Python scripts (runs with `python3`)
- `sh`: Shell scripts (runs with `bash`)
- `bin`: Binary executables (runs directly)

## Time Format

The delay parameter supports the following formats:
- `s`: seconds (e.g., "30s")
- `m`: minutes (e.g., "5m")
- `h`: hours (e.g., "1h")
- `d`: days (e.g., "2d")

## Uninstallation

To remove Serpent from your system, run:
```bash
sudo ./uninstall.sh
```

This will:
- Remove all installed files
- Stop and disable the service
- Clean up systemd configuration

## Technical Details

- Tasks are stored in a SQLite database at `/var/serpent/jobs.db`
- The service runs as a systemd unit named `serpent.service`
- Each task runs in its own thread to prevent blocking
- The service automatically restarts if it crashes
- Tasks can be enabled/disabled without removing them from the database

## Notes

- The installation script must be run as root
- Make sure your scripts have the appropriate execute permissions
- For Python scripts, ensure Python 3 is installed
- The service runs with system privileges, so be careful with task permissions 
