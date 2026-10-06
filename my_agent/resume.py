"""Résumé → ResumeProfile. One public function: load_profile(pdf_path) -> ResumeProfile.

The PDF goes to Bedrock as a document content block; Strands' structured_output() forces the reply
into the ResumeProfile schema. Result is cached on the SHA-256 of the PDF bytes, so the model is
called once per résumé version, ever.
"""

import hashlib
import sys
from pathlib import Path

from strands import Agent
from strands.models import BedrockModel

from config import settings
from models import ResumeProfile
from agent import agent



def load_profile(pdf_path: Path) -> ResumeProfile:
    pdf_bytes = pdf_path.read_bytes()
    digest = hashlib.sha256(pdf_bytes).hexdigest()[:16]

    cache_dir = settings.data_dir / "profiles"
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / f"{digest}.json"
    if cache_path.exists():
        return ResumeProfile.model_validate_json(cache_path.read_text())

    profile = agent().structured_output(
        ResumeProfile,
        [
            {
                "document": {
                    "format": "pdf",
                    "name": "resume",
                    "source": {"bytes": pdf_bytes},
                }
            },
            {"text": "Convert this résumé into a ResumeProfile."},
        ],
    )
    cache_path.write_text(profile.model_dump_json(indent=2))
    return profile


if __name__ == "__main__":
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("resume.pdf")
    profile = load_profile(path)
    text = profile.model_dump_json(indent=2)
    print(text)
    print(f"\n~{len(text) // 4} tokens")  # rough: 4 chars/token. Target is under ~500.
