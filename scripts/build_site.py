#!/usr/bin/env python3
"""DeLernen 构建脚本（只用 Python 标准库，部署时在服务器上运行）。

用法：python3 scripts/build_site.py <仓库目录> <输出目录>

做三件事：
1. 把站点文件复制到输出目录（不含 scripts/、deploy/ 等）。
2. 版本号自动化：页面里引用的本站 .js/.json（src=、href=、fetch('…')、file:'…'）
   一律改成 ?v=<文件内容哈希>。文件内容变了哈希就变，浏览器和 Cloudflare 都会取新文件；
   没变则继续用缓存。以后改词库不用再手动改 ?v=。
3. 生成 search/index.json（全站搜索用的语法/星图/文章索引），
   并把全站文件清单和版本写进 sw.js（离线缓存）。
"""
import hashlib, html, json, os, re, shutil, sys

SITE_ITEMS = ['index.html', 'manifest.webmanifest', 'pwa.js', 'sw.js', 'icons', 'search',
              'a1a2', 'a1b2', 'grammatik', 'kurs', 'nicos', 'memorize', 'alice']

REF_RE = re.compile(r'''(?P<q>["'])(?P<path>(?!https?:|//|data:)[\w./-]+\.(?:js|json))(?:\?v=[\w.-]*)?(?P=q)''')


def h8(path):
    with open(path, 'rb') as f:
        return hashlib.sha1(f.read()).hexdigest()[:8]


def strip_tags(s):
    s = re.sub(r'<(script|style)\b.*?</\1>', ' ', s, flags=re.S | re.I)
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', html.unescape(s)).strip()


def build_search_index(dst):
    items = []
    def add(**kw):
        items.append({k: v for k, v in kw.items() if v})
    # 语法 A1-B2（grammatik）
    p = os.path.join(dst, 'grammatik/grammar_learn.json')
    if os.path.exists(p):
        for g in json.load(open(p, encoding='utf8')):
            ex = ' '.join(' '.join(e) for e in g.get('examples', []))
            add(t='grammar', lv=g.get('level'), title=g.get('title'), sub=g.get('titleDe'),
                text=(g.get('explain', '') + ' ' + ex)[:1500], url='/grammatik/#g-' + g['id'])
    # 课程语法 A1-C1（kurs）
    for lv, fn in [('a1', 'grammar_kurs.json'), ('a2', 'grammar_a2.json'), ('b1', 'grammar_b1.json'),
                   ('b2', 'grammar_b2.json'), ('c1', 'grammar_c1.json')]:
        p = os.path.join(dst, 'kurs', lv, fn)
        if not os.path.exists(p):
            continue
        for g in json.load(open(p, encoding='utf8')):
            ex = ' '.join(' '.join(e) for e in g.get('examples', []))
            add(t='kurs', lv=lv.upper(), title=g.get('title'), sub=(g.get('num', '') + ' ' + g.get('titleDe', '')).strip(),
                text=(g.get('explain', '') + ' ' + ex)[:1500], url='/kurs/%s/#k-%s' % (lv, g['id']))
    # 单词星图（a1a2 / a1b2）：动词词干组、词族、语法组
    for sm, name in [('a1a2', 'A1-A2 星图'), ('a1b2', 'A1-B2 星图')]:
        base = os.path.join(dst, sm)
        p = os.path.join(base, 'verb_groups.json')
        if os.path.exists(p):
            for g in json.load(open(p, encoding='utf8'))['groups']:
                words = ' '.join('%s %s' % (m.get('verb', ''), m.get('zh', '')) for m in g['members'])
                add(t='star', lv=g.get('level'), title='%s 词干组' % g['stem'], sub='%s · %s' % (name, g.get('stemZh', '')),
                    text=words, url='/%s/' % sm)
        p = os.path.join(base, 'word_families.json')
        if os.path.exists(p):
            for g in json.load(open(p, encoding='utf8'))['families']:
                words = ' '.join('%s %s' % (m.get('word', ''), m.get('zh', '')) for m in g['members'])
                add(t='star', title='%s- 词族' % g['root'], sub=name, text=words, url='/%s/' % sm)
        p = os.path.join(base, 'grammar.json')
        if os.path.exists(p):
            for g in json.load(open(p, encoding='utf8'))['groups']:
                words = ' '.join('%s %s %s' % (m.get('word', ''), m.get('zh', ''), m.get('ex', '')) for m in g['members'])
                add(t='star', lv=g.get('level'), title=g.get('title'), sub='%s · %s' % (name, g.get('titleZh', '')),
                    text=words, url='/%s/' % sm)
    # Alice 笔记
    adir = os.path.join(dst, 'alice')
    if os.path.isdir(adir):
        for fn in sorted(os.listdir(adir)):
            if not fn.endswith('.html') or fn == 'index.html':
                continue
            s = open(os.path.join(adir, fn), encoding='utf8').read()
            m = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
            title = strip_tags(m.group(1)) if m else fn
            lv = re.match(r'\[(\w\d)\]', title)
            body = strip_tags(re.sub(r'<h1[^>]*>.*?</h1>', ' ', s, count=1, flags=re.S))
            add(t='alice', lv=lv.group(1) if lv else None, title=re.sub(r'^\[\w\d\]\s*', '', title),
                sub='Alice 笔记', text=body[:3000], url='/alice/' + fn)
    os.makedirs(os.path.join(dst, 'search'), exist_ok=True)
    with open(os.path.join(dst, 'search/index.json'), 'w', encoding='utf8') as f:
        json.dump(items, f, ensure_ascii=False, separators=(',', ':'))
    return len(items)


