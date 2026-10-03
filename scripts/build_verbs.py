import glob, re, json
from collections import Counter, defaultdict

verb_defs = {}
verb_set = set()
for ch in 'abcdefghijklmnopqrstuvwxyz':
    try:
        with open(f'/opt/htd-edu-data/outputs/词汇星图/dicts/{ch}.jsonl', encoding='utf-8') as f:
            for line in f:
                try:
                    e = json.loads(line)
                    lemma = e.get('lemma', '').lower()
                    senses = e.get('senses', [])
                    is_verb = any(s.get('partOfSpeech') == 'verb' for s in senses)
                    if is_verb and lemma.endswith('en') and len(lemma) > 3:
                        verb_set.add(lemma)
                        if lemma not in verb_defs:
                            for s in senses:
                                if s.get('partOfSpeech') == 'verb':
                                    d = s.get('definitionEn', {})
                                    txt = d.get('text', '') if isinstance(d, dict) else ''
                                    if txt:
                                        verb_defs[lemma] = txt
                                        break
                except:
                    pass
    except:
        pass

verbs = Counter()
for fp in glob.glob('/opt/htd-edu-data/outputs/背书工具/*/source.txt'):
    try:
        text = open(fp, encoding='utf-8').read().lower()
        for w in re.findall(r'[a-zäöüß]{4,}en', text):
            verbs[w] += 1
    except:
        pass

real_verbs = {w: c for w, c in verbs.items() if w in verb_set}

PREFIXES = sorted(['zurück', 'zusammen', 'wieder', 'weiter', 'ab', 'an', 'auf', 'aus', 'bei', 'ein', 'mit', 'nach', 'vor', 'zu', 'los', 'weg', 'fest', 'fern', 'her', 'hin', 'dar', 'durch', 'über', 'um', 'unter', 'wider', 'be', 'ent', 'er', 'ver', 'zer', 'ge', 'miss', 'emp'], key=len, reverse=True)

def get_stem(verb):
    for p in PREFIXES:
        if verb.startswith(p) and len(verb) > len(p) + 2:
            stem = verb[len(p):]
            if stem in verb_set:
                return stem, p
    return verb, None

groups = defaultdict(list)
for v in real_verbs:
    stem, prefix = get_stem(v)
    groups[stem].append({'verb': v, 'prefix': prefix, 'count': real_verbs[v], 'def': verb_defs.get(v, '')})

result = []
for stem in sorted(groups.keys(), key=lambda s: -len(groups[s])):
    members = groups[stem]
    if len(members) >= 2:
        members.sort(key=lambda m: (m['prefix'] is not None, m['verb']))
        result.append({
            'stem': stem,
            'stemDef': verb_defs.get(stem, ''),
            'members': members
        })

with open('/tmp/verb_groups.json', 'w', encoding='utf-8') as f:
    json.dump({'groups': result, 'totalVerbs': len(real_verbs)}, f, ensure_ascii=False)

print('groups:', len(result), 'total verbs:', len(real_verbs))
