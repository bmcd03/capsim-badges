"""Capsim badge prototype generator.

Reads a completion roster + team standings (standard Capsim-style exports),
emits:
  badges/<credential-id>.html   - one public credential page per student
  linkedin_merge.csv            - mail-merge file with personalized Add-to-LinkedIn links
  badges/index.html             - demo directory of all generated credentials

Usage:  python generate.py
"""

import csv
import hashlib
import html
import urllib.parse
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------- config ---

ROOT = Path(__file__).parent
# Where the credential pages will be publicly hosted. For the GitHub Pages
# prototype set this to e.g. "https://<user>.github.io/capsim-badges".
# In production it becomes "https://www.capsim.com/badges".
BASE_URL = "https://bmcd03.github.io/capsim-badges"

ISSUER_NAME = "Capsim Management Simulations"
ISSUE_DATE = date.today()

BADGES = {
    "participation": {
        "title": "Capstone Business Simulation — Participant",
        "image": "../assets/badge-participation.svg",
        "blurb": ("completed the Capstone Business Simulation, running a "
                  "multi-million-dollar virtual company and making integrated "
                  "decisions across R&amp;D, marketing, production, and finance "
                  "over multiple competitive rounds."),
    },
    "first_place": {
        "title": "Capstone Business Simulation — First Place Team",
        "image": "../assets/badge-first-place.svg",
        "blurb": ("led their company to a first-place finish in the Capstone "
                  "Business Simulation, outperforming competing student teams "
                  "on cumulative results across R&amp;D, marketing, production, "
                  "and finance."),
    },
}

