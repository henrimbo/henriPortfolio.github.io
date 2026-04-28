"""
update_index.py
Modifies index.html to replace the projects cards with full resume content.

Reads in binary mode, normalises to LF, makes all changes (each exactly once),
then restores the original line endings before writing back.

Idempotent: each change is only applied if the find-string is still present,
so re-running the script on an already-updated file is safe.
"""

import sys

HTML_PATH = r"c:\Users\henri\Documents\Python\Python Scripts\MyProjects\PortWebsite\index.html"

# ── Read in binary mode ──────────────────────────────────────────────────────
with open(HTML_PATH, "rb") as f:
    raw = f.read()

original_endings = b"\r\n" if b"\r\n" in raw else b"\n"
content = raw.replace(b"\r\n", b"\n").decode("utf-8")

changes_made = 0

# ── Change 1: Update the Continue button ────────────────────────────────────
find1 = '<li><a href="resume.html" class="button icon solid solo fa-arrow-right">Continue</a></li>'
repl1 = '<li><a href="#main" class="button icon solid solo fa-arrow-down scrolly">Continue</a></li>'

if find1 in content:
    count = content.count(find1)
    if count != 1:
        print(f"[ERROR] Change 1: expected 1 occurrence, found {count}. Aborting.")
        sys.exit(1)
    content = content.replace(find1, repl1)
    changes_made += 1
    print("[OK] Change 1: Continue button updated.")
elif repl1 in content:
    print("[SKIP] Change 1: already applied.")
else:
    print("[FAIL] Change 1: neither find nor replacement string found.")

# ── Change 2: Update nav active state ───────────────────────────────────────
find2 = (
    '\t\t\t\t<li><a href="resume.html">Resume</a></li>\n'
    '\t\t\t\t<li><a href="thv.html">THV Surf Co</a></li>\n'
    '\t\t\t\t<li class="active"><a href="index.html">Projects</a></li>\n'
    '\t\t\t\t<li><a href="achievements.html">Awards &amp; Recognition</a></li>\n'
    '\t\t\t\t<li><a href="knowledge.html">Knowledge Hub</a></li>'
)
repl2 = (
    '\t\t\t\t<li class="active"><a href="resume.html">Resume</a></li>\n'
    '\t\t\t\t<li><a href="thv.html">THV Surf Co</a></li>\n'
    '\t\t\t\t<li><a href="index.html">Projects</a></li>\n'
    '\t\t\t\t<li><a href="achievements.html">Awards &amp; Recognition</a></li>\n'
    '\t\t\t\t<li><a href="knowledge.html">Knowledge Hub</a></li>'
)

if find2 in content:
    count = content.count(find2)
    if count != 1:
        print(f"[ERROR] Change 2: expected 1 occurrence, found {count}. Aborting.")
        sys.exit(1)
    content = content.replace(find2, repl2)
    changes_made += 1
    print("[OK] Change 2: Nav active state updated.")
elif repl2 in content:
    print("[SKIP] Change 2: already applied.")
else:
    print("[FAIL] Change 2: neither find nor replacement string found.")

