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

agent("Extract and summarize content of https://www.joannesfigueroa.com/")
