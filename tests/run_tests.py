#!/usr/bin/env python3
"""
QuranIndexRun1 — automated test suite.
Tests:
  1. concepts.json  -> valid JSON, required fields, surah 1-114, ayah in valid range
  2. Live API       -> every (surah, ayah) occurrence resolves on alquran.cloud + tafsir_api
  3. Live API       -> MyMemory translation endpoint responds for each supported lang
Writes: results JSON + HTML body fragment for the report.
"""
import json, sys, argparse, datetime, urllib.request, urllib.error

# --- valid ayah counts per surah (to validate references) ---
from itertools import accumulate
COUNTS = [7,286,200,176,120,165,206,75,129,109,123,111,43,52,99,128,111,110,98,135,
112,78,118,64,77,227,93,88,69,60,34,30,73,54,45,83,182,88,75,85,54,53,89,59,37,35,
38,29,18,45,60,49,62,55,78,96,29,22,24,13,14,11,11,18,12,12,30,52,52,44,28,28,20,56,
40,31,50,40,46,42,29,19,36,25,22,17,19,26,30,20,15,21,11,8,8,19,5,8,8,11,11,8,3,9,5,4,
7,3,6,3,5,4,5,6]
TOTALS = list(accumulate(COUNTS))

def valid_ref(s, a):
    return 1 <= s <= 114 and 1 <= a <= COUNTS[s-1]

def check_url(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": "quranindex-ci/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status == 200, r.status
    except urllib.error.HTTPError as e:
        return False, e.code
    except Exception as e:
        return False, str(e)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default="tests/results.json")
    ap.add_argument("--html", default="tests/report_body.html")
    args = ap.parse_args()

    results = {"time": datetime.datetime.now().isoformat(), "tests": []}
    def log(name, ok, detail=""):
        results["tests"].append({"name": name, "pass": bool(ok), "detail": detail})
        print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}")

    # ── 1. Load & validate concepts.json ──────────────────────────
    try:
        concepts = json.load(open("data/concepts.json"))
        log("concepts.json parses as valid JSON", True, f"{len(concepts)} concepts")
    except Exception as e:
        log("concepts.json parses as valid JSON", False, str(e))
        concepts = []

    ids = set()
    required = ["id", "canonical_name", "malayalam_name", "arabic_root", "occurrences"]
    for c in concepts:
        cid = c.get("id", "<missing>")
        missing = [k for k in required if k not in c]
        log(f"[{cid}] has all required fields", not missing, f"missing: {missing}" if missing else "")
        dup = cid in ids; ids.add(cid)
        log(f"[{cid}] id is unique", not dup, "duplicate id" if dup else "")
        occ = c.get("occurrences", [])
        log(f"[{cid}] has at least 1 occurrence", len(occ) >= 1, f"{len(occ)} occurrences")
        for o in occ:
            s, a = o.get("surah"), o.get("ayah")
            log(f"[{cid}] ref {s}:{a} is a valid Quran reference", valid_ref(s, a),
                "" if valid_ref(s, a) else f"surah has {COUNTS[s-1]} ayahs" if 1 <= (s or 0) <= 114 else "surah out of range")

    # ── 2. Live API tests for every occurrence ────────────────────
    langs = ["ml", "ur", "id", "tr", "fr"]
    for c in concepts:
        for o in c.get("occurrences", []):
            s, a = o["surah"], o["ayah"]
            ok, d = check_url(f"https://api.alquran.cloud/v1/ayah/{s}:{a}/quran-uthmani")
            log(f"API ayah {s}:{a} (alquran.cloud)", ok, d)
            ok, d = check_url(f"https://cdn.jsdelivr.net/gh/spa5k/tafsir_api@main/tafsir/en-tafisr-ibn-kathir/{s}/{a}.json")
            log(f"API tafsir {s}:{a} (Ibn Kathir)", ok, d)

    # ── 3. MyMemory translation endpoint (one probe per lang) ─────
    q = urllib.parse.quote("In the name of God, the Most Gracious, the Most Merciful") if False else None
    import urllib.parse
    q = urllib.parse.quote("the patient will be rewarded")
    for lang in langs:
        ok, d = check_url(f"https://api.mymemory.translated.net/get?q={q}&langpair=en|{lang}")
        log(f"MyMemory translation en->{lang}", ok, d)

    # ── write outputs ─────────────────────────────────────────────
    npass = sum(1 for t in results["tests"] if t["pass"])
    results["summary"] = {"total": len(results["tests"]), "passed": npass,
                          "failed": len(results["tests"]) - npass}
    json.dump(results, open(args.json, "w"), indent=2)

    # HTML fragment
    rows = "".join(
        f"<tr class='{'pass' if t['pass'] else 'fail'}'><td>{'PASS' if t['pass'] else 'FAIL'}</td>"
        f"<td>{t['name']}</td><td>{t['detail']}</td></tr>" for t in results["tests"])
    html = f"""<h2>Automated Test Results</h2>
<p><b>{npass} / {len(results['tests'])} passed</b> · run at {results['time']}</p>
<table><tr><th>Result</th><th>Test</th><th>Detail</th></tr>{rows}</table>"""
    open(args.html, "w").write(html)
    print(f"\n{npass}/{len(results['tests'])} passed")
    sys.exit(0 if npass == len(results["tests"]) else 1)

if __name__ == "__main__":
    main()
