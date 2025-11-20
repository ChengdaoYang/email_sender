nteractive Cron Scheduler for send_ip.py
# Assumes this script is in the same directory as send_ip.py
# ================================================

echo "=== IP Email Scheduler ==="

# -------------------------------
# 1️⃣ Determine send_ip.py path
# -------------------------------
SCRIPT_PATH="$(cd "$(dirname "$0")"; pwd)/send_ip.py"

if [ ! -f "$SCRIPT_PATH" ]; then
    echo "Error: send_ip.py not found in the current directory."
    exit 1
fi

# -------------------------------
# 2️⃣ Ask for frequency
# -------------------------------
echo "Select schedule frequency:"
echo "1) Daily"
echo "2) Weekly"
read -p "Enter choice [1-2]: " FREQ

if [[ "$FREQ" != "1" && "$FREQ" != "2" ]]; then
    echo "Invalid choice. Exiting."
    exit 1
fi

# -------------------------------
# 3️⃣ Ask for time
# -------------------------------
read -p "Enter time to run (HH:MM, 24-hour format): " TIME
HOUR=$(echo "$TIME" | cut -d':' -f1)
MINUTE=$(echo "$TIME" | cut -d':' -f2)

if ! [[ "$HOUR" =~ ^[0-9]+$ ]] || ! [[ "$MINUTE" =~ ^[0-9]+$ ]] || [ "$HOUR" -lt 0 ] || [ "$HOUR" -gt 23 ] || [ "$MINUTE" -lt 0 ] || [ "$MINUTE" -gt 59 ]; then
    echo "Invalid time format. Exiting."
    exit 1
fi

# -------------------------------
# 4️⃣ Python path
# -------------------------------
PYTHON_PATH=$(which python3)
if [ -z "$PYTHON_PATH" ]; then
    echo "Error: python3 not found in PATH"
    exit 1
fi

# -------------------------------
# 5️⃣ Test run
# -------------------------------
echo "Performing a test run of send_ip.py..."
echo "This will attempt to send your current public IP to the configured recipients."

$PYTHON_PATH "$SCRIPT_PATH"

echo ""
read -p "Did you receive the test email? (y/n): " CONFIRM
if [[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]]; then
    echo "Test email not confirmed. Exiting without scheduling cron."
    exit 0
fi

# -------------------------------
# 6️⃣ Cron schedule string
# -------------------------------
if [ "$FREQ" == "1" ]; then
    CRON_SCHEDULE="$MINUTE $HOUR * * *"    # Daily
else
    CRON_SCHEDULE="$MINUTE $HOUR * * 0"    # Weekly (Sunday)
fi

# -------------------------------
# 7️⃣ Cron command
# -------------------------------
LOG_FILE="$SCRIPT_PATH.log"
CRON_CMD="$PYTHON_PATH $SCRIPT_PATH >> $LOG_FILE 2>&1"

# -------------------------------
# 8️⃣ Check if cron job exists
# -------------------------------
(crontab -l 2>/dev/null | grep -F "$SCRIPT_PATH") && echo "Cron job already exists. Exiting." && exit 0

# -------------------------------
# 9️⃣ Schedule cron job
# -------------------------------
(crontab -l 2>/dev/null; echo "$CRON_SCHEDULE $CRON_CMD") | crontab -

echo ""
echo "✅ Cron job installed successfully!"
echo "Schedule: $( [ "$FREQ" == 1 ] && echo "Daily" || echo "Weekly") at $TIME"
echo "Python script: $SCRIPT_PATH"
echo "Logs: $LOG_FILE"

