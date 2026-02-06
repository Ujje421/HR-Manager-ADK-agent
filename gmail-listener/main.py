import base64
import schedule
import time
import re
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from ask_hr_agent import get_hr_reply


def extract_email(sender):
    """Extract pure email from 'Name <email@domain.com>'"""
    match = re.search(r"<(.+?)>", sender)
    return match.group(1) if match else sender.strip()


def send_reply(service, sender, subject, body):
    recipient_email = extract_email(sender)

    message = f"""To: {recipient_email}
Subject: {subject}
Content-Type: text/plain; charset="UTF-8"

{body}
"""

    raw = base64.urlsafe_b64encode(message.encode("utf-8")).decode("utf-8")

    service.users().messages().send(
        userId="me",
        body={"raw": raw}
    ).execute()


def extract_body(payload):
    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain":
                data = part["body"].get("data")
                if data:
                    return base64.urlsafe_b64decode(data).decode(errors="ignore")
    return "No readable body found"


def read_unread_emails():
    creds = Credentials.from_authorized_user_file("token.json")
    service = build("gmail", "v1", credentials=creds)

    results = service.users().messages().list(
        userId="me", labelIds=["UNREAD"], maxResults=5
    ).execute()

    messages = results.get("messages", [])
    if not messages:
        print("📭 No new emails\n")
        return

    for msg in messages:
        msg_data = service.users().messages().get(
            userId="me", id=msg["id"], format="full"
        ).execute()

        headers = msg_data["payload"]["headers"]
        sender = next((h["value"] for h in headers if h["name"] == "From"), "Unknown")
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
        body = extract_body(msg_data["payload"])

        # 🔹 Use Gmail threadId as sessionId for ADK memory
        thread_id = msg_data["threadId"]
        sender_email = extract_email(sender)

        email_text = f"From: {sender}\nSubject: {subject}\nBody: {body}"

        print(f"📩 Processing email from {sender_email} | Subject: {subject}")

        # 🔹 Ask HR Agent
        hr_reply = get_hr_reply(email_text, sender_email, thread_id)

        print("🤖 HR Agent Decision:", hr_reply)

        # 🔹 Only reply if HR intent detected
        if hr_reply["action"] == "reply":
            send_reply(service, sender, hr_reply["subject"], hr_reply["body"])
            print("📤 HR reply sent\n")
        else:
            print("🚫 Not an HR email — skipped\n")

        # Mark as read
        service.users().messages().modify(
            userId="me", id=msg["id"], body={"removeLabelIds": ["UNREAD"]}
        ).execute()


schedule.every(2).minutes.do(read_unread_emails)

print("🚀 HR Gmail Listener Running...")
while True:
    schedule.run_pending()
    time.sleep(1)
