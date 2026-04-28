#!/usr/bin/env python3
"""
Patch script for knowledge.html — adds Courses tab.
Run once then delete.
"""
import sys

path = r'c:\Users\henri\Documents\Python\Python Scripts\MyProjects\PortWebsite\knowledge.html'

with open(path, 'rb') as f:
    content = f.read()

original_size = len(content)
results = []

# ─── Detect line ending ───────────────────────────────────────────────────────
has_crlf = b'\r\n' in content
NL = b'\r\n' if has_crlf else b'\n'
results.append(f"Line ending: {'CRLF' if has_crlf else 'LF'}")

# ─── Change 1 — Add Courses button after Windows Shortcuts button ──────────────
# Find the actual bytes for the windows line
old_btn = b'data-tab="windows">Windows Shortcuts</button>'
idx = content.find(old_btn)
if idx == -1:
    results.append("Change 1: FAILURE — could not find windows button text")
else:
    # Find end of this line (after the button closing tag)
    end_of_line = content.find(NL, idx)
    # Get the indentation of this line by going back to start of line
    start_of_line = content.rfind(NL, 0, idx)
    if start_of_line == -1:
        start_of_line = 0
    else:
        start_of_line += len(NL)
    line_bytes = content[start_of_line:end_of_line]
    # Extract leading whitespace
    indent = b''
    for b in line_bytes:
        if b in (ord(' '), ord('\t')):
            indent += bytes([b])
        else:
            break
    new_courses_btn = NL + indent + b'<button class="tab-btn" data-tab="courses">Courses</button>'
    insert_pos = end_of_line
    content = content[:insert_pos] + new_courses_btn + content[insert_pos:]
    results.append(f"Change 1: SUCCESS — Courses button inserted (indent={repr(indent)})")

# ─── Change 2 — Insert courses tab panel before </section> ────────────────────
# Find </div> that closes the windows tab panel, followed by </section>
# The windows panel's closing div is the one right before </section>
# Pattern: NL + (tabs) + </div> + NL + NL + (tabs) + </section>

# Search from the end of tab-windows panel
windows_panel_start = content.find(b'id="tab-windows"')
if windows_panel_start == -1:
    results.append("Change 2: FAILURE — could not find id=\"tab-windows\"")
