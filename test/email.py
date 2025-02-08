import imaplib
import email
from email.header import decode_header

def read_gmail():
    # Account credentials
    username = "your_email@gmail.com"
    password = "your_app_password"  # Generated App Password

    # Connect to Gmail IMAP server
    imap = imaplib.IMAP4_SSL("imap.gmail.com")

    # Login
    imap.login(username, password)

    # Select the mailbox you want to use (inbox here)
    imap.select("inbox")

    # Search for all emails
    status, messages = imap.search(None, "ALL")

    # Convert messages to a list of email IDs
    email_ids = messages[0].split()

    # Fetch the last 10 emails
    for email_id in email_ids[-10:]:
        # Fetch the email by ID
        status, msg_data = imap.fetch(email_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                # Parse the email bytes to a message
                msg = email.message_from_bytes(response_part[1])

                # Decode email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8")

                # Decode sender
                from_ = msg.get("From")

                print(f"Subject: {subject}")
                print(f"From: {from_}")

                # If the email has a body
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))

                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            # Decode email content
                            body = part.get_payload(decode=True).decode()
                            print(f"Body: {body}")
                else:
                    # Extract content for non-multipart emails
                    body = msg.get_payload(decode=True).decode()
                    print(f"Body: {body}")

    # Logout from the account
    imap.logout()

if __name__ == "__main__":
    read_gmail()

