import os, requests
import logging
from strands import Agent, tool
from strands_tools import file_read
from strands_tools.exa import exa_search, exa_get_contents
from dotenv import load_dotenv

load_dotenv()

# sites = {"indeed": None, "greenhouse": "https://job-boards.greenhouse.io/greenhouse"}

# prompt = """
# Extract and summarize software engineer roles at a Greenhouse. Try its ATS API first, then crawl
#     its careers page. Return the public ATS API or None if none exists. Also, return 
# """

# prompt = """Extract and summarize 20 software engineer roles from this public ATS API:
# https://boards-api.greenhouse.io/v1/boards/greenhouse/jobs?content=true
#  """
# prompt = """Extract and summarize top 5 software engineer roles from each:
# Indeed, ZipRecruiter, my.greenhouse.io, https://hiringcafe.com/, Wellfound, CalJOBS, Jack and Jill. 
#  """

prompt = """Find public ATS API. Return object mapping company name
endpoint. Only include those were you can query all their listings in a single
request similar to Greenhouse.
"""

print(prompt)
agent = Agent(
    system_prompt="Report tool failures rather than answering from memory.",
    tools=[exa_search, exa_get_contents],
)

agent(prompt)

# Greenhouse: https://boards.greenhouse.io/greenhouse
# Indeed: https://api.indeed.com
# Jack and Jill: None,
# LinkedIn: needs login
# Ashby:  https://api.ashbyhq.com/posting-api/job-board/{JOB_BOARD_NAME}