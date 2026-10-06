from strands import Agent, tool
from strands_tools import file_read
from strands_tools.exa import exa_search, exa_get_contents
from dotenv import load_dotenv
from tavily import TavilyClient

# load_dotenv()

# if not os.getenv("TAVILY_API_KEY"):
#     raise ValueError("TAVILY_API_KEY environment variable is required")


# prompt = """
# Extract the first 5 software engineer job listings on greenhouse. Return an object with:
# job title, company, summarize blurb of company info/purpose,
# role requirements, qualifications, preferred qualification(nice to have),
# link to the job listing

# never infer requirements or qualifications from a search snippet; if the posting body wasn't retrieved, leave the field null..
# """

# resp = TavilyClient(api_key=os.getenv("TAVILY_API_KEY")).search(
#     query=query,
#     include_domains=domains,
#     max_results=20,
#     search_depth="basic",
#     include_raw_content=False,
# )
SYSTEM_PROMPT = """You convert a résumé into a compact, factual profile.

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

agent = Agent(system_prompt=SYSTEM_PROMPT, callback_handler=None)

