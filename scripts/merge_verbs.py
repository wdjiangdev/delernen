import json, sys
sys.path.insert(0, '/tmp')
from verb_data import VERBS

d = json.load(open('/tmp/verb_groups.json', encoding='utf-8'))

missing = []
for g in d['groups']:
    for m in g['members']:
        v = m['verb']
        if v in VERBS:
            past, pp, zh = VERBS[v]
            m['past'] = past
            m['pp'] = pp
            m['zh'] = zh
        else:
            missing.append(v)
            m['past'] = ''
            m['pp'] = ''
            m['zh'] = ''

if missing:
    print('MISSING:', missing)

json.dump(d, open('/tmp/verb_groups.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('done, groups:', len(d['groups']))
