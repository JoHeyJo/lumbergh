import re
from greenhouse import fetch_board
from extract import extract_requirements

years = re.compile(r"\b\d+\+?\s*(years|yrs)\b", re.I)
for l in listings:  # same ten as the script
    kept, _ = extract_requirements(l)  # cached, no model calls
    in_posting = bool(years.search(l.description))
    in_gates = any(r.gate and years.search(r.source_span) for r in kept)
    if in_posting != in_gates:
        print(f"MISMATCH  posting={in_posting} gate={in_gates}  {l.title}")
