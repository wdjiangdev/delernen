#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 delernen 网站数据源转换成 Android App (android/app/src/main/assets/data/) 用的 JSON。

可重复运行、幂等：每次全量重写输出文件，不依赖任何中间状态。

输出文件与数据源对照：
  nicos_a1.json / nicos_a2.json / nicos_b1.json   <- nicos/{a1,a2,b1}/vocab.js（原样转 JSON）
  verb_groups_a1a2.json / verb_groups_a1b2.json   <- {a1a2,a1b2}/verb_groups.json（原样拷贝）
  word_families_a1a2.json / word_families_a1b2.json
  grammar_a1a2.json / grammar_a1b2.json
  sep_a1a2.json / sep_a1b2.json                   <- memorize/sep_*.js（原样转 JSON）
  kurs.json                                       <- kurs/{a1,a2,b1,b2,c1}/grammar*.json（五级合并，补 level 字段）
  alice.json                                      <- alice/01..17-*.html（转结构化块数组）
"""
import html as html_mod
import json
import re
import shutil
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "android" / "app" / "src" / "main" / "assets" / "data"

# 简报给出的源数据条数（用于校验）
EXPECTED = {
    "nicos_a1": 1725,
    "nicos_a2": 1731,
    "nicos_b1": 961,
    "sep_a1a2": 27,
    "sep_a1b2": 49,
    "kurs_total": 94,
    "alice_notes": 17,
}


def load_js_array(path: Path):
    """读取 `var NAME=[...];` 形式的 JS 文件，返回解析后的数组。"""
    s = path.read_text(encoding="utf-8")
    i = s.find("[")
    if i < 0:
        raise ValueError(f"{path}: 找不到 JSON 数组")
    return json.loads(s[i:].rstrip().rstrip(";"))


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write("\n")


def norm_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


# ---------------------------------------------------------------- nicos / sep
def convert_nicos():
    counts = {}
    for lvl in ("a1", "a2", "b1"):
        src = ROOT / "nicos" / lvl / "vocab.js"
        data = load_js_array(src)
        write_json(OUT_DIR / f"nicos_{lvl}.json", data)
        counts[f"nicos_{lvl}"] = len(data)
    return counts


def convert_sep():
    counts = {}
    for name in ("sep_a1a2", "sep_a1b2"):
        src = ROOT / "memorize" / f"{name}.js"
        data = load_js_array(src)
        write_json(OUT_DIR / f"{name}.json", data)
        counts[name] = len(data)
    return counts


# ---------------------------------------------------------------- 原样拷贝
def copy_json(rel_src: str, out_name: str):
    shutil.copyfile(ROOT / rel_src, OUT_DIR / out_name)


# ---------------------------------------------------------------- kurs 合并
def convert_kurs():
    merged = []
    per_level = {}
    for lvl in ("a1", "a2", "b1", "b2", "c1"):
        d = ROOT / "kurs" / lvl
        # a1 的文件叫 grammar_kurs.json，其余等级叫 grammar_<level>.json，两种都接受
        cand = [d / "grammar_kurs.json", d / f"grammar_{lvl}.json"]
        src = next((p for p in cand if p.exists()), None)
        if src is None:
            raise FileNotFoundError(f"kurs/{lvl}: 找不到 grammar_kurs.json 或 grammar_{lvl}.json")
        cards = json.loads(src.read_text(encoding="utf-8"))
        if not isinstance(cards, list):
            raise ValueError(f"{src}: 顶层不是数组")
        for card in cards:
            if "level" not in card:
                card["level"] = lvl.upper()
        merged.extend(cards)
        per_level[lvl.upper()] = len(cards)
    write_json(OUT_DIR / "kurs.json", merged)
    return per_level


# ---------------------------------------------------------------- alice
ALICE_DIR = ROOT / "alice"

# 产出块的内联容器（不直接产生块）；块级标签产生块；其余内联标签透明
CONTAINER_TAGS = {"main", "div", "ul", "ol", "table", "tbody", "thead", "tfoot"}
BLOCK_TAGS = {"p", "h1", "h2", "h3", "h4", "li"}
CELL_TAGS = {"td", "th"}


def _split_vocab_items(s: str):
    """按零括号深度的 ', ' / '｜' / '、' 切分词条串。"""
    parts, cur, depth = [], [], 0
    i, n = 0, len(s)
    while i < n:
        ch = s[i]
        if ch in "（(":
            depth += 1
            cur.append(ch)
        elif ch in "）)":
            depth = max(0, depth - 1)
            cur.append(ch)
        elif depth == 0 and (ch == "｜" or ch == "、"):
            parts.append("".join(cur))
            cur = []
        elif depth == 0 and ch == "," and i + 1 < n and s[i + 1] == " ":
            parts.append("".join(cur))
            cur = []
            i += 1  # 跳过空格
        else:
            cur.append(ch)
        i += 1
    parts.append("".join(cur))
    return [p.strip() for p in parts if p.strip()]


def _try_vocab(text: str):
    """严格匹配「标签：词1（释义1）, 词2（释义2）…」段落，失败返回 None（回退为 p）。"""
    m = re.match(r"^([^：]{1,20})：(.+)$", text, re.S)
    if not m:
        return None
    label = m.group(1).strip()
    rest = m.group(2).strip()
    if not label or "（" not in rest:
        return None
    items = _split_vocab_items(rest)
    if len(items) < 2:
        return None
    out = []
    for it in items:
        mm = re.match(r"^(.+?)（(.+)）$", it, re.S)
        if not mm:
            return None
        de = norm_ws(mm.group(1))
        zh = norm_ws(mm.group(2))
        if not de or not zh or "：" in de:
            return None
        out.append({"type": "vocab", "text": de, "zh": zh})
    return label, out


class AliceParser(HTMLParser):
    """只取 <main> 内正文语义：h2/h3 -> h，p -> p，li -> li，表格按行转 p；
    满足严格模式的「标签：词（释义）」段落拆成 vocab 块。丢弃 CSS/脚本/导航。"""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_main = False
        self.stack = []          # frame: dict(kind=..., ...)
        self.blocks = []         # 产出块
        self.title = ""
        self.level = ""
        self._badge = ""         # 最近一个 .lv 徽章文本

    # ---- 标签 ----
    def handle_starttag(self, tag, attrs):
        if tag == "main":
            self.in_main = True
            return
        if not self.in_main:
            return
        if tag in ("script", "style"):
            self.stack.append({"kind": "skip"})
            return
        cls = dict(attrs).get("class", "")
        if tag == "span" and re.search(r"(^|\s)lv(\s|$)", cls):
            self.stack.append({"kind": "badge", "buf": []})
            return
        if tag in BLOCK_TAGS:
            self.stack.append({"kind": "block", "tag": tag, "buf": [], "badge": ""})
        elif tag in CELL_TAGS:
            self.stack.append({"kind": "cell", "buf": []})
        elif tag == "tr":
            self.stack.append({"kind": "row", "cells": []})
        elif tag in CONTAINER_TAGS:
            self.stack.append({"kind": "container"})
        # 其余内联标签（a/strong/em/small/span...）透明，文本直接进当前块

    def handle_data(self, data):
        for fr in reversed(self.stack):
            if fr["kind"] in ("block", "cell", "badge"):
                fr["buf"].append(data)
                return
            if fr["kind"] == "skip":
                return
        # 容器直接子文本（罕见）忽略

    def handle_endtag(self, tag):
        if tag == "main":
            self.in_main = False
            return
        if not self.stack:
            return
        if tag in ("script", "style"):
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i]["kind"] == "skip":
                    del self.stack[i:]
                    return
            return
        if tag == "span":
            if self.stack and self.stack[-1]["kind"] == "badge":
                fr = self.stack.pop()
                self._badge = norm_ws("".join(fr["buf"]))
                if self.level == "" and self._badge:
                    self.level = self._badge
                for j in range(len(self.stack) - 1, -1, -1):
                    if self.stack[j]["kind"] == "block":
                        self.stack[j]["badge"] = self._badge
                        break
            return
        if tag in CELL_TAGS:
            if self.stack and self.stack[-1]["kind"] == "cell":
                fr = self.stack.pop()
                txt = norm_ws("".join(fr["buf"]))
                for j in range(len(self.stack) - 1, -1, -1):
                    if self.stack[j]["kind"] == "row":
                        self.stack[j]["cells"].append(txt)
                        break
            return
        if tag == "tr":
            if self.stack and self.stack[-1]["kind"] == "row":
                fr = self.stack.pop()
                cells = [c for c in fr["cells"]]
                if any(c for c in cells):
                    self.blocks.append({"type": "p", "text": " | ".join(cells)})
            return
        if tag in BLOCK_TAGS:
            if self.stack and self.stack[-1]["kind"] == "block":
                self._finalize_block(self.stack.pop())
            return
        if tag in CONTAINER_TAGS:
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i]["kind"] == "container":
                    del self.stack[i:]
                    return

    def _finalize_block(self, fr):
        text = norm_ws("".join(fr["buf"]))
        badge = fr["badge"]
        if badge:
            if text == badge:            # 纯等级徽章段（元数据，level 字段已记录）
                return
            if text.startswith(badge):   # 徽章 + 后续正文，去掉徽章文本
                text = text[len(badge):].lstrip()
        if not text:
            return
        tag = fr["tag"]
        if tag in ("h2", "h3", "h4"):
            self.blocks.append({"type": "h", "text": text})
        elif tag == "li":
            self.blocks.append({"type": "li", "text": text})
        else:  # p
            v = _try_vocab(text)
            if v:
                label, items = v
                self.blocks.append({"type": "p", "text": label})
                self.blocks.extend(items)
            else:
                self.blocks.append({"type": "p", "text": text})


def _clean_tagged(s: str) -> str:
    return norm_ws(re.sub(r"<[^>]+>", "", s))


def load_alice_index():
    """alice/index.html -> {文件名: (level, 标题)}"""
    s = (ALICE_DIR / "index.html").read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r'<a class="idx-card" href="([^"]+)">(.*?)</a>', s, re.S):
        href, inner = m.group(1), m.group(2)
        lv = re.search(r'lv-([ABC]\d)', inner)
        tm = re.search(r"</span>(.*?)</h2>", inner, re.S)
        if lv and tm:
            out[href] = (lv.group(1), _clean_tagged(tm.group(1)))
    return out


def convert_alice():
    index_map = load_alice_index()
    notes = []
    warnings = []
    for path in sorted(ALICE_DIR.glob("[0-9][0-9]-*.html")):
        raw = path.read_text(encoding="utf-8")
        p = AliceParser()
        p.feed(raw)
        title_m = re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.S)
        title = _clean_tagged(html_mod.unescape(title_m.group(1))) if title_m else ""
        if not title and path.name in index_map:
            title = index_map[path.name][1]
        level = p.level
        if not level:
            m = re.match(r"^\[([ABC]\d)\]", title)
            if m:
                level = m.group(1)
        if not level and path.name in index_map:
            level = index_map[path.name][0]
        if not level:
            warnings.append(f"{path.name}: 无法确定等级")
            level = ""
        if path.name in index_map:
            exp_lv, exp_title = index_map[path.name]
            if level and exp_lv and level != exp_lv:
                warnings.append(f"{path.name}: 页内等级 {level} 与目录 {exp_lv} 不一致")
            if exp_title and title and norm_ws(exp_title) != norm_ws(title):
                warnings.append(f"{path.name}: 标题与目录不一致（页内 {title!r} / 目录 {exp_title!r}）")
        notes.append({"title": title, "level": level, "blocks": p.blocks})
    if len(notes) != EXPECTED["alice_notes"]:
        raise ValueError(f"alice 笔记 {len(notes)} 篇 != 预期 {EXPECTED['alice_notes']}")
    for w in warnings:
        print(f"  [warn] {w}", file=sys.stderr)
    write_json(OUT_DIR / "alice.json", notes)
    return notes


# ---------------------------------------------------------------- 主流程
def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    report = []

    # 1) nicos（原样转 JSON）
    nicos_counts = convert_nicos()
    for k, n in nicos_counts.items():
        if n != EXPECTED[k]:
            raise ValueError(f"{k}: {n} 条 != 预期 {EXPECTED[k]}")
        report.append((f"{k}.json", n, EXPECTED[k]))

    # 2) 可分动词分组 / 词族 / 语法（原样拷贝）
    copies = [
        ("a1a2/verb_groups.json", "verb_groups_a1a2.json"),
        ("a1b2/verb_groups.json", "verb_groups_a1b2.json"),
        ("a1a2/word_families.json", "word_families_a1a2.json"),
        ("a1b2/word_families.json", "word_families_a1b2.json"),
        ("a1a2/grammar.json", "grammar_a1a2.json"),
        ("a1b2/grammar.json", "grammar_a1b2.json"),
    ]
    for src, out in copies:
        copy_json(src, out)
        d = json.loads((OUT_DIR / out).read_text(encoding="utf-8"))
        key = "groups" if "groups" in d else "families"
        report.append((out, len(d[key]), "-"))

    # 拷贝校验：JSON 结构完整即可（totalVerbs 是网站侧统计口径，
    # 不等于分组内 members 数之和，不做等式断言，仅打印对照）
    for out in ("verb_groups_a1a2.json", "verb_groups_a1b2.json"):
        d = json.loads((OUT_DIR / out).read_text(encoding="utf-8"))
        mem = sum(len(g["members"]) for g in d["groups"])
        print(f"{out}: groups={len(d['groups'])} members={mem} totalVerbs(源元数据)={d['totalVerbs']}")

    # 3) sep（原样转 JSON）
    sep_counts = convert_sep()
    for k, n in sep_counts.items():
        if n != EXPECTED[k]:
            raise ValueError(f"{k}: {n} 条 != 预期 {EXPECTED[k]}")
        report.append((f"{k}.json", n, EXPECTED[k]))

    # 4) kurs 五级合并
    kurs_per_level = convert_kurs()
    kurs_total = sum(kurs_per_level.values())
    if kurs_total != EXPECTED["kurs_total"]:
        raise ValueError(f"kurs: {kurs_total} 卡 != 预期 {EXPECTED['kurs_total']}")
    report.append(("kurs.json", kurs_total, EXPECTED["kurs_total"]))
    print("kurs 分级条数: " + ", ".join(f"{k}={v}" for k, v in kurs_per_level.items()))

    # 5) alice
    notes = convert_alice()
    lv_counts = {}
    for nt in notes:
        lv_counts[nt["level"]] = lv_counts.get(nt["level"], 0) + 1
    print("alice 等级分布: " + ", ".join(f"{k}={v}" for k, v in sorted(lv_counts.items())))
    total_blocks = sum(len(n["blocks"]) for n in notes)
    print(f"alice 总块数: {total_blocks}")
    report.append(("alice.json", len(notes), EXPECTED["alice_notes"]))

    # 汇总
    print("\n=== 输出文件清单 ===")
    for name, n, exp in report:
        flag = "OK" if (exp == "-" or n == exp) else "MISMATCH!"
        exp_s = str(exp)
        print(f"{name:28s} 条数={n:<6d} 源数据={exp_s:<6s} {flag}")
    print(f"\n全部输出目录: {OUT_DIR}")
    print("文件数:", len(list(OUT_DIR.glob('*.json'))))


if __name__ == "__main__":
    main()