# ------------------------------------------------------------- templates ---

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — {name}</title>
<style>
  :root {{
    /* Capsim brand: slate + blue pulled from capsim.com */
    --navy: #19262f; --navy-dark: #10181e; --red: #0050d0;
    --gold: #d9a62e; --paper: #f5f6f8; --ink: #23293a;
  }}
  * {{ box-sizing: border-box; margin: 0; }}
  body {{
    font-family: "Segoe UI", Arial, Helvetica, sans-serif;
    background: var(--paper); color: var(--ink); line-height: 1.55;
  }}
  .band {{
    background: linear-gradient(160deg, var(--navy), var(--navy-dark));
    height: 220px; text-align: center; padding-top: 30px;
  }}
  /* the served logo asset is full-color; whiten it on the dark band */
  .band img {{ height: 26px; filter: brightness(0) invert(1); }}
  .card {{
    max-width: 680px; margin: -160px auto 40px; background: #fff;
    border-radius: 14px; box-shadow: 0 10px 34px rgba(14,31,56,.18);
    padding: 44px 48px 40px; text-align: center;
  }}
  .badge-img {{ width: 220px; height: 220px; }}
  .issuer {{
    margin-top: 18px; font-size: 12px; font-weight: 700; letter-spacing: 2.5px;
    text-transform: uppercase; color: var(--red);
  }}
  h1 {{ font-size: 26px; color: var(--navy); margin-top: 6px; }}
  .earner {{ font-size: 21px; margin-top: 22px; }}
  .earner strong {{ color: var(--navy); }}
  .blurb {{ margin-top: 12px; color: #4a5163; }}
  .meta {{
    display: flex; justify-content: center; gap: 34px; flex-wrap: wrap;
    margin-top: 26px; padding-top: 22px; border-top: 1px solid #e6e9ef;
  }}
  .meta div {{ min-width: 120px; }}
  .meta .k {{ font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; color: #8a90a0; }}
  .meta .v {{ font-size: 15px; font-weight: 600; color: var(--navy); margin-top: 2px; }}
  .li-btn {{
    display: inline-block; margin-top: 30px; background: #0a66c2; color: #fff;
    font-weight: 600; font-size: 16px; text-decoration: none;
    padding: 13px 26px; border-radius: 28px;
  }}
  .li-btn:hover {{ background: #084d92; }}
  .site-link {{ margin-top: 16px; }}
  .site-link a {{ color: var(--red); font-weight: 600; font-size: 15px; text-decoration: none; }}
  .site-link a:hover {{ text-decoration: underline; }}
  .about {{
    max-width: 680px; margin: 0 auto 60px; text-align: center;
    font-size: 14px; color: #5a6172; padding: 0 24px;
  }}
  .about a {{ color: var(--red); font-weight: 600; }}
</style>
</head>
<body>
<div class="band"><img src="../assets/capsim-wordmark.png" alt="Capsim"></div>
<div class="card">
  <img class="badge-img" src="{image}" alt="{title} badge">
  <div class="issuer">{issuer}</div>
  <h1>{title}</h1>
  <p class="earner">Awarded to <strong>{name}</strong></p>
  <p class="blurb">{name_first} {blurb}</p>
  <div class="meta">
    <div><div class="k">Course</div><div class="v">{course}</div></div>
    <div><div class="k">Term</div><div class="v">{term}</div></div>
    <div><div class="k">Credential ID</div><div class="v">{cred_id}</div></div>
    <div><div class="k">Issued</div><div class="v">{issued}</div></div>
  </div>
  <a class="li-btn" href="{li_url}" target="_blank" rel="noopener">Add to LinkedIn profile</a>
  <div class="site-link"><a href="https://www.capsim.com">www.capsim.com</a></div>
</div>
<p class="about">
  The Capstone Business Simulation by <a href="https://www.capsim.com">Capsim</a> puts student
  teams in charge of a virtual company competing head-to-head across R&amp;D, marketing,
  production, and finance. This page verifies the credential shown above.
</p>
</body>
</html>
"""

# --------------------------------------------------------------- helpers ---

def credential_id(email: str, badge_key: str, term: str) -> str:
    """Deterministic, unguessable-enough ID: same input always yields same ID."""
    digest = hashlib.sha256(f"{email}|{badge_key}|{term}".encode()).hexdigest()[:8].upper()
    year = ISSUE_DATE.year
    prefix = "CAP1ST" if badge_key == "first_place" else "CAP"
    return f"{prefix}-{year}-{digest}"


def linkedin_add_url(badge_title: str, cred_id: str, cred_url: str) -> str:
    """Pre-filled LinkedIn 'Add certification' deep link."""
    params = {
        "startTask": "CERTIFICATION_NAME",
        "name": badge_title,
        "organizationName": ISSUER_NAME,
        "issueYear": ISSUE_DATE.year,
        "issueMonth": ISSUE_DATE.month,
        "certUrl": cred_url,
        "certId": cred_id,
    }
    return "https://www.linkedin.com/profile/add?" + urllib.parse.urlencode(params)


# ------------------------------------------------------------------ main ---

def main() -> None:
    roster_path = ROOT / "sample_data" / "completion_roster.csv"
    standings_path = ROOT / "sample_data" / "team_standings.csv"
    out_dir = ROOT / "badges"
    out_dir.mkdir(exist_ok=True)

    with open(standings_path, newline="", encoding="utf-8-sig") as f:
        winners = {r["team"].strip() for r in csv.DictReader(f) if r["rank"].strip() == "1"}

    with open(roster_path, newline="", encoding="utf-8-sig") as f:
        students = [r for r in csv.DictReader(f) if r.get("email", "").strip()]

    merge_rows = []
    index_items = []

    for s in students:
        first, last = s["first_name"].strip(), s["last_name"].strip()
        email, team, term = s["email"].strip().lower(), s["team"].strip(), s["term"].strip()
        earned = ["participation"] + (["first_place"] if team in winners else [])

        for key in earned:
            badge = BADGES[key]
            cred_id = credential_id(email, key, term)
            cred_url = f"{BASE_URL}/badges/{cred_id}.html"
            li_url = linkedin_add_url(badge["title"], cred_id, cred_url)

            page = PAGE_TEMPLATE.format(
                title=html.escape(badge["title"]),
                name=html.escape(f"{first} {last}"),
                name_first=html.escape(first),
                blurb=badge["blurb"],
                image=badge["image"],
                issuer=html.escape(ISSUER_NAME),
                course=html.escape(s["course"].strip()),
                term=html.escape(term),
                cred_id=cred_id,
                issued=ISSUE_DATE.strftime("%B %Y"),
                li_url=html.escape(li_url),
            )
            (out_dir / f"{cred_id}.html").write_text(page, encoding="utf-8")

            merge_rows.append({
                "first_name": first, "last_name": last, "email": email,
                "badge": badge["title"], "credential_id": cred_id,
                "credential_url": cred_url, "add_to_linkedin_url": li_url,
            })
            index_items.append(
                f'<li><a href="{cred_id}.html">{html.escape(first)} {html.escape(last)}'
                f' — {html.escape(badge["title"])}</a></li>'
            )

    merge_path = ROOT / "linkedin_merge.csv"
    with open(merge_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(merge_rows[0].keys()))
        writer.writeheader()
        writer.writerows(merge_rows)

    (out_dir / "index.html").write_text(
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        "<title>Generated credentials (demo index)</title>"
        "<style>body{font-family:Segoe UI,Arial,sans-serif;max-width:720px;"
        "margin:40px auto;line-height:1.7}h1{color:#14294b}</style></head><body>"
        "<h1>Generated credentials — demo index</h1>"
        "<p>This index is for the prototype demo only; in production students "
        "receive their own link by email and there is no public directory.</p>"
        f"<ul>{''.join(index_items)}</ul></body></html>",
        encoding="utf-8",
    )

    print(f"Generated {len(merge_rows)} credential pages -> {out_dir}")
    print(f"Mail-merge file -> {merge_path}")


if __name__ == "__main__":
    main()
