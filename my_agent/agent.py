import os, requests
import logging
from strands import Agent, tool
from strands_tools import file_read
from strands_tools.exa import exa_search, exa_get_contents
from dotenv import load_dotenv
import asyncio, os, aiohttp

load_dotenv()


k = os.environ.get("EXA_API_KEY")

async def t():
    async with aiohttp.ClientSession() as s:
        async with s.post(
            "https://api.exa.ai/search",
            headers={"x-api-key": os.environ["EXA_API_KEY"]},
            json={"query": "test", "numResults": 1},
        ) as r:
            print("=====",r.status, (await r.text())[:200])


asyncio.run(t())

r = requests.post(
    "https://api.exa.ai/search",
    headers={
        "x-api-key": os.environ["EXA_API_KEY"],
        "Content-Type": "application/json",
    },
    json={"query": "test", "numResults": 1},
)
print(">>>>>", r.status_code, r.text[:300])

# Enables Strands debug log level
logging.getLogger("strands").setLevel(logging.DEBUG)

# Sets the logging format and streams logs to stderr
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s", handlers=[logging.StreamHandler()]
)

agent = Agent(tools=[exa_search, exa_get_contents])

agent("Search for 5 job listing websites")