# ── Change 3: Replace entire #main section ──────────────────────────────────
new_main = (
    "\t\t<!-- Main -->\n"
    "\t\t<div id=\"main\">\n"
    "\t\t\t<section class=\"post\">\n"
    "\n"
    "\t\t\t\t<!-- Page title -->\n"
    "\t\t\t\t<header class=\"major\">\n"
    "\t\t\t\t\t<h1>Henrique Borges</h1>\n"
    "\t\t\t\t\t<p>Master of Analytics &nbsp;|&nbsp; Analytics &amp; Settlements Professional<br />\n"
    "\t\t\t\t\tSydney, NSW &nbsp;&middot;&nbsp; <a href=\"mailto:henriquemborges45@hotmail.com\">henriquemborges45@hotmail.com</a> &nbsp;&middot;&nbsp; +61 432 849 841</p>\n"
    "\t\t\t\t</header>\n"
    "\n"
    "\t\t\t\t<!-- Download button -->\n"
    "\t\t\t\t<div class=\"resume-download\">\n"
    "\t\t\t\t\t<a href=\"Henrique_Borges_Resume_Final.pdf\" download class=\"button primary icon solid fa-download\">Download PDF Resume</a>\n"
    "\t\t\t\t</div>\n"
    "\n"
    "\t\t\t\t<!-- About -->\n"
    "\t\t\t\t<h3 class=\"resume-section-title\">About Me</h3>\n"
    "\t\t\t\t<p class=\"resume-about\">\n"
    "\t\t\t\t\tOriginally from Brazil and now calling Sydney home, I am an analytics professional who has taken an unconventional path \u2014 from military service and running my own surf brand, to leading Python automation projects in Australia's energy market. I hold a Master of Analytics from UNSW and currently work at Alinta Energy, where I specialise in environmental and financial settlements, data reconciliation, and building tools that make teams faster and more accurate. I bring a rare mix of technical rigour and process discipline, shaped by years working across regulated, high-stakes environments. When I am not automating something, you will find me on the tennis court or tracking down a great coffee.\n"
    "\t\t\t\t</p>\n"
    "\n"
    "\t\t\t\t<!-- Experience -->\n"
    "\t\t\t\t<h3 class=\"resume-section-title\">Experience</h3>\n"
    "\n"
    "\t\t\t\t<div class=\"resume-job\">\n"
    "\t\t\t\t\t<div class=\"resume-job-header\">\n"
    "\t\t\t\t\t\t<span class=\"resume-job-title\">Analyst, Treasury Operations &amp; Settlements &mdash; <span class=\"resume-job-company\">Alinta Energy</span></span>\n"
    "\t\t\t\t\t\t<span class=\"resume-job-meta\">Apr 2024 \u2013 Present &nbsp;|&nbsp; Sydney, NSW \u2013 Hybrid</span>\n"
    "\t\t\t\t\t</div>\n"
    "\t\t\t\t\t<ul>\n"
    "\t\t\t\t\t\t<li>Manage end-to-end settlement processes for environmental and financial products including LGCs, STCs, and ACCUs, ensuring accuracy and compliance across all trades.</li>\n"
    "\t\t\t\t\t\t<li>Perform daily reconciliations and validations using <strong>Python, SQL, and advanced Excel</strong> across Treasury and Settlements workflows.</li>\n"
    "\t\t\t\t\t\t<li>Build <strong>Power BI</strong> dashboards and automated Excel reports delivering near real-time insights to Finance, Trading, and Risk teams.</li>\n"
    "\t\t\t\t\t\t<li>Collaborate with traders, brokers, and internal stakeholders to resolve discrepancies, strengthen data integrity, and support audit and compliance requirements.</li>\n"
    "\t\t\t\t\t\t<li>Serve as an active member of the Company Safety &amp; Wellbeing Committee, contributing to monthly cross-functional discussions on safety and employee wellbeing programs.</li>\n"
    "\t\t\t\t\t</ul>\n"
    "\t\t\t\t\t<p class=\"resume-achievements\">Key Achievements</p>\n"
    "\t\t\t\t\t<ul>\n"
    "\t\t\t\t\t\t<li>Spearheaded Python automation initiatives that streamlined reconciliation workflows, reduced manual effort, and improved settlement speed and accuracy.</li>\n"
    "\t\t\t\t\t\t<li>Delivered accurate and timely settlements for complex environmental and financial instruments through cross-functional collaboration.</li>\n"
    "\t\t\t\t\t\t<li>Received 4 spotlights from across multiple teams and 2 Lunch Recognition Awards within 2 years, recognising both project-specific contributions and consistent high performance.</li>\n"
    "\t\t\t\t\t</ul>\n"
    "\t\t\t\t</div>\n"
    "\n"
    "\t\t\t\t<div class=\"resume-job\">\n"
    "\t\t\t\t\t<div class=\"resume-job-header\">\n"
    "\t\t\t\t\t\t<span class=\"resume-job-title\">Career Transition &amp; Professional Development &mdash; <span class=\"resume-job-company\"></span></span>\n"
    "\t\t\t\t\t\t<span class=\"resume-job-meta\">Aug 2018 \u2013 Jan 2024 &nbsp;|&nbsp; Sydney, NSW / Brazil (Remote)</span>\n"
    "\t\t\t\t\t</div>\n"
    "\t\t\t\t\t<ul>\n"
    "\t\t\t\t\t\t<li>Relocated from Brazil to Australia in 2018 to pursue further education and professional development in data analytics.</li>\n"
    "\t\t\t\t\t\t<li>Earned postgraduate qualifications in Data Analytics at UNSW and Swinburne University of Technology, building expertise in Python, SQL, and BI tools through coursework and portfolio projects.</li>\n"
    "\t\t\t\t\t\t<li>Managed invoicing, payments, and administrative operations for family business in Brazil remotely, maintaining commercial continuity across time zones.</li>\n"
    "\t\t\t\t\t\t<li>Worked casually in hospitality, logistics, and construction while studying, building adaptability, communication, and teamwork skills in the Australian working environment.</li>\n"
    "\t\t\t\t\t</ul>\n"
    "\t\t\t\t</div>\n"
    "\n"
    "\t\t\t\t<div class=\"resume-job\">\n"
    "\t\t\t\t\t<div class=\"resume-job-header\">\n"
    "\t\t\t\t\t\t<span class=\"resume-job-title\">Notarial &amp; Quality Systems Officer &mdash; <span class=\"resume-job-company\">Tabelionato de Notas (Notary Public Office)</span></span>\n"
    "\t\t\t\t\t\t<span class=\"resume-job-meta\">Mar 2014 \u2013 Aug 2018 &nbsp;|&nbsp; Porto Alegre, Brazil</span>\n"
    "\t\t\t\t\t</div>\n"
    "\t\t\t\t\t<ul>\n"
    "\t\t\t\t\t\t<li>Verified, registered, and validated high-value legal and financial documents including contracts, debt instruments, and certificates in a regulated notarial environment.</li>\n"
    "\t\t\t\t\t\t<li>Led process documentation and internal audits to align operations with <strong>ISO 9001 Quality Management</strong> standards, resulting in full certification.</li>\n"
    "\t\t\t\t\t\t<li>Partnered with IT to digitise and modernise workflows, reducing manual data entry errors and improving turnaround times.</li>\n"
    "\t\t\t\t\t\t<li>Designed and maintained Standard Operating Procedures (SOPs) and compliance documentation across the organisation.</li>\n"
    "\t\t\t\t\t\t<li>Trained and mentored staff on updated quality and documentation processes, ensuring ongoing audit readiness.</li>\n"
    "\t\t\t\t\t</ul>\n"
    "\t\t\t\t\t<p class=\"resume-achievements\">Key Achievements</p>\n"
    "\t\t\t\t\t<ul>\n"
    "\t\t\t\t\t\t<li>Achieved ISO 9001 Certification by owning end-to-end documentation, auditing, and process improvement initiatives.</li>\n"
    "\t\t\t\t\t\t<li>Recognised for precision and reliability in managing sensitive, confidential legal data in a high-compliance environment.</li>\n"
    "\t\t\t\t\t</ul>\n"
    "\t\t\t\t</div>\n"
    "\n"
    "\t\t\t\t<div class=\"resume-job\">\n"
    "\t\t\t\t\t<div class=\"resume-job-header\">\n"
    "\t\t\t\t\t\t<span class=\"resume-job-title\">Founder &amp; Owner &mdash; <span class=\"resume-job-company\"><a href=\"thv.html\" style=\"color:inherit;border-bottom:1px dotted rgba(74,158,218,0.5);\">THV Surf Co</a></span></span>\n"
    "\t\t\t\t\t\t<span class=\"resume-job-meta\">2015 \u2013 2018 &nbsp;|&nbsp; Porto Alegre, Brazil</span>\n"
    "\t\t\t\t\t</div>\n"
    "\t\t\t\t\t<ul>\n"
    "\t\t\t\t\t\t<li>Founded and operated a surf apparel brand, managing the full business cycle from supplier negotiations and inventory procurement to sales and customer engagement.</li>\n"
    "\t\t\t\t\t\t<li>Managed supplier relationships and financial operations including budgeting, cost control, and margin tracking.</li>\n"
    "\t\t\t\t\t\t<li>Developed and executed sales and marketing strategies, building brand presence through social channels and direct-to-consumer sales.</li>\n"
    "\t\t\t\t\t</ul>\n"
    "\t\t\t\t</div>\n"
    "\n"
    "\t\t\t\t<div class=\"resume-job\">\n"
    "\t\t\t\t\t<div class=\"resume-job-header\">\n"
    "\t\t\t\t\t\t<span class=\"resume-job-title\">Soldier &mdash; <span class=\"resume-job-company\">Brazilian Armed Forces</span></span>\n"
    "\t\t\t\t\t\t<span class=\"resume-job-meta\">Mar 2013 \u2013 Mar 2014 &nbsp;|&nbsp; Porto Alegre, Brazil</span>\n"
    "\t\t\t\t\t</div>\n"
    "\t\t\t\t\t<ul>\n"
    "\t\t\t\t\t\t<li>Served full-time in the Brazilian Armed Forces, developing strong discipline, teamwork, and resilience under pressure.</li>\n"
    "\t\t\t\t\t\t<li>Awarded a Merit and Honour Certificate for outstanding service and exemplary conduct.</li>\n"
    "\t\t\t\t\t</ul>\n"
    "\t\t\t\t</div>\n"
    "\n"
    "\t\t\t\t<!-- Education -->\n"
    "\t\t\t\t<h3 class=\"resume-section-title\">Education</h3>\n"
    "\n"
    "\t\t\t\t<div class=\"resume-edu\">\n"
    "\t\t\t\t\t<span><span class=\"resume-edu-degree\">Master of Analytics</span> &mdash; <span class=\"resume-edu-school\">University of New South Wales</span></span>\n"
    "\t\t\t\t\t<span class=\"resume-edu-year\">Completed Dec 2024</span>\n"
    "\t\t\t\t</div>\n"
    "\t\t\t\t<div class=\"resume-edu\">\n"
    "\t\t\t\t\t<span><span class=\"resume-edu-degree\">Graduate Certificate in Data Analytics</span> &mdash; <span class=\"resume-edu-school\">Swinburne University of Technology</span></span>\n"
    "\t\t\t\t\t<span class=\"resume-edu-year\">Completed Dec 2022</span>\n"
    "\t\t\t\t</div>\n"
    "\n"
    "\t\t\t\t<!-- Skills -->\n"
    "\t\t\t\t<h3 class=\"resume-section-title\">Skills &amp; Tools</h3>\n"
    "\n"
    "\t\t\t\t<div class=\"skills-group\">\n"
    "\t\t\t\t\t<span class=\"skills-label\">Technical:</span>\n"
    "\t\t\t\t\t<span class=\"skill-tag\">Python</span>\n"
    "\t\t\t\t\t<span class=\"skill-tag\">SQL</span>\n"
    "\t\t\t\t\t<span class=\"skill-tag\">Power BI</span>\n"
    "\t\t\t\t\t<span class=\"skill-tag\">Advanced Excel</span>\n"
    "\t\t\t\t\t<span class=\"skill-tag\">Data Reconciliation</span>\n"
    "\t\t\t\t\t<span class=\"skill-tag\">Process Automation</span>\n"
    "\t\t\t\t</div>\n"
    "\t\t\t\t<div class=\"skills-group\">\n"
    "\t\t\t\t\t<span class=\"skills-label\">Domain:</span>\n"
    "\t\t\t\t\t<span class=\"skill-tag\">Energy Markets</span>\n"
    "\t\t\t\t\t<span class=\"skill-tag\">Environmental Settlements (LGCs, STCs, ACCUs)</span>\n"
    "\t\t\t\t\t<span class=\"skill-tag\">Financial Instruments</span>\n"
    "\t\t\t\t\t<span class=\"skill-tag\">Compliance &amp; Audit</span>\n"
    "\t\t\t\t\t<span class=\"skill-tag\">ISO 9001</span>\n"
    "\t\t\t\t</div>\n"
    "\t\t\t\t<div class=\"skills-group\">\n"
    "\t\t\t\t\t<span class=\"skills-label\">Languages:</span>\n"
    "\t\t\t\t\t<span class=\"skill-tag\">English (fluent)</span>\n"
    "\t\t\t\t\t<span class=\"skill-tag\">Portuguese (native)</span>\n"
    "\t\t\t\t</div>\n"
    "\n"
    "\t\t\t\t<!-- Projects link -->\n"
    "\t\t\t\t<h3 class=\"resume-section-title\">Projects</h3>\n"
    "\t\t\t\t<p>View my data analytics projects including Tableau dashboards and capstone work.</p>\n"
    "\t\t\t\t<ul class=\"actions\">\n"
    "\t\t\t\t\t<li><a href=\"projects.html\" class=\"button\">View Projects</a></li>\n"
    "\t\t\t\t</ul>\n"
    "\n"
    "\t\t\t</section>\n"
    "\t\t</div>"
)

