# Quran Index — Working Prototype (v0.1)

This is a live, deployable proof-of-concept for the Global Quranic Concordance Platform described in the project charter. It is intentionally small — 5 sample concepts — so you can test the core idea (and show it to your father and advisors) before committing to the full build.

## What it actually does

No fake data. Every ayah and every tafsir excerpt is fetched live, in the browser, from public APIs:

1. You pick a concept (e.g. "Patience").
2. The app calls **api.alquran.cloud** for the Arabic ayah (Uthmani script), by exact surah:ayah reference.
3. It calls **spa5k/tafsir_api** (served via jsDelivr) for the matching entry in **Tafsir Ibn Kathir**.
4. It sends *that tafsir excerpt* — not an existing Quran translation — to **MyMemory Translation Memory** to produce a draft translation in your chosen language.
5. Every draft is labeled "pending scholar review." Nothing is presented as final.

This matches the sourcing principle from the charter: **tafsir first, translation second** — the meaning comes from classical exegesis, and translation is a downstream step applied to that meaning, not an upstream shortcut through someone else's translation.

## Run it locally

Static site, no build step. You just need a local server (browsers block `fetch()` of local JSON files opened via `file://`):

```bash
cd ayaatmap
python3 -m http.server 8000
# open http://localhost:8000
```

## Deploy to GitHub Pages (5 minutes)

1. Create a new repo, e.g. `ayaatmap`.
2. Push these two files/folders to the repo root: `index.html`, `data/concepts.json`, `README.md`.
3. In the repo: **Settings → Pages → Source → Deploy from a branch → main → / (root)**.
4. Your prototype will be live at `https://<your-username>.github.io/ayaatmap/` within a minute or two.

No server, no database, no API keys, no cost. This is deliberate — it proves the concept without committing budget.

## Extending it toward the full charter

- Swap `data/concepts.json` for your father's digitized index (same shape: `id`, `canonical_name`, `malayalam_name`, `arabic_root`, `occurrences`).
- Add more tafsir sources by changing `TAFSIR_SLUG` — spa5k/tafsir_api serves 25+ tafsirs (Ibn Kathir, Tabari, Qurtubi, Al-Muyassar, and non-Arabic ones like Urdu's Bayan-ul-Quran). Showing 2–3 tafsirs side by side is a natural next step and directly supports the "multi-scholar review" mitigation in the charter's risk register.
- Replace MyMemory (a demo-grade MT service) with a proper NMT provider once budget allows — this is the one component in this prototype that is explicitly not production-grade.
- The cross-reference engine, root-based search, and offline mode from the charter are not in this prototype; it exists to validate the sourcing pipeline first.
