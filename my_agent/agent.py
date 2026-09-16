import os, requests
import logging
from strands import Agent, tool
from strands_tools import file_read
from strands_tools.exa import exa_search, exa_get_contents
from dotenv import load_dotenv
import asyncio, os, aiohttp

load_dotenv()




agent = Agent(tools=[exa_search, exa_get_contents])

agent("Search for 5 job listing websites")
