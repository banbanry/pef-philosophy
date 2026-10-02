from pathlib import Path
import markdown

root = Path(r"D:\WorkBuddy\pef-philosophy")
md_path = root / "_cn_outside_01.md"
out_path = root / "docs" / "cn-outside-01.html"
text = md_path.read_text(encoding="utf-8")

summary = text.split("## Summary", 1)[1].split("---", 1)[0].strip()
body_md = text.split("---", 1)[1]
body_html = markdown.markdown(body_md, extensions=["extra"])

html = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>悟者的路是孤独的 — 影子、锚与河 · 门外</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect x='8' y='8' width='48' height='48' fill='none' stroke='%23c9a227' stroke-width='3'/%3E%3Ccircle cx='32' cy='32' r='16' fill='none' stroke='%23e8e3d6' stroke-width='2'/%3E%3C/svg%3E" />
<link rel="stylesheet" href="assets/style.css" />
<style>body{{font-family: "Noto Serif SC", "Source Han Serif SC", "Microsoft YaHei", serif;}}</style>
</head>
<body>
<div class="wrap">
<div class="cta-row" style="margin-bottom:24px;">
<a class="ghost" href="cn.html">← 返回中文目录</a>
</div>
<article class="article">
<div class="eyebrow">门外 · 番外第一篇</div>
<div class="summary">{summary}</div>
<div class="article-body">
<h1>悟者的路是孤独的</h1>
{body_html}
</div>
</article>
<footer>门外之作 · 随九篇之后追加，按“只追加，不涂改”归档。<a class="ghost" href="index.html">English</a></footer>
</div>
</body>
</html>
"""
out_path.write_text(html, encoding="utf-8")
print(out_path)
