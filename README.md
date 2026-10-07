```markdown
# lsi-hba-temp

A lightweight, robust hardware monitoring utility that polls and evaluates real-time temperatures for Broadcom / LSI storage controllers (HBAs). It supports ad-hoc terminal queries, interactive console intervals, and headless background deployment via systemd.

## Features

* **Wide Chipset Support:** Automatically detects and queries LSI/Broadcom controllers across generations (SAS1 to SAS4 chips) using `lsiutil`, `storcli64`, or `storcli2`.
* **Flexible Execution:** Runs as a quick one-shot query, a live-updating terminal loop, or a detached system daemon.
* **Smart Traps:** Intercepts termination signals (`SIGTERM`/`SIGINT`) to interrupt sleep cycles instantly and exit cleanly without leaving orphaned background processes.
* **Color-Coded Console Output:** Features automatic scannable status highlighting (`ok`, `warning`, `critical`) when outputting directly to a terminal screen.

## Installation

### Prerequisites
The script requires root privileges for hardware polling and relies on standard system utilities:
* `pciutils` (`lspci`)
* `gawk`
* `util-linux`

Ensure your vendor-specific CLI utilities (`storcli64`, `storcli2`, or `lsiutil`) are installed and accessible in your system's `$PATH`.

### Manual Installation
1. Clone the repository and navigate to the project directory:
   ```bash
   git clone [https://github.com/the-art-of-server/lsi-hba-temp.git](https://github.com/the-art-of-server/lsi-hba-temp.git)
   cd lsi-hba-temp

```

2. Make the script executable:
```bash
chmod +x lsi-hba-temp

```


3. Run an ad-hoc check:
```bash
sudo ./lsi-hba-temp

```



## Usage

```text
Usage: lsi-hba-temp [OPTIONS]

Options:
    -d, --daemon           Run in systemd daemon mode (forces output to syslog).
    -i, --interval <sec>   Run continuously in loop mode at specified interval.
    -o, --output <dest>    Set output destination: console, file, syslog (Default: console)
                           Note for Unraid: Use a persistent path like /boot/ or /mnt/ 
                           if saving to a file.
    -h, --help             Display this help text.

```

### Examples

**Standard Ad-hoc Query:**

```bash
sudo ./lsi-hba-temp

```

**Interactive Terminal Loop (updates every 10 seconds):**

```bash
sudo ./lsi-hba-temp --interval 10

```

**Log Directly to a File:**

```bash
sudo ./lsi-hba-temp --interval 60 --output file

```

## Project Directory Structure

```text
lsi-hba-temp/
├── LICENSE
├── README.md
├── lsi-hba-temp.sh
├── systemd/
│   ├── lsi-hba-temp.service
│   └── lsi-hba-temp.timer
└── packaging/
    ├── rpm/
    │   └── lsi-hba-temp.spec
    └── deb/

```

## License

This project is licensed under the GNU General Public License v3 - see the [LICENSE](https://www.google.com/search?q=LICENSE) file for the full text.

```text
Copyright (C) 2026 Art of Server <the.art.of.server@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

```

```

```
