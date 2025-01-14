# Advanced Remote Keylogger

⚠️ **Disclaimer**: This project is intended solely for educational purposes. Unauthorized use of keyloggers is illegal and unethical. Always obtain explicit consent before deploying this software.

This project involves creating an **Advanced Keylogger** using Python, which extends beyond basic keystroke logging. It incorporates advanced features like capturing screenshots, recording audio, collecting clipboard data, and gathering system information. All collected data, including keystrokes, is sent to a configured email address, enabling remote monitoring.

---

## Features

- **Keystroke Logging**: Records all keystrokes made on the keyboard.
- **Clipboard Data Capture**: Extracts and stores data from the clipboard.
- **System Information Gathering**: Retrieves system and network details, including IP addresses.
- **Audio Recording**: Records microphone input for a defined duration.
- **Screenshot Capture**: Takes screenshots of the user's screen.
- **Email Reporting**: Sends all collected data and logs via email with attachments.

---

## Prerequisites

### Install Python and Required Libraries
1. Install Python 3.x.
2. Install the following Python libraries using pip:
pip install pynput scipy sounddevice Pillow requests pywin32

### Set Up Gmail for Email Reporting
1. Create or use an existing Gmail account for sending emails.
2. Enable **App-Specific Passwords** (if 2FA is enabled).
3. Replace placeholder values in the script with your credentials.

---

## Project Structure

The keylogger creates the following files during operation:
- `key_log.txt`: Logs all keystrokes.
- `systeminfo.txt`: System and network information.
- `clipboard.txt`: Data extracted from the clipboard.
- `audio.wav`: Microphone recording.
- `screenshot.png`: Captured screenshot.

---

## Setup

### Clone the Repository
  git clone https://github.com/ishan2491/Advanced-Remote-Keylogger.git
  cd Advanced-Remote-Keylogger

### Configure Email and File Paths
  Open the script (`keylogger.py`) and replace placeholders with your values:
    email_address = "your_email@example.com"
    password = "your_app_password"
    toaddr = "recipient_email@example.com"
    file_path = "C:\Path\To\Save\Files"

---

## Usage

### Run the Keylogger
To start logging keystrokes and collecting data:
  python keylogger.py

### Send Data via Email
The script will periodically send all collected data (logs, screenshots, recordings) to the configured email address.

---

## Functions Explained

### System Information Gathering
  Collects system details such as:
    - OS version
    - Processor type
    - Public and private IP addresses
    - Hostname

### Clipboard Data Extraction
  Reads and stores content from the clipboard.

### Keystroke Logging
  Monitors and records every key pressed, appending data to `key_log.txt`.

### Screenshot Capture
  Captures the screen's current state and saves it as an image (`screenshot.png`).

### Audio Recording
  Records microphone input for a specified duration and saves it as `audio.wav`.

### Email Transmission
  Sends an email with all logs as attachments using SMTP.

---

## Advanced Mode

  The script can be configured to send keystroke logs every 10 seconds in real-time. Modify the `main1()` function in the script to enable this behavior.

---

## Additional Notes

  1. The script can be converted into an executable using tools like [PyInstaller](https://pyinstaller.org/):
    pyinstaller --onefile keylogger.py
  2. You can hide the executable in an image file using WinRAR's SFX archive feature for stealth deployment.

---

## References

For more information, check out:
- YouTube Tutorial on Advanced Keyloggers.
- [Perplexity AI](https://www.perplexity.ai) for additional insights.

---
