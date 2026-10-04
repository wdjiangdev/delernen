# A1 课程整理（按站内实际模块顺序：32 个语法点 + 9 个词汇点）
# 数据源：站内课程目录+课件要点（已登录核验）；讲解为原创重写（贴近原文要点），例句采用课程原文短句，不含视频内容
# 生成：python3 scripts/build_kurs_grammar.py -> kurs/a1/grammar_kurs.json
import json, os

GRAMMAR_POINTS = [{'num': 'M01-01',
  'id': 'zimu',
  'cat': 'yuyin',
  'title': '德语字母表',
  'titleDe': 'Alphabet',
  'explain': '德语字母表共 30 个：26 个基本拉丁字母 + 4 个特殊字母（Ä ä、Ö ö、Ü ü、ß）。Ä、Ö、Ü 是变元音；ß 叫 Eszett，读 '
             '[ɛs-tsɛt]，只有小写没有大写。最容易和英语搞混的几个优先记：V 读 [fao]、W 读 [ve:]、J 读 [jɔt]、C 读 [tse:]、Z 读 '
             '[tsɛt]、Y 读 [ypsilɔn]。R 读 '
             '[ɛr]（小舌音）是初学者公认难点，老师原话：没有特别神奇的方法，"一般只能含着水漱口然后等待缘分的到来"。德语没有声调，页面录音的字母都读"一声"，其他视频里读轻声也对，德国人听不出区别，不要纠结。大小写都要会认：德语所有名词首字母大写，拼写大小写不能错。页面上每个字母可点击播放标准读音，建议用电脑打开（手机浏览器缓存不足会导致部分音频点不开）。\n'
             '\n'
             '🇬🇧 英语对照：英语 26 个字母，Z 读 [zi:]；德语 Z 读 [tsɛt]，还多了 4 个特殊字母，ß 只在小写出现。',
  'table': [['字母', '读音', '备注'],
            ['V v', '[fao]', '不读英语的 [vi:]'],
            ['W w', '[ve:]', '不读 [ˈdʌbəlju:]'],
            ['J j', '[jɔt]', '不读 [dʒei]'],
            ['C c', '[tse:]', '不读 [si:]'],
            ['Z z', '[tsɛt]', '不读 [zi:]'],
            ['Y y', '[ypsilɔn]', '不读 [wai]'],
            ['R r', '[ɛr]', '小舌音，公认难点'],
            ['ß', '[ɛs-tsɛt]', '叫 Eszett，只有小写']],
  'examples': [['V v —— [fao]', '不读英语的 [vi:]'],
               ['W w —— [ve:]', '不读 [ˈdʌbəlju:]'],
               ['R r —— [ɛr]', '小舌音，含着水漱口练'],
               ['ß —— [ɛs-tsɛt]', '叫 Eszett，只有小写']]},
 {'num': 'M01-02~04',
  'id': 'fayin',
  'cat': 'yuyin',
  'title': '发音规则',
  'titleDe': 'Ausspracheregeln',
  'explain': '元音长短对立是德语发音的灵魂：长音和短音能区分词义（da [da:] vs dann '
             '[dan]），必须发准。拼写判断规律：元音后只跟一个辅音读长音（da、den、du、ihm、Ofen），跟两个及以上辅音读短音（dann、denn、dumm、im、offen）。p/t/k '
             '是送气清音，b/d/g 是不送气浊音；对中文母语者区别主要在"送气与否"（类似"坡/播"）。词尾清化：b/d/g 在词尾发成 [p]/[t]/[k]（Tag 读 '
             '[ta:k]），在词中则正常发音（Tage 的 g 发 [g]）。s 看位置发音：元音前发 [z]（Hansa），词尾/辅音前发 [s]（Hans）；z 永远发 '
             '[ts]。f 发 [f]，v 和 w 都发 [v]，常同音，靠拼写区分（如 Fest/West）。ch 的规则：a o u 后读 [x]（Bach），其余读 '
             '[ç]（ich），外来词读 [k]，词尾 -ig 读 [iç]。r：词首发 [r]，元音后或词尾发 [ɐ]。组合：sch=[ʃ]，词首 '
             'sp=[ʃp]、st=[ʃt]（只在词首！），z=[ts]，ng 的 g '
             '不发音。双元音：ei=[ai]、au=[ao]、eu/äu=[ɔy]。老师强调：长短不分"也能听懂"，但想说得地道就必须区分——先保区分度，再求标准度。\n'
             '\n'
             '🇬🇧 英语对照：英语发音例外更多，德语规则性强得多；但德语有英语没有的音：ch（ich/Bach 对立）、小舌音 r、词尾清化。',
  'table': [['规则', '例子'],
            ['长音：1辅音/aa/元音+h', 'da [da:]、Ofen'],
            ['短音：2+辅音', 'dann [dan]、offen'],
            ['送气：p/t/k vs b/d/g', 'Post（送气）vs Boss（不送气）'],
            ['s：元音前[z]其余[s]', 'Hansa [z] / Hans [s]'],
            ['ch：aou后[x]其余[ç]', 'Bach [x] / ich [ç]'],
            ['词尾清化 bdg→ptk', 'Tag→[ta:k]'],
            ['词首sp/st→ʃp/ʃt', 'Sport、Stadt'],
            ['双元音', 'mein [ai]、Haus [ao]、heute [ɔy]']],
  'examples': [['da [da:] —— dann [dan]', '长音 vs 短音，能区分词义'],
               ['Tag [ta:k] —— Tage', '词尾 g 清化，词中正常发音'],
               ['Post —— Boss', '[p]送气清音 vs [b]不送气'],
               ['Hans [s] —— Hansa [z]', 's 看位置发音']]},
 {'num': 'M01-05',
  'id': 'artikel_nomen',
  'cat': 'mingci',
  'title': '冠词、名词的性与单复数',
  'titleDe': 'Artikel & Nomen',
  'explain': '德语名词分三种性：阳性（der）、阴性（die）、中性（das）；背单词必须连同冠词一起背，der/die/das 就是词性标记。不定冠词：阳性/中性 ein，阴性 '
             'eine；定冠词 der/die/das；所有复数定冠词统一是 die。老师给了三个"概率记忆法"：①67% 的单音节名词是阳性，剩下多是中性；②90% 以字母 e '
             '结尾的名词是阴性；③90% 以 Ge 开头的名词是中性。硬性规则：以 -chen 结尾的都是中性词，表示"小"，如 das '
             'Mädchen（小女孩）。复数变化逐个记：der Zug → die Züge（加变音+en），die Frage → die Fragen（+n），die Stadt '
             '→ die Städte，das Haus → die Häuser，das Bild → die Bilder，das Auto → die '
             'Autos（+s）。易错点：不要按自然性别猜词性（如 Mädchen 是中性不是阴性），拿不准就查词典。ein/eine 既是"一"也是不定冠词（对应英语 '
             'a/an）；复数没有不定冠词。\n'
             '\n'
             '🇬🇧 英语对照：英语 a/an/the 不分性；德语冠词自带"性数"标记，是语法的地基。',
  'table': [['', '阳性', '阴性', '中性', '复数'],
            ['定冠词', 'der Mann', 'die Frau', 'das Kind', 'die Kinder'],
            ['不定冠词', 'ein Mann', 'eine Frau', 'ein Kind', '—（没有）']],
  'examples': [['ein Tag - a day', '一天（阳性，不定冠词）'],
               ['der Tag - the day', '这一天（阳性定冠词）'],
               ['die Tage - the days', '这些天（复数定冠词统一 die）'],
               ['das Mädchen', '小女孩（-chen 结尾，中性）']]},
 {'num': 'M01-06',
  'id': 'konjugation',
  'cat': 'dongci',
  'title': '人称代词和动词变位',
  'titleDe': 'Personalpronomen & Konjugation',
  'explain': '代词先跟"语法性别"走，不跟自然性别：der Hund→er，die Katze→sie，das Pferd→es；桌子 der Tisch 也用 er '
             '指。规则动词变位口诀：找词干（去 -en/-n），ich+e，du+st，er/sie/es+t，wir/sie 用原形，ihr+t。三个特殊拼写规则：①词干以 '
             't/d/ffn/tm/gn/chn/dn 结尾，先加 e 再变位（du arbeitest）；②词干以 s/ß/x/z 结尾，du 直接加 t（du heißt）；③以 '
             '-ern/-eln 结尾，去 n 得词干（wir feiern）。不规则变化只发生在 du 和 er/sie/es：词尾仍规则，词干元音可能加变音（du '
             'fährst）或 e→i（du sprichst），辅音有时双写（du nimmst）。sein（ich bin, du bist, er ist）和 '
             'haben（ich habe, du hast, er hat）全不规则，单独背。易错点：sie（她/他们/它们）vs Sie（您）大小写决定含义；du（你）vs '
             'ihr（你们）vs Sie（您）别混。答疑确认：er/sie/es 的复数形式是 sie；-eln 结尾的动词都读 [əln]，要背下来（如 sammeln）。\n'
             '\n'
             '🇬🇧 英语对照：英语变位只剩三单加 s；德语六个人称全变，是动词语法的第一道坎。',
  'table': [['人称', '词尾', 'machen', '备注'],
            ['ich', '-e', 'mache', ''],
            ['du', '-st', 'machst', 's/ß/x/z结尾只加-t'],
            ['er/sie/es', '-t', 'macht', '不规则只变这里'],
            ['wir', '-en', 'machen', ''],
            ['ihr', '-t', 'macht', 'du的复数是ihr'],
            ['sie/Sie', '-en', 'machen', '']],
  'examples': [['Der Hund schläft. Er ist müde.', '狗在睡觉。它累了。（der Hund→er）'],
               ['Die Katze spielt. Sie ist klein.', '猫在玩。它很小。（die Katze→sie）'],
               ['Ich komme aus China.', '我来自中国。'],
               ['Er heißt Thomas.', '他叫 Thomas。']]},
 {'num': 'M01-07',
  'id': 'satzbau',
  'cat': 'jufa',
  'title': '德语句式结构',
  'titleDe': 'Satzbau',
  'explain': '陈述句铁律：变位动词永远在第二位，主语通常在第一位（Ich lerne Deutsch in '
             'Berlin）。强调技巧：把想强调的成分提前到第一位，主语必须紧跟变位动词——Deutsch lerne ich in Berlin 强调"学的是德语"，In '
             'Berlin lerne ich Deutsch 强调"在柏林学"。一般疑问句：把变位动词提前到句首即可（Lernst du Deutsch in Berlin?），答 '
             'Ja/Nein。特殊疑问句 = 疑问词 + '
             '一般疑问句：was（什么）、wie（怎样）、wer（谁，主格）、wo（哪里）、woher（从哪里）、wohin（去哪里）。der/die/das 可直接作代词（类似 '
             'this/that）；主系表结构中 das 可代指任何词性的名词，所以永远问 Was ist das?。细节：Wie geht es dir? 主语是 '
             'es（"你的近况对你而言怎么样"），dir '
             '是"对你而言"——不能用汉语翻译反推德语语法。老师纠正：记住两句——"陈述句想强调什么放句首；把陈述句变位动词提前到句首就变成一般疑问句"。\n'
             '\n'
             '🇬🇧 英语对照：英语语序相对固定（SVO）；德语是"动词第二位"语言，句首位置是强调位。',
  'table': [['类型', '结构', '例子'],
            ['陈述句', '主语 + 动词2位', 'Ich lerne Deutsch.'],
            ['状语前置', '时间 + 动词2位 + 主语', 'Heute lerne ich Deutsch.'],
            ['一般问句', '动词1位 + 主语', 'Lernst du Deutsch?'],
            ['特殊问句', '疑问词 + 动词2位 + 主语', 'Woher kommst du?']],
  'examples': [['Ich lerne Deutsch in Berlin.', '我在柏林学德语。'],
               ['Deutsch lerne ich in Berlin.', '在柏林我学的是德语。（宾语前置表强调）'],
               ['Lernst du Deutsch in Berlin?', '你在柏林学德语吗？'],
               ['Woher kommen Sie? — Ich komme aus China.', '您从哪里来？——我来自中国。']]},
 {'num': 'M01-12',
  'id': 'possessiv',
  'cat': 'mingci',
  'title': '物主代词',
  'titleDe': 'Possessivpronomen',
  'explain': '物主代词 = 人称代词词干 + 冠词词尾：mein/dein/Ihr/sein/ihr/unser/euer，词尾变化和不定冠词 ein '
             '完全一样。词尾看"被拥有者"的性数格，不是拥有者：mein Name（阳单）、meine Muttersprache（阴单）、mein Land（中单）、meine '
             'Lehrer（复数）。易错点：sein（他/它的）vs ihr（她/他们/它们的）；"您"的 Ihr 永远大写。euer 的形式：euer Name / eure '
             'Muttersprache / euer Land / eure Lehrer。记忆技巧：先背熟 ein/eine 变格表，物主代词直接套用，一通百通（mein 和 '
             'ein 长得像不是巧合）。课程把 mein/dein… '
             '称为"物主代词"（Possessivpronomen），有的教材叫"物主冠词"（Possessivartikel），两种说法都对。\n'
             '\n'
             '🇬🇧 英语对照：英语 my/your 不变形；德语物主代词要跟着名词变词尾，和 ein 变格一模一样。',
  'table': [['', '阳性', '阴性', '中性', '复数'],
            ['mein', 'mein Vater', 'meine Mutter', 'mein Kind', 'meine Eltern'],
            ['euer', 'euer Vater', 'eure Mutter', 'euer Kind', 'eure Eltern']],
  'examples': [['mein Name', '我的名字（阳性单数）'],
               ['deine Muttersprache', '你的母语（阴性单数）'],
               ['Ihr Name', '您的名字（敬称永远大写）'],
               ['euer Land', '你们的国家']]},
 {'num': 'M02-01',
  'id': 'trennbar',
  'cat': 'dongci',
  'title': '可分动词',
  'titleDe': 'Trennbare Verben',
  'explain': '可分动词 = 可分前缀 + 动词词干；陈述句中前缀分离并放到句尾（fernsehen → Er sieht … fern）。不可分前缀只有 8 '
             '个：be-、emp-、ent-、er-、ge-、miss-、ver-、zer-，永远不分离（如 besuchen、verkaufen）。两可前缀 6 '
             '个：durch-、über-、um-、unter-、voll-、wieder-，可分不可分意思不同（Ich fahre die Frau um 撞倒 vs Ich '
             'umfahre die Frau '
             '绕行）。发音判断法：可分时重音在第一个音节（ˈumfahren=撞倒），不可分时重音一般在第二个音节（umˈfahren=绕行）。框架结构：Ich will die '
             'Frau umfahren——情态动词 will '
             '第二位，动词原形蹲句尾，前缀不分离。易错点：不要见前缀就分离；先判断是"八大不可分"还是"两可六兄弟"，其他的默认全可分。记忆技巧：死记 8 个不可分 + 6 '
             '个两可，剩下的默认可分——用排除法比逐个记省力。\n'
             '\n'
             '🇬🇧 英语对照：英语也有可分短语动词（pick up → pick it up）；德语的前缀是直接粘在动词上的，分离后蹲句尾。',
  'table': [['前缀类型', '例子', '重音'],
            ['不可分', 'be-/ver-/er-…', '第二音节'],
            ['可分', 'an-/auf-/aus-…', '第一音节'],
            ['两用', 'umfahren 撞倒/绕行', '按意义']],
  'examples': [['Er sieht gerne mit Sarah zu Hause fern.', '他喜欢和 Sarah 在家看电视。（fernsehen 分离）'],
               ['Ich fahre die Frau um.', '我把那位女士撞倒了。（可分）'],
               ['Ich umfahre die Frau.', '我开车绕过那位女士。（不可分）'],
               ['Ich will die Frau umfahren.', '我想开车撞倒那位女士。（框架结构）']]},
 {'num': 'M02-02',
  'id': 'modal',
  'cat': 'dongci',
  'title': '情态动词',
  'titleDe': 'Modalverben',
  'explain': '六大情态动词：können（能）、müssen（必须）、sollen（应该）、wollen（想要）、mögen（喜欢）、dürfen（被允许）；变位单记（ich '
             'kann/muss/soll/will/mag/darf）。框架结构铁律：情态动词变位后居第二位，实义动词原形蹲句尾（Ich kann Deutsch '
             'sprechen）；nicht 不能打破框架，只能放动词原形前面。框架内强调规律：越往后的成分越被强调。大坑：müssen 的否定是"不必须"（Du musst '
             'nicht… = don\'t have to）；"必须不"要用 nicht dürfen（= mustn\'t）。möchte- 是 mögen 的第二虚拟式，比 '
             'wollen 更礼貌委婉，点餐专用（Ich möchte einen Kaffee）；wollen 欲望更强、更不客气。口语偷懒：dürfen 常被 können '
             '代替。所有情态动词都能作实义动词（Ich kann Deutsch. 我会德语；Ich mag dich. 我喜欢你）；表示"喜欢做某事"用 gern+实义动词（Ich '
             'lerne gern Deutsch），不用 mag 的肯定式。\n'
             '\n'
             '🇬🇧 英语对照：英语 can/must/may；德语情态动词也要变位，且实义动词原形蹲句尾是框架结构。',
  'table': [['', 'können', 'müssen', 'wollen'],
            ['ich/er', 'kann', 'muss', 'will'],
            ['du', 'kannst', 'musst', 'willst'],
            ['否定含义', '—', 'nicht müssen=不必', '—']],
  'examples': [['Ich kann Deutsch sprechen.', '我会说德语。'],
               ['Du musst nicht jeden Tag lesen.', '你不必每天读书。（不必须）'],
               ['Entschuldigung, du darfst hier nicht schlafen.', '抱歉，这里不许睡觉。（必须不）'],
               ['Ich möchte eine Tasse Kaffee trinken.', '我想喝杯咖啡。（委婉点餐）']]},
 {'num': 'M02-03',
  'id': 'negation',
  'cat': 'jufa',
  'title': '否定句',
  'titleDe': 'Negation',
  'explain': '分工：kein 只否定"不确指名词的存在"（ein Ausgang→kein Ausgang），其他所有情况一律用 nicht。kein '
             '的变格跟着冠词走：kein/keine/keinen/keinem…（Ich trinke keine Milch；Es gibt keinen Kaffee im '
             'Zimmer）。nicht 否定动词时"能多靠后就多靠后"：无情态动词放句末（Ich arbeite bei BASF '
             'nicht）；有情态动词放动词原形前（…nicht ins Restaurant gehen）。nicht 的位置决定否定对象：Nico geht nicht '
             'morgen…（否定"明天"）vs …mit Lisa nicht zusammen…（否定"一起"）——想否定谁就把 nicht '
             '放谁前面。易错点：专有名词是确指的，只能用 nicht（Das ist nicht Deutschland，不用 kein）；否定可分动词时 nicht '
             '放句尾前缀前（Nico geht morgen nicht aus）。主系表结构主语表语都用第一格，所以 Das ist ein Ausgang 的否定是 kein '
             'Ausgang（不是 keinen）。"Nicht Nico geht…" 中 nicht+Nico 是一个整体占第一位，动词依然在第二位。\n'
             '\n'
             '🇬🇧 英语对照：英语 no/not 分工类似；德语 kein 要变格，且 nicht 的位置决定否定范围，比英语精细。',
  'table': [['', 'kein（不确指名词）', 'nicht（其他）'],
            ['例子', 'kein Geld（没有钱）', 'nicht gut（不好）'],
            ['变格', '随 ein 变', '不变'],
            ['位置', '名词前', '常居句末/动词原形前']],
  'examples': [['Das ist kein Ausgang.', '这不是出口。（否定不确指名词）'],
               ['Ich trinke keine Milch.', '我不喝牛奶。'],
               ['Ich arbeite bei BASF nicht.', '我不在 BASF 工作。（nicht 句末）'],
               ['Nico möchte morgen nicht ins Restaurant gehen.', 'Nico 明天不想去餐厅。（nicht 在动词原形前）']]},
 {'num': 'M02-04',
  'id': 'imperativ',
  'cat': 'dongci',
  'title': '命令式',
  'titleDe': 'Imperativ',
  'explain': '命令式对象：du、ihr、Sie、wir；Sie/wir 变位同现在时且主语不能省（Lesen Sie…/Lesen wir…），ihr 可省（Lest das '
             'Buch），du 必须省。du 的命令式：去词尾，表强调可加 -e（Lies das Buch；Komm(e) her；Schließ(e) das Buch）。必须加 '
             '-e：动词原形的词干以 t、d、er、el、chn、fn、tm 结尾时（Öffne die '
             'Tür!）。不规则规律：现在时加变音（Umlaut）的，命令式变回规则（schläfst→schlaf!）；加了新字母的保留变化（sprich!、iss!）；wissen '
             '是"特例中的特例"（wisse!）只能硬背。sein/haben 全不规则：du sei/hab(e)，ihr seid/habt，Sie/wir '
             'seien/haben（Seien Sie bitte still.）。对 Sie 说话习惯加 bitte 表礼貌；命令式动词一般在句首第一位，偶尔前面可加 '
             'dann。学员笔记（老师认可）：加 Umlaut 的变化不带入命令式，引入新字母的变化要带入命令式。\n'
             '\n'
             '🇬🇧 英语对照：英语命令式就是动词原形；德语命令式分四种人称，du 还要去词尾。',
  'table': [['对象', '形式', '例子'],
            ['du', '去 -st（t/d结尾加-e）', 'Komm her! / Arbeite!'],
            ['ihr', '同现在时', 'Kommt her!'],
            ['Sie', 'Sie + 原形', 'Kommen Sie bitte her!'],
            ['不规则', '保留换字母', 'Sprich! / Iss! / Lies!']],
  'examples': [['Lesen Sie bitte das Buch.', '请读这本书。（Sie）'],
               ['Lies das Buch.', '读这本书！（du）'],
               ['Lest das Buch.', '读这本书！（ihr）'],
               ['Sei ein Mann!', '像个男人！（sein 不规则）']]},
 {'num': 'M03-01',
  'id': 'akkusativ',
  'cat': 'gejie',
  'title': '第四格',
  'titleDe': 'Akkusativ',
  'explain': '第一格（Nominativ）= 主格：主语和表语都用第一格（Die Tasche ist schön；Das bin '
             'ich）——和英语表语用宾格不同。第四格（Akkusativ）= '
             '直接宾格：直接宾语、人称代词、冠词、物主代词都要变格。省力技巧：变格只看"阳性单数"——der→den、ein→einen、kein→keinen、mein→meinen；阴性/中性/复数四格形式与一格相同。es '
             'gibt 永远支配第四格（Es gibt dort keinen '
             'Computer），高频搭配。人称代词四格：mich/dich/ihn/sie/es/uns/euch/sie/Sie；注意 er→ihn，es '
             '不变。易错点：sein/werden/bleiben 连接的是主系表，表语用一格（Das ist kein Ausgang，不是 '
             'keinen）。泛指不可数名词/复数前不用冠词（Es gibt morgen Unterricht），但格位依然是四格。\n'
             '\n'
             '🇬🇧 英语对照：英语宾格只有代词变形（I→me）；德语冠词也要变，但只看阳性单数就行。',
  'table': [['格', '阳性', '阴性', '中性', '复数'],
            ['一格', 'der', 'die', 'das', 'die'],
            ['四格', 'den', 'die', 'das', 'die'],
            ['人称代词', 'ihn', 'sie', 'es', 'sie']],
  'examples': [['Ich habe einen Kugelschreiber.', '我有一支圆珠笔。（阳单四格）'],
               ['Ich liebe den Kugelschreiber.', '我爱这支圆珠笔。'],
               ['Es gibt dort keinen Computer.', '那儿没有电脑。（es gibt 永+四格）'],
               ['Meine Freundin liebt mich.', '我女朋友爱我。（代词四格）']]},
 {'num': 'M03-02',
  'id': 'dativ',
  'cat': 'gejie',
  'title': '第三格',
  'titleDe': 'Dativ',
  'explain': '第三格（Dativ）= 间接宾格：双宾语动词中，直接宾语（物）四格、间接宾语（人）三格（Ich schreibe meinem Lehrer einen '
             'Brief）。变格规律：阳性/中性 +(e)m（dem/einem/meinem），阴性 +(e)r（der/einer/meiner），复数 '
             '+(e)n（den/meinen）。复数三格名词后加 n（den Lehrern、meinen Kindern），除非复数本身已是 -n/-s 结尾（den '
             'Autos）。人称代词三格：mir/dir/ihm/ihr/ihm/uns/euch/ihnen/Ihnen；"我"mir、"你"dir '
             '单记。介词后也可能出现三格（in dem Restaurant, aus der Schweiz），介词支配的格位单独记。易错点：sie 的三格是 ihr（她）/ '
             'ihnen（他们），别和四格的 sie 搞混。老师列了 19 '
             '个常见双宾动词（geben、schreiben、schenken、zeigen…）：四格一般是物、三格一般是人，但看语境。\n'
             '\n'
             '🇬🇧 英语对照：英语 give him a book 语序定乾坤；德语靠格标记，语序更自由。',
  'table': [['格', '阳性', '阴性', '中性', '复数'],
            ['一格', 'der', 'die', 'das', 'die'],
            ['三格', 'dem', 'der', 'dem', 'den + n'],
            ['人称代词', 'ihm', 'ihr', 'ihm', 'ihnen']],
  'examples': [['Gib mir die Tasche.', '把包给我。（mir 三格）'],
               ['Ich schreibe meinem Lehrer einen Brief.', '我给老师写信。（人三格+物四格）'],
               ['Gib meinen Kindern das Buch.', '把书给我的孩子们。（复数三格加 n）'],
               ['Ich komme aus der Schweiz.', '我来自瑞士。（介词+三格）']]},
 {'num': 'M03-03',
  'id': 'praep_dativ',
  'cat': 'gejie',
  'title': '只支配第三格的介词',
  'titleDe': 'Präpositionen mit Dativ',
  'explain': '十个只支配三格的介词：ab、aus、außer、bei、mit、nach、seit、von、zu、gegenüber。记忆口诀（学员笔记，老师认可）：aus außer '
             '买（bei）米（mit）拿（nach）菜（seit）放（von）醋（zu），再加 ab 和 gegenüber。seit vs ab：seit '
             '是"自从"，只能跟过去的时间点（seit drei Monaten）；ab 无此限制（ab 13 Uhr）。nach 表方位时强调"顺序"（Nach dem Regal '
             'gibt es einen Tisch），纯方位用 hinter；Meiner Meinung nach（依我看）是固定搭配。gegenüber '
             '最特殊：支配名词时可前可后（gegenüber meiner Wohnung / meinem Büro gegenüber），支配代词时必须放后（mir '
             'gegenüber）。易错点：判断格位先看"谁支配谁"——Es gibt meinem Büro gegenüber ein Restaurant 里 meinem '
             'Büro 是 gegenüber 的宾语（三格），ein Restaurant 才是 gibt 的宾语（四格），不能按距离下结论。von 永远支配三格（Was sind '
             'Sie von Beruf?）；zum = zu dem，缩写不算错。\n'
             '\n'
             '🇬🇧 英语对照：英语介词后一律宾格；德语介词各自"认格"，十个只认三格。',
  'table': [['介词', '含义', '例子'],
            ['aus / von', '从…里 / 来自', 'aus China / von mir'],
            ['bei / mit', '在…处 / 和…', 'bei Eltern / mit Bus'],
            ['nach / seit', '往…/自从', 'nach Hause / seit 2020'],
            ['zu', '向…', 'zum Arzt（zu+dem）'],
            ['gegenüber', '在…对面', 'mir gegenüber']],
  'examples': [['Ich komme aus China.', '我来自中国。'],
               ['Ich lerne seit drei Monaten Deutsch.', '我学了三个月德语。（seit+过去时间点）'],
               ['Ich gehe mit meinem Freund.', '我和朋友一起去。'],
               ['Mir gegenüber möchte er das nicht sagen.', '他不想当着我的面说。（代词后置）']]},
 {'num': 'M03-04',
  'id': 'praep_akk',
  'cat': 'gejie',
  'title': '只支配第四格的介词',
  'titleDe': 'Präpositionen mit Akkusativ',
  'explain': '五个只支配四格的介词：durch、ohne、gegen、um、für，首字母连起来是"dog '
             'uf"——老师给的记忆神器。含义：für（为了/给）、ohne（没有）、gegen（反对/逆）、durch（穿过，= through）、um（围绕 / '
             '在…点）。定冠词的"确指"含义：ohne Schinken（不带火腿，泛指）vs ohne den '
             'Schinken（不带"那种"火腿）——加不加冠词意思不同。易错点：für 后的"咖啡"是四格介词宾语（einen '
             'Kaffee），不要套用"直接/间接宾语"的动词概念分析介词。口语里 Ich kann ohne dich nicht leben 和 Ich kann nicht '
             'ohne dich leben 都对，nicht 位置可调。补充：bis 也是只支配四格的介词（答疑区老师确认）。\n'
             '\n'
             '🇬🇧 英语对照：英语 for/without/against；德语这五个只认四格，首字母 dog uf 一秒记住。',
  'table': [['介词', '含义', '例子'],
            ['durch', '穿过', 'durch den Park'],
            ['ohne', '没有', 'ohne dich'],
            ['gegen', '反对/撞上', 'gegen den Baum'],
            ['um', '围绕/在…点', 'um 8 Uhr'],
            ['für', '为了', 'für dich']],
  'examples': [['Für mich bitte einen Kaffee.', '请给我一杯咖啡。'],
               ['Ich kann nicht ohne dich leben.', '没有你我活不下去。'],
               ['Er geht um 5 Uhr ins Bett.', '他五点上床睡觉。'],
               ['Vielen Dank für die Einladung!', '谢谢邀请！']]},
 {'num': 'M03-06',
  'id': 'uhrzeit',
  'cat': 'jufa',
  'title': '询问和播报时间',
  'titleDe': 'Uhrzeit',
  'explain': '问时间三句型：Wie viel Uhr ist es? / Wie spät ist es? / Wie viel Uhr haben Sie?。24 '
             '小时制用于正式场合（电视、广播、交通、商务），Uhr 不能省略（Es ist dreizehn Uhr sieben）；12 小时制用于日常口语。12 '
             '小时制核心词：nach（过）、vor（差）、Viertel（一刻）、halb（半）；halb 指"下一个整点的一半"（halb vier = '
             '三点半）。南部/东部方言：viertel vier（= Viertel nach drei）、dreiviertel vier（= Viertel vor '
             'vier）；考试按标准语作答。问"某事在几点发生"用 um（Um wie viel Uhr kommt sie?），回答也带 um（Sie kommt um '
             'Viertel vor vier）——um '
             '是介词不能省。补充说明早晚：nachts（凌晨）、vormittags（上午）、mittags（中午）、nachmittags（下午）、abends（晚上）、morgens（早上）；半夜十二点直接说 '
             'um Mitternacht。强调整点：Punkt neun / genau neun；表大概：ungefähr acht、gegen neun Uhr。易错点：用了 '
             'nach/vor 就不再加 Uhr（Es ist fünf nach drei）；Es ist ein Uhr 和 Es ist eins 都对。\n'
             '\n'
             '🇬🇧 英语对照：英语 half past three；德语 halb vier 是"向四点去一半"=三点半，方向反过来。',
  'table': [['时间', '说法'],
            ['8:00', 'acht Uhr'],
            ['8:15', 'viertel nach acht'],
            ['8:30', 'halb neun'],
            ['8:45', 'viertel vor neun']],
  'examples': [['Wie viel Uhr ist es?', '几点了？'],
               ['Es ist fünf nach halb vier.', '三点三十五。（过半点五分）'],
               ['Es ist Viertel vor vier.', '差一刻四点。'],
               ['Um wie viel Uhr kommt sie? — Sie kommt um Viertel vor vier.', '她几点来？——她差一刻四点到。']]},
 {'num': 'M04-01',
  'id': 'mengen',
  'cat': 'mingci',
  'title': '量词',
  'titleDe': 'Mengenangaben',
  'explain': '德语量词是"放在名词前的名词"：ein Stück Kuchen、eine Tasse Kaffee、eine Flasche Mineralwasser。数字>1 '
             '时：阴性量词变复数（Tasse→Tassen），阳性/中性量词不变（Stück、Glas、Kasten、Paar）；量词后的可数名词也要变复数。量词当普通名词用时三个性都有复数（zwei '
             'Gläser、zwei Kästen、zwei Tassen）。口语偷懒：Kaffee/Cola/Tee 前单数量词可省略（Ich möchte einen '
             'Kaffee）；数词+mal 代替量词（einmal Kaffee=一杯咖啡，zweimal '
             'Tee=两杯茶）。变格时只有量词变，被修饰的名词不变；作主语时动词跟着量词走（Zwei Tassen Kaffee reichen aus，用复数）。易错点：严格说法是 '
             'zwei Glas Wasser（生活中很多人说 zwei Gläser Wasser，但严格算错）；Reis/Cola 等液体一般不可数。Glas vs '
             'Flasche：Flasche 是细颈瓶（材质不重要），Glas 是玻璃瓶（形状不重要）；Tasse 是茶杯，Glas 是玻璃杯。\n'
             '\n'
             '🇬🇧 英语对照：英语 a piece of / a cup of；德语量词本身也是名词，有性数格变化。',
  'table': [['量词', '例子'],
            ['ein Glas', 'ein Glas Wasser（一杯水）'],
            ['eine Tasse', 'eine Tasse Tee（一杯茶）'],
            ['ein Stück', 'ein Stück Kuchen（一块蛋糕）'],
            ['eine Flasche', 'eine Flasche Wein（一瓶酒）']],
  'examples': [['Ich möchte ein Stück Kuchen.', '我想要一块蛋糕。'],
               ['Ich möchte zwei Tassen Kaffee.', '我想要两杯咖啡。（阴性量词变复数）'],
               ['Ich möchte zwei Stück Kuchen.', '我想要两块蛋糕。（中性量词不变）'],
               ['Ich habe zwei Gläser.', '我有两个玻璃杯。']]},
 {'num': 'M04-03',
  'id': 'wechsel',
  'cat': 'gejie',
  'title': '“静三动四”原则',
  'titleDe': 'Wechselpräpositionen',
  'explain': '九个"静三动四"介词：an、auf、hinter、in、neben、über、unter、vor、zwischen；主语与介词宾语相对静止用三格，相对运动用四格。"动"一定是相对的、有方向变化的：在健身房里跑（im，三格）vs '
             '正往健身房里跑（ins，四格）。提问区分：对三格宾语用 wo（Wo läufst du?），对四格宾语用 wohin（Wohin läufst '
             'du?）。动静难判的硬记：Ich schreibe auf dem Buch（在书上写字，三格）vs Schreiben Sie bitte die Antworten '
             'auf das Buch（写到书上去，四格）。易错点：直接/间接宾语是"动词"的概念，不能套用到介词宾语上；静三动四只管方位，不管时间。时态不影响格位：Wir sind '
             'in den Urlaub gefahren 里 in 仍是四格——"静三动四跟时态没关系"。缩写：in dem=im，in '
             'das=ins；先判断动静，再选格位，最后记得缩写。\n'
             '\n'
             '🇬🇧 英语对照：英语 in/into 靠介词本身区分；德语靠格区分，in+三格=in，in+四格=into。',
  'table': [['介词', '静三（wo）', '动四（wohin）'],
            ['in', 'Ich bin in der Schule.', 'Ich gehe in die Schule.'],
            ['auf', 'Das Buch liegt auf dem Tisch.', 'Ich lege das Buch auf den Tisch.'],
            ['an', 'Das Bild hängt an der Wand.', 'Er hängt das Bild an die Wand.']],
  'examples': [['Ernst isst jetzt in der Mensa.', 'Ernst 正在食堂吃饭。（静止三格）'],
               ['Ernst geht heute in die Mensa.', 'Ernst 今天去食堂。（运动四格）'],
               ['Das Buch liegt auf dem Stuhl.', '书在椅子上。（静止）'],
               ['Ich lege das Buch auf den Stuhl.', '我把书放到椅子上。（运动）']]},
 {'num': 'M04-04',
  'id': 'adjektiv',
  'cat': 'xingrong',
  'title': '形容词词尾变化',
  'titleDe': 'Adjektivdeklination',
  'explain': '形容词作定语才变词尾，作表语不变（Der Kaffee ist gut，不加词尾）。零冠词：形容词词尾 = 定冠词词尾（Guter Kaffee / Guten Tag '
             '/ mit chinesischem Tee / Frisches Sushi）。定冠词后记"en 大法"：den/dem 后、复数 die 后、三格后一律 '
             '-en；单数一/四格 der/die/das 后一律 -e。不定冠词/物主代词后：einen/einem/-en/-em 后一律 -en；ein/eine '
             '后跟定冠词词尾走（ein neuer Drucker / eine neue WG / ein neues Auto）。万能口诀（学员总结，老师认可）：①见 '
             '-en/-em 后面形容词一律 -en；②复数冠词/物主代词后一律 -en；③三格后一律 -en；④单数一/四格 der/die/das 后一律 '
             '-e；⑤ein/eine 后跟 der/die/das 词尾；⑥零冠词时形容词词尾=定冠词词尾。易错点：kein/keine 和物主代词当 ein/eine 看；-in '
             '结尾阴性名词复数加 -nen（Lehrerinnen）；单个名词作时间状语一般是四格（den ganzen Tag）。\n'
             '\n'
             '🇬🇧 英语对照：英语形容词永远不变；德语形容词词尾是"冠词词尾的替补"，哪里缺标记补哪里。',
  'table': [['', '阳性', '阴性', '中性', '复数'],
            ['定冠词后', 'der gute', 'die gute', 'das gute', 'die guten'],
            ['不定冠词后', 'ein guter', 'eine gute', 'ein gutes', '—'],
            ['零冠词', 'guter', 'gute', 'gutes', 'gute']],
  'examples': [['Guten Tag!', '你好！（零冠词，词尾=定冠词词尾）'],
               ['Ich mag die neue Lehrerin.', '我喜欢这位新老师。（die 后 -e）'],
               ['Das ist ein neuer Drucker!', '这是台新打印机！（ein 后跟 der 词尾）'],
               ['Ich wohne in einem alten Haus.', '我住在老房子里。（-em 后 -en）']]},
 {'num': 'M04-06',
  'id': 'perfekt',
  'cat': 'dongci',
  'title': '现在完成时',
  'titleDe': 'Perfekt',
  'explain': '构成：助动词（haben/sein）+ 过去分词，遵守框架结构（助动词第二位，分词句尾）。规则动词：ge+词干+t（machen→gemacht）；词干以 '
             't/d/ffn/chn/gn/tm/dn 结尾先加 e（arbeiten→gearbeitet）；-ieren 结尾不加 '
             'ge（studieren→studiert）。不规则三类：①ge+变元音词干+en（sprechen→gesprochen）；②ge+词干+en（sehen→gesehen）；③ge+变元音词干+t（bringen→gebracht、kennen→gekannt）。用 '
             'sein '
             '的三类：①位置变化的不及物动词（gehen/kommen/fahren→gegangen/gekommen/gefahren）；②状态变化（sterben→gestorben）；③系动词 '
             'sein/bleiben/werden（gewesen/geblieben/geworden）。前缀规则：不可分前缀不加 '
             'ge（besuchen→besucht）；可分前缀=前缀+完整过去分词（ankommen→angekommen）；可分+不可分也不加 '
             'ge（vorbereiten→vorbereitet）。用法：德语现在完成时≈英语一般过去时；口语中基本取代一般过去时（sein/haben/情态动词除外）；瑞士等方言区几乎只用完成时。易错点：助动词看"含义"不看"形式"——fahren '
             '作"运送"（及物）用 haben（Er hat einen Verletzten ins Krankenhaus gefahren），作"行驶"（不及物+位移）用 '
             'sein。\n'
             '\n'
             '🇬🇧 英语对照：英语 I have done 表"已完成"；德语完成时≈英语一般过去时，是口语主力时态。',
  'table': [['', 'haben', 'sein'],
            ['结构', 'ich habe gemacht', 'ich bin gegangen'],
            ['用于', '大多数动词', '位移 + 状态变化 + sein/bleiben/werden']],
  'examples': [['Ich habe meine Hausaufgaben gemacht.', '我做完作业了。'],
               ['Ich bin nach China gegangen.', '我去过中国。（位移用 sein）'],
               ['Er ist gestern gekommen.', '他昨天来了。'],
               ['Ich bin in Berlin gewesen.', '我在柏林待过。（sein 用 sein）']]},
 {'num': 'M04-07',
  'id': 'praet_hs',
  'cat': 'dongci',
  'title': 'sein 和 haben 的过去时',
  'titleDe': 'Präteritum von sein/haben',
  'explain': '一般过去时在口语中基本被现在完成时代替，但 sein、haben、情态动词是例外——口语里也要用过去时（war/hatte）。变位：ich war/hatte，du '
             'warst/hattest，er war/hatte，wir waren/hatten，ihr wart/hattet，sie/Sie '
             'waren/hatten。三种问法意思一样：Warst du schon mal in Berlin?（过去时）= Bist du schon mal in '
             'Berlin gewesen?（完成时）；南部/瑞士/奥地利几乎只用完成时。易错点：war/hatte 本身就是过去时变位，不能再加 ge- '
             '或套完成时框架。记忆技巧：war 系列（war/warst/waren/wart）和 hatte '
             '系列（hatte/hattest/hatten/hattet）各记一套，词干 + 人称词尾。\n'
             '\n'
             '🇬🇧 英语对照：英语 was/had 天天用；德语 war/hatte 也是口语高频，地位对等。',
  'table': [['', 'haben', 'sein'],
            ['ich', 'hatte', 'war'],
            ['du', 'hattest', 'warst'],
            ['er/sie/es', 'hatte', 'war'],
            ['wir/sie', 'hatten', 'waren']],
  'examples': [['Warst du schon mal in Berlin?', '你去过柏林吗？（过去时）'],
               ['Bist du schon mal in Berlin gewesen?', '你去过柏林吗？（完成时，同义）'],
               ['Hattest du einen Hund?', '你养过狗吗？'],
               ['Ja, ich hatte einen Hund.', '对，我养过。（口语也要用 hatte）']]},
 {'num': 'M05-01',
  'id': 'adj_nom',
  'cat': 'xingrong',
  'title': '形容词的名词化',
  'titleDe': 'Nominalisierte Adjektive',
  'explain': '形容词首字母大写、去掉后接名词即名词化（angestellt→der Angestellte '
             '雇员）；词尾变化完全按形容词词尾规则（零冠词取定冠词词尾）。阳/阴性名词化通常指人（der/die Alte 老人），中性指物（das Interessante '
             '令人感兴趣的事、das Gesagte 说过的话）。特例：Deutscher（德国人）是形容词名词化（Ich bin Deutscher），其他国籍如 '
             'Chinese/Chinesin、Amerikaner 是普通名词、不按形容词变格。说语言：用"说 + Deutsch"（Ich spreche gut '
             'Deutsch）或"用 + das Deutsche"（vom Chinesischen ins '
             'Deutsche，固定搭配）。不是所有形容词都能名词化，约定俗成要背。\n'
             '\n'
             '🇬🇧 英语对照：英语 the rich / the poor 也有形容词作名词，但不变格；德语名词化后完整走一遍性数格。',
  'table': [['', '单数', '复数'],
            ['表人（阳）', 'der Deutsche', 'die Deutschen'],
            ['表人（阴）', 'die Alte', 'die Alten'],
            ['表物（中）', 'das Beste', '—']],
  'examples': [['Ein Deutscher wohnt nebenan.', '一个德国人住在隔壁。'],
               ['Hast du etwas Neues gehört?', '你听到什么新鲜事了吗？'],
               ['Das Beste kommt noch.', '最好的还在后头。'],
               ['Ich spreche gut Deutsch.', '我说德语说得很好。']]},
 {'num': 'M05-02',
  'id': 'adj_sonder',
  'cat': 'xingrong',
  'title': '形容词词尾的特殊变化',
  'titleDe': 'Besondere Adjektive',
  'explain': '-el 结尾：去 e 再加词尾（dunkel→dunklen、sensibel→sensibles、übel→üble）。-auer/-euer 结尾：去 e '
             '再加词尾（teuer→teuren、sauer→saures）。hoch→hoh 再加词尾（einen hohen '
             'Berg）。永远不加词尾的：rosa/lila/prima/extra/mega（a '
             '结尾）、beige/orange/türkis（颜色外来词）、super/klasse。\n'
             '\n'
             '🇬🇧 英语对照：类似英语的不规则（good→better），都是高频词的特殊形式，单独记。',
  'table': [['形容词', '变化', '例子'],
            ['dunkel', '→ dunkl-', 'ein dunkles Zimmer'],
            ['teuer', '→ teur-', 'eine teure Uhr'],
            ['hoch', '→ hoh-', 'ein hoher Berg'],
            ['rosa / lila', '不变', 'eine rosa Blume']],
  'examples': [['Der Berg ist sehr hoch.', '这山很高。'],
               ['Ein hohes Haus steht dort.', '那里有一栋高楼。'],
               ['Das Zimmer ist dunkel.', '房间很暗。'],
               ['Sie trägt eine rosa Blume im Haar.', '她头发上戴着一朵粉色的花。']]},
 {'num': 'M05-03',
  'id': 'viel_wenig',
  'cat': 'xingrong',
  'title': 'viel(e) 和 wenig(e) 的用法',
  'titleDe': 'viel / wenig',
  'explain': 'viel/wenig 修饰不可数名词（= much / a little），viele/wenige 修饰复数可数名词（= many / a few）；wie viel '
             '/ wie viele 对应 how much / how many。修饰不可数名词的 viel/wenig：前面有冠词时按普通形容词加词尾（das viele '
             'Geld），无冠词时不加词尾（viel Milch）。修饰可数名词的 viele/wenige：无论有无冠词一律按形容词加词尾（vielen hundert '
             'Jahren）。书面语 ein wenig = ein bisschen；viel/wenig 前不可能出现不定冠词 ein。\n'
             '\n'
             '🇬🇧 英语对照：英语 much/many 按可数不可数区分，德语按"修饰可数还是不可数"决定用哪套，再看有无冠词决定加不加词尾。',
  'table': [['', '不可数（viel/wenig）', '可数复数（viele/wenige）'],
            ['无冠词', 'viel Milch（不加）', 'viele Leute（加）'],
            ['有冠词', 'das viele Geld（加）', 'die vielen Leute（加）']],
  'examples': [['Ich habe viel Arbeit.', '我有很多工作。'],
               ['Er hat wenig Geld.', '他没什么钱。'],
               ['Viele Leute warten draußen.', '很多人在外面等。'],
               ['Wie viel kostet das?', '这个多少钱？']]},
 {'num': 'M05-04',
  'id': 'datum',
  'cat': 'mingci',
  'title': '日期、月份、年份和序数词',
  'titleDe': 'Datum & Ordinalzahlen',
  'explain': '星期、月份都是阳性（12 个月份拼写近英语，别混淆）。序数词：1–19 加 -te（erste/zweite/dritte 特例），20 以上加 '
             '-ste；wievielte- 提问"第几"，按形容词加词尾。年份读法：2000 年及以后 zweitausend+（2026 = '
             'zweitausendsechsundzwanzig），1000–1999 用 hundert（1995 = '
             'neunzehnhundertfünfundneunzig）。"在几月几号"用 an（am 23. Oktober）；省略月份时序数词名词化大写（am '
             'Dreiundzwanzigsten）；日期顺序日-月-年，用点分隔。不带介词的时间状语用第四格（den 5. Juni）。\n'
             '\n'
             '🇬🇧 英语对照：英语 October 23rd / on Monday；德语日期用序数词 + 三格（am dreiundzwanzigsten Oktober），和英语 '
             'on the 23rd of October 思路接近。',
  'table': [['表达', '德语'],
            ['在某天', 'am 4. Oktober'],
            ['在星期几', 'am Montag'],
            ['在某年', 'im Jahr 2026'],
            ['序数词', 'der erste, der zweite, der dritte'],
            ['无介词时间状语', 'den 5. Juni（四格）']],
  'examples': [['Heute ist der vierte Oktober.', '今天是十月四号。'],
               ['Wir treffen uns am Montag.', '我们周一见。'],
               ['Mein Geburtstag ist am zwölften Mai.', '我生日是五月十二号。'],
               ['Er wurde am ersten Januar geboren.', '他出生在一月一日。']]},
 {'num': 'M05-05',
  'id': 'jahrhundert',
  'cat': 'mingci',
  'title': '世纪与年代',
  'titleDe': 'Jahrhundert',
  'explain': '世纪 = das Jahrhundert，配序数词（aus dem 20. Jahrhundert，读 zwanzigsten）。基数词加 -er 名词化：der '
             'Zehner（10 元面值/10 路车/十位）、die Zwanziger（20 年代，复数）、die Zwanzigerin（20 多岁的女人）。"XX 年代"：in '
             'den Zwanzigern / in den 20er-Jahren，前面可加世纪（in den 1920ern）。注意不是所有基数词加 -er '
             '都能表货币，约定俗成。\n'
             '\n'
             '🇬🇧 英语对照：英语 the 20th century / the 90s；德语 Jahrhundert 中性、年代加 -er，基数词大写变名词。',
  'table': [['表达', '德语'],
            ['世纪', 'aus dem 21. Jahrhundert'],
            ['年代', 'in den 80er Jahren'],
            ['数字名词', 'der Zehner（十位/十元）'],
            ['二十多岁', 'die Zwanzigerin']],
  'examples': [['Das war im 20. Jahrhundert.', '那是二十世纪的事。'],
               ['Die Musik der 80er ist toll.', '八十年代的音乐很棒。'],
               ['In den 1920ern war Berlin wild.', '1920 年代的柏林很狂野。'],
               ['Sie ist in den Zwanzigern.', '她二十多岁。']]},
 {'num': 'M06-01',
  'id': 'komparativ',
  'cat': 'xingrong',
  'title': '比较级和最高级：规则变化',
  'titleDe': 'Komparativ & Superlativ',
  'explain': '德语不分单/多音节：比较级一律 +er，最高级一律 +st。作表语的比较级：+er（ist interessanter）；作定语：+er 后再按形容词词尾变（ein '
             'schöneres Haus）。作表语的最高级：am + -sten（am schönsten，与主语性别无关，固定形式）；南德口语可用 das '
             'schönste。作定语的最高级：定冠词 + 原级 + st + 词尾（das schönste Haus、den billigsten '
             'Tisch）。副词比较级/最高级构成同表语形容词（schneller、am schnellsten）。表语只跟 sein/bleiben/werden 系动词。\n'
             '\n'
             '🇬🇧 英语对照：和英语 faster / the fastest 几乎一一对应；am + -sten 是固定形式，不跟主语变。',
  'table': [['', '原级', '比较级', '最高级（表语）'],
            ['规则', 'schnell', 'schneller', 'am schnellsten'],
            ['变元音', 'groß', 'größer', 'am größten'],
            ['定语', '—', 'ein schöneres Haus', 'das schönste Haus']],
  'examples': [['Mein Auto ist schneller als deins.', '我的车比你的快。'],
               ['Sie ist größer als ihr Bruder.', '她比她哥哥高。'],
               ['Das ist der schönste Tag!', '这是最美好的一天！'],
               ['Er läuft am schnellsten.', '他跑得最快。']]},
 {'num': 'M06-02',
  'id': 'komparativ_halb',
  'cat': 'xingrong',
  'title': '比较级和最高级：半规则变化',
  'titleDe': 'Halbregelmäßige Steigerung',
  'explain': '-el/-auer/-euer 类同样去 e 再加比较级词尾（dunkel→dunkler、teuer→teurer）。-en/-er 结尾：作定语去 e（den '
             'trockneren Wein），作表语/副词保留 e（ist trockener）。最高级：-t/-haft/-s/-sk/-ß/-x/-z 结尾先加 -e 再加 '
             '-st（am interessantesten、am süßesten）；-d/-sch 结尾的单音节或部分双音节也先加 -e（am rundesten），多音节直接加 '
             '-st（am bedeutendsten）。部分单音节加 Umlaut（共 21 '
             '个）：alt→älter、jung→jünger、kurz→kürzer、kalt、klug、stark；部分可加可不加（gesund、glatt、nass）；英文借词双写辅音（fit→fitter）。定语用法：先完成特殊变化，再按性数格加词尾（das '
             'interessanteste Buch）。\n'
             '\n'
             '🇬🇧 英语对照：英语也有"半规则"（narrow→narrower 可加可不加 more）；德语的规则更细，但高频词就那 21 个变元音的。',
  'table': [['类型', '原级', '比较级/最高级'],
            ['去e', 'dunkel / teuer', 'dunkler / teurer'],
            ['最高级加e', 'interessant', 'am interessantesten'],
            ['变元音', 'alt / jung / kurz', 'älter / jünger / kürzer'],
            ['借词双写', 'fit', 'fitter']],
  'examples': [['Der dunklere Wein schmeckt besser.', '颜色更深的酒更好喝。'],
               ['Das ist das interessanteste Buch.', '这是最有意思的书。'],
               ['Er ist älter als ich.', '他比我大。'],
               ['Sie wird immer schöner.', '她越来越漂亮。']]},
 {'num': 'M06-03',
  'id': 'komparativ_unreg',
  'cat': 'xingrong',
  'title': '比较级和最高级：不规则变化',
  'titleDe': 'Unregelmäßige Steigerung',
  'explain': '不规则表死记：gut→besser→am besten；gern→lieber→am liebsten；hoch→höher→am '
             'höchsten；viel→mehr→am meisten；wenig→weniger→am wenigsten；nah→näher→am '
             'nächsten；groß→größer→am größten；bald→eher→am ehesten。nächste '
             '已独立为"下一个"，作四格时间状语时不加定冠词（nächste Woche、nächstes Jahr）。mehr/weniger 永远只能作副词，不加词尾（Ich '
             'habe weniger Geld als du.）；meisten/wenigsten 在定冠词后作形容词时要加词尾（Die meisten Leute）。定语用 '
             'das größte Haus，不用 am。\n'
             '\n'
             '🇬🇧 英语对照：和英语 good→better→best、much→more→most 一样，都是最高频词的不规则变化。',
  'table': [['原级', '比较级', '最高级'],
            ['gut', 'besser', 'am besten'],
            ['viel', 'mehr', 'am meisten'],
            ['gern', 'lieber', 'am liebsten'],
            ['hoch', 'höher', 'am höchsten']],
  'examples': [['Das Wetter wird immer besser.', '天气越来越好。'],
               ['Ich trinke lieber Tee als Kaffee.', '比起咖啡我更爱喝茶。'],
               ['Er hat die meisten Punkte.', '他得分最高。'],
               ['Nächste Woche fliege ich weg.', '下周我飞走。（四格不加冠词）']]},
 {'num': 'M06-04',
  'id': 'komparativ_use',
  'cat': 'xingrong',
  'title': '比较级和最高级：用法总结',
  'titleDe': 'Gebrauch der Steigerung',
  'explain': 'A>B：比较连词 als（≠介词，后面名词格位与被比较对象一致：Ich liebe dich mehr als sie. '
             '有歧义，格位定意思）；noch/viel/etwas/ein bisschen + 比较级表程度；um/四格名词表差异（um 50%、einen Monat '
             'jünger 小一个月）；immer + 比较级 = 越来越；aller- + 最高级强调独一无二（der allerschnellste Wagen）；序数词去 e '
             '+ 最高级（zweitbeste 第二好、drittgrößte）。A=B：so…wie…（so schnell wie möglich '
             '尽量快）、ebenso/genauso 强调完全一致。A<B：weniger + 原级 / am wenigsten（原级按需加词尾：das am wenigsten '
             'teure Auto）；"最不"常用反义词最高级代替（billigste 最便宜 = 最不贵）。\n'
             '\n'
             '🇬🇧 英语对照：als = than（但 als 是连词，格位跟比较对象一致）；so…wie = as…as；immer + 比较级 = more and more。',
  'table': [['含义', '结构', '例子'],
            ['A>B', 'als + 比较级', 'größer als du'],
            ['差异', 'um/四格 + 比较级', 'um 50% teurer'],
            ['越来越', 'immer + 比较级', 'immer besser'],
            ['A=B', 'so…wie…', 'so groß wie du'],
            ['A<B', 'weniger + 原级', 'weniger teuer']],
  'examples': [['Er ist einen Monat jünger als ich.', '他比我小一个月。'],
               ['Das Wetter wird immer besser.', '天气越来越好。'],
               ['So schnell wie möglich!', '越快越好！'],
               ['Das ist das zweitbeste Ergebnis.', '这是第二好的成绩。']]},
 {'num': 'M07-01',
  'id': 'dass_satz',
  'cat': 'jufa',
  'title': 'dass 引导的名词性从句',
  'titleDe': 'dass-Satz',
  'explain': '尾语序：变位动词永远居从句最后一位，非变位动词（过去分词、动词原形）倒数第二位；可分动词在从句中不再分开（einkauft、mitkommt）。书面语中 dass '
             '和逗号不可省略；口语中主句动词为 finden/hoffen/denken/glauben（感觉/希望/认为/相信）时 dass 可省略，其他动词后一般不省略。dass '
             '还可引导主语从句/同位语从句（Schön, dass ihr da seid!；Er ist der Meinung, dass… 后者是第二格固定搭配），这些 '
             'dass 都不能省略。主从句时态不必一致，尊重事实；从句整体占首位时主句倒装（变位动词第二位）。\n'
             '\n'
             '🇬🇧 英语对照：和英语 that 从句意思一样，但英语语序不变（I think that you are right），德语动词必须放从句末尾。',
  'table': [['', '主句', '从句'],
            ['基本', 'Ich weiß,', 'dass er heute kommt.'],
            ['带情态', 'Ich glaube,', 'dass sie Deutsch lernen will.'],
            ['可分动词', 'Ich sehe,', 'dass er einkauft.（不分开）']],
  'examples': [['Ich denke, dass du recht hast.', '我觉得你是对的。'],
               ['Er sagt, dass er keine Zeit hat.', '他说他没时间。'],
               ['Ich hoffe, dass das Wetter gut bleibt.', '我希望天气保持晴朗。'],
               ['Schön, dass ihr da seid!', '你们能来真好！']]},
 {'num': 'M07-09',
  'id': 'futur',
  'cat': 'dongci',
  'title': '将来时',
  'titleDe': 'Futur I',
  'explain': '将来时 = werden 变位 + 动词原形居句尾（框架结构）；从句中 werden 按尾语序放最后（…, die ich hier essen '
             'werde）。将来时带有承诺/希望/预言的感情色彩（政客、推销、算命常用）。日常生活中德国人一般用现在时代替将来时（Ich studiere nächstes Jahr '
             'in den USA.），除非明确表达承诺/期待。别和英语 will 画等号滥用。\n'
             '\n'
             '🇬🇧 英语对照：对应英语 will + 动词，但德语口语更爱用现在时表将来（类似英语 I am calling you tomorrow 用进行时表将来）。',
  'table': [['', '结构', '例子'],
            ['将来时', 'werden + 原形', 'Ich werde dir helfen.'],
            ['从句', '尾语序', '…, die ich essen werde.'],
            ['口语常用', '现在时 + 时间', 'Morgen helfe ich dir.']],
  'examples': [['Ich werde dich morgen anrufen.', '我明天给你打电话。'],
               ['Es wird morgen regnen.', '明天会下雨。'],
               ['Morgen besuche ich meine Oma.', '明天我去看奶奶。（口语更常用）'],
               ['Wirst du mir helfen?', '你会帮我吗？']]},
 {'num': 'M08-01',
  'id': 'praeteritum',
  'cat': 'dongci',
  'title': '一般过去时',
  'titleDe': 'Präteritum',
  'explain': '一般过去时主要用于书面语；口语用现在完成时，但 sein/haben/情态动词/es gibt 在口语中也常用过去时。规则动词：词干 + te + '
             '人称词尾（fragte、arbeitete），特殊词干规则与现在时相同。haben→hatte、sein→war；情态动词：musste/konnte/sollte/durfte/wollte/mochte。不规则动词按元音变换死记：e→a→e（geben→gab→gegeben）、i→a→u（finden→fand→gefunden）、ei→ie（schreiben→schrieb）、o→a（kommen→kam）、ie→o（fliegen→flog）。过去时词尾 '
             '-te/-test/-tet/-ten 中的 e 读 [ə]。\n'
             '\n'
             '🇬🇧 英语对照：对应英语过去时 did/went，但德语口语里完成时抢了它的活，分工比英语更彻底。',
  'table': [['', '规则', '不规则'],
            ['结构', '词干 + te', '元音变化'],
            ['ich', 'machte', 'ging / gab'],
            ['du', 'machtest', 'gingst / gabst'],
            ['er', 'machte', 'ging / gab']],
  'examples': [['Er ging nach Hause.', '他回家了。（书面/叙述）'],
               ['Sie kam zu spät.', '她迟到了。'],
               ['Ich konnte nicht schlafen.', '我睡不着。（情态动词口语也用过去时）'],
               ['Es gab ein Problem.', '出了个问题。']]},
 {'num': 'M01-09',
  'id': 'jishu',
  'cat': 'vokabel',
  'title': '基数词',
  'titleDe': 'Kardinalzahlen',
  'explain': '1–12 硬背；13–19 = 个位 + zehn（sechzehn 去 s，siebzehn 去 en）；整十 = 数字 + zig（dreißig 写 '
             'ß）；21–99 = 个位 + und + 十位（einundzwanzig）；100 = (ein)hundert，1000 = (ein)tausend。eins '
             '后接词时去掉 s（ein Apfel）。读音：vierzehn 的 vier 是短音（例外）；und 的 d 吞音；sechs/sechzehn 的 ch 读 '
             '[ks]；zehn 读 [tseːn] 不读 [tsiːn]。\n'
             '\n'
             '🇬🇧 英语对照：英语 13–19 也是"个位+teen"，21–99 '
             '也是"十位-个位"（twenty-one）；德语把个位放前面（einundzwanzig），顺序反的。',
  'table': [['数字', '德语'],
            ['0–12',
             'null, eins, zwei, drei, vier, fünf, sechs, sieben, acht, neun, zehn, elf, zwölf'],
            ['13–19', 'dreizehn, vierzehn, fünfzehn, sechzehn, siebzehn, achtzehn, neunzehn'],
            ['整十', 'zwanzig, dreißig, vierzig, fünfzig, sechzig, siebzig, achtzig, neunzig'],
            ['21', 'einundzwanzig（个位+und+十位）'],
            ['100 / 1000', '(ein)hundert / (ein)tausend']],
  'examples': [['Wie alt bist du? – Ich bin zwanzig.', '你多大了？——我二十岁。'],
               ['Das Buch kostet zwölf Euro.', '这本书十二欧。'],
               ['Ein Apfel und eine Birne, bitte.', '请来一个苹果、一个梨。'],
               ['Hundert minus zwanzig ist achtzig.', '100 减 20 等于 80。']]},
 {'num': 'M01-10',
  'id': 'guoming',
  'cat': 'vokabel',
  'title': '国名、语言和国籍',
  'titleDe': 'Länder, Sprachen & Nationalitäten',
  'explain': '国民词两类：中/英/法/俄/土/瑞典等男国民以 -e 结尾（der Chinese），复数 +n；其余男国民以 -er 结尾、单复同形（der '
             'Amerikaner）。女性一律加 -in，复数 +nen（die Chinesin/die Chinesinnen）——所有女性国民复数都是 '
             '+nen。语言词尾几乎都是 -isch（印度 Hindi 例外），形容词也都是 -isch。特殊国名：die USA、die Niederlande 是复数；die '
             'Türkei、die Schweiz 阴性；der Iran 阳性；其余中性。der/die 国名冠词不可省；中性国名通常不带冠词（有形容词修饰时可加 das：das '
             'schöne China）。读音：元音前 s 读 [z]（Syrien）；Chinesin 的 i 是短音。\n'
             '\n'
             '🇬🇧 英语对照：英语 China→Chinese 男女同形；德语男女国民词分开，且女性复数一律 -nen，规则得多。',
  'table': [['国家', '语言', '男国民', '女国民', '形容词'],
            ['中国', 'Chinesisch', 'der Chinese', 'die Chinesin', 'chinesisch'],
            ['美国', 'Englisch', 'der Amerikaner', 'die Amerikanerin', 'amerikanisch'],
            ['德国', 'Deutsch', 'der Deutsche', 'die Deutsche', 'deutsch'],
            ['法国', 'Französisch', 'der Franzose', 'die Französin', 'französisch'],
            ['日本', 'Japanisch', 'der Japaner', 'die Japanerin', 'japanisch']],
  'examples': [['Ich komme aus China.', '我来自中国。'],
               ['Er ist Amerikaner, sie ist Amerikanerin.', '他是美国人，她是美国人（女）。'],
               ['Sprichst du Deutsch?', '你会说德语吗？'],
               ['Die Schweiz ist sehr schön.', '瑞士很美。']]},
 {'num': 'M01-11',
  'id': 'xueye',
  'cat': 'vokabel',
  'title': '学业和职业',
  'titleDe': 'Studium & Beruf',
  'explain': 'lernen（学习，泛指）vs studieren（上大学）。学校：die Schule（中小学）/ der Schüler（中小学生）/ die '
             'Universität / der Student（大学生）。女性职业词以 -in 结尾、复数 +nen；男性以 -er 结尾单复同形；以 t 结尾的男性复数 '
             '+en；Koch→Köche、Arzt→Ärzte 加变元音。以 -tik 结尾的名词是阴性（die Informatik）。Kommissar '
             '指刑侦警探，Polizist 是警察统称。\n'
             '\n'
             '🇬🇧 英语对照：英语 teacher/student 不分男女；德语职业词分阴阳性，女性统一 -in，和法语 -euse 思路类似。',
  'table': [['职业', '阳性', '阴性'],
            ['老师', 'der Lehrer', 'die Lehrerin'],
            ['医生', 'der Arzt', 'die Ärztin'],
            ['大学生', 'der Student', 'die Studentin'],
            ['工程师', 'der Ingenieur', 'die Ingenieurin'],
            ['厨师', 'der Koch', 'die Köchin'],
            ['学科', 'die Architektur（建筑）', 'die Informatik（计算机）'],
            ['学科', 'die Medizin（医学）', 'Jura（法律，无冠词）']],
  'examples': [['Ich studiere Medizin in Berlin.', '我在柏林学医。'],
               ['Meine Mutter ist Lehrerin.', '我妈妈是老师。'],
               ['Er arbeitet als Ingenieur.', '他当工程师。'],
               ['Was bist du von Beruf?', '你是做什么工作的？']]},
 {'num': 'M06-05',
  'id': 'yanse',
  'cat': 'vokabel',
  'title': '颜色的表达',
  'titleDe': 'Farben',
  'explain': '形容词首字母大写即变为中性名词（das Rot 红色）。hell-/dunkel- 前缀表浅深（hellblau 浅蓝）。本土颜色词作定语要加词尾（ein '
             'schwarzes Auto）；外来颜色词作定语不加词尾（ein rosa Auto）——"ein rosanes '
             'Auto"这种写法连本族人都常犯错。提问：Welche Farbe hat…?（…是什么颜色？）\n'
             '\n'
             '🇬🇧 英语对照：英语 pink/blue 作定语永远不变；德语本土颜色词要加词尾，外来词不加——这是个"土著 vs 外来"的双轨制。',
  'table': [['颜色', '形容词', '名词'],
            ['红', 'rot', 'das Rot'],
            ['蓝', 'blau', 'das Blau'],
            ['绿', 'grün', 'das Grün'],
            ['黄', 'gelb', 'das Gelb'],
            ['黑', 'schwarz', 'das Schwarz'],
            ['白', 'weiß', 'das Weiß'],
            ['粉（外来，不变）', 'rosa', 'das Rosa'],
            ['紫（外来，不变）', 'lila', 'das Lila']],
  'examples': [['Welche Farbe hat dein Auto? – Es ist rot.', '你车什么颜色？——红色的。'],
               ['Sie trägt ein blaues Kleid.', '她穿着一条蓝裙子。'],
               ['Das Rosa steht dir gut.', '粉色很适合你。'],
               ['Ich mag dunkelblau.', '我喜欢深蓝色。']]},
 {'num': 'M06-06',
  'id': 'siji',
  'cat': 'vokabel',
  'title': '一年四季',
  'titleDe': 'Jahreszeiten',
  'explain': '春 der Frühling、夏 der Sommer、秋 der Herbst、冬 der Winter——四个全是阳性。季节前用 im（im Frühling '
             '在春天）。天气动词：regnen（下雨）、schneien（下雪），主语用 es：Es regnet. / Es schneit.。\n'
             '\n'
             '🇬🇧 英语对照：英语 in spring / in summer；德语 im = in dem（三格），季节是阳性所以用 dem。',
  'table': [['季节', '词汇'],
            ['春 der Frühling', 'der Regen（雨）、Es regnet.、der Wind（风）、die Wolke（云）'],
            ['夏 der Sommer', 'Die Sonne scheint.、die Hitze（酷热）、das Gewitter（雷暴）'],
            ['秋 der Herbst', 'der Sturm（暴风雨）、der Nebel（雾）'],
            ['冬 der Winter', 'der Schnee（雪）、Es schneit.、das Eis（冰）、die Kälte（寒冷）']],
  'examples': [['Im Frühling blühen die Blumen.', '春天花开。'],
               ['Im Sommer ist es sehr heiß.', '夏天很热。'],
               ['Im Herbst fällt das Laub.', '秋天落叶。'],
               ['Im Winter schneit es oft.', '冬天经常下雪。']]},
 {'num': 'M06-09',
  'id': 'wupin',
  'cat': 'vokabel',
  'title': '个人物品',
  'titleDe': 'Persönliche Gegenstände',
  'explain': '三类：箱包、衣物、随身物品。Rucksack 是双肩包，Mappe '
             '是夹在腋下的小包/文件夹。女套装区分：Kostüm（裙式套装）、Hosenanzug（裤式套装）、Badeanzug（连体泳衣）vs Bikini（分体）。\n'
             '\n'
             '🇬🇧 英语对照：英语 backpack/handbag；德语箱包词多且细（Koffer 箱子 vs Tasche 包），买错词会闹笑话。',
  'table': [['类别', '词汇'],
            ['箱包', 'der Koffer（箱子）、der Rucksack（双肩包）、die Handtasche（手提包）'],
            ['衣物',
             'das Hemd（衬衫）、die Hose（裤子）、das Kleid（连衣裙）、der Mantel（大衣）、der Pullover（毛衣）、die '
             'Socke（袜子）'],
            ['随身',
             'das Geld（钱）、der Pass（护照）、das Handy（手机）、der Regenschirm（雨伞）、die Sonnenbrille（墨镜）、der '
             'Führerschein（驾照）']],
  'examples': [['Wo ist mein Pass?', '我的护照在哪？'],
               ['Nimm einen Regenschirm mit!', '带把伞！'],
               ['Die Hose ist zu lang.', '这裤子太长了。'],
               ['Hast du dein Handy dabei?', '你带手机了吗？']]},
 {'num': 'M07-07',
  'id': 'jianzhu',
  'cat': 'vokabel',
  'title': '建筑、居家与方位',
  'titleDe': 'Gebäude, Wohnen & Richtung',
  'explain': '方位：in der Stadt（城里）vs auf dem Land（乡下，介词不同！）、am Stadtrand（城郊）；东西南北 der '
             'Osten/Westen/Süden/Norden；links 左转、rechts 右转、geradeaus 直走。楼层：das Erdgeschoss 是底楼（德语从 '
             '0 开始，erste Stock = 我们的二楼！）。电梯 der Aufzug/Fahrstuhl。Keller 多指昏暗的地窖式地下室，Untergeschoss '
             '可指商场地下一层。室内地面 der Boden vs 室外 die Erde。问洗手间：餐厅用 Toilette，别用 '
             'Bad/Badezimmer（必须带洗澡设施）；Klo 是口语，正式场合不用。Balkon 小阳台 vs Terrasse 大平台/露台。\n'
             '\n'
             '🇬🇧 英语对照：英语 first floor 在英美还不一样（英=我们的二楼，美=一楼）；德语 Erdgeschoss + erste Stock '
             '跟英式一致，租房看房时别走错层。',
  'table': [['类别', '词汇'],
            ['方位', 'in der Stadt（城里）、auf dem Land（乡下）、links/rechts/geradeaus'],
            ['建筑', 'das Haus（房子）、die Wohnung（公寓）、das Hochhaus（高楼）、die Villa（别墅）'],
            ['楼层', 'das Erdgeschoss（底楼）、der erste Stock、der Aufzug（电梯）、die Treppe（楼梯）'],
            ['房间', 'das Wohnzimmer（客厅）、das Schlafzimmer（卧室）、die Küche（厨房）、der Balkon（阳台）'],
            ['周边', 'der Bahnhof（火车站）、die Apotheke（药店）、das Rathaus（市政厅）']],
  'examples': [['Ich wohne auf dem Land.', '我住在乡下。'],
               ['Gehen Sie geradeaus, dann links.', '直走，然后左转。'],
               ['Wir wohnen im dritten Stock.', '我们住在三楼（德语 3 层）。'],
               ['Wo ist die Toilette, bitte?', '请问洗手间在哪？']]},
 {'num': 'M07-08',
  'id': 'zhufang',
  'cat': 'vokabel',
  'title': '住房申请',
  'titleDe': 'Wohnungsbewerbung',
  'explain': '模拟租房申请表（中介 '
             'Immobilienmaklerbüro）。个人信息：Name（姓）、Vorname（名）、Geburtsdatum（出生日期）、Geschlecht（性别）、Geburtsort（出生地）、Nationalität（国籍）、Arbeitgeber（雇主）、Monatliches '
             'Einkommen（月收入）。住房要求：Anzahl der Zimmer（房间数）、Größe in Quadratmeter（平米）、Maximale Miete '
             'inkl. NK（最高租金含杂费）、Etage（楼层）、Lage（位置）、Ausstattung（配置）。Makler 可以是个人或机构，Agentur '
             '只能指机构。金额写法 2900,– Euro（逗号是小数点，短横表示整）。\n'
             '\n'
             '🇬🇧 英语对照：英语租房也填 application form；德语 NK = Nebenkosten（杂费），看房时租金分 Kaltmiete（冷租）和 '
             'Warmmiete（暖租含杂费），问价要问 inkl. NK。',
  'table': [['字段', '德语', '中文'],
            ['姓名', 'der Name / der Vorname', '姓 / 名'],
            ['出生日期', 'das Geburtsdatum', ''],
            ['国籍', 'die Nationalität', ''],
            ['雇主', 'der Arbeitgeber', ''],
            ['月收入', 'das monatliche Einkommen', ''],
            ['房间数', 'die Anzahl der Zimmer', ''],
            ['面积', 'die Größe in Quadratmeter', '平米'],
            ['租金', 'die Miete inkl. NK', '含杂费']],
  'examples': [['Wie hoch ist die Miete inkl. NK?', '含杂费租金多少？'],
               ['Die Wohnung hat drei Zimmer.', '这公寓有三个房间。'],
               ['Was ist Ihr monatliches Einkommen?', '您的月收入是多少？'],
               ['Die Wohnung liegt im zweiten Stock.', '公寓在二楼。']]},
 {'num': 'M08-02',
  'id': 'shenti',
  'cat': 'vokabel',
  'title': '身体部位',
  'titleDe': 'Körperteile',
  'explain': '23 '
             '个词，复数要一起背。注意变音复数：Hand→Hände、Zahn→Zähne、Fuß→Füße、Kopf→Köpfe、Mund→Münder、Arm→Arme（不加变音也对，常用 '
             'Arme）、Finger 单复同形。说"哪疼"：Dativ + wehtun（Mein Kopf tut weh. 我头疼）。\n'
             '\n'
             '🇬🇧 英语对照：英语 tooth→teeth、foot→feet 也是变元音复数；德语变音复数（ä/ö/ü）是对应现象，成体系得多。',
  'table': [['部位', '单数', '复数'],
            ['头', 'der Kopf', 'die Köpfe'],
            ['眼', 'das Auge', 'die Augen'],
            ['鼻', 'die Nase', 'die Nasen'],
            ['嘴', 'der Mund', 'die Münder'],
            ['牙', 'der Zahn', 'die Zähne'],
            ['手', 'die Hand', 'die Hände'],
            ['手指', 'der Finger', 'die Finger'],
            ['胳膊', 'der Arm', 'die Arme'],
            ['腿', 'das Bein', 'die Beine'],
            ['脚', 'der Fuß', 'die Füße'],
            ['膝', 'das Knie', 'die Knie'],
            ['背', 'der Rücken', 'die Rücken'],
            ['肚', 'der Bauch', 'die Bäuche'],
            ['耳', 'das Ohr', 'die Ohren']],
  'examples': [['Mein Kopf tut weh.', '我头疼。'],
               ['Er hat blaue Augen.', '他有蓝眼睛。'],
               ['Wasch dir die Hände!', '洗手！'],
               ['Mein Fuß tut weh.', '我脚疼。']]}]

def main():
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'kurs', 'a1')
    os.makedirs(out_dir, exist_ok=True)
    data = []
    for p in GRAMMAR_POINTS:
        data.append({
            'num': p['num'], 'id': p['id'], 'cat': p['cat'],
            'title': p['title'], 'titleDe': p['titleDe'],
            'explain': p['explain'], 'table': p.get('table', []),
            'examples': [list(e) for e in p['examples']],
        })
    out = os.path.join(out_dir, 'grammar_kurs.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f'wrote {out} ({len(data)} points)')

if __name__ == '__main__':
    main()
