import os
from strands import Agent, tool
from strands_tools import file_read
from strands_tools.exa import exa_search, exa_get_contents
from dotenv import load_dotenv
load_dotenv()

import boto3


# Create an agent with tools from the community-driven strands-tools package
# as well as our custom letter_counter tool
agent = Agent(tools=[exa_search, exa_get_contents])

# Ask the agent a question that uses the available tools
message = """
Can you find all recent software engineer roles posted on https://www.greenhouse.com/?
"""
agent(message)
