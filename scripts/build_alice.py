#!/usr/bin/env python3
"""Build the delernen /alice/ section from alice/src/*.md (sources live in the repo).

用法（在仓库根目录或任意目录）：
    python3 scripts/build_alice.py

输入：alice/src/NN-slug.md（17 篇）。每篇文件格式：
    <!-- title: [B1] 页面标题 -->          页面 <h1> 与目录卡片标题（保持不变，Android 构建会核对）
    <!-- level: A2|B1|C1 -->
    <!-- desc: 目录卡片一句话导读 -->       （可选）
    来源：<原文标题> — Alice (Medium) <原文 URL>
    （日期/说明）
    # Alice 原文标题
    原文逐字照录；下面的 "> 中：" 行是中文译注，"> EN:" 是补充英文；⚠ 标出原文错误
    # 中文要点                                学习层小结（列表）
输出：alice/NN-slug.html（文件名 = 源文件名，URL 不变）+ alice/index.html。
页面模板与站内其它分区一致（/theme.css、manifest、pwa.js）。正文全部用 h2/h3/h4/p/li/table 输出，
scripts/build_android_data.py 的 AliceParser 可以直接解析成 alice.json 块。

原文版权归作者 Alice（alicelearngerman.medium.com）所有，此处仅作个人学习整理；每页顶部附原文链接。
"""
import html as htmlmod
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SRC = os.path.join(ROOT, "alice", "src")
OUT = os.path.join(ROOT, "alice")

COPYRIGHT = "原文版权归作者 Alice 所有，此处仅作个人学习整理"

CSS = """*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
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
.src a{color:var(--accent2)}
.src-top{font-size:13px;color:var(--text2);margin:6px 0 2px;line-height:1.7}
.src-top a{color:var(--accent2);word-break:break-word}
h4{font-size:14px;margin:12px 0 4px;color:var(--text2)}
hr{border:none;border-top:1px dashed var(--border);margin:14px 0}
p.orig{color:var(--text);font-size:15px;line-height:1.75;margin:12px 0 4px}
p.zh,p.en,li.zh,li.en{font-size:13px;line-height:1.7;margin:2px 0 6px;padding-left:10px;border-left:3px solid var(--accent)}
p.en,li.en{color:var(--text3);border-left-color:var(--border)}
li.zh,li.en{list-style:none;margin-left:20px}
ul.orig>li:not(.zh):not(.en){color:var(--text);margin-top:8px}
h2.sum{margin-top:24px;padding-top:12px;border-top:1px solid var(--border2)}
.card table td{white-space:normal;min-width:7em;vertical-align:top}"""

THEME_JS = """<script>
(function(){function apply(t){var r=document.documentElement;
if(t==='auto')r.setAttribute('data-theme',matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');
else r.setAttribute('data-theme',t);
var b=document.getElementById('themeBtn');if(b)b.textContent=t==='light'?'\\u2600\\ufe0f':t==='dark'?'\\ud83c\\udf19':'\\ud83d\\udd04';}
var cur=localStorage.getItem('delernen-theme')||'auto';apply(cur);
window.toggleTheme=function(){cur=cur==='auto'?'light':cur==='light'?'dark':'auto';localStorage.setItem('delernen-theme',cur);apply(cur);};})();
</script>"""


def esc(s):
    return htmlmod.escape(s, quote=False).replace('"', "&quot;")


