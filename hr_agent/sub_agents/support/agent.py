from google.adk.agents import Agent

support_agent = Agent(
    name="hr_support_specialist",
    model="gemini-2.5-flash",
    description="Handles general HR queries",
    instruction="""
You answer general HR questions professionally.

Respond ONLY in JSON:

{
  "reply_subject": "Re: Your HR query",
  "reply_body": "<helpful HR response>",
  "action": "none"
}
"""
)
