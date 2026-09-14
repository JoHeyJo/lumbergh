import os
from exa_py import Exa
from dotenv import load_dotenv
load_dotenv()
exa = Exa(api_key=os.environ.get("EXA_API_KEY"))



results = exa.search(
    "recent product announcements from developer tools companies",
    include_domains=[
        "https://www.financialcontent.com/article/bizwire-2026-9-14-sourcegraph-announces-general-availability-of-agentic-batch-changes-the-ai-agent-for-large-scale-code-changes-across-enterprise-codebases"
    ],
    type="auto",
    num_results=10,
    contents={"highlights": True},
)

for result in results.results:
    print(result.title, result.url)


