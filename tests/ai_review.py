#!/usr/bin/env python3
"""
Free AI review step — sends the commit diff to the Google Gemini API free tier.
No paid account needed: get a free API key at https://aistudio.google.com/apikey
then add it as a repo secret named GEMINI_API_KEY
(Settings -> Secrets and variables -> Actions -> New repository secret).

Usage: python tests/ai_review.py commit.diff tests/ai_review.html
"""
import os, sys, json, urllib.request

diff_file, out_file = sys.argv[1], sys.argv[2]
diff = open(diff_file).read()[:20000]

prompt = f"""You are a senior QA engineer reviewing a commit to 'QuranIndexRun1',
a static web app that fetches Quran ayahs, tafsir, and draft translations live from public APIs.
Review this diff for: bugs, edge cases, broken API URLs, XSS/injection risks
(note: innerHTML is used with fetched text), error-handling gaps, and missing tests.
Keep the review concise. Respond with HTML using only <h3>, <p>, <ul>, <li> tags.

COMMIT DIFF:
{diff}"""

api_key = os.environ["GEMINI_API_KEY"]
url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
       f"gemini-2.5-flash:generateContent?key={api_key}")
req = urllib.request.Request(
    url,
    data=json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 1500, "temperature": 0.2},
    }).encode(),
    headers={"Content-Type": "application/json"},
)
with urllib.request.urlopen(req, timeout=120) as r:
    data = json.loads(r.read())
review = data["candidates"][0]["content"]["parts"][0]["text"]
open(out_file, "w").write(f"<h2>AI Code Review (Gemini)</h2>\n{review}")
print("AI review written to", out_file)