else:
    # Find the section closing tag after the windows panel
    section_close = b'</section>'
    section_idx = content.find(section_close, windows_panel_start)
    if section_idx == -1:
        results.append("Change 2: FAILURE — could not find </section> after windows panel")
    else:
        # Find start of line for </section>
        section_line_start = content.rfind(NL, 0, section_idx)
        section_line_start_pos = section_line_start + len(NL)
        # Get indentation of the </section> line
        sec_indent = b''
        for b_val in content[section_line_start_pos:]:
            if b_val in (ord(' '), ord('\t')):
                sec_indent += bytes([b_val])
            else:
                break

        # Find the </div> that immediately precedes </section> (with possible blank lines between)
        # Go backwards from section_idx to find the last </div>
        search_region = content[windows_panel_start:section_idx]
        last_div_close = search_region.rfind(b'</div>')
        div_close_abs = windows_panel_start + last_div_close

        # Get indentation of the </div> line
        div_line_start_idx = content.rfind(NL, 0, div_close_abs)
        div_line_start_pos = div_line_start_idx + len(NL)
        div_indent = b''
        for b_val in content[div_line_start_pos:]:
            if b_val in (ord(' '), ord('\t')):
                div_indent += bytes([b_val])
            else:
                break

        # Build the courses panel — insert point is right before the </section> line
        # (after the last blank line following </div>)
        insert_point = section_line_start_pos  # start of the </section> line

        T = b'\t'  # single tab
        panel_indent = sec_indent + T  # one level deeper than </section>
        inner1 = panel_indent + T
        inner2 = panel_indent + T + T
        inner3 = panel_indent + T + T + T

        def line(*parts):
            return b''.join(parts) + NL

        courses_html = (
            line(panel_indent + b'<div class="tab-panel" id="tab-courses">') +
            NL +
            line(inner1 + b'<h3 class="section-title">Featured Resource</h3>') +
            NL +
            line(inner1 + b'<div class="course-featured">') +
            line(inner2 + b'<div class="course-featured-inner">') +
            line(inner3 + b'<div class="course-featured-badge">\xe2\xad\x90 Top Pick</div>') +
            line(inner3 + b'<h4 class="course-featured-name">Analyst Builder</h4>') +
            line(inner3 + b'<p class="course-featured-desc">The best structured platform for learning SQL, Python, and data analytics from scratch or levelling up. Real-world practice problems, video walkthroughs, and a focus on what actually matters in analytics roles.</p>') +
            line(inner3 + b'<a href="https://www.analystbuilder.com" target="_blank" class="button">Visit Analyst Builder &rarr;</a>') +
            line(inner2 + b'</div>') +
            line(inner1 + b'</div>') +
            NL +
            line(inner1 + b'<h3 class="section-title">SQL</h3>') +
            line(inner1 + b'<div class="course-grid">') +
            # Card 1
            line(inner2 + b'<div class="course-card">') +
            line(inner3 + b'<span class="course-tag">Free + Paid</span>') +
            line(inner3 + b'<h4 class="course-name">Analyst Builder \xe2\x80\x94 SQL</h4>') +
            line(inner3 + b'<p class="course-desc">Hundreds of SQL practice problems sorted by difficulty. The closest thing to real interview and on-the-job SQL you\'ll find online.</p>') +
            line(inner3 + b'<a href="https://www.analystbuilder.com" target="_blank" class="course-link">analystbuilder.com &rarr;</a>') +
            line(inner2 + b'</div>') +
            # Card 2
            line(inner2 + b'<div class="course-card">') +
            line(inner3 + b'<span class="course-tag">Free</span>') +
            line(inner3 + b'<h4 class="course-name">SQLZoo</h4>') +
            line(inner3 + b'<p class="course-desc">Interactive SQL exercises in the browser. Great for beginners \xe2\x80\x94 covers SELECT through to advanced JOINs and subqueries with immediate feedback.</p>') +
            line(inner3 + b'<a href="https://sqlzoo.net" target="_blank" class="course-link">sqlzoo.net &rarr;</a>') +
            line(inner2 + b'</div>') +
            # Card 3
            line(inner2 + b'<div class="course-card">') +
            line(inner3 + b'<span class="course-tag">Free</span>') +
            line(inner3 + b'<h4 class="course-name">Mode SQL Tutorial</h4>') +
            line(inner3 + b'<p class="course-desc">Clean, well-structured introduction to SQL for data analysis. From basic queries to window functions \xe2\x80\x94 written with analysts in mind.</p>') +
            line(inner3 + b'<a href="https://mode.com/sql-tutorial" target="_blank" class="course-link">mode.com/sql-tutorial &rarr;</a>') +
            line(inner2 + b'</div>') +
            line(inner1 + b'</div>') +
            NL +
            line(inner1 + b'<h3 class="section-title">Python</h3>') +
            line(inner1 + b'<div class="course-grid">') +
            # Card 1
            line(inner2 + b'<div class="course-card">') +
            line(inner3 + b'<span class="course-tag">Free + Paid</span>') +
            line(inner3 + b'<h4 class="course-name">Analyst Builder \xe2\x80\x94 Python</h4>') +
            line(inner3 + b'<p class="course-desc">Python for data analysis \xe2\x80\x94 pandas, NumPy, and real-world problem sets. Practical focus that mirrors what you actually do on the job.</p>') +
            line(inner3 + b'<a href="https://www.analystbuilder.com" target="_blank" class="course-link">analystbuilder.com &rarr;</a>') +
            line(inner2 + b'</div>') +
            # Card 2
            line(inner2 + b'<div class="course-card">') +
            line(inner3 + b'<span class="course-tag">Free</span>') +
            line(inner3 + b'<h4 class="course-name">freeCodeCamp \xe2\x80\x94 Python</h4>') +
            line(inner3 + b'<p class="course-desc">Full Python curriculum from zero. Covers fundamentals, data structures, and projects. Free, browser-based, and well-paced for self-study.</p>') +
            line(inner3 + b'<a href="https://www.freecodecamp.org/learn/scientific-computing-with-python/" target="_blank" class="course-link">freecodecamp.org &rarr;</a>') +
            line(inner2 + b'</div>') +
            # Card 3
            line(inner2 + b'<div class="course-card">') +
            line(inner3 + b'<span class="course-tag">Paid</span>') +
            line(inner3 + b'<h4 class="course-name">Automate the Boring Stuff</h4>') +
            line(inner3 + b'<p class="course-desc">Free to read online. Practical Python for automation \xe2\x80\x94 file handling, Excel, web scraping, and scheduling. Excellent for building real tools fast.</p>') +
            line(inner3 + b'<a href="https://automatetheboringstuff.com" target="_blank" class="course-link">automatetheboringstuff.com &rarr;</a>') +
            line(inner2 + b'</div>') +
            line(inner1 + b'</div>') +
            NL +
            line(inner1 + b'<h3 class="section-title">Tableau</h3>') +
            line(inner1 + b'<div class="course-grid">') +
            # Card 1
            line(inner2 + b'<div class="course-card">') +
            line(inner3 + b'<span class="course-tag">Free</span>') +
            line(inner3 + b'<h4 class="course-name">Tableau Public Training</h4>') +
            line(inner3 + b'<p class="course-desc">Official Tableau free training videos and e-learning. Covers everything from connecting data to building dashboards and calculated fields.</p>') +
            line(inner3 + b'<a href="https://www.tableau.com/learn/training" target="_blank" class="course-link">tableau.com/learn &rarr;</a>') +
            line(inner2 + b'</div>') +
            # Card 2
            line(inner2 + b'<div class="course-card">') +
            line(inner3 + b'<span class="course-tag">Free</span>') +
            line(inner3 + b'<h4 class="course-name">Tableau Public Gallery</h4>') +
            line(inner3 + b'<p class="course-desc">Browse thousands of real dashboards created by the Tableau community. The best way to learn what\'s possible and get inspired for your own work.</p>') +
            line(inner3 + b'<a href="https://public.tableau.com" target="_blank" class="course-link">public.tableau.com &rarr;</a>') +
            line(inner2 + b'</div>') +
            # Card 3
            line(inner2 + b'<div class="course-card">') +
            line(inner3 + b'<span class="course-tag">Paid</span>') +
            line(inner3 + b'<h4 class="course-name">Udemy \xe2\x80\x94 Tableau A-Z</h4>') +
            line(inner3 + b'<p class="course-desc">Kirill Eremenko\'s comprehensive Tableau course. One of the most popular on Udemy \xe2\x80\x94 covers all core features with hands-on exercises. Watch for sales.</p>') +
            line(inner3 + b'<a href="https://www.udemy.com/topic/tableau/" target="_blank" class="course-link">udemy.com &rarr;</a>') +
            line(inner2 + b'</div>') +
            line(inner1 + b'</div>') +
            NL +
            line(inner1 + b'<h3 class="section-title">Analytics &amp; General</h3>') +
            line(inner1 + b'<div class="course-grid">') +
            # Card 1
            line(inner2 + b'<div class="course-card">') +
            line(inner3 + b'<span class="course-tag">Free + Paid</span>') +
            line(inner3 + b'<h4 class="course-name">Coursera \xe2\x80\x94 Google Data Analytics</h4>') +
            line(inner3 + b'<p class="course-desc">Google\'s professional certificate covering the full analytics workflow. Spreadsheets, SQL, R, and Tableau \xe2\x80\x94 solid foundation for career starters.</p>') +
            line(inner3 + b'<a href="https://www.coursera.org/professional-certificates/google-data-analytics" target="_blank" class="course-link">coursera.org &rarr;</a>') +
            line(inner2 + b'</div>') +
            # Card 2
            line(inner2 + b'<div class="course-card">') +
            line(inner3 + b'<span class="course-tag">Free</span>') +
            line(inner3 + b'<h4 class="course-name">Khan Academy \xe2\x80\x94 Statistics</h4>') +
            line(inner3 + b'<p class="course-desc">Free, clear statistics fundamentals. Essential background knowledge for any analytics professional \xe2\x80\x94 probability, distributions, regression basics.</p>') +
            line(inner3 + b'<a href="https://www.khanacademy.org/math/statistics-probability" target="_blank" class="course-link">khanacademy.org &rarr;</a>') +
            line(inner2 + b'</div>') +
            line(inner1 + b'</div>') +
            NL +
            line(panel_indent + b'</div>') +
            NL
        )

        content = content[:insert_point] + courses_html + content[insert_point:]
        results.append(f"Change 2: SUCCESS — Courses tab panel inserted (panel_indent={repr(panel_indent)})")

