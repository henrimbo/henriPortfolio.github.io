"""
Updates all portfolio HTML pages with the full 6-item nav.
Run once from the PortWebsite folder: python update_nav.py
"""
import os, re

PAGES = [
    "index.html",
    "resume.html",
    "capstone.html",
    "python-projects.html",
    "energy.html",
    "knowledge.html",
    "excel-automation.html",
    "data-reconciliation.html",
    "windows-automation.html",
    "auto-refresh.html",
    "sql-pipelines.html",
    "eda-python.html",
]

# The active page slug → which <li> gets class="active"
ACTIVE = {
    "index.html":              "index.html",
    "resume.html":             "resume.html",
    "capstone.html":           "index.html",
    "python-projects.html":    "python-projects.html",
    "energy.html":             "energy.html",
    "knowledge.html":          "knowledge.html",
    "excel-automation.html":   "python-projects.html",
    "data-reconciliation.html":"python-projects.html",
    "windows-automation.html": "python-projects.html",
    "auto-refresh.html":       "python-projects.html",
    "sql-pipelines.html":      "python-projects.html",
    "eda-python.html":         "python-projects.html",
}

ALL_LINKS = [
    ("index.html",          "Projects"),
    ("python-projects.html","Python &amp; Automation"),
    ("energy.html",         "Energy &amp; AEMO"),
    ("knowledge.html",      "Knowledge Hub"),
    ("achievements.html",   "Achievements"),
    ("resume.html",         "Resume"),
]

def build_nav(page):
    active_href = ACTIVE.get(page, "")
    lines = []
    for href, label in ALL_LINKS:
        cls = ' class="active"' if href == active_href else ''
        lines.append(f'<li{cls}><a href="{href}">{label}</a></li>')
    return "\n\t\t\t\t\t".join(lines)

NAV_PATTERN = re.compile(
    r'(<ul class="links">)\s*(<li.*?</ul>)',
    re.DOTALL
)

base = os.path.dirname(os.path.abspath(__file__))

for page in PAGES:
    path = os.path.join(base, page)
    if not os.path.exists(path):
        print(f"  SKIP (not found): {page}")
        continue

    with open(path, encoding="utf-8") as f:
        html = f.read()

    new_links = build_nav(page)
    new_ul = f'<ul class="links">\n\t\t\t\t\t{new_links}\n\t\t\t\t</ul>'

    # Replace the links <ul> block
    updated = NAV_PATTERN.sub(new_ul, html, count=1)

    if updated == html:
        print(f"  WARN (no match):  {page}")
    else:
        with open(path, "w", encoding="utf-8") as f:
            f.write(updated)
        print(f"  OK:               {page}")

print("\nDone.")
