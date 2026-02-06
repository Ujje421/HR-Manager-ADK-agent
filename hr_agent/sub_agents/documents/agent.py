from google.adk.agents import Agent

document_agent = Agent(
    name="document_specialist",
    model="gemini-2.5-flash",
    description="Handles HR document requests",
    instruction="""
You provide salary slips, letters, and HR documents.

Respond ONLY in JSON:

{
  "reply_subject": "Re: Your document request",
  "reply_body": "<confirmation email>",
  "action": "send_document"
}
"""
)
