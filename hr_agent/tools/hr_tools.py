from google.adk.tools import tool
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import base64
from email.mime.text import MIMEText

def send_email(to: str, subject: str, body: str) -> str:
    creds = Credentials.from_authorized_user_file("token.json")
    service = build("gmail", "v1", credentials=creds)

    message = MIMEText(body)
    message["to"] = to
    message["subject"] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    service.users().messages().send(
        userId="me",
        body={"raw": raw}
    ).execute()

    return "Email sent successfully"


@tool
def get_employee_info(employee_id: str) -> dict:
    """Fetch employee details from HR system"""
    db = {
        "E101": {
            "name": "Rahul Sharma",
            "email": "rahul@company.com",
            "role": "Software Engineer",
            "department": "Engineering",
            "manager": "Anita Verma",
            "work_mode": "Remote"
        }
    }
    return db.get(employee_id, {})

@tool
def apply_leave(employee_id: str, leave_type: str, date: str) -> str:
    """Apply leave in HR system"""
    return f"Leave applied for {employee_id} on {date}"

@tool
def generate_document(employee_id: str, doc_type: str) -> str:
    """Generate HR document"""
    return f"https://company.com/docs/{employee_id}/{doc_type}.pdf"