# ─── Change 3 — Add CSS before </style> ───────────────────────────────────────
style_close_tag = b'</style>'
style_idx = content.find(style_close_tag)
if style_idx == -1:
    results.append("Change 3: FAILURE — could not find </style>")
else:
    # Get indentation of the </style> line
    style_line_start = content.rfind(NL, 0, style_idx)
    style_line_start_pos = style_line_start + len(NL)
    style_indent = b''
    for b_val in content[style_line_start_pos:]:
        if b_val in (ord(' '), ord('\t')):
            style_indent += bytes([b_val])
        else:
            break

    T = b'\t'
    css_indent = style_indent + T  # one level deeper

    def cline(*parts):
        return b''.join(parts) + NL

    css_block = (
        NL +
        cline(css_indent + b'/* \xe2\x94\x80\xe2\x94\x80 Courses tab styles \xe2\x94\x80\xe2\x94\x80 */') +
        cline(css_indent + b'.course-featured {') +
        cline(css_indent + T + b'margin: 0 0 2em;') +
        cline(css_indent + b'}') +
        cline(css_indent + b'.course-featured-inner {') +
        cline(css_indent + T + b'background: rgba(74,158,218,0.07);') +
        cline(css_indent + T + b'border: 1px solid rgba(74,158,218,0.25);') +
        cline(css_indent + T + b'border-left: 5px solid #4a9eda;') +
        cline(css_indent + T + b'border-radius: 6px;') +
        cline(css_indent + T + b'padding: 1.6em 2em;') +
        cline(css_indent + b'}') +
        cline(css_indent + b'.course-featured-badge {') +
        cline(css_indent + T + b'font-size: 0.72em;') +
        cline(css_indent + T + b'text-transform: uppercase;') +
        cline(css_indent + T + b'letter-spacing: 0.12em;') +
        cline(css_indent + T + b'color: #4a9eda;') +
        cline(css_indent + T + b'margin-bottom: 0.5em;') +
        cline(css_indent + b'}') +
        cline(css_indent + b'.course-featured-name {') +
        cline(css_indent + T + b'font-size: 1.25em;') +
        cline(css_indent + T + b'font-weight: 700;') +
        cline(css_indent + T + b'margin: 0 0 0.5em;') +
        cline(css_indent + T + b'color: inherit;') +
        cline(css_indent + b'}') +
        cline(css_indent + b'.course-featured-desc {') +
        cline(css_indent + T + b'font-size: 0.95em;') +
        cline(css_indent + T + b'line-height: 1.7;') +
        cline(css_indent + T + b'margin-bottom: 1.2em;') +
        cline(css_indent + T + b'opacity: 0.9;') +
        cline(css_indent + b'}') +
        cline(css_indent + b'.course-grid {') +
        cline(css_indent + T + b'display: grid;') +
        cline(css_indent + T + b'grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));') +
        cline(css_indent + T + b'gap: 1.2em;') +
        cline(css_indent + T + b'margin: 0 0 1.5em;') +
        cline(css_indent + b'}') +
        cline(css_indent + b'.course-card {') +
        cline(css_indent + T + b'background: rgba(255,255,255,0.03);') +
        cline(css_indent + T + b'border: 1px solid rgba(255,255,255,0.1);') +
        cline(css_indent + T + b'border-radius: 5px;') +
        cline(css_indent + T + b'padding: 1.1em 1.3em;') +
        cline(css_indent + T + b'display: flex;') +
        cline(css_indent + T + b'flex-direction: column;') +
        cline(css_indent + T + b'gap: 0.4em;') +
        cline(css_indent + b'}') +
        cline(css_indent + b'.course-tag {') +
        cline(css_indent + T + b'display: inline-block;') +
        cline(css_indent + T + b'background: rgba(74,158,218,0.1);') +
        cline(css_indent + T + b'border: 1px solid rgba(74,158,218,0.25);') +
        cline(css_indent + T + b'border-radius: 3px;') +
        cline(css_indent + T + b'padding: 0.1em 0.45em;') +
        cline(css_indent + T + b'font-size: 0.7em;') +
        cline(css_indent + T + b'text-transform: uppercase;') +
        cline(css_indent + T + b'letter-spacing: 0.08em;') +
        cline(css_indent + T + b'color: #4a9eda;') +
        cline(css_indent + T + b'align-self: flex-start;') +
        cline(css_indent + b'}') +
        cline(css_indent + b'.course-name {') +
        cline(css_indent + T + b'font-size: 0.95em;') +
        cline(css_indent + T + b'font-weight: 700;') +
        cline(css_indent + T + b'margin: 0;') +
        cline(css_indent + T + b'color: inherit;') +
        cline(css_indent + b'}') +
        cline(css_indent + b'.course-desc {') +
        cline(css_indent + T + b'font-size: 0.87em;') +
        cline(css_indent + T + b'line-height: 1.6;') +
        cline(css_indent + T + b'margin: 0;') +
        cline(css_indent + T + b'opacity: 0.85;') +
        cline(css_indent + T + b'flex: 1;') +
        cline(css_indent + b'}') +
        cline(css_indent + b'.course-link {') +
        cline(css_indent + T + b'font-size: 0.8em;') +
        cline(css_indent + T + b'color: #4a9eda;') +
        cline(css_indent + T + b'text-decoration: none;') +
        cline(css_indent + T + b'opacity: 0.8;') +
        cline(css_indent + T + b'margin-top: auto;') +
        cline(css_indent + b'}') +
        cline(css_indent + b'.course-link:hover { opacity: 1; }')
    )

    content = content[:style_idx] + css_block + content[style_idx:]
    results.append(f"Change 3: SUCCESS — Course CSS inserted before </style> (indent={repr(style_indent)})")

# ─── Write output ─────────────────────────────────────────────────────────────
with open(path, 'wb') as f:
    f.write(content)

print(f"Original size: {original_size} bytes")
print(f"New size:      {len(content)} bytes  (+{len(content)-original_size})")
print(f"CRLF preserved: {NL == b'\\r\\n'}")
for r in results:
    print(r)

# Quick verification
print()
print("Verification:")
print(f"  Courses button present:     {b'data-tab=\"courses\">Courses</button>' in content}")
print(f"  tab-courses panel present:  {b'id=\"tab-courses\"' in content}")
print(f"  course-featured CSS:        {b'.course-featured {' in content}")
print(f"  course-link:hover CSS:      {b'.course-link:hover { opacity: 1; }' in content}")
print(f"  CRLF preserved:             {b'\\r\\n' in content}")
