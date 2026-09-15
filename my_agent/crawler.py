import os
from exa_py import Exa
from dotenv import load_dotenv
load_dotenv()
exa = Exa(api_key=os.environ.get("EXA_API_KEY"))



# response = exa.search(
#     "Find software engineer roles. Open the post and return the jobs responsibilities.",
#     include_domains=["https://www.greenhouse.com/careers"],
#     type="auto",
#     num_results=5,
#     contents={
#         "highlights": True,
#         "subpages": 10,
#         "subpage_target": ["job", "position", "opening"],
#         "livecrawl": "fallback",
#     },
# )

# response = exa.search(
#     "Find software engineer roles.",
#     include_domains=["https://www.greenhouse.com"],
#     num_results=10,
#     contents={
#         "subpages": 10,
#         "subpage_target": ["job", "position", "opening"],
#         "text": True,
#         "extras": {"links": 50},
#     },
# )

exa.get_contents(
    ["https://www.greenhouse.com"],
    text=True,
    subpages=20,
    subpage_target=["job", "position", "opening"],
    livecrawl="always",
)


for result in response.results:
    print(f"result: {result}")
    # print(f"Title: {result.title}")
    # print(f"URL: {result.url}")
    # if result.highlights:
    #     print(f"Highlight: {result.highlights}")
    print("-" * 40)
