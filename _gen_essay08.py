from pathlib import Path
import markdown

root = Path(r"D:\WorkBuddy\pef-philosophy")
md_path = root / "essays" / "08-the-next-stroke.md"
out_path = root / "docs" / "essay-08.html"
text = md_path.read_text(encoding="utf-8")

# Extract summary between "## Summary" and next heading
parts = text.split("## Summary", 1)
summary = parts[1].split("---", 1)[0].strip()
body_md = parts[1].split("---", 1)[1]
# Remove Before You Read heading duplication? Keep as body.
body_html = markdown.markdown(body_md, extensions=["extra"])

html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>The Mind Is Not a Mirror: It Is the Next Stroke — PEF Philosophy</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect x='8' y='8' width='48' height='48' fill='none' stroke='%23c9a227' stroke-width='3'/%3E%3Ccircle cx='32' cy='32' r='16' fill='none' stroke='%23e8e3d6' stroke-width='2'/%3E%3C/svg%3E" />
<link rel="stylesheet" href="assets/style.css" />
</head>
<body>
<div class="wrap">
<div class="cta-row" style="margin-bottom:24px;">
<a class="ghost" href="index.html">← Back to index</a>
</div>
<article class="article">
<div class="eyebrow">Essay 08 · Closing essay</div>
<div class="summary">{summary}</div>
<div class="article-body">
<h1>The Mind Is Not a Mirror: It Is the Next Stroke</h1>
{body_html}
</div>
</article>
<footer>pef-philosophy · <a class="ghost" href="https://github.com/banbanry/pef-philosophy/blob/main/essays/08-the-next-stroke.md">View Markdown on GitHub</a></footer>
</div>
</body>
</html>
"""
out_path.write_text(html, encoding="utf-8")
print(out_path)
