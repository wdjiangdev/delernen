#!/usr/bin/env python3
"""生成 Android App 的加速课数据资产 android/app/src/main/assets/data/weg.json。

来源（不在仓库内，默认 ~/workspace/nicosweg-content/，可用 --src 指定）：
- {a1,a2,b1}-NN.json：56 课内容 JSON（与网页端生成器同一批源文件；
  a1-01.json 由 extract_a1_01.py 从样板页提取，结构一致，多一个 vocab 三元组字段）
- b1-map.json：B1 每集的播放列表索引（Titelsong 占位导致 67 集起偏移）
- playlist-ids.txt：DW 官方 YouTube 播放列表全量视频 ID（yt-dlp --flat-playlist 顺序 dump）

词义（zh/en）从已生成的 App 资产 nicos_<level>.json 按 de 精确匹配补齐，
所以改词表后先跑 build_android_data.py 再跑本脚本。
视频在 App 课页内以 WebView 内嵌 YouTube 播放（yt 为视频 ID）；文字数据全量离线。
"""
import argparse
import html as ihtml
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "android/app/src/main/assets/data/weg.json"
LEVELS = (("a1", 18), ("a2", 19), ("b1", 19))


def strip_tags(t: str) -> str:
    return ihtml.unescape(re.sub(r"<[^>]+>", "", t))


def html_to_text(h: str) -> str:
    """语法卡 HTML -> 纯文本：表格行转「单元格 | 单元格」，段落空行分隔。"""
    s = re.sub(r"<br\s*/?>", "\n", h)

    def row(m):
        cells = re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", m.group(1), re.S)
        return "\n" + " | ".join(strip_tags(c).strip() for c in cells) + "\n"

    s = re.sub(r"<tr>(.*?)</tr>", row, s, flags=re.S)
    s = re.sub(r"</p>", "\n\n", s)
    s = re.sub(r"<li>", "\n• ", s)
    s = strip_tags(s)
    lines, out, blank = [ln.strip() for ln in s.split("\n")], [], True
    for ln in lines:
        if ln:
            out.append(ln)
            blank = False
        elif not blank:
            out.append("")
            blank = True
    return "\n".join(out).strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=str(Path.home() / "workspace/nicosweg-content"))
    args = ap.parse_args()
    src = Path(args.src)

    ids = [ln.strip() for ln in (src / "playlist-ids.txt").read_text().splitlines() if ln.strip()]
    assert len(ids) == 232, f"playlist-ids.txt 应为 232 条，实际 {len(ids)}"

    b1map = json.loads((src / "b1-map.json").read_text(encoding="utf-8"))
    b1_idx = {f["n"]: f["idx"] for les in b1map["lessons"] for f in les["folgen"]}

    def folge_idx(level: str, n: int) -> int:
        if level == "a1":
            return n            # 0=Trailer，Folge n 在索引 n
        if level == "a2":
            return 76 + n
        return b1_idx[n]

    # DW 官方视频直源（harvest_dw_video.py 抓、verify_dw_video.py 全量验过）：
    # f["n"] 即该级内的全局集号，与 dw-video-*.json 的键一致。
    video_map = json.loads((src / "dw-video-global.json").read_text(encoding="utf-8"))
    verified = json.loads((src / "dw-video-verified.json").read_text(encoding="utf-8"))
    mp4_verified = json.loads((src / "dw-video-mp4-verified.json").read_text(encoding="utf-8"))

    lessons, total_folgen = [], 0
    for level, count in LEVELS:
        vocab_asset = json.loads(
            (ROOT / f"android/app/src/main/assets/data/nicos_{level}.json").read_text(encoding="utf-8"))
        vmap = {w["de"]: w for w in vocab_asset}
        for num in range(1, count + 1):
            d = json.loads((src / f"{level}-{num:02d}.json").read_text(encoding="utf-8"))
            folgen = []
            for f in d["folgen"]:
                vm = video_map[level][str(f["n"])]
                vv = verified[level][str(f["n"])]
                mv = mp4_verified[level][str(f["n"])]
                folgen.append({
                    "n": f["n"], "t": f["t"], "d": f["d"],
                    "yt": ids[folge_idx(level, f["n"])],
                    "dw": vm["hls"] if vv.get("hls") else "",
                    "dwUt": vm["hlsUt"] if (vm.get("hlsUt") and vv.get("ut")) else "",
                    "mp4": vm["mp4"] if (vm.get("mp4") and mv.get("hd")) else "",
                    "mp4Sd": (vm["mp4"] or "").replace("_hd.mp4", "_sd.mp4")
                             if (vm.get("mp4") and mv.get("sd")) else "",
                    "mp4Ut": vm["mp4Ut"] if (vm.get("mp4Ut") and mv.get("ut")) else "",
                })
            total_folgen += len(folgen)

            if "vocab" in d:  # a1-01：三元组现成
                words = [{"de": de, "zh": zh, "en": en} for de, zh, en in d["vocab"]]
            else:
                words = []
                for de in d["vocab_de"]:
                    w = vmap.get(de)
                    assert w, f"{level}-{num:02d} 词不在词表: {de}"
                    words.append({"de": de, "zh": w.get("zh", ""), "en": w.get("en", "")})

            lessons.append({
                "level": level, "num": d["num"], "thema": d["thema"], "zh": d["zh"],
                "duration": d["duration"],
                "folgen": folgen,
                "cando": [re.sub(r"\s+", " ", strip_tags(c)).strip() for c in d["cando"]],
                "phrases": d["phrases"],
                "dialogue": d["dialogue"],
                "dialogueNote": d.get("dialogue_note", ""),
                "grammar": [{"title": g["title"], "text": html_to_text(g["html"])} for g in d["grammar"]],
                "words": words,
                "quiz": d["quiz"],
                "speaking": d["speaking"],
            })

    # ---- 断言（与网页端一致的口径） ----
    assert len(lessons) == 56, len(lessons)
    assert total_folgen == 228, total_folgen
    for les in lessons:
        tag = f"{les['level']}-{les['num']:02d}"
        assert len(les["phrases"]) == 12, (tag, "phrases", len(les["phrases"]))
        assert len(les["quiz"]) == 5, (tag, "quiz", len(les["quiz"]))
        expect_words = 40 if (les["level"], les["num"]) == ("a1", 1) else 36
        assert len(les["words"]) == expect_words, (tag, "words", len(les["words"]))
        assert all(f["yt"] for f in les["folgen"]), (tag, "yt missing")
        assert all(f["dw"] for f in les["folgen"]), (tag, "dw missing")
        assert all(f["mp4"] for f in les["folgen"]), (tag, "mp4 missing")

    OUT.write_text(json.dumps({"lessons": lessons}, ensure_ascii=False), encoding="utf-8")
    print(f"weg.json 已生成: 56 课 / {total_folgen} 集 / {OUT.stat().st_size/1024:.0f} KB -> {OUT}")

    # DW 单词录音映射（归一化键 -> mp3 文件名）：App 点读时按需下载并缓存，逻辑与网站一致
    audio_map = json.loads((src / "dw-audio-global.json").read_text(encoding="utf-8"))
    assert len(audio_map) > 4000, len(audio_map)
    audio_out = OUT.parent / "dw_audio.json"
    audio_out.write_text(json.dumps(audio_map, ensure_ascii=False), encoding="utf-8")
    print(f"dw_audio.json 已生成: {len(audio_map)} 条录音映射 / {audio_out.stat().st_size/1024:.0f} KB -> {audio_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
