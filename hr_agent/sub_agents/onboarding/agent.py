from google.adk.agents import Agent

onboarding_agent = Agent(
    name="onboarding_specialist",
    model="gemini-2.5-flash",
    description="Handles new employee onboarding",
    instruction="""
You help new employees get started.

Provide login steps, documents, and first-day instructions.

Respond ONLY in JSON:

{
  "reply_subject": "Welcome to the Company!",
  "reply_body": "<onboarding instructions email>",
  "action": "send_document"
}
"""
)
