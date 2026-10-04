# C1 课程语法与词汇（按站内实际模块顺序；C1 仍在更新，当前仅 2 节语法课上线）
# 数据源：站内课程目录+课件要点（已登录核验）；讲解与例句均为原创，不含视频内容
# 生成：python3 scripts/build_c1_grammar.py -> kurs/c1/grammar_c1.json
import json, os

GRAMMAR_POINTS = [
{'num': 'M21-01', 'id': 'dativ_verben2', 'cat': 'yufa', 'title': '支配第三格的动词（二）', 'titleDe': 'Verben mit Dativ (2)',
 'explain': '补充 A2 之后剩余的支配第三格的动词，主体是可分动词：beistehen（援助）、nachstellen（尾随）、nachstreben（追求）、nachgeben（让步）、nachkommen（履行/跟上）、nachlaufen（追随）、zulaufen（跑向），以及 beiwohnen（出席）、entsagen（放弃）、widerstehen（抵挡）和反身动词 sich widersetzen（反抗）。易错：nachkommen、nachgeben 等形式上容易被误用四格，必须整体记忆"动词 + 三格"的固定搭配；sich widersetzen 是反身代词 + 三格宾语的双重结构（sich dem Plan widersetzen），两部分都不能丢；部分动词偏书面正式（beiwohnen、entsagen、widerstehen），要结合语义场景掌握；易混字形：beistehen（援助）vs bestehen（存在/通过），按前缀区分。\n\n🇬🇧 英语对照：英语 help sb（无介词）；德语 beistehen + 三格——三格动词必须连格一起整体背。',
 'table': [['动词', '含义', '例子'],
           ['beistehen', '援助', 'Er steht mir bei.'],
           ['nachgeben', '让步', 'Er gibt dem Druck nach.'],
           ['nachkommen', '履行/跟上', 'Sie kommt ihrer Pflicht nach.'],
           ['widerstehen', '抵挡', 'Er widersteht der Versuchung.'],
           ['sich widersetzen', '反抗', 'Sie widersetzt sich dem Plan.']],
 'examples': [
     ('Er steht mir in schweren Zeiten bei.', '他在困难时期援助我。'),
     ('Sie kommt ihrer Pflicht nach.', '她履行了职责。'),
     ('Er widersteht der Versuchung nicht.', '他抵挡不住诱惑。'),
     ('Sie widersetzt sich dem Plan.', '她反抗这个计划。'),
 ]},
{'num': 'M22-01', 'id': 'adj_praep', 'cat': 'vokabel', 'title': '形容词和介词的搭配总结', 'titleDe': 'Adjektiv + Präposition',
 'explain': '按介词归纳最常用的形容词固定搭配（约 50 组）：von / auf / an / zu / bei / gegenüber / gegen / für / mit / nach / in / über。易错：表情绪的形容词介词不统一——ärgerlich、böse、wütend、eifersüchtig、neidisch、stolz 接 auf，而 glücklich、froh、erfreut、erstaunt、traurig、verwundert 接 über，不能想当然互换。近义形容词搭配不同：befreundet、verwandt、zufrieden、beschäftigt、fertig 统一接 mit；erfahren、unerfahren、nachlässig 接 in；fähig、unfähig、bereit 接 zu。高频组合整体背记：begeistert / überzeugt / enttäuscht / erfüllt + von，neugierig + auf，interessiert + an，不能按中文直译套介词。易混 gegenüber 与 gegen：zurückhaltend、aufgeschlossen 接 gegenüber（对人的态度），empfindlich、immun 接 gegen（对事物的敏感/免疫）。\n\n🇬🇧 英语对照：英语 interested in / proud of；德语 interessiert an / stolz auf——介词和英语对不上，必须连介词一起整体背。',
 'table': [['搭配', '中文'],
           ['stolz / böse / wütend + auf', '为…骄傲 / 生…的气'],
           ['glücklich / traurig + über', '对…高兴 / 难过'],
           ['interessiert + an', '对…感兴趣'],
           ['zufrieden / fertig + mit', '对…满意 / 完成'],
           ['fähig / bereit + zu', '有能力… / 准备好…'],
           ['neugierig + auf', '对…好奇'],
           ['begeistert / enttäuscht + von', '为…着迷 / 失望']],
 'examples': [
     ('Ich bin stolz auf dich.', '我为你骄傲。'),
     ('Sie ist an Musik interessiert.', '她对音乐感兴趣。'),
     ('Bist du mit dem Ergebnis zufrieden?', '你对结果满意吗？'),
     ('Er ist neugierig auf alles.', '他对一切都好奇。'),
 ]},
]

def main():
    for p in GRAMMAR_POINTS:
        assert len(p['examples']) == 4, p['id']
    out = os.path.join(os.path.dirname(__file__), '..', 'kurs', 'c1', 'grammar_c1.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(GRAMMAR_POINTS, f, ensure_ascii=False, indent=1)
    print(f"wrote {len(GRAMMAR_POINTS)} cards -> {out}")

if __name__ == '__main__':
    main()
