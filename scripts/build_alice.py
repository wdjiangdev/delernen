#!/usr/bin/env python3
"""Build delernen /alice/ section from ~/workspace/alice-notes/md/*.md.

Each markdown file -> alice/<slug>.html + alice/index.html card list.
Visual language follows grammatik/kurs sections (theme vars, cards).
Original explanations rewritten by assistant; short quotes only; source links included.
"""
import html as htmlmod
import os
import re
import sys

SRC = os.path.expanduser("~/workspace/alice-notes/md")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "alice")

CSS = """:root{--bg:#0a0e1a;--bg-card:#111830;--bg-elev:#141b30;--bg-deep:#0d1326;
--text:#e0e6f0;--text2:#b0b8d0;--text3:#8a93a8;--text4:#6a7490;
--border:#2a3350;--border2:#232c48;--accent:#4a7aca;--accent2:#6ab0ff;--accentbg:#2a4a8a;
--green:#7dd87d;--orange:#ffb84d;--red:#ff7d7d}
[data-theme="light"]{--bg:#f4f6fa;--bg-card:#ffffff;--bg-elev:#e9edf4;--bg-deep:#e2e8f1;
--text:#1c2536;--text2:#3c4c66;--text3:#5c6e88;--text4:#8a9bb5;
--border:#cfd8e6;--border2:#dfe6f0;--accent:#3868c8;--accent2:#2c5ab5;--accentbg:#d4e2fa;
--green:#2a8a3a;--orange:#c87a1a;--red:#c83a3a}
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{background:var(--bg);color:var(--text);font-family:-apple-system,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;min-height:100vh}
header{position:sticky;top:0;z-index:10;background:var(--bg);padding:14px 16px 10px;border-bottom:1px solid var(--border2);text-align:center}
header h1{font-size:19px;font-weight:700}
header .back{display:inline-block;margin-top:6px;font-size:13px;color:var(--accent2);text-decoration:none}
main{padding:16px;max-width:720px;margin:0 auto 40px}
.card{background:var(--bg-card);border:1px solid var(--border2);border-radius:14px;padding:16px;margin:14px 0}
h2{font-size:17px;margin:18px 0 8px}
h3{font-size:15px;margin:14px 0 6px;color:var(--accent2)}
p{font-size:14px;color:var(--text2);line-height:1.8;margin:8px 0}
li{font-size:14px;color:var(--text2);line-height:1.8;margin:4px 0 4px 20px}
table{border-collapse:collapse;margin:10px 0;font-size:13px;display:block;overflow-x:auto;max-width:100%}
th,td{border:1px solid var(--border);padding:7px 10px;text-align:left;white-space:nowrap}
th{background:var(--bg-elev);color:var(--accent2)}
.ex{margin:8px 0;padding:10px 12px;background:var(--bg-deep);border-left:3px solid var(--accent);border-radius:0 8px 8px 0}
.ex .de{font-size:15px;font-weight:500}
.ex .zh{font-size:13px;color:var(--text3);margin-top:3px}
.tip{background:var(--bg-elev);border:1px dashed var(--border);border-radius:10px;padding:10px 12px;font-size:13px;color:var(--text3);margin:12px 0;line-height:1.7}
.meta{font-size:12px;color:var(--text4);margin:6px 0;line-height:1.7}
.meta a{color:var(--accent2)}
.lv{display:inline-block;font-size:11px;font-weight:700;padding:2px 10px;border-radius:8px;margin-right:8px}
.lv-A2{background:#1a3a5a;color:var(--accent2)}
.lv-B1{background:var(--orange);color:#3a2a10}
.lv-C1{background:var(--red);color:#3a1010}
[data-theme="light"] .lv-B1{color:#fff}
[data-theme="light"] .lv-C1{color:#fff}
.idx-card{display:block;background:var(--bg-card);border:1px solid var(--border2);border-radius:14px;padding:16px;margin:12px 0;text-decoration:none;color:var(--text)}
.idx-card h2{margin:0 0 4px;font-size:16px}
.idx-card p{font-size:13px;margin:4px 0}
.sec-h{font-size:14px;color:var(--text3);margin:22px 0 4px;letter-spacing:1px}
#themeBtn{position:fixed;top:14px;right:14px;background:var(--bg-card);border:1px solid var(--border);border-radius:50%;width:38px;height:38px;font-size:18px;cursor:pointer;z-index:20}
.src{font-size:12px;color:var(--text4);margin-top:16px;line-height:1.7}
.src a{color:var(--accent2)}"""

THEME_JS = """<script>
(function(){function apply(t){var r=document.documentElement;
if(t==='auto')r.setAttribute('data-theme',matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');
else r.setAttribute('data-theme',t);
var b=document.getElementById('themeBtn');if(b)b.textContent=t==='light'?'\\u2600\\ufe0f':t==='dark'?'\\ud83c\\udf19':'\\ud83d\\udd04';}
var cur=localStorage.getItem('delernen-theme')||'auto';apply(cur);
window.toggleTheme=function(){cur=cur==='auto'?'light':cur==='light'?'dark':'auto';localStorage.setItem('delernen-theme',cur);apply(cur);};})();
</script>"""


def esc(s):
    return htmlmod.escape(s)


def inline(s):
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    return s


