#!/usr/bin/env python3
"""
Step 1 — search ATS job-board domains by ROLE, not by company.

The Google equivalent of what this does:
    site:job-boards.greenhouse.io "Senior Backend Engineer" Rust remote

Note that the domain restriction goes in Tavily's include_domains parameter,
NOT in the query string. Tavily does not parse `site:` operators; putting one
in the query just adds noise that competes for relevance.

Usage:
    export TAVILY_API_KEY=tvly-...
    python search_boards.py "Senior Backend Engineer Rust remote"
    python search_boards.py "ML Engineer" --platform greenhouse lever --max 20
    python search_boards.py "Platform Engineer" --json
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from tavily import TavilyClient

# Search both Greenhouse domains: they migrated to job-boards.greenhouse.io,
# but boards.greenhouse.io still resolves and is still heavily indexed.
PLATFORM_DOMAINS: dict[str, list[str]] = {
    "greenhouse": ["job-boards.greenhouse.io", "boards.greenhouse.io"],
    "lever": ["jobs.lever.co", "jobs.eu.lever.co"],
    "ashby": ["jobs.ashbyhq.com"],
    "smartrecruiters": ["jobs.smartrecruiters.com"],
}


def search_boards(
    query: str,
    platforms: list[str] | None = None,
    max_results: int = 20,
) -> list[dict]:
    """Search ATS board domains for a role description.

    Returns raw Tavily results (title, url, content, score). Slug extraction
    is deliberately NOT done here — that's the next step.

    search_depth is "basic" and include_raw_content is False because we only
    care about the URLs. Paying for page bodies we'd discard is waste.
    """
    platforms = platforms or ["greenhouse"]
    unknown = set(platforms) - PLATFORM_DOMAINS.keys()
    if unknown:
        raise ValueError(f"unknown platform(s): {sorted(unknown)}")

    domains = [d for p in platforms for d in PLATFORM_DOMAINS[p]]

    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        raise RuntimeError("TAVILY_API_KEY is not set")

    resp = TavilyClient(api_key=api_key).search(
        query=query,
        include_domains=domains,
        max_results=max_results,
        search_depth="basic",
        include_raw_content=False,
    )

    # Dedupe on URL, preserving rank order.
    seen: set[str] = set()
    out: list[dict] = []
    for r in resp.get("results", []):
        url = r.get("url", "")
        if url and url not in seen:
            seen.add(url)
            out.append(r)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("query", help='e.g. "Senior Backend Engineer Rust remote"')
    ap.add_argument(
        "--platform",
        "-p",
        nargs="+",
        default=["greenhouse"],
        choices=sorted(PLATFORM_DOMAINS),
        help="ATS domains to search",
    )
    ap.add_argument("--max", "-n", type=int, default=20, help="max results")
    ap.add_argument("--json", action="store_true", help="dump raw JSON")
    args = ap.parse_args()

    try:
        results = search_boards(args.query, args.platform, args.max)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(results, indent=2))
        return 0

    domains = [d for p in args.platform for d in PLATFORM_DOMAINS[p]]
    print(f"query    : {args.query}")
    print(f"domains  : {', '.join(domains)}")
    print(f"results  : {len(results)}\n")
    for i, r in enumerate(results, 1):
        print(f"{i:>3}. {r['url']}")
        print(f"     {r.get('title', '')[:100]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
