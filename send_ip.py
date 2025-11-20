import requests
import json
from pathlib import Path
from email_sender import EmailSender

# -------------------------------
# File paths
# -------------------------------
MODULE_DIR = Path(__file__).parent
IP_STORE_PATH = MODULE_DIR / "ip_last.json"
RECIPIENTS_PATH = MODULE_DIR / "email_recipients.json"

# -------------------------------
# Default recipients (create file if not exists)
# -------------------------------
DEFAULT_RECIPIENTS = [
    "chengdaoyang@live.com",
    "chengdaoyang@gmail.com"
]

if not RECIPIENTS_PATH.exists():
    with open(RECIPIENTS_PATH, "w") as f:
        json.dump({"recipients": DEFAULT_RECIPIENTS}, f, indent=4)
    print(f"Created recipients file at {RECIPIENTS_PATH}")

# -------------------------------
# Functions
# -------------------------------
def fetch_public_ip():
    """Fetch the machine's public IP address."""
    try:
        response = requests.get("https://api.ipify.org", timeout=5)
        response.raise_for_status()
        return response.text.strip()
    except Exception as e:
        return f"Unknown (Error: {e})"


def load_previous_ip():
    """Load the last stored IP from file."""
    if IP_STORE_PATH.exists():
        try:
            with open(IP_STORE_PATH, "r") as f:
                data = json.load(f)
                return data.get("last_ip", None)
        except Exception:
            return None
    return None


def save_current_ip(ip):
    """Save the current IP to file."""
    with open(IP_STORE_PATH, "w") as f:
        json.dump({"last_ip": ip}, f)


def load_recipients():
    """Load recipient emails from JSON file."""
    try:
        with open(RECIPIENTS_PATH, "r") as f:
            data = json.load(f)
            recipients = data.get("recipients", [])
            if isinstance(recipients, str):
                return [recipients]
            return recipients
    except Exception as e:
        print(f"Error reading recipients: {e}")
        return []


def send_ip_if_changed():
    """Fetch public IP and send email to all recipients if IP changed."""
    current_ip = fetch_public_ip()
    previous_ip = load_previous_ip()

    if current_ip == previous_ip:
        print(f"No change in IP ({current_ip}). Email not sent.")
        return

    recipients = load_recipients()
    if not recipients:
        print("No recipients found. Email not sent.")
        return

    sender = EmailSender()

    subject = "Server Public IP Address Changed"
    message = (
        "Hello,\n\n"
        f"The public IP address of this machine has changed:\n\n"
        f"    {current_ip}\n\n"
        "This message was sent automatically by the Python EmailSender module.\n\n"
        "Regards,\n"
        "Your Server"
    )

    sender.send_email(subject, message, recipients)
    print(f"Email sent to: {recipients} with new IP: {current_ip}")

    save_current_ip(current_ip)


if __name__ == "__main__":
    send_ip_if_changed()