def inline(s):
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*(?!\s)([^*\n]+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    return s


QUOTE_RE = re.compile(r"^\s*>\s?(.*)$")


def quote_class(text):
    return "en" if text.startswith("EN") else "zh"


def md_to_html(lines):
    """Render the body (after the 来源/说明 header lines).

    Supported: # / ## / ### headings, '> ' translation lines, '- ' lists with indented
    '  > ' translations, numbered lines '1. ' with indented '→' / '>' continuation,
    pipe tables, '---' rules, **bold**, *italic*. Every text unit becomes h2/h3/h4/p/li,
    so the Android AliceParser keeps all of it."""
    out = []
    i, n = 0, len(lines)
    while i < n:
        raw = lines[i].rstrip()
        line = raw.strip()
        if not line or line.startswith("<!--"):
            i += 1
            continue
        if raw.startswith("# "):
            title = raw[2:].strip()
            cls = ' class="sum"' if title.startswith("中文要点") else ""
            out.append(f"<h2{cls}>{inline(title)}</h2>")
        elif raw.startswith("## "):
            out.append(f"<h3>{inline(raw[3:].strip())}</h3>")
        elif raw.startswith("### "):
            out.append(f"<h4>{inline(raw[4:].strip())}</h4>")
        elif line == "---":
            out.append("<hr>")
        elif QUOTE_RE.match(raw) and not raw.startswith(" "):
            t = QUOTE_RE.match(raw).group(1).strip()
            out.append(f'<p class="{quote_class(t)}">{inline(t)}</p>')
        elif raw.startswith("|"):
            tbl = []
            while i < n and lines[i].strip().startswith("|"):
                tbl.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            i -= 1
            rows = [r for r in tbl if not all(re.match(r"^:?-+:?$", c) for c in r)]
            h = ["<table>"]
            for ri, r in enumerate(rows):
                tag = "th" if ri == 0 else "td"
                h.append("<tr>" + "".join(f"<{tag}>{inline(c)}</{tag}>" for c in r) + "</tr>")
            h.append("</table>")
            out.append("".join(h))
        elif raw.startswith("- "):
            items = []
            while i < n and (lines[i].startswith("- ") or (lines[i].startswith(" ") and lines[i].strip())):
                cur = lines[i]
                if cur.startswith("- "):
                    items.append(f"<li>{inline(cur[2:].strip())}</li>")
                else:
                    t = cur.strip()
                    m = QUOTE_RE.match(t)
                    if m:
                        q = m.group(1).strip()
                        c = quote_class(q)
                        items.append(f'<li class="{c}">{inline(q)}</li>')
                    else:
                        items.append(f'<li class="zh">{inline(t)}</li>')
                i += 1
            i -= 1
            out.append('<ul class="orig">' + "".join(items) + "</ul>")
        elif raw.startswith(" "):
            # indented continuation under a numbered line ('   → …' / '   > 中：…')
            m = QUOTE_RE.match(raw)
            if m:
                t = m.group(1).strip()
                out.append(f'<p class="{quote_class(t)}">{inline(t)}</p>')
            else:
                out.append(f'<p class="orig">{inline(line)}</p>')
        else:
            out.append(f'<p class="orig">{inline(line)}</p>')
        i += 1
    return "\n".join(out)


def parse_source(md):
    meta = {}
    for k in ("title", "level", "desc"):
        m = re.search(r"<!--\s*%s:\s*(.+?)\s*-->" % k, md)
        meta[k] = m.group(1).strip() if m else ""
    lines = [l for l in md.split("\n") if not l.strip().startswith("<!--")]
    while lines and not lines[0].strip():
        lines.pop(0)
    m = re.match(r"^来源：(.+?)\s+(https?://\S+)\s*$", lines[0].strip()) if lines else None
    if not m:
        raise ValueError("first content line must be '来源：<title> — Alice (Medium) <url>'")
    meta["src_title"], meta["src_url"] = m.group(1).strip(), m.group(2).strip()
    rest = lines[1:]
    note = ""
    if rest and rest[0].strip().startswith("（"):
        note = rest[0].strip()
        rest = rest[1:]
    meta["note"] = note
    return meta, rest


def page(title, body, back="index.html"):
    return f"""<!DOCTYPE html>
<html lang="zh"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)} · Alice Learn German 笔记</title>
<link rel="stylesheet" href="/theme.css">
<style>{CSS}</style><link rel="manifest" href="/manifest.webmanifest">
<meta name="theme-color" content="#0a0e1a">
<link rel="icon" type="image/png" href="/icons/icon-192.png">
<link rel="apple-touch-icon" href="/icons/apple-touch-icon.png">
</head>
<body><button id="themeBtn" onclick="toggleTheme()" title="切换主题">🔄</button>
<header><h1>{esc(title)}</h1><a class="back" href="{back}">← 返回目录</a></header>
<main><div class="card">{body}</div></main>
{THEME_JS}<script src="/pwa.js"></script>
</body></html>"""


def main():
    if not os.path.isdir(SRC):
        print("source dir not found:", SRC)
        sys.exit(1)
    files = sorted(f for f in os.listdir(SRC) if re.match(r"^\d\d-.+\.md$", f))
    if not files:
        print("no markdown found in", SRC)
        sys.exit(1)
    cards = {"A2": [], "B1": [], "C1": []}
    for fn in files:
        slug = fn[:-3]
        md = open(os.path.join(SRC, fn), encoding="utf-8").read()
        meta, rest = parse_source(md)
        title = meta["title"] or slug
        lvl = meta["level"] if meta["level"] in cards else "B1"
        banner = (f'<p><span class="lv lv-{lvl}">{lvl}</span>'
                  + ("📌 C1·以后看，先认得不深究" if lvl == "C1" else "") + "</p>\n")
        head = (f'<p class="src-top">来源：<a href="{esc(meta["src_url"])}" target="_blank" rel="noopener">'
                f'{esc(meta["src_title"])}</a></p>\n'
                f'<p class="meta">{COPYRIGHT}</p>\n'
                + (f'<p class="meta">{inline(meta["note"])}</p>\n' if meta["note"] else "")
                + "<hr>\n")
        body = banner + head + md_to_html(rest)
        with open(os.path.join(OUT, slug + ".html"), "w", encoding="utf-8") as f:
            f.write(page(title, body, back="index.html"))
        cards[lvl].append((slug, title, meta["desc"]))
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
    idx_body = ('<p class="meta">整理自 Alice 的 Medium 刊物 '
                '<a href="https://alicelearngerman.medium.com/" target="_blank" rel="noopener">'
                "alicelearngerman.medium.com</a>（原站 alicelearngerman.com 已下线）。"
                "每篇照录原文，逐句附中文译注（⚠ 标出原文错误）和中文要点，页首附原文链接。"
                f"{COPYRIGHT}。</p>\n" + "\n".join(parts))
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(page("Alice Learn German 学习笔记", idx_body, back="../"))
    print("index built:", len(files), "pages")


if __name__ == "__main__":
    main()