# Sentinel strings to detect whether this change is already applied
find3_old_marker = '<section class="posts">'    # present only in the un-modified file
find3_new_marker = '<section class="post">'     # present once change is applied

start_marker = "<!-- Main -->"
start_marker_pos = content.find(start_marker)

if start_marker_pos == -1:
    print("[FAIL] Change 3: '<!-- Main -->' marker not found.")
elif find3_old_marker not in content and find3_new_marker in content:
    print("[SKIP] Change 3: already applied.")
else:
    main_div_token = '<div id="main">'
    main_div_start = content.find(main_div_token, start_marker_pos)

    if main_div_start == -1:
        print("[FAIL] Change 3: '<div id=\"main\">' not found after marker.")
    else:
        # Walk forward counting <div nesting depth to find the matching </div>
        depth = 0
        pos = main_div_start
        end_pos = -1

        while pos < len(content):
            open_match = content.find("<div", pos)
            close_match = content.find("</div>", pos)

            if open_match == -1 and close_match == -1:
                break

            if open_match != -1 and (close_match == -1 or open_match < close_match):
                depth += 1
                pos = open_match + len("<div")
            else:
                depth -= 1
                close_end = close_match + len("</div>")
                if depth == 0:
                    end_pos = close_end
                    break
                pos = close_end

        if end_pos == -1:
            print("[FAIL] Change 3: Could not find matching closing </div> for #main.")
        else:
            content = content[:start_marker_pos] + new_main + content[end_pos:]
            changes_made += 1
            print("[OK] Change 3: #main section replaced with resume content.")

