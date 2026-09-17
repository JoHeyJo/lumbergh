import os, requests
import logging
from strands import Agent, tool
from strands_tools import file_read
from strands_tools.exa import exa_search, exa_get_contents
from dotenv import load_dotenv

load_dotenv()


agent = Agent(
    system_prompt="Report tool failures rather than answering from memory",
    tools=[exa_search, exa_get_contents],
)

agent(
    """Let's get the API endpoints that you can access for these job board sites:
      career builder
    """
)

# Greenhouse: https://harvest.greenhouse.io/v1
# Indeed: https://api.indeed.com
# Jack and Jill: None,
# LinkedIn: needs login
# Ashby:  https://api.ashbyhq.com/posting-api/job-board/{JOB_BOARD_NAME}