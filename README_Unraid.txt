# How to Install and Run on Unraid

Deploying this on Unraid requires a few specific adjustments. Unraid runs completely out of a volatile RAM disk (tmpfs). On every single boot, the root filesystem is wiped clean and re-created from the USB flash drive.

To ensure the script, its configuration, and its required proprietary binaries persist across reboots, follow this optimized deployment guide.

1. Directory Structure on the Flash Drive
To organize everything cleanly, use Unraid's persistent storage on your USB boot flash drive (/boot/). Create a dedicated folder structure under your custom configuration directory.

Open your Unraid terminal and run:

# mkdir -p /boot/config/plugins/lsi-hba-temp/bin

Copy the bash script and configuration files so they match this layout:

/boot/config/plugins/lsi-hba-temp/lsi-hba-temp (The main Bash script)
/boot/config/plugins/lsi-hba-temp/lsi-hba-temp.conf (The configuration file)

Make sure the main script is marked executable:

# chmod +x /boot/config/plugins/lsi-hba-temp/lsi-hba-temp

The lsi-hba-temp script uses proprietary utilities (lsiutil, storcli64, or storcli2) from LSI/Broadcom and these need to be installed so that lsi-hba-temp can call them. Which utility you require depends on which LSI HBA controller(s) you have installed. The script can auto-detect your LSI HBA controller(s) and tell you if it cannot find the required utility. Use this feature by first running it manually so it displays error messages about which utility your system needs.

# /boot/config/plugins/lsi-hba-temp/lsi-hba-temp

Once you determine which LSI/Broadcom utility you need (lsiutil, storcli64, or storcli2), download the utility and copy it into the "bin" folder:

/boot/config/plugins/lsi-hba-temp/bin/ (Drop your proprietary lsiutil or storcli64 / storcli2 binaries here)

storcli64 and storcli2 can be downloaded from broadcom.com. The lsiutil source code can be found online, but a pre-compiled static binary is available from my website here:

https://artofserver.com/downloads/lsi/utilities/linux/lsiutil

Finally, make sure the proprietary binaries are also marked executable:

# chmod +x /boot/config/plugins/lsi-hba-temp/bin/{lsiutil,storcli64,storcli2}

2. Tailoring the Configuration File for Unraid
Because Unraid uses a RAM disk, /var/log/ vanishes on reboot (which is fine for logs), but pointing the custom binary variables directly to the flash drive removes the need to manually symlink them into the system PATH on every boot.

Edit your /boot/config/plugins/lsi-hba-temp/lsi-hba-temp.conf file to explicitly use the flash drive paths:

# ==============================================================================
# lsi-hba-temp configuration file
# ==============================================================================

# Time interval in seconds between temperature polls when running in loop modes.
INTERVAL=60

# Warning and Critical temperature thresholds in Celsius.
WARN_TEMP=65
CRIT_TEMP=80

# The destination path for background daemon execution logging.
LOG_FILE="/var/log/lsi-hba-temp.log"

# The path to the process ID file used to track the standalone daemon.
PID_FILE="/var/run/lsi-hba-temp.pid"

# Default output format for standard loops (console, file, syslog)
LOG_MODE="console"

# ------------------------------------------------------------------------------
# Custom Binary Paths (Mapped directly to your persistent Unraid Flash Drive)
# ------------------------------------------------------------------------------
# Override these paths if your binaries are stored outside the system PATH.
# Leave them blank or commented out to let the script auto-detect them in PATH.
# Example: LSIUTIL="/boot/config/custom/bin/lsiutil"
LSIUTIL="/boot/config/plugins/lsi-hba-temp/bin/lsiutil"
STORCLI="/boot/config/plugins/lsi-hba-temp/bin/storcli64"
STORCLI2="/boot/config/plugins/lsi-hba-temp/bin/storcli2"

At this point, it is a good idea to test the utility manually and make sure it works by running:

# /boot/config/plugins/lsi-hba-temp/lsi-hba-temp

If it works, you should see message(s) showing the temperature(s) of your LSI HBA controllers. If it doesn't work, there should be error messages to help you diagnose the problem.

3. Automation and Boot Persistence
You have two choices to ensure this utility starts automatically when your Unraid server boots. Option A is the recommended unraid community approach because it provides a clean graphical interface to view log output and manage state.

Option A: The User Scripts Plugin (Recommended)

Install the User Scripts plugin from the Apps tab if you don't have it already.

Navigate to Settings -> User Scripts and click Add New Script. Name it lsi-hba-temp.

Click the gear icon next to the new script and select Edit Script.

Paste the following execution sequence:

===== BEGIN SCRIPT =====
#!/bin/bash
# Description: Launch the LSI HBA temperature monitoring daemon

SCRIPT_PATH="/boot/config/plugins/lsi-hba-temp/lsi-hba-temp"

if [ -f "$SCRIPT_PATH" ]; then
    # Launching via daemon flag allows User Scripts to complete cleanly 
    # while the isolated grandchild process handles the background loop.
    $SCRIPT_PATH --daemon
else
    logger -t lsi-hba-temp "Error: Monitor script missing at $SCRIPT_PATH"
fi
===== END SCRIPT =====

Save the changes. Change the scheduling dropdown from "Manual" to At Startup of Array.

Option B: The Native go Script

If you prefer a lightweight deployment without installing plugins, you can append a hook directly to Unraid's native boot file.

Edit /boot/config/go on your flash drive and add this line at the bottom:

# Start LSI HBA Temperature Monitoring Daemon
/boot/config/plugins/lsi-hba-temp/lsi-hba-temp --daemon

4. Operational Usage Commands
Once deployed, you can interact with the utility directly via the standard Unraid terminal.

Ad-hoc Live Query
To do a quick check on current temperatures without starting a loop, run the script manually. It will auto-discover the configuration file located in its parent directory and output straight to the console:

/boot/config/plugins/lsi-hba-temp/lsi-hba-temp

Checking the Service Logs

In background daemon mode, all recurring updates and logged messages are routed straight into Unraid's central engine. You can view them in real-time alongside other hardware events using:

tail -f /var/log/syslog | grep lsi-hba-temp

Alternatively, you can click the Log button at the top right of the Unraid WebUI interface to view them graphically.

Stopping the Daemon
If you change your thresholds or intervals in the .conf file and need to safely cycle the background daemon, the built-in termination mechanics handle it gracefully:

/boot/config/plugins/lsi-hba-temp/lsi-hba-temp --stop