# ── Change 4a: Add resume CSS before the hide-static-bg comment ─────────────
find4a = "\t\t/* ── Hide static bg so video shows through ── */"
resume_css_marker = "\t\t/* ── Resume-specific styles ── */"

repl4a = (
    "\t\t/* ── Resume-specific styles ── */\n"
    "\n"
    "\t\t/* Section headings with blue accent line */\n"
    "\t\t.resume-section-title {\n"
    "\t\t\tfont-size: 1.1em;\n"
    "\t\t\ttext-transform: uppercase;\n"
    "\t\t\tletter-spacing: 0.15em;\n"
    "\t\t\tcolor: #4a9eda;\n"
    "\t\t\tborder-bottom: 2px solid #4a9eda;\n"
    "\t\t\tpadding-bottom: 0.4em;\n"
    "\t\t\tmargin: 2.5em 0 1.2em;\n"
    "\t\t}\n"
    "\n"
    "\t\t/* About paragraph */\n"
    "\t\t.resume-about {\n"
    "\t\t\tfont-size: 1em;\n"
    "\t\t\tline-height: 1.75;\n"
    "\t\t\tmargin-bottom: 0;\n"
    "\t\t}\n"
    "\n"
    "\t\t/* Experience cards */\n"
    "\t\t.resume-job {\n"
    "\t\t\tmargin-bottom: 2em;\n"
    "\t\t\tpadding-bottom: 2em;\n"
    "\t\t\tborder-bottom: 1px solid rgba(255,255,255,0.1);\n"
    "\t\t}\n"
    "\t\t.resume-job:last-child {\n"
    "\t\t\tborder-bottom: none;\n"
    "\t\t}\n"
    "\t\t.resume-job-header {\n"
    "\t\t\tdisplay: flex;\n"
    "\t\t\tjustify-content: space-between;\n"
    "\t\t\talign-items: baseline;\n"
    "\t\t\tflex-wrap: wrap;\n"
    "\t\t\tgap: 0.3em;\n"
    "\t\t}\n"
    "\t\t.resume-job-title {\n"
    "\t\t\tfont-weight: 700;\n"
    "\t\t\tfont-size: 1.05em;\n"
    "\t\t\tmargin: 0;\n"
    "\t\t}\n"
    "\t\t.resume-job-company {\n"
    "\t\t\tcolor: #4a9eda;\n"
    "\t\t\tfont-weight: 600;\n"
    "\t\t}\n"
    "\t\t.resume-job-meta {\n"
    "\t\t\tfont-size: 0.85em;\n"
    "\t\t\topacity: 0.65;\n"
    "\t\t\tfont-style: italic;\n"
    "\t\t}\n"
    "\t\t.resume-job ul {\n"
    "\t\t\tmargin: 0.8em 0 0.5em 1.2em;\n"
    "\t\t\tpadding: 0;\n"
    "\t\t}\n"
    "\t\t.resume-job ul li {\n"
    "\t\t\tmargin-bottom: 0.35em;\n"
    "\t\t\tline-height: 1.6;\n"
    "\t\t}\n"
    "\t\t.resume-achievements {\n"
    "\t\t\tfont-weight: 600;\n"
    "\t\t\tcolor: #4a9eda;\n"
    "\t\t\tfont-style: italic;\n"
    "\t\t\tmargin: 0.8em 0 0.3em;\n"
    "\t\t\tfont-size: 0.95em;\n"
    "\t\t}\n"
    "\n"
    "\t\t/* Education entries */\n"
    "\t\t.resume-edu {\n"
    "\t\t\tdisplay: flex;\n"
    "\t\t\tjustify-content: space-between;\n"
    "\t\t\talign-items: baseline;\n"
    "\t\t\tflex-wrap: wrap;\n"
    "\t\t\tgap: 0.3em;\n"
    "\t\t\tmargin-bottom: 0.8em;\n"
    "\t\t}\n"
    "\t\t.resume-edu-degree {\n"
    "\t\t\tfont-weight: 700;\n"
    "\t\t}\n"
    "\t\t.resume-edu-school {\n"
    "\t\t\tcolor: #4a9eda;\n"
    "\t\t}\n"
    "\t\t.resume-edu-year {\n"
    "\t\t\tfont-size: 0.85em;\n"
    "\t\t\topacity: 0.65;\n"
    "\t\t\tfont-style: italic;\n"
    "\t\t}\n"
    "\n"
    "\t\t/* Skills tags */\n"
    "\t\t.skills-group {\n"
    "\t\t\tmargin-bottom: 1em;\n"
    "\t\t}\n"
    "\t\t.skills-label {\n"
    "\t\t\tfont-weight: 700;\n"
    "\t\t\tmargin-right: 0.5em;\n"
    "\t\t\tfont-size: 0.95em;\n"
    "\t\t}\n"
    "\t\t.skill-tag {\n"
    "\t\t\tdisplay: inline-block;\n"
    "\t\t\tbackground: rgba(74, 158, 218, 0.15);\n"
    "\t\t\tborder: 1px solid rgba(74, 158, 218, 0.4);\n"
    "\t\t\tcolor: inherit;\n"
    "\t\t\tborder-radius: 3px;\n"
    "\t\t\tpadding: 0.2em 0.6em;\n"
    "\t\t\tmargin: 0.2em 0.25em 0.2em 0;\n"
    "\t\t\tfont-size: 0.85em;\n"
    "\t\t}\n"
    "\n"
    "\t\t/* Download button area */\n"
    "\t\t.resume-download {\n"
    "\t\t\ttext-align: center;\n"
    "\t\t\tmargin: 2.5em 0 0.5em;\n"
    "\t\t}\n"
    "\n"
    "\t\t/* ── Hide static bg so video shows through ── */"
)

