import smtplib
from email.message import EmailMessage
import os

EMAIL_SENDER = "ukzn.component@gmail.com"
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
EMAIL_ADMIN = "221008769@stu.ukzn.ac.za"

msg = EmailMessage()
msg["From"] = EMAIL_SENDER
msg["To"] = EMAIL_ADMIN
msg["Subject"] = "SMTP Test"
msg.set_content("This is a test email from your Flask app.")

with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    server.send_message(msg)
    print("Test email sent!")