def md_to_html(md):
    """Minimal markdown: headings, tables, lists, bold, links, paragraphs.
    Special blocks: lines starting with '例句|' -> example card (de|zh);
    lines starting with '提示|' -> tip box."""
    out = []
    lines = md.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            i += 1
            continue
        if line.startswith("### "):
            out.append(f"<h3>{inline(line[4:])}</h3>")
        elif line.startswith("## "):
            out.append(f"<h2>{inline(line[3:])}</h2>")
        elif line.startswith("# "):
            pass  # title handled separately
        elif line.startswith("例句|"):
            parts = line[3:].split("|")
            de = parts[0].strip() if len(parts) > 0 else ""
            zh = parts[1].strip() if len(parts) > 1 else ""
            out.append(f'<div class="ex"><div class="de">{esc(de)}</div>'
                       + (f'<div class="zh">{esc(zh)}</div>' if zh else "") + "</div>")
        elif line.startswith("提示|"):
            out.append(f'<div class="tip">💡 {inline(line[3:])}</div>')
        elif line.startswith("来源|"):
            out.append(f'<div class="src">来源：{inline(line[3:])}</div>')
        elif line.startswith("|"):
            tbl = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                tbl.append(cells)
                i += 1
            i -= 1
            # drop separator row
            rows = [r for r in tbl if not all(re.match(r"^:?-+:?$", c) for c in r)]
            h = ["<table>"]
            for ri, r in enumerate(rows):
                tag = "th" if ri == 0 else "td"
                h.append("<tr>" + "".join(f"<{tag}>{inline(c)}</{tag}>" for c in r) + "</tr>")
            h.append("</table>")
            out.append("".join(h))
        elif line.startswith("- "):
            items = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                items.append(f"<li>{inline(lines[i].strip()[2:])}</li>")
                i += 1
            i -= 1
            out.append("<ul>" + "".join(items) + "</ul>")
        else:
            out.append(f"<p>{inline(line)}</p>")
        i += 1
    return "\n".join(out)


def parse_meta(md):
    """First '# ' line = title. Optional '<!-- level:A2 -->' '<!-- desc:... -->' markers."""
    title = "笔记"
    level, desc = "B1", ""
    for line in md.split("\n"):
        if line.startswith("# "):
            title = line[2:].strip()
            m = re.match(r"\[(A2|B1|C1)\]", title)
            if m:
                level = m.group(1)
        m = re.match(r"<!--\s*level:(\w+)\s*-->", line)
        if m:
            level = m.group(1)
        m = re.search(r"难度：\*\*(A2|B1|C1)\*\*", line)
        if m:
            level = m.group(1)
        m = re.match(r"<!--\s*desc:(.+?)\s*-->", line)
        if m:
            desc = m.group(1).strip()
        if not desc:
            m = re.search(r"导读：(.+)$", line)
            if m:
                desc = m.group(1).strip()[:60]
    return title, level, desc


def page(title, body, back="../"):
    return f"""<!DOCTYPE html>
<html lang="zh"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)} · Alice Learn German 笔记</title>
<style>{CSS}</style></head>
<body><button id="themeBtn" onclick="toggleTheme()" title="切换主题">🔄</button>
<header><h1>{esc(title)}</h1><a class="back" href="{back}">← 返回目录</a></header>
<main><div class="card">{body}</div></main>
{THEME_JS}</body></html>"""


def main():
    files = sorted(f for f in os.listdir(SRC) if f.endswith(".md"))
    if not files:
        print("no markdown found in", SRC)
        sys.exit(1)
    os.makedirs(OUT, exist_ok=True)
    cards = {"A2": [], "B1": [], "C1": []}
    for fn in files:
        slug = fn[:-3]
        md = open(os.path.join(SRC, fn), encoding="utf-8").read()
        title, level, desc = parse_meta(md)
        body = md_to_html(md)
        lvl = level if level in cards else "B1"
        banner = (f'<p><span class="lv lv-{lvl}">{lvl}</span>'
                  + ("📌 C1·以后看，先认得不深究" if lvl == "C1" else "") + "</p>\n") if lvl == "C1" \
            else f'<p><span class="lv lv-{lvl}">{lvl}</span></p>\n'
        open(os.path.join(OUT, slug + ".html"), "w", encoding="utf-8").write(
            page(title, banner + body, back="index.html"))
        cards[lvl].append((slug, title, desc))
        print("built", slug)
    sec_names = {"A2": "A2 · 跟冲刺", "B1": "B1 · 冲刺后半段", "C1": "C1 · 以后看"}
    parts = []
    for lvl in ("A2", "B1", "C1"):
        if not cards[lvl]:
            continue
        parts.append(f'<div class="sec-h">{sec_names[lvl]}（{len(cards[lvl])}篇）</div>')
        for slug, title, desc in cards[lvl]:
            parts.append(
                f'<a class="idx-card" href="{slug}.html"><h2>'
                f'<span class="lv lv-{lvl}">{lvl}</span>{esc(title)}</h2>'
                + (f"<p>{esc(desc)}</p>" if desc else "") + "</a>")
    idx_body = ("<p class=\"meta\">整理自 Alice 的 Medium 刊物 "
                '<a href="https://alicelearngerman.medium.com/" target="_blank" rel="noopener">'
                "alicelearngerman.medium.com</a>（原站 alicelearngerman.com 已下线）。"
                "讲解为原创重写，仅引用短例句；每篇附原文链接。</p>\n" + "\n".join(parts))
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(
        page("Alice Learn German 学习笔记", idx_body, back="../"))
    print("index built:", len(files), "pages")


if __name__ == "__main__":
    main()
