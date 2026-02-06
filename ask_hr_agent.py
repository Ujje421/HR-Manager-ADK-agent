import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

# 🔹 CONFIGURATION
ADK_BASE = os.getenv("ADK_BASE_URL", "http://localhost:8000")
APP_NAME = "hr_agent"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")  # your Gmail address
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # app password

# 🔹 FUNCTION — Get HR reply from ADK
def get_hr_reply(email_text: str, sender_email: str, session_id: str) -> dict:
    """
    Sends email text to ADK HR agent and extracts a safe reply.
    Returns dict: {"subject": str, "body": str, "action": "reply"|"ignore"}
    """
    try:
        # Ensure session exists
        session_url = f"{ADK_BASE}/apps/{APP_NAME}/users/{sender_email}/sessions/{session_id}"
        requests.post(session_url, timeout=10)

        # Send message to ADK
        run_url = f"{ADK_BASE}/run"
        payload = {
            "appName": APP_NAME,
            "userId": sender_email,
            "sessionId": session_id,
            "newMessage": {
                "role": "user",
                "parts": [{"text": email_text}]
            }
        }

        response = requests.post(run_url, json=payload, timeout=30)
        response.raise_for_status()
        raw_data = response.json()
        print("🧠 ADK RAW RESPONSE:", raw_data)

        # Extract text safely
        def extract_text(item: dict) -> str | None:
            content = item.get("content", {})
            parts = content.get("parts", [])
            for part in parts:
                func_resp = part.get("functionResponse", {}).get("response", {})
                if func_resp.get("result"):
                    return func_resp["result"].strip()
                if part.get("text"):
                    return part["text"].strip()
            return None

        agent_text = None
        if isinstance(raw_data, list):
            for item in reversed(raw_data):
                agent_text = extract_text(item)
                if agent_text:
                    break
        elif isinstance(raw_data, dict):
            agent_text = extract_text(raw_data)

        # Handle empty or IGNORE_EMAIL
        if not agent_text or agent_text.upper() == "IGNORE_EMAIL":
            return {"subject": "", "body": "", "action": "ignore"}

        # Try to parse JSON from agent_text
        try:
            parsed = json.loads(agent_text)
            subject = parsed.get("subject", "Re: Your HR Request")
            body = parsed.get("body", "")
        except (json.JSONDecodeError, TypeError):
            # fallback to plain text
            subject = "Re: Your HR Request"
            body = agent_text

        return {
            "subject": subject,
            "body": body,
            "action": "reply"
        }

    except requests.RequestException as req_err:
        print("❌ Network/HTTP Error:", req_err)
        return {"subject": "", "body": "", "action": "ignore"}
    except Exception as e:
        print("❌ HR Agent Error:", e)
        return {"subject": "", "body": "", "action": "ignore"}

# 🔹 FUNCTION — Send email via Gmail
def send_email(to: str, subject: str, body: str):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        print(f"✅ Email sent to {to}")

# 🔹 MAIN LOOP — Example Gmail listener
def process_incoming_email(email_text: str, sender_email: str, session_id: str):
    reply = get_hr_reply(email_text, sender_email, session_id)

    if reply["action"] == "ignore":
        print(f"ℹ️ Skipping email from {sender_email} — no HR action required")
        return

    send_email(
        to=sender_email,
        subject=reply["subject"],
        body=reply["body"]
    )

# 🔹 MOCK TEST
if __name__ == "__main__":
    # Example incoming email
    incoming_text = "Hi HR, I need my login credentials and welcome kit."
    sender = "employee@example.com"
    session = "session123"

    process_incoming_email(incoming_text, sender, session)
