# 🤖 AI HR Email Auto-Responder

This project connects a Gmail inbox with an AI HR Agent (ADK-based) to automatically read employee emails and send intelligent HR-style replies such as:

- Welcome emails  
- Login credential guidance  
- Leave clarification requests  
- General HR onboarding help  

The system ensures clean human-readable emails are sent — even if the AI agent returns JSON.

---

## 🚀 How It Works

1. An incoming employee email is received.
2. The email text is sent to the HR AI Agent running on ADK.
3. The AI generates a response (sometimes in JSON format).
4. The system extracts:
   - subject
   - body
5. A properly formatted email is sent back to the employee via Gmail SMTP.

---

## 📦 Features

✅ Connects to ADK AI agent  
✅ Handles raw JSON responses from the agent  
✅ Converts AI output into a clean HR email  
✅ Sends emails using Gmail SMTP  
✅ Ignores emails when AI says no response is needed  

---

## 🛠 Requirements

- Python 3.10+
- A running ADK agent server
- Gmail account with App Password enabled

Install dependencies:

pip install requests

(Other libraries like smtplib and email come built into Python.)

---

## ⚙️ Environment Variables

Set these before running:

Variable        Description
ADK_BASE_URL    URL of your ADK server (default: http://localhost:8000)
EMAIL_ADDRESS   Your Gmail address used to send emails
EMAIL_PASSWORD  Gmail App Password (NOT your real Gmail password)

### Example (Mac/Linux)

export EMAIL_ADDRESS="yourgmail@gmail.com"
export EMAIL_PASSWORD="your_app_password"
export ADK_BASE_URL="http://localhost:8000"

### Example (Windows PowerShell)

setx EMAIL_ADDRESS "yourgmail@gmail.com"
setx EMAIL_PASSWORD "your_app_password"
setx ADK_BASE_URL "http://localhost:8000"

---

## 🧠 AI Agent Response Format

Your HR agent can return either:

### Option 1 — Plain Text

Welcome to the company! Here are your login steps...

### Option 2 — JSON (Recommended)

{
  "subject": "Welcome to the Company 🎉",
  "body": "Dear Employee,\n\nHere are your login credentials...",
  "action": "reply"
}

The system automatically detects and formats both correctly.

---

## ▶️ Running the Script

python your_script_name.py

Example test inside the script:

incoming_text = "Hi HR, I need my login credentials and welcome kit."
sender = "employee@example.com"
session = "session123"

---

## 📧 Email Flow

Step 1: Employee sends email  
Step 2: Email text goes to ADK HR Agent  
Step 3: Agent generates response  
Step 4: System extracts subject & message  
Step 5: Clean email is sent via Gmail  

---

## 🛡 Error Handling

The system safely handles:

- ADK server failures  
- Network timeouts  
- Invalid JSON from agent  
- Empty responses  
- "IGNORE_EMAIL" signals  

If something goes wrong, the email is skipped instead of crashing.

---

## 🔮 Future Improvements

- Connect to real Gmail inbox via IMAP listener  
- Add HTML email formatting  
- Store email logs in a database  
- Add multiple HR agents (Payroll, IT Support, etc.)  
- Web dashboard for monitoring conversations  

---

## 👨‍💻 Author
Developer - Ujjwal Jagtap

Built as an AI HR Automation System using:
- Python
- Gmail SMTP
- ADK Agent Framework
