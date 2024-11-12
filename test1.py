import smtplib

email_address = "temp26204@gmail.com"
password = "ipjuszgndaumfbeb"
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
