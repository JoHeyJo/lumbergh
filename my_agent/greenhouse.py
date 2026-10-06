"""Greenhouse adapter. One public function: fetch_board(slug) -> list[Listing].

Greenhouse's public board API needs no key:
  GET https://boards-api.greenhouse.io/v1/boards/{slug}            -> {"name": "Acme", ...}
  GET https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true
      -> {"jobs": [{"id", "title", "absolute_url", "location": {"name"}, "content", ...}]}

`content` is HTML that has been entity-escaped, so it needs html.unescape() and then tag stripping.
"""

import html
import json
from datetime import date, datetime
from html.parser import HTMLParser

import httpx

from config import settings
from models import Listing

BASE = "https://boards-api.greenhouse.io/v1/boards"


class _TextExtractor(HTMLParser):
    """Strip tags, keep line breaks at block boundaries. Stdlib only; no bs4."""

    BLOCK = {"p", "div", "li", "br", "h1", "h2", "h3", "h4", "ul", "ol", "tr"}

    def __init__(self):
        super().__init__()
        self.parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in self.BLOCK:
            self.parts.append("\n")

    def handle_data(self, data):
        self.parts.append(data)

    def text(self) -> str:
        lines = (ln.strip() for ln in "".join(self.parts).splitlines())
        return "\n".join(ln for ln in lines if ln)


def html_to_text(escaped_html: str) -> str:
    p = _TextExtractor()
    p.feed(html.unescape(escaped_html))
    return p.text()


def _get_cached(slug: str) -> dict:
    """Raw API payloads, cached per slug per day. Phase 7 may swap this for something smarter."""
    cache_dir = settings.data_dir / "greenhouse"
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / f"{slug}-{date.today().isoformat()}.json"
    if path.exists():
        return json.loads(path.read_text())

    with httpx.Client(timeout=30) as client:
        board = client.get(f"{BASE}/{slug}")
        board.raise_for_status()  # 404 here means the slug is wrong — fail loudly
        jobs = client.get(f"{BASE}/{slug}/jobs", params={"content": "true"})
        jobs.raise_for_status()

    payload = {"board": board.json(), "jobs": jobs.json()["jobs"]}
    path.write_text(json.dumps(payload))
    return payload


def fetch_board(slug: str) -> list[Listing]:
    payload = _get_cached(slug)
    company = payload["board"]["name"]
    now = datetime.now()
    return [
        Listing(
            id=f"greenhouse:{slug}:{j['id']}",
            source="greenhouse",
            company=company,
            title=j["title"],
            url=j["absolute_url"],
            description=html_to_text(j.get("content", "")),
            location=(j.get("location") or {}).get("name"),
            fetched_at=now,
        )
        for j in payload["jobs"]
    ]


if __name__ == "__main__":
    # Five boards with a steady flow of entry/mid software roles. If one 404s, swap it for an alternate:
    # stripe, reddit, coinbase, mongodb, twilio.
    SLUGS = ["cloudflare", "figma", "discord", "duolingo", "databricks"]

    total = 0
    for slug in SLUGS:
        listings = fetch_board(slug)
        total += len(listings)
        eng = [l for l in listings if "engineer" in l.title.lower()]
        print(
            f"{slug:12} {len(listings):4} listings  {len(eng):4} with 'engineer' in title  ({listings[0].company})"
        )
        for l in eng[:3]:
            print(f"{'':12} - {l.title}  [{l.location}]")
    print(f"\n{total} listings total")

    # Eyeball one description to confirm the HTML stripping is sane.
    sample = next(l for l in fetch_board(SLUGS[0]) if "engineer" in l.title.lower())
    print(f"\n--- {sample.title} ({sample.url}) ---\n{sample.description[:1500]}")
