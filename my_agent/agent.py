import os, requests
import logging
from strands import Agent, tool
from strands_tools import file_read, tavily
from strands_tools.exa import exa_search, exa_get_contents
from dotenv import load_dotenv



load_dotenv()

if not os.getenv("TAVILY_API_KEY"):
    raise ValueError("TAVILY_API_KEY environment variable is required")


prompt = """
Extract the top 5 software engineer job listings on Indeed. Return an object with:
job title, company, role, summarize blurb of company info/purpose,
role requirements, qualifications, preferred qualification(nice to have),
link to the job listing.
"""

print(prompt)
agent = Agent(
    system_prompt="Report tool failures rather than answering from memory.",
    tools=[tavily],
)

agent(prompt)
