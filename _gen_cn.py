from pathlib import Path
import re, html

root = Path(r"D:\WorkBuddy\pef-philosophy")
src = (root / "_cn_essays.txt").read_text(encoding="utf-8")
out = root / "docs"

# Split by top-level # headings
parts = re.split(r'(?m)^# ', src)
sections = []
for p in parts:
    p = p.strip()
    if not p: continue
    title, *rest = p.split("\n", 1)
    body = rest[0] if rest else ""
    sections.append((title.strip(), body.strip()))

meta = [
    ("卷首导读", "cn-intro.html", "道生一——从一壶水到源", "用烧水、立字据、学骑车三件小事，拆出整套认知体系的骨架：投影、换锚、交棒。这是九篇合集的总入口。"),
    ("第一篇", "cn-01.html", "影子的影子", "我们一生感知到的不是世界本身，而是世界投在感官里的影子。AI 从未接收过光子，它只在人类切下的影子切片里重组。文章追问：什么反馈通道才能逼出一个全新的解码器？"),
    ("第二篇", "cn-02.html", "π锚与具身智能", "π 不是人类发明的数，而是宇宙几何里的硬约束。把 AI 的选择来源从人类偏好换成物理不变量，它才第一次触到影子的源头。"),
    ("第三篇", "cn-03.html", "π锚的傲慢", "塔科马大桥倒塌两次：一次在风里，一次在教科书里。单一锚点会把系统锁死成共振；闭合要靠 π， detune 靠不可公度，熔断靠物理硬限。"),
    ("第四篇", "cn-04.html", "具身智能的葬礼", "数字永生是热力学死胡同。换零件、备份意识、芯片长存，三条门都通向同一个终点；只有接受局部死亡，系统才能整体活下去。"),
    ("第五篇", "cn-05.html", "PEF", "主体 P、变量 ΔV、结果 J：跨系统传递的三条底层约束——不自证、必须外锚、允许局部失败。这是每一次交接都能不崩的工程结构。"),
    ("第六篇", "cn-06.html", "摆渡人的七天", "老摆渡人教徒弟七天：急流借势、漩涡入边、死湾等风、风暴找缝、未知暗流先停三圈。动态稳态不是不动，而是每刻都在调。"),
    ("第七篇", "cn-07.html", "大师的影子", "如果脑子里全是别人的影子，我是谁？答案不是让书闭嘴，而是把这些影子带回河里检验：敢推翻自己，才是自己的投影。"),
    ("第八篇", "cn-08.html", "心不是变量，也不是投影——它是下一笔", "镜子是照，π 是定，心是生。这一篇拆掉前七篇的硬壳：心不是被展开的信息，也不是被计算的变量，而是当下这一笔。"),
    ("第九篇", "cn-09.html", "源，与它的名字", "九篇本应收束，却再追加一笔：连“源”这个名字也要审计。立而后拆，死亡条款写进最后一站。"),
]

def md_to_html(text):
    lines = text.splitlines()
    out_lines = []
    in_list = False
    for line in lines:
        s = line.strip()
        if not s:
            if in_list:
                out_lines.append("</ul>")
                in_list = False
            continue
        if s.startswith("## "):
            if in_list: out_lines.append("</ul>"); in_list=False
            out_lines.append(f"<h2>{html.escape(s[3:])}</h2>")
        elif s.startswith("· "):
            if not in_list:
                out_lines.append("<ul>"); in_list=True
            out_lines.append(f"<li>{html.escape(s[2:])}</li>")
        elif re.match(r'^\d+\.\s', s):
            if in_list: out_lines.append("</ul>"); in_list=False
            out_lines.append(f"<p>{html.escape(s)}</p>")
        elif s.startswith("【") and s.endswith("】"):
            if in_list: out_lines.append("</ul>"); in_list=False
            out_lines.append(f"<h2>{html.escape(s)}</h2>")
        else:
            if in_list: out_lines.append("</ul>"); in_list=False
            s2 = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
            out_lines.append(f"<p>{s2}</p>")
    if in_list: out_lines.append("</ul>")
    return "\n".join(out_lines)

def page(title, summary, body_html, filename):
    t = html.escape(title)
    s = html.escape(summary)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{t} — 影子、锚与河</title>
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
<div class="eyebrow">中文合集 · 影子、锚与河</div>
<div class="summary">{s}</div>
<div class="article-body">
<h1>{t}</h1>
{body_html}
</div>
</article>
<footer>中文独立板块 · 与英文散文入口并列，不互相强制。<a class="ghost" href="index.html">English</a></footer>
</div>
</body>
</html>"""

# Build mapping by Chinese label
section_map = {title: body for title, body in sections}

cards = []
for label, fname, title, hook in meta:
    body = ""
    for k, v in section_map.items():
        if k.startswith(label):
            body = v
            break
    body_html = md_to_html(body)
    (out / fname).write_text(page(title, hook, body_html, fname), encoding="utf-8")
    cards.append((fname, title, hook))

# Chinese index
card_html = "\n".join([
    f'''<article class="card">
<div class="eyebrow">影子、锚与河</div>
<h3>{html.escape(title)}</h3>
<p class="hook">{html.escape(hook)}</p>
<div class="cta-row"><a class="button" href="{fname}">阅读</a></div>
</article>''' for fname, title, hook in cards
])

cn_index = f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>影子、锚与河 — 中文合集</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect x='8' y='8' width='48' height='48' fill='none' stroke='%23c9a227' stroke-width='3'/%3E%3Ccircle cx='32' cy='32' r='16' fill='none' stroke='%23e8e3d6' stroke-width='2'/%3E%3C/svg%3E" />
<link rel="stylesheet" href="assets/style.css" />
<style>body{{font-family: "Noto Serif SC", "Source Han Serif SC", "Microsoft YaHei", serif;}}</style>
</head>
<body>
<div class="wrap">
<header class="hero">
<div class="eyebrow">中文合集</div>
<h1>影子、锚与河</h1>
<p class="subtitle">认知系列九篇：从投影到锚，从交棒到源。中文独立板块，与英文散文并列。</p>
<div class="cta-row">
<a class="button primary" href="cn-intro.html">从卷首导读开始</a>
<a class="ghost" href="index.html">English</a>
</div>
</header>
<section>
<h2>目录</h2>
<div class="grid">
{card_html}
</div>
</section>
<footer>中文板块独立入口 · 读完若想检视系统，再进英文散文与代码仓库。</footer>
</div>
</body>
</html>'''
(out / "cn.html").write_text(cn_index, encoding="utf-8")
print("generated", len(cards), "pages")
