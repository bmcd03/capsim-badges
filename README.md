# Capsim Digital Badge Prototype

Zero-platform-fee digital badging for Capstone: students get a public credential
page and a one-click "Add to LinkedIn" button. No Capsim platform dev — the
generator runs on standard course exports.

## What's here

| Path | What it is |
|---|---|
| `generate.py` | The pipeline: exports in → credential pages + mail-merge CSV out |
| `sample_data/` | Fake completion roster + team standings (stand-ins for real Capsim exports) |
| `assets/` | Badge artwork (participation + first-place SVGs) |
| `badges/` | Generated credential pages (one per student per badge) + demo index |
| `linkedin_merge.csv` | Generated: one row per credential with the personalized Add-to-LinkedIn URL — feed this to any mail-merge/email tool |

## Run it

```
py generate.py
```

Local preview: `py -m http.server 8931 --directory .` then open
http://localhost:8931/badges/index.html

## Deploy the prototype to GitHub Pages

1. Create a public GitHub repo named `capsim-badges`.
2. In `generate.py`, set `BASE_URL = "https://<your-github-username>.github.io/capsim-badges"` and re-run `py generate.py`.
3. Push this folder to the repo (main branch).
4. Repo Settings → Pages → Source: "Deploy from a branch" → main / root → Save.
5. After a minute, credential pages are live at
   `https://<user>.github.io/capsim-badges/badges/<CREDENTIAL-ID>.html`
   and the Add-to-LinkedIn buttons work end to end.

## How each term works (production vision)

1. Pull the end-of-course completion roster and team standings exports.
2. Drop them in `sample_data/` (same column layout) and run `py generate.py`.
3. Upload the new `badges/` pages to the web host (later: capsim.com/badges).
4. Send the congratulations email using `linkedin_merge.csv` — each row has the
   student's personal `add_to_linkedin_url`.

## Notes

- Credential IDs are deterministic (hash of email + badge + term): re-running
  the generator never changes an already-issued URL.
- First-place students receive BOTH badges (participant + first place).
- The LinkedIn button pre-fills name, issuer, date, credential ID and URL;
  the student just clicks Save. LinkedIn requires no badging platform for this.
- For production, `organizationName` in `generate.py` can be swapped for
  LinkedIn's numeric `organizationId` of the Capsim company page so the badge
  entry links to Capsim's LinkedIn page with logo.
