#!/usr/bin/env python3
"""Send the commit diff to Claude and write an HTML review section."""
import os, sys, json, urllib.request

diff_file, out_file = sys.argv[1], sys.argv[2]
diff = open(diff_file).read()[:20000]
prompt = f"""You are a senior QA engineer reviewing a commit to 'QuranIndexRun1',
a static web app that fetches Quran ayahs, tafsir, and draft translations live from public APIs.
Review this diff for: bugs, edge cases, broken API URLs, XSS/injection risks (note: innerHTML is
used with fetched text), error-handling gaps, and missing tests.
Keep the review concise. Use HTML with <h3>, <p>, <ul><li> only.

COMMIT DIFF:
{diff}"""

req = urllib.request.Request(
    "https://api.anthropic.com/v1/messages",
    data=json.dumps({
        "model": "claude-sonnet-4-6",
        "max_tokens": 1500,
        "messages": [{"role": "user", "content": prompt}],
    }).encode(),
    headers={
        "x-api-key": os.environ["ANTHROPIC_API_KEY"],
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    },
)
with urllib.request.urlopen(req, timeout=120) as r:
    data = json.loads(r.read())
review = "".join(b["text"] for b in data["content"])
open(out_file, "w").write(f"<h2>AI Code Review (Claude)</h2>\n{review}")
print("AI review written to", out_file)
