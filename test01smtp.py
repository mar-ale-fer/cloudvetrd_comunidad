import smtplib, ssl
#fuente: https://realpython.com/python-send-email/
port = 465  # For SSL
password = input("Type your password and press enter: ")
sender_email = "<redigi>[una cuenta]@gmail.com"  # Enter your address
receiver_email = "<redigi>[una cuenta]@gmail.com"  # Enter receiver address
message = """\
Subject: Hi there

This message is sent from Python."""

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("<redigi>[una cuenta]@gmail.com", password)
    server.sendmail(sender_email, receiver_email, message)