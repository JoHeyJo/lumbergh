import os, requests
import logging
from strands import Agent, tool
from strands_tools import file_read, tavily
from strands_tools.exa import exa_search, exa_get_contents
from dotenv import load_dotenv



load_dotenv()

prompt = """
Extract and summarize the top 10 software engineer job listings on Indeed using the tavily tool.
"""

print(prompt)
agent = Agent(
    system_prompt="Report tool failures rather than answering from memory.",
    tools=[tavily],
)

agent(prompt)