if find4a in content and resume_css_marker not in content:
    count = content.count(find4a)
    if count != 1:
        print(f"[ERROR] Change 4a: expected 1 occurrence of hide-bg comment, found {count}. Aborting.")
        sys.exit(1)
    content = content.replace(find4a, repl4a)
    changes_made += 1
    print("[OK] Change 4a: Resume CSS styles added.")
elif resume_css_marker in content:
    print("[SKIP] Change 4a: already applied.")
else:
    print("[FAIL] Change 4a: hide-static-bg comment not found.")

# ── Change 4b: Update #main .posts rule to include .post ────────────────────
find4b = (
    "\t\t#main .posts { background: rgba(255, 255, 255, 0.96) !important; border-radius: 6px; padding: 2em !important; color: #1a2035 !important; }\n"
    "\t\t#main .posts p, #main .posts h2, #main .posts h3, #main .posts h4 { color: #1a2035 !important; }\n"
    "\t\t#main .posts article header h2 a { color: #0d1b2a !important; }"
)
repl4b = (
    "\t\t#main .post  { background: rgba(255, 255, 255, 0.96) !important; border-radius: 6px; padding: 2.5em !important; color: #1a2035 !important; }\n"
    "\t\t#main .posts { background: rgba(255, 255, 255, 0.96) !important; border-radius: 6px; padding: 2em !important; color: #1a2035 !important; }\n"
    "\t\t#main .post p, #main .post li, #main .posts p, #main .posts h2, #main .posts h3, #main .posts h4 { color: #1a2035 !important; }\n"
    "\t\t#main .post h1, #main .post h2, #main .post h3, #main .post h4 { color: #0d1b2a !important; }\n"
    "\t\t#main .posts article header h2 a { color: #0d1b2a !important; }"
)
find4b_applied_marker = "#main .post  { background"

if find4b in content:
    count = content.count(find4b)
    if count != 1:
        print(f"[ERROR] Change 4b: expected 1 occurrence, found {count}. Aborting.")
        sys.exit(1)
    content = content.replace(find4b, repl4b)
    changes_made += 1
    print("[OK] Change 4b: #main .post CSS rule added.")
elif find4b_applied_marker in content:
    print("[SKIP] Change 4b: already applied.")
else:
    print("[FAIL] Change 4b: existing .posts CSS rule not found.")

# ── Restore original line endings and write back ─────────────────────────────
output = content.encode("utf-8")
if original_endings == b"\r\n":
    output = output.replace(b"\n", b"\r\n")

with open(HTML_PATH, "wb") as f:
    f.write(output)

print(f"\nDone. {changes_made} change(s) applied this run. index.html written successfully.")
