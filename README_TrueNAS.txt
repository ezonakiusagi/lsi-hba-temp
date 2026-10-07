# How to Install and Run on TrueNAS Scale

Setting this up in TrueNAS SCALE requires a slightly different approach, even though TrueNAS SCALE is built on a standard Debian Linux base, it treats the boot drive as a highly locked-down, read-only firmware appliance. Modifying /etc/ or standard system binary paths directly will result in your changes being completely wiped out during the next TrueNAS update. To keep everything permanent, you must host the script and configuration on a storage pool and utilize TrueNAS SCALE’s native Init/Shutdown Scripts engine via the WebUI.

1. Directory Structure on a Storage Pool
Instead of using the boot drive, store the utility on your primary, persistent storage pool dataset.

Connect to your TrueNAS shell (via SSH or the WebUI Shell).

Create an administrative directory inside your main pool (replace "tank" with the actual name of your storage pool):

# mkdir -p /mnt/tank/apps/lsi-hba-temp/bin

Copy the bash script and configuration files into this layout:

/mnt/tank/apps/lsi-hba-temp/lsi-hba-temp (The main Bash script)
/mnt/tank/apps/lsi-hba-temp/lsi-hba-temp.conf (The configuration file)

Mark the script as executable:

# chmod +x /mnt/tank/apps/lsi-hba-temp/lsi-hba-temp

The lsi-hba-temp script uses proprietary utilities (lsiutil, storcli64, or storcli2) from LSI/Broadcom and these need to be installed so that lsi-hba-temp can call them. Which utility you require depends on which LSI HBA controller(s) you have installed. The script can auto-detect your LSI HBA controller(s) and tell you if it cannot find the required utility. Use this feature by first running it manually so it displays error messages about which utility your system needs.

# /mnt/tank/apps/lsi-hba-temp/lsi-hba-temp

Once you determine which LSI/Broadcom utility you need (lsiutil, storcli64, or storcli2), download the utility and copy it into the "bin" folder:

/mnt/tank/apps/lsi-hba-temp/bin/ (Place your pre-compiled lsiutil, storcli64, or storcli2 binaries here)

storcli64 and storcli2 can be downloaded from broadcom.com. The lsiutil source code can be found online, but a pre-compiled static binary is available from my website here:

https://artofserver.com/downloads/lsi/utilities/linux/lsiutil

Finally, make sure the proprietary binaries are also marked executable:

# chmod +x /mnt/tank/apps/lsi-hba-temp/bin/{lsiutil,storcli64,storcli2}

2. Adjusting the Configuration File for TrueNAS SCALE
Open your /mnt/tank/apps/lsi-hba-temp/lsi-hba-temp.conf file. We want to explicitly define the paths to your pool-hosted binaries so they integrate cleanly with TrueNAS SCALE:

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
# Custom Binary Paths (Unraid / TrueNAS Special Deployments)
# ------------------------------------------------------------------------------
# Override these paths if your binaries are stored outside the system PATH.
# Leave them blank or commented out to let the script auto-detect them in PATH.
# Example: LSIUTIL="/boot/config/custom/bin/lsiutil"
LSIUTIL="/mnt/tank/apps/lsi-hba-temp/bin/lsiutil"
STORCLI="/mnt/tank/apps/lsi-hba-temp/bin/storcli64"
STORCLI2="/mnt/tank/apps/lsi-hba-temp/bin/storcli2"

(Remember to replace tank with your actual storage pool name.)

At this point, it is a good idea to test the utility manually and make sure it works by running:

# /mnt/tank/apps/lsi-hba-temp/lsi-hba-temp

If it works, you should see message(s) showing the temperature(s) of your LSI HBA controllers. If it doesn't work, there should be error messages to help you diagnose the problem.

3. Automation via TrueNAS SCALE WebUI
TrueNAS SCALE provides a built-in mechanism to run automated scripts during system boot loops without messing with standard crontabs or systemd units.

Log into your TrueNAS SCALE WebUI.

Navigate to System Settings -> Advanced.

Scroll down to the Init/Shutdown Scripts card and click Add.

Configure the form fields exactly like this:

Description: LSI HBA Temperature Monitor Daemon

Type: Command

Command: /mnt/tank/apps/lsi-hba-temp/lsi-hba-temp --daemon

When: Post Init (This ensures the storage pool is fully mounted before the script attempts to execute)

Click Save.

The utility will now gracefully spin up as a completely decoupled background daemon every time your TrueNAS machine finishes booting.

4. Operational Usage Commands
Checking Live Status Manually
If you ever want to run a quick, ad-hoc check straight to the console:

# /mnt/tank/apps/lsi-hba-temp/lsi-hba-temp

Viewing Daemon Output (Journald)
Because TrueNAS SCALE is systemd-based and the script uses logger, your metrics map straight into the journal engine. You can read them in real-time by running:

# journalctl -f -t lsi-hba-temp

Stopping the Daemon Safely
If you need to make changes to your temperature thresholds or polling intervals, you don't have to reboot. Just run the script with the built-in stop flag to clear the queue:

# /mnt/tank/apps/lsi-hba-temp/lsi-hba-temp --stop
