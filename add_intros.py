"""
add_intros.py
Inserts an #intro div into each of the 5 portfolio HTML files,
immediately after the closing </div> of the .video-bg block.
Preserves original line endings (CRLF or LF).
"""

import os

BASE = r"c:\Users\henri\Documents\Python\Python Scripts\MyProjects\PortWebsite"

# Each entry: (filename, intro_html_with_unix_newlines)
FILES = [
    (
        "resume.html",
        "\n\t<!-- Intro -->\n\t<div id=\"intro\">\n\t\t<h1>Resume</h1>\n\t\t<p>Analytics &amp; Settlements Professional<br />\n\t\tMaster of Analytics &nbsp;&middot;&nbsp; Swinburne University</p>\n\t\t<ul class=\"actions\">\n\t\t\t<li><a href=\"#main\" class=\"button icon solid solo fa-arrow-down scrolly\">Continue</a></li>\n\t\t</ul>\n\t</div>\n",
    ),
    (
        "achievements.html",
        "\n\t<!-- Intro -->\n\t<div id=\"intro\">\n\t\t<h1>Awards &amp;<br />Recognition</h1>\n\t\t<p>Certifications &nbsp;&middot;&nbsp; Academic Awards &nbsp;&middot;&nbsp; Professional Milestones</p>\n\t\t<ul class=\"actions\">\n\t\t\t<li><a href=\"#main\" class=\"button icon solid solo fa-arrow-down scrolly\">Continue</a></li>\n\t\t</ul>\n\t</div>\n",
    ),
    (
        "thv.html",
        "\n\t<!-- Intro -->\n\t<div id=\"intro\">\n\t\t<h1>THV Surf Co</h1>\n\t\t<p>Brand Strategy &nbsp;&middot;&nbsp; Market Analysis &nbsp;&middot;&nbsp; Consumer Insights</p>\n\t\t<ul class=\"actions\">\n\t\t\t<li><a href=\"#main\" class=\"button icon solid solo fa-arrow-down scrolly\">Continue</a></li>\n\t\t</ul>\n\t</div>\n",
    ),
    (
        "knowledge.html",
        "\n\t<!-- Intro -->\n\t<div id=\"intro\">\n\t\t<h1>Knowledge Hub</h1>\n\t\t<p>Solar &amp; Energy &nbsp;&middot;&nbsp; Python &nbsp;&middot;&nbsp; SQL &nbsp;&middot;&nbsp; Excel &nbsp;&middot;&nbsp; Shortcuts</p>\n\t\t<ul class=\"actions\">\n\t\t\t<li><a href=\"#main\" class=\"button icon solid solo fa-arrow-down scrolly\">Continue</a></li>\n\t\t</ul>\n\t</div>\n",
    ),
    (
        "swinburne-capstone.html",
        "\n\t<!-- Intro -->\n\t<div id=\"intro\">\n\t\t<h1>Digital Maturity<br />Analysis</h1>\n\t\t<p>Graduate Capstone &nbsp;&middot;&nbsp; Swinburne University</p>\n\t\t<ul class=\"actions\">\n\t\t\t<li><a href=\"#main\" class=\"button icon solid solo fa-arrow-down scrolly\">Continue</a></li>\n\t\t</ul>\n\t</div>\n",
    ),
]

# Marker that uniquely identifies the video-bg HTML block in the <body>
VIDEO_BG_DIV_OPEN = b'<div class="video-bg">'
# The closing sequence we look for after the video-bg block
VIDEO_CLOSE_TAG   = b"</video>"
DIV_CLOSE_TAG     = b"</div>"


def process_file(filename, intro_lf):
    path = os.path.join(BASE, filename)

    # ── Read raw bytes ──────────────────────────────────────────────────────
    with open(path, "rb") as f:
        raw = f.read()

    # ── Detect line ending ──────────────────────────────────────────────────
    crlf = b"\r\n" in raw
    le = b"\r\n" if crlf else b"\n"

    # ── Work in normalised LF space so indexing is simpler ──────────────────
    content = raw.replace(b"\r\n", b"\n") if crlf else raw

    # ── Guard: skip if #intro already present ───────────────────────────────
    if b'id="intro"' in content:
        print(f"  SKIPPED {filename} — #intro already present.")
        return

    # ── Locate the video-bg div in the <body> (second occurrence is in body) ─
    # Find all occurrences; use the last one which is inside <body>
    search_start = content.rfind(VIDEO_BG_DIV_OPEN)
    if search_start == -1:
        print(f"  ERROR  {filename} — could not find video-bg div.")
        return

    # Find </video> after the video-bg open tag
    video_close_pos = content.find(VIDEO_CLOSE_TAG, search_start)
    if video_close_pos == -1:
        print(f"  ERROR  {filename} — could not find </video> tag.")
        return

    # Find the </div> that follows </video> — that closes the video-bg wrapper
    div_close_pos = content.find(DIV_CLOSE_TAG, video_close_pos + len(VIDEO_CLOSE_TAG))
    if div_close_pos == -1:
        print(f"  ERROR  {filename} — could not find closing </div> after </video>.")
        return

    # Insertion point: immediately after that </div>
    insert_at = div_close_pos + len(DIV_CLOSE_TAG)

    # ── Build the intro bytes (convert LF intro to file's line ending) ──────
    intro_bytes = intro_lf.encode("utf-8")
    if crlf:
        intro_bytes = intro_bytes.replace(b"\n", b"\r\n")

    # ── Splice in the intro ─────────────────────────────────────────────────
    new_content = content[:insert_at] + intro_bytes + content[insert_at:]

    # ── Restore original line endings before writing ─────────────────────────
    if crlf:
        new_content = new_content.replace(b"\n", b"\r\n")

    # ── Write back ──────────────────────────────────────────────────────────
    with open(path, "wb") as f:
        f.write(new_content)

    print(f"  OK     {filename} — intro inserted after video-bg </div>.")


def main():
    print("add_intros.py — inserting #intro sections\n")
    for filename, intro in FILES:
        process_file(filename, intro)
    print("\nDone.")


if __name__ == "__main__":
    main()
