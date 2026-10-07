from strands import Agent
from models import ResumeProfile

SYSTEM_PROMPT = """
Convert a résumé into a compact, factual profile.
Rules:
- Only record what the résumé states. Do not infer skills, seniority, or years not written there.
- Every list entry is one short, self-contained line that could be quoted as evidence on its own.
- experience: one line per role, formatted "Title, Company, start–end: 2–4 concrete things done."
  Keep the dates exactly as written.
- skills: concrete technologies, languages, tools. No soft skills.
- education: degree, school, year if given.
- other: certifications, work authorization, languages, publications — only if explicitly stated.
- Leave a list empty rather than guess.
- Report tool failures rather than answering from memory."""

agent = Agent(system_prompt=SYSTEM_PROMPT, structured_output_model=ResumeProfile, callback_handler=None)

