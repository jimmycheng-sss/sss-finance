import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
import sys

def send_email_with_attachment(to_email, subject, body, attachment_path):
    # Load credentials
    creds = {}
    try:
        with open('/data/.openclaw/credentials/gmail.env', 'r') as f:
            for line in f:
                if '=' in line:
                    k, v = line.strip().split('=', 1)
                    creds[k] = v
    except Exception as e:
        return f"Error loading credentials: {str(e)}"

    gmail_user = creds.get('GMAIL_USER')
    gmail_password = creds.get('GMAIL_APP_PASSWORD')

    if not gmail_user or not gmail_password:
        return "Error: Gmail credentials not found."

    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with open(attachment_path, "rb") as f:
            part = MIMEApplication(
                f.read(),
                Name=os.path.basename(attachment_path)
            )
        # After the file is closed
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
        msg.attach(part)
    except Exception as e:
        return f"Error attaching file: {str(e)}"

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(gmail_user, gmail_password)
        server.send_message(msg)
        server.quit()
        return "Email sent successfully!"
    except Exception as e:
        return f"Error sending email: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python send_email.py <to_email>")
        sys.exit(1)
    
    to_email = sys.argv[1]
    subject = "Swift Spark Studios - Landing Page Draft"
    body = "Hi Jimmy,\n\nHere is the draft HTML file for the Swift Spark Studios landing page we discussed.\n\nYou can open this file directly in Chrome or Safari to preview the design.\n\nBest,\nAsa"
    attachment = "/data/.openclaw/workspace/swift_spark_studios/index.html"
    
    print(send_email_with_attachment(to_email, subject, body, attachment))
