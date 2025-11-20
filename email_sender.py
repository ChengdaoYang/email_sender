import os
import json
import smtplib
from pathlib import Path
from email.mime.text import MIMEText


class EmailSender:
    """
    Email sender class with persistent storage of sender credentials.
    Stores sender email & SMTP settings in .email_sender_config.json
    """

    MODULE_DIR = Path(__file__).parent
    CONFIG_PATH = MODULE_DIR / ".email_sender_config.json"

    def __init__(self):
        self.config = self._load_or_setup_config()

    # ----------------------------------------------------------------------
    # Load or create config
    # ----------------------------------------------------------------------
    def _load_or_setup_config(self):
        """
        Loads sender email + SMTP info.
        If not found, prompts user to create one.
        """
        if self.CONFIG_PATH.exists():
            with open(self.CONFIG_PATH, "r") as f:
                return json.load(f)

        print("Email sender not configured. Creating new config...")

        sender_email = input("Sender email: ").strip()
        smtp_server = input("SMTP server (e.g., smtp.gmail.com): ").strip()
        smtp_port = int(input("SMTP port (587 recommended): ").strip())
        app_password = input("Email app-password (NOT your login password): ").strip()

        config = {
            "sender_email": sender_email,
            "smtp_server": smtp_server,
            "smtp_port": smtp_port,
            "app_password": app_password
        }

        self._save_config(config)
        return config

    def _save_config(self, config: dict):
        """Writes config to ~/.email_sender_config.json"""
        with open(self.CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=4)

    # ----------------------------------------------------------------------
    # Public API: send email
    # ----------------------------------------------------------------------
    def send_email(self, subject: str, message: str, target_emails):
        """
        Sends an email using saved sender credentials.
        - target_emails: string or list of strings
        """
        if isinstance(target_emails, str):
            recipients = [target_emails]
        else:
            recipients = list(target_emails)

        mime = MIMEText(message)
        mime["Subject"] = subject
        mime["From"] = self.config["sender_email"]
        mime["To"] = ", ".join(recipients)

        with smtplib.SMTP(self.config["smtp_server"], self.config["smtp_port"]) as smtp:
            smtp.starttls()
            smtp.login(self.config["sender_email"], self.config["app_password"])
            smtp.sendmail(self.config["sender_email"], recipients, mime.as_string())

        print(f"Email successfully sent to: {recipients}")


