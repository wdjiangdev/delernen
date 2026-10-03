import json, sys
sys.path.insert(0, '/tmp')
from word_families import FAMILIES

result = []
for root, members in FAMILIES.items():
    ms = []
    for item in members:
        if len(item) == 5:
            w, pos, zh, past, pp = item
        else:
            w, pos, zh = item[0], item[1], item[2]
            past, pp = '', ''
        ms.append({'word': w, 'pos': pos, 'zh': zh, 'past': past, 'pp': pp})
    result.append({'root': root, 'members': ms})

with open('/tmp/word_families.json', 'w', encoding='utf-8') as f:
    json.dump({'families': result}, f, ensure_ascii=False)
print('families:', len(result))
