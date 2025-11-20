# EmailSender Python Module

send yourself via email the remote machine's public ip address if the ip changed. for people who work on a remote machine without static ip

---

## Quick Start

1. **Clone the repository**:

```bash
git clone https://github.com/<USERNAME>/email_sender_project.git
cd email_sender
```

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

3. **Run a test email**:

```bash
python3 send_ip.py
```

4. **Schedule automatic sending**:

```bash
./schedule_python_cron.sh
```

* Follow prompts to choose frequency and time
* Confirm you received the test email before scheduling

---

## Features

* Object-oriented email sending
* Supports multiple recipients via JSON (`email_recipients.json`)
* Stores sender credentials locally (`email_sender_config.json`)
* Sends email only if the public IP changes
* Easy automation via cron with an interactive scheduler

---

## Project Structure

```
email_sender/
├── __init__.py
├── email_sender.py
├── send_ip.py
├── schedule_python_cron.sh
├── email_last.json
├── ip_last.json
├── email_recipients.json
└── __pycache__/
```

---

## Configuration

1. **Sender email & credentials**

* On first run of `send_ip.py`, enter your sender email, SMTP server, port, and app password.
* Stored in `email_sender_config.json`.

2. **Recipients**

* Edit `email_recipients.json` to add/remove recipients:

```json
{
  "recipients": [
    "chengdaoyang@live.com",
    "chengdaoyang@gmail.com"
  ]
}
```

---

## Usage

### Test sending IP

```bash
python3 send_ip.py
```

* Sends your public IP to all recipients if changed
* Logs output to `send_ip.py.log`

### Schedule automatic sending

```bash
chmod +x schedule_python_cron.sh
./schedule_python_cron.sh
```

* Choose daily or weekly
* Set the time (HH:MM)
* Perform a **test run** and confirm receipt before scheduling
* Logs saved to `send_ip.py.log`

---

## Security Notes

* Do **not** commit `email_sender_config.json` or `email_last.json`
* Use Gmail **App Passwords** instead of main passwords
* `.gitignore` excludes configs, logs, and virtual environments:

```
email_sender_config.json
email_last.json
email_recipients.json
*.log
venv/
__pycache__/
```

---

## Requirements

```text
requests>=2.31.0
```

---

## Contact

For questions, contact: **[chengdaoyang@live.com](mailto:chengdaoyang@live.com)**
