#!/usr/bin/env python3
"""Merge all report sections into one styled HTML, then print PDF via wkhtmltopdf."""
import subprocess, pathlib, datetime

def read(p):
    return pathlib.Path(p).read_text() if pathlib.Path(p).exists() else ""

ai = read("tests/ai_review.html") or "<h2>AI Code Review (Claude)</h2><p><i>Skipped — set the ANTHROPIC_API_KEY secret to enable.</i></p>"
body = read("tests/report_body.html")

diff_stat = ""
try:
    diff_stat = subprocess.check_output(
        ["git", "diff", "--stat", "HEAD~1", "HEAD"], text=True, stderr=subprocess.DEVNULL)
except Exception:
    pass

html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
body {{ font-family: Helvetica, Arial, sans-serif; font-size: 12px; color: #1E293B; margin: 40px; }}
h1 {{ color: #10235c; border-bottom: 3px solid #2b79ff; padding-bottom: 8px; }}
h2 {{ color: #2b79ff; margin-top: 28px; }}
table {{ border-collapse: collapse; width: 100%; margin-top: 10px; }}
th, td {{ border: 1px solid #E2E8F0; padding: 6px 10px; text-align: left; }}
th {{ background: #F1F5F9; }}
tr.pass td:first-child {{ color: #10B981; font-weight: bold; }}
tr.fail td:first-child {{ color: #EF4444; font-weight: bold; background: #FEF2F2; }}
pre {{ background: #F8FAFC; padding: 12px; border-radius: 8px; font-size: 10px; }}
.meta {{ color: #64748B; font-size: 11px; }}
</style></head><body>
<h1>QuranIndexRun1 — Commit Test Report</h1>
<p class="meta">Generated {datetime.datetime.now():%Y-%m-%d %H:%M} · commit {open("/dev/stdin").read() if False else ""}
{subprocess.check_output(["git","rev-parse","--short","HEAD"], text=True).strip()}</p>
<h2>Commit Summary (git diff --stat)</h2><pre>{diff_stat or "(first commit or no diff)"}</pre>
{body}
{ai}
</body></html>"""
pathlib.Path("tests/report.html").write_text(html)
subprocess.run(["wkhtmltopdf", "--enable-local-file-access", "tests/report.html", "test-report.pdf"], check=True)
print("PDF built: test-report.pdf")
