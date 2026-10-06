import os, requests
import logging
from strands import Agent, tool
from strands_tools import file_read
from strands_tools.exa import exa_search, exa_get_contents
from dotenv import load_dotenv
from tavily import TavilyClient

# indeed = works
# greenhouse = in progress

# fetch at ATS APIs
# Prompt Notes:
# Allow agent to express "I couldn't get this"
# Company blurbs deserve their own cache keyed on company name. A company's purpose doesn't change between runs, and that alone eliminates most of your repeat searches.
# Make every extracted field Optional[str] = None, add a source: Literal["full_posting", "search_snippet"] per listing
# create fetch_ats_jobs(company_slug) tool to return clean JSON deterministically - LLM never has to decide how to get data — only how to normalize it.
# Add call budget. Make exceeding the cap return partial results with an explicit incomplete: true rather than letting the agent improvise.
# No deduplication


load_dotenv()

if not os.getenv("TAVILY_API_KEY"):
    raise ValueError("TAVILY_API_KEY environment variable is required")


# prompt = """
# Extract the first 5 software engineer job listings on greenhouse. Return an object with:
# job title, company, summarize blurb of company info/purpose,
# role requirements, qualifications, preferred qualification(nice to have),
# link to the job listing

# never infer requirements or qualifications from a search snippet; if the posting body wasn't retrieved, leave the field null..
# """

query = "Senior Backend Engineer Rust remote"
domains = ["job-boards.greenhouse.io", "boards.greenhouse.io"]

resp = TavilyClient(api_key=os.getenv("TAVILY_API_KEY")).search(
    query=query,
    include_domains=domains,
    max_results=20,
    search_depth="basic",
    include_raw_content=False,
)

print(prompt)
agent = Agent(
    system_prompt="Report tool failures rather than answering from memory.",
    tools=[tavily],
)

agent(prompt)