def main(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.makedirs(dst)
    for it in SITE_ITEMS:
        s = os.path.join(src, it)
        if os.path.isdir(s):
            shutil.copytree(s, os.path.join(dst, it))
        elif os.path.exists(s):
            shutil.copy2(s, os.path.join(dst, it))
    n_idx = build_search_index(dst)

    htmls = []
    for root, _, files in os.walk(dst):
        for fn in files:
            if fn.endswith('.html'):
                htmls.append(os.path.join(root, fn))

    stamped = 0
    for p in htmls:
        d = os.path.dirname(p)
        s = open(p, encoding='utf8').read()
        def rep(m):
            nonlocal stamped
            path = m.group('path')
            if path.endswith('/sw.js') or path == 'sw.js':
                return m.group(0)
            target = os.path.join(dst, path.lstrip('/')) if path.startswith('/') else os.path.join(d, path)
            target = os.path.normpath(target)
            if not os.path.isfile(target):
                return m.group(0)
            stamped += 1
            return '%s%s?v=%s%s' % (m.group('q'), path, h8(target), m.group('q'))
        s2 = REF_RE.sub(rep, s)
        if s2 != s:
            open(p, 'w', encoding='utf8').write(s2)

    # sw.js：全站文件清单 + 版本
    assets = []
    for root, _, files in os.walk(dst):
        for fn in sorted(files):
            full = os.path.join(root, fn)
            rel = '/' + os.path.relpath(full, dst).replace(os.sep, '/')
            if rel == '/sw.js':
                continue
            if fn == 'index.html':
                rel = rel[:-len('index.html')]
            assets.append((rel, full))
    assets.sort()
    hv = hashlib.sha1()
    for rel, full in assets:
        hv.update(rel.encode())
        hv.update(open(full, 'rb').read())
    version = hv.hexdigest()[:10]
    swp = os.path.join(dst, 'sw.js')
    if os.path.exists(swp):
        sw = open(swp, encoding='utf8').read()
        sw = sw.replace("var VERSION='dev';", "var VERSION='%s';" % version)
        sw = sw.replace('var PRECACHE=[];', 'var PRECACHE=%s;' % json.dumps([a for a, _ in assets], ensure_ascii=False))
        open(swp, 'w', encoding='utf8').write(sw)
    print('build ok: %d html, %d refs stamped, %d search items, %d precache files, version %s'
          % (len(htmls), stamped, n_idx, len(assets), version))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
