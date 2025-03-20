# Serpent Task Runner

Serpent is a lightweight task scheduling and automation tool that allows you to run Python scripts, shell scripts, and binary executables at specified intervals. It runs as a system service and provides a simple command-line interface for management.

## Features

- Run Python scripts, shell scripts, and binary executables
- Schedule tasks with configurable intervals (seconds, minutes, hours, days)
- Enable/disable tasks without removing them
- Persistent task storage using SQLite
- System service integration
- Simple command-line interface
- Task dependencies support
- Comprehensive logging and execution history
- Error tracking and reporting

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
serpent create -n <name> -p <path> -d <delay> -t <type> [--deps <dependencies>]
```

Options:
- `-n, --name`: Name of your task (must be unique)
- `-p, --path`: Path to the script/executable
- `-d, --delay`: Time interval between runs (e.g., "30s", "5m", "1h", "2d")
- `-t, --type`: File type ("py" for Python, "sh" for shell scripts, "bin" for binaries)
- `--deps`: Comma-separated list of job dependencies (optional)

Example:
```bash
# Create a backup job that depends on a cleanup job
serpent create -n cleanup -p /home/user/cleanup.sh -d 1h -t sh
serpent create -n backup -p /home/user/backup.sh -d 1h -t sh --deps cleanup
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

## Task Dependencies

Tasks can have dependencies on other tasks. When a task has dependencies:
1. It will only run if all its dependencies are enabled
2. It will wait for all dependencies to complete successfully before running
3. If any dependency fails, the dependent task will not run until the dependency succeeds

Example of task dependencies:
```bash
# Create a data processing pipeline
serpent create -n fetch_data -p /home/user/fetch.sh -d 1h -t sh
serpent create -n process_data -p /home/user/process.py -d 1h -t py --deps fetch_data
serpent create -n generate_report -p /home/user/report.sh -d 1h -t sh --deps process_data
```

## Logging and Monitoring

Serpent maintains comprehensive logs and execution history:

1. **Service Logs**
   - Location: `/var/serpent/serpent.log`
   - Contains detailed information about:
     - Task registration and configuration
     - Task execution attempts
     - Success/failure status
     - Error messages and stack traces
     - Dependency checks and waiting periods

2. **Execution History**
   - Stored in the SQLite database
   - Records for each task execution:
     - Start and end times
     - Execution status (success/failed/error)
     - Error messages (if any)
     - Command output

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
- Dependencies are stored as comma-separated strings in the database
- Execution history is maintained in a separate table

## Notes

- The installation script must be run as root
- Make sure your scripts have the appropriate execute permissions
- For Python scripts, ensure Python 3 is installed
- The service runs with system privileges, so be careful with task permissions
- Check the log file at `/var/serpent/serpent.log` for detailed execution information
- When using dependencies, ensure there are no circular dependencies 