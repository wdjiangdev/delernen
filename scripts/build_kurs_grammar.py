# A1 课程语法+词汇（按站内实际模块顺序，41 个卡片）
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
  'explain': '构成：形容词首字母大写、去掉后面名词即完成名词化（如 der Angestellte 雇员、der Fremde '
             '陌生人）。名词化形容词按形容词词尾变化走弱变化；零冠词时阳性单数主格为 -er（如 ein Angestellter、zwei '
             'Angestellte）。中性名词化表抽象事物：das Deutsche（德语）、das Interessante（令人感兴趣的事）、das '
             'Schlimme（糟糕的事）。类比记忆：英语 the young/the rich 也是形容词名词化，德语同理，只是变化更复杂。中国学生常见错误：用"形容词 + '
             'Ding/Leute/Mann"绕开名词化（如"糟糕的事"），要学会直接用 das Schlimme 这类形式。helfen 只支配三格：Wir sollen den '
             'Alten helfen. 中 den Alten 是三格复数（"帮助那些老人"），不能理解为四格单数。Schlimmes 在 Es ist schon '
             'Schlimmes passiert. 中是真正主语，es 是形式主语——德语喜欢把真实主语后置。中性名词化表示语言：vom Chinesischen ins '
             'Deutsche（从中文到德语），介词后冠词缩合。\n'
             '\n'
             '🇬🇧 英语对照：英语 the rich（形容词名词化）；德语一样，但名词化后还要变格。',
  'table': [['', '单数', '复数'],
            ['表人（阳）', 'der Deutsche', 'die Deutschen'],
            ['表人（阴）', 'die Alte', 'die Alten'],
            ['表物（中）', 'das Beste', '—']],
  'examples': [['Ich bin Deutscher.', '我是德国人。'],
               ['Wir sollen den Alten helfen.', '我们应该帮助那些老人。（helfen+三格）'],
               ['Kennst du den Fremden?', '你认识那个陌生人吗？'],
               ['Es ist schon Schlimmes passiert.', '糟糕的事情已经发生了。（es 形式主语）']]},
 {'num': 'M05-02',
  'id': 'adj_sonder',
  'cat': 'xingrong',
  'title': '形容词词尾的特殊变化',
  'titleDe': 'Besondere Adjektive',
  'explain': '以 -el 结尾的形容词加词尾前先去 '
             'e（dunkel→dunklen、sensibel→sensibles、übel→üble、parallel→parallelen），前提是不影响发音。以 '
             '-auer/-euer 结尾的形容词先去 e 再加词尾（teuer→teuren、ungeheuer→ungeheures、sauer→saures）。hoch '
             '加词尾时先变为 '
             'hoh（hoch→hohen）。永远不加词尾的形容词要单独背：rosa、lila、prima、extra、mega、beige、orange、türkis、super、klasse。"穿过"的强调靠介词 '
             'durch（表"经过、穿过"）；口语常省略介词，但要强调"穿越"最好保留 durch。变元音配合去 e：übel→üble 加词尾时同时变元音（u→ü）。易错点：去 e '
             '规则只改变词干，词尾变化表照常套用；特例形容词必须单独记忆。表语形容词永远不加词尾，只有作定语时才触发上述特殊变化。\n'
             '\n'
             '🇬🇧 英语对照：英语形容词无变化；德语少数形容词连词干都要先"整形"再加词尾。',
  'table': [['形容词', '变化', '例子'],
            ['dunkel', '→ dunkl-', 'ein dunkles Zimmer'],
            ['teuer', '→ teur-', 'eine teure Uhr'],
            ['hoch', '→ hoh-', 'ein hoher Berg'],
            ['rosa / lila', '不变', 'eine rosa Blume']],
  'examples': [['Wir müssen durch den dunklen Wald durchgehen.', '我们必须穿过这片阴暗的树林。（dunkel 去 e）'],
               ['Wir diskutieren ein ganz sensibles Thema.', '我们在讨论一个非常敏感的话题。'],
               ['Er fährt einen teuren Wagen.', '他开一辆昂贵的车。（teuer 去 e）'],
               ['Ich sehe einen hohen Berg.', '我看见一座高山。（hoch→hoh）']]},
 {'num': 'M05-03',
  'id': 'viel_wenig',
  'cat': 'xingrong',
  'title': 'viel(e) 和 wenig(e) 的用法',
  'titleDe': 'viel / wenig',
  'explain': '词义对应：viel（很多，修饰不可数名词）/ wenig（很少，修饰不可数）/ viele（很多，修饰可数复数）/ '
             'wenige（少数几个，修饰可数复数）。疑问句：Wie viel + 不可数名词（Wie viel Geld hast du?）；Wie viele + '
             '复数可数名词（Wie viele Zimmer hat die Wohnung?）。变格规则：viele/wenige 修饰可数名词时始终按普通形容词变格（Viele '
             'junge Leute）；viel/wenig 修饰不可数名词时，只有前面有定冠词才变格（das viele Geld），无冠词时不变（mit viel '
             'Milch）。viel/wenig 前面不可能出现不定冠词 ein 和否定冠词 kein；不可数名词如 Geld 前永远不会有 ein。书面表达：ein wenig '
             '可替代 ein bisschen 表"一点点"。易错点：im Zentrum von München, wenige Minuten vom Hauptbahnhof '
             'entfernt 中，介词 von 的宾语是 Hauptbahnhof，wenige Minuten '
             '是主语（一格），不要误判格位。判断词尾三步法：先看名词可数还是不可数；可数→viel/wenig 当形容词正常加词尾；不可数→看前面有没有定冠词。\n'
             '\n'
             '🇬🇧 英语对照：英语 much/many 按可数分；德语 viel/wenig 也一样，只是多了变格这一步。',
  'table': [['', '不可数（viel/wenig）', '可数复数（viele/wenige）'],
            ['无冠词', 'viel Milch（不加）', 'viele Leute（加）'],
            ['有冠词', 'das viele Geld（加）', 'die vielen Leute（加）']],
  'examples': [['Ja, mit viel Milch, aber wenig Zucker.', '好的，加很多牛奶，但少加糖。（无冠词不变）'],
               ['Viele junge Leute übernachten dort.', '很多年轻人在那里过夜。（正常变格）'],
               ['Wie viel Geld hast du?', '你有多少钱？（不可数）'],
               ['Wie viele Zimmer hat die Wohnung?', '这套房子有几个房间？（可数复数）']]},
 {'num': 'M05-04',
  'id': 'datum',
  'cat': 'mingci',
  'title': '日期、月份、年份和序数词',
  'titleDe': 'Datum & Ordinalzahlen',
  'explain': '星期和月份均为阳性；日期用"日-月-年"点式书写（01.02.2009），不用斜杠。读缩写日期：日和月按序数词读、年按基数词读（der 01.02.2009 = der '
             'erste zweite zweitausendneun；am 01.02.2009 = am ersten zweiten '
             'zweitausendneun）。提问"第几个"用 wievielte-，按普通形容词加词尾（mein/dein 后强变化：Dein wievieltes；den '
             '后永远 -en：den wievielten）。"als + 名词化的序数词"表示"作为第几个人"，紧跟在变位动词后（Ich muss als Erster die '
             'Aufgabe beenden.）；名词化序数词的性与隐含名词一致。问星期几：Welchen Wochentag haben wir heute?（Wochentag '
             '四格阳性用 welchen）；口语问日期常用 Der Wievielte ist heute?（默认隐含 der Tag）；问"几号"用 Welches Datum '
             'ist heute?。Was ist denn heute für ein Tag? 中 was für 是固定搭配意为"什么样的"，für 在此作连词而非介词，所以 '
             'ein 不用变成 einen。表达观点顺序用副词：erstens、zweitens、drittens。am Montag, dem 5. Juni 与 am '
             'Montag, den 5. Juni 都可：dem 是继续作 an 的宾语（静三），den 则是脱离 an 作无介词四格时间状语。\n'
             '\n'
             '🇬🇧 英语对照：英语 the 1st of February；德语 der erste zweite，月日都用序数词。',
  'table': [['表达', '德语'],
            ['在某天', 'am 4. Oktober'],
            ['在星期几', 'am Montag'],
            ['在某年', 'im Jahr 2026'],
            ['序数词', 'der erste, der zweite, der dritte'],
            ['无介词时间状语', 'den 5. Juni（四格）']],
  'examples': [['Welchen Wochentag haben wir heute?', '今天星期几？'],
               ['Das ist mein erstes Auto.', '这是我的第一辆车。'],
               ['Dein wievieltes Auto ist das?', '这是你的第几辆车？'],
               ['Ich muss als Erster die Aufgabe beenden.', '我必须第一个完成任务。']]},
 {'num': 'M05-05',
  'id': 'jahrhundert',
  'cat': 'mingci',
  'title': '世纪与年代',
  'titleDe': 'Jahrhundert',
  'explain': 'Jahrhundert 是中性；"在某世纪"用 im + 序数词（im zwanzigsten Jahrhundert）。二十年代（不特指某世纪）的说法：den '
             'Zwanzigern、in den Zwanzigern、in den zwanziger Jahren；特指 1920 年代：in den 1920ern、in '
             'den 1920er-Jahren。Zehner 双重含义：10 路公交车（der Zehner，复数 die Zehner）和十欧元纸币/硬币；口语 haste = '
             'hast du，\'nen = einen。易错：im zwanzigsten Jahrhundert = 1900–1999（二十世纪）；中文"十九世纪"对应 im '
             'neunzehnten Jahrhundert（1800–1899）。aus dem 15. bis zum 18. '
             'Jahrhundert：表示作品/藏品"来自"某世纪区间用 aus 表来源。序数词读法："20." 读 zwanzigsten；"15. bis zum 18." 读 '
             'fünfzehnten bis zum achtzehnten。1920 年代口语还可说 Neunzehnhundertzwanziger Jahre。\n'
             '\n'
             '🇬🇧 英语对照：英语 in the 20th century；德语 im zwanzigsten Jahrhundert，世纪=Jahrhundert（百年）。',
  'table': [['表达', '德语'],
            ['世纪', 'aus dem 21. Jahrhundert'],
            ['年代', 'in den 80er Jahren'],
            ['数字名词', 'der Zehner（十位/十元）'],
            ['二十多岁', 'die Zwanzigerin']],
  'examples': [['Die Pinakothek der Moderne zeigt bedeutende Kunstwerke aus dem 20. Jahrhundert.',
                '慕尼黑现代艺术陈列馆展示了来自二十世纪的重要艺术作品。'],
               ['Sie kam im 16. Jahrhundert mit spanischen Seefahrern von Südamerika nach Europa.',
                '它在16世纪和西班牙水手们一起从南美洲来到了欧洲。'],
               ['Sie ist ein international bedeutendes Museum für Kunst aus dem 20. Jahrhundert.',
                '它是国际知名的20世纪艺术博物馆。'],
               ["Haste mal 'nen Zehner für mich?", '你有十欧元能给我吗？（口语）']]},
 {'num': 'M06-01',
  'id': 'komparativ',
  'cat': 'xingrong',
  'title': '比较级和最高级：规则变化',
  'titleDe': 'Komparativ & Superlativ',
  'explain': '规则：比较级 = 形容词原级 + er；最高级 = am + 形容词原级 + sten（作表语/状语）或 定冠词 + 形容词原级 + ste + '
             '形容词词尾（作定语）。am + 最高级作表语/状语（Das Haus ist am schönsten.）；冠词 + 最高级 + 词尾作定语（das schönste '
             'Haus；den billigsten '
             'Tisch）。最高级的词尾变化完全套用形容词原级的词尾规则，只是把词干换成最高级形式——记住这一点就不用背新表。易错点：作定语的最高级必须跟冠词并加词尾；表语最高级只能用 '
             'am + sten。英语思路不适用：德语没有"多音节词配 more/the most"结构，规则变化范围内所有形容词都用统一的 -er/-ste '
             '后缀。解题三步法：定词性（表语还是定语）→ 定级（比较还是最高）→ 定词尾。\n'
             '\n'
             '🇬🇧 英语对照：英语 more beautiful / the most beautiful；德语 schöner / am schönsten，一律加后缀。',
  'table': [['', '原级', '比较级', '最高级（表语）'],
            ['规则', 'schnell', 'schneller', 'am schnellsten'],
            ['变元音', 'groß', 'größer', 'am größten'],
            ['定语', '—', 'ein schöneres Haus', 'das schönste Haus']],
  'examples': [['Das Buch ist interessanter.', '这本书更有意思。'],
               ['Das ist ein schöneres Haus.', '这是一栋更漂亮的房子。'],
               ['Ich habe einen billigeren Tisch.', '我有一张更便宜的桌子。'],
               ['Das Haus ist am schönsten.', '这房子最漂亮。（表语 am+sten）']]},
 {'num': 'M06-02',
  'id': 'komparativ_halb',
  'cat': 'xingrong',
  'title': '比较级和最高级：半规则变化',
  'titleDe': 'Halbregelmäßige Steigerung',
  'explain': '半规则定义：部分形容词加比较级/最高级词尾前，词干需发生特殊变化（去 e、加变音、加 e 再加 st 等），规律性弱于规则变化但有迹可循。以 -el/-er '
             '结尾的形容词（如 trocken、bitter）加比较级时，作表语/副词保留词干 e（trockener、bitterer），作定语则去 e 再加词尾（den '
             'trockneren Wein）。以 -t、-haft、-s、-sk、-ß、-x、-z 结尾的形容词，加最高级时先加 -e 再加 -st（am '
             'interessantesten），避免辅音丛难读。单音节及部分双音节形容词加变音：alt→älter、jung→jünger、kurz→kürzer、kalt→kälter、warm→wärmer '
             '等；老师用"红与黑"故事帮助记忆全部变音形容词。部分形容词变音可加可不加：口语（尤南德）多用变音形式（gesünder），书面语多用无变音形式（gesunder）。易错点：作定语的比较级/最高级仍要按性数格加词尾（den '
             'trockneren Wein）——半规则只管词干，词尾规则照常。发音细节：der、schneller、Kellner 三个 -er 结尾的元音都是 [ɐ]，但 der '
             '是长音 [deːɐ]。\n'
             '\n'
             '🇬🇧 英语对照：英语 good→better 是彻底不规则；德语"半规则"=词干小整形，程度轻得多。',
  'table': [['类型', '原级', '比较级/最高级'],
            ['去e', 'dunkel / teuer', 'dunkler / teurer'],
            ['最高级加e', 'interessant', 'am interessantesten'],
            ['变元音', 'alt / jung / kurz', 'älter / jünger / kürzer'],
            ['借词双写', 'fit', 'fitter']],
  'examples': [['Dieser Wein ist trockener.', '这种葡萄酒更干。（表语保留 e）'],
               ['Ich mag den trockneren Wein.', '我喜欢更干的那种葡萄酒。（定语去 e）'],
               ['Dieses Gericht schmeckt bitterer.', '这道菜尝起来更苦。'],
               ['Das Buch ist am interessantesten.', '这本书最有意思。（先加 e 再加 st）']]},
 {'num': 'M06-03',
  'id': 'komparativ_unreg',
  'cat': 'xingrong',
  'title': '比较级和最高级：不规则变化',
  'titleDe': 'Unregelmäßige Steigerung',
  'explain': '不规则表必须死记：bald→eher→am ehesten；gern→lieber→am liebsten；groß→größer→am '
             'größten；gut→besser→am besten；hoch→höher→am höchsten；nah→näher→am '
             'nächsten；viel→mehr→am meisten；wenig→weniger/minder→am wenigsten/mindesten。nächste '
             '已独立为"下一个"：作四格时间状语时前不加定冠词（Nächstes Jahr reise ich...），要加则用 im（Im nächsten '
             'Jahr...）。mehr/weniger 永远只能作副词，不能作定语形容词、不加词尾（Ich habe weniger Geld als du. 中修饰 '
             'Geld）。meisten/wenigsten 跟在定冠词后可当形容词用，需加词尾（das berühmteste Wirtshaus）。minder '
             '只用于书面/正式场合：mehr oder minder（大体上）作方式状语；nicht minder（不亚于、同样地）修饰其后形容词/动词。"Ich bin der '
             'Meinung, dass..." 是二格固定搭配（类似英语 of the opinion that），需整体背诵。发音：am wenigsten 中 g 发 '
             '[ç]。\n'
             '\n'
             '🇬🇧 英语对照：英语 good→better→best；德语 gut→besser→am besten，路数一样，逐个背。',
  'table': [['原级', '比较级', '最高级'],
            ['gut', 'besser', 'am besten'],
            ['viel', 'mehr', 'am meisten'],
            ['gern', 'lieber', 'am liebsten'],
            ['hoch', 'höher', 'am höchsten']],
  'examples': [['Ich zahle lieber mit Kreditkarte.', '我宁愿用信用卡付。'],
               ['Ich habe weniger Geld als du.', '我没有你那么多钱。（weniger 作副词）'],
               ['München bietet noch viel mehr, zum Beispiel das berühmteste Wirtshaus der Welt.',
                '慕尼黑还有更多，比如世界上最著名的啤酒馆。'],
               ['Wir waren mehr oder minder einer Meinung.', '我们大体上意见一致。（书面 minder）']]},
 {'num': 'M06-04',
  'id': 'komparativ_use',
  'cat': 'xingrong',
  'title': '比较级和最高级：用法总结',
  'titleDe': 'Gebrauch der Steigerung',
  'explain': '三种比较关系：A>B 用 als + 比较级；A=B 用 so...wie...（可替换为 ebenso/genauso 或副词 gleich）；A<B 用 '
             'weniger + 原级或 am wenigsten + 原级（词尾照常加）。强调与程度副词：noch + 比较级（甚至更……）、viel + '
             '比较级（更得多）、etwas/ein bisschen + 比较级（稍……一点）、immer + 比较级（越来越……）、um + 四格或直接四格表差异程度（um '
             'einen Monat jünger）。最高级前加 aller- 强调独一无二（der allerschnellste Wagen）；序数词去 e '
             '加最高级前表"第几最"（die zweitschönste Frau；die drittgrößte Stadt）。als/wie '
             '是连词非介词：比较对象的格位须与被比较对象一致（Peter ist älter als ich. 用一格 ich）。weniger/wenigsten '
             '作副词修饰形容词时，后面的形容词用原级但仍加词尾（das am wenigsten teure Auto；teuer 去 e）。易错：表语最高级用 am + '
             'sten，作定语则定冠词 + 最高级词尾；不能混淆。语言习惯：meine zweite Schwester 不说 meine zweitälteste '
             'Schwester；表达"最不……"时优先用反义词的最高级。Ich habe dein zweitbestes Buch gelesen. 中 dein '
             '替代了定冠词，不可再加冠词。\n'
             '\n'
             '🇬🇧 英语对照：英语 than 后接宾格（than me 口语）；德语 als 后格位与被比较对象一致（als ich）。',
  'table': [['含义', '结构', '例子'],
            ['A>B', 'als + 比较级', 'größer als du'],
            ['差异', 'um/四格 + 比较级', 'um 50% teurer'],
            ['越来越', 'immer + 比较级', 'immer besser'],
            ['A=B', 'so…wie…', 'so groß wie du'],
            ['A<B', 'weniger + 原级', 'weniger teuer']],
  'examples': [['Peter ist älter als ich.', 'Peter 比我年长。（als 后用一格）'],
               ['Er ist um einen Monat jünger als ich.', '他比我小一个月。（um+四格表差异）'],
               ['Das ist das am wenigsten teure Auto.', '这是最不贵的那辆车。'],
               ['Ich liebe dich mehr als sie.', '我爱你胜过爱她。/我比她更爱你。（歧义句）']]},
 {'num': 'M07-01',
  'id': 'dass_satz',
  'cat': 'jufa',
  'title': 'dass 引导的名词性从句',
  'titleDe': 'dass-Satz',
  'explain': 'dass 从句是名词性从句（可作主语、宾语、表语、补语）；dass 旧时写作 daß，1996 年正字法改革后统一写作 dass。书面语中 dass '
             '及其前面的逗号都不能省略。口语中 dass 可省略（Er sagt, er kommt aus Deutschland.），但否定句中 dass '
             '一般不省略。口语中主句动词为 finden/hoffen/denken/glauben（感觉、希望、认为、相信）时 dass 可省略；其他动词后不能省略；schön '
             '后的从句 dass 也不能省略（Schön, dass ihr da seid!）。dass 从句提前作主语时主句要倒装（Dass er mein Geschenk '
             'nicht mag, hat mich ziemlich überrascht.）。从句中动词位置：变位动词居句末（dass er aus Deutschland '
             'kommt；dass sie mir ein Geschenk gekauft hat）。易错：Ich glaube, du kannst ein '
             'ausgezeichneter Schauspieler werden. 中 werden/sein/bleiben 是系动词，表语用主格（ein '
             'ausgezeichneter Schauspieler）而非四格。从句时态独立于主句，按从句所表达的时间确定（Sie hat gesagt, dass sie '
             'morgen mitkommt. 用现在时表将来）。\n'
             '\n'
             '🇬🇧 英语对照：英语 that 从句（I think (that) he is right）；德语 dass 口语可省、书面不可省，且从句动词蹲句末。',
  'table': [['', '主句', '从句'],
            ['基本', 'Ich weiß,', 'dass er heute kommt.'],
            ['带情态', 'Ich glaube,', 'dass sie Deutsch lernen will.'],
            ['可分动词', 'Ich sehe,', 'dass er einkauft.（不分开）']],
  'examples': [['Er sagt, dass er aus Deutschland kommt.', '他说他来自德国。'],
               ['Er sagt, er kommt aus Deutschland.', '他说他来自德国。（口语省 dass）'],
               ['Dass er mein Geschenk nicht mag, hat mich ziemlich überrascht.',
                '他不喜欢我的礼物，这让我很惊讶。（从句前置主句倒装）'],
               ['Ich glaube, du kannst ein ausgezeichneter Schauspieler werden.',
                '我相信你能成为一名优秀的演员。（表语用主格）']]},
 {'num': 'M07-09',
  'id': 'futur',
  'cat': 'dongci',
  'title': '将来时',
  'titleDe': 'Futur I',
  'explain': '构成：werden（变位，第二位）+ '
             '动词不定式（句末），服从框型结构。情感色彩：将来时带有强烈的"承诺、希望、预言"色彩，常被政客、推销员、算命师使用。德国人日常谈论未来多用现在时，即使事情离现在很远（Ich '
             'studiere nächstes Jahr in den USA.；Meine Mutter besucht morgen einen Freund von '
             'ihr.；Ich komme bald.）。从句中的将来时：变位动词居从句末（die letzte Pizza, die ich hier essen '
             'werde）。易错：将来时不是德语表达未来的默认方式，不要像英语一样逢未来就用 werden 对应 will。bald '
             '表"马上（短时间内）"，gleich/sofort 表"立即"；Ich komme bald. 是约定好的近未来。\n'
             '\n'
             '🇬🇧 英语对照：英语 will 表未来是默认选项；德语默认用现在时，将来时自带"承诺/预言"语气。',
  'table': [['', '结构', '例子'],
            ['将来时', 'werden + 原形', 'Ich werde dir helfen.'],
            ['从句', '尾语序', '…, die ich essen werde.'],
            ['口语常用', '现在时 + 时间', 'Morgen helfe ich dir.']],
  'examples': [['Wir werden deine Tasche sicher finden.', '我们一定会找到你的包的。（承诺）'],
               ['Ich studiere nächstes Jahr in den USA.', '我明年将在美国学习。（现在时表未来）'],
               ['Ich komme bald.', '我马上过来。'],
               ['Er wird sicher gleich kommen.', '他肯定很快就会来的。']]},
 {'num': 'M08-01',
  'id': 'praeteritum',
  'cat': 'dongci',
  'title': '一般过去时',
  'titleDe': 'Präteritum',
  'explain': '两种表过去的方法：一般过去时（Präteritum）主要用于书面语；口语中一般用现在完成时（但 sein、haben、情态动词、es gibt '
             '即使在口语中也常用一般过去时）。构成规则：规则动词：词干 + te + 人称词尾（wohnte）；不规则动词：换词干 + '
             '人称词尾（war、hatte、ging、kam）。一、三人称单数在规则动词过去时中形式相同（ich/er/sie/es wohnte）；不规则动词也相同（ich '
             'war/er war；ich hatte/er '
             'hatte）。不规则动词过去时词干记忆规律（老师口诀）：e→a→e（geben–gab、lesen–las、sehen–sah、essen–aß、vergessen–vergaß）；i→a→u（finden–fand、trinken–trank、singen–sang、beginnen–begann）；ei→ie→ie（bleiben–blieb、schreiben–schrieb、steigen–stieg、leihen–lieh）。其他词干变化组：a→ie（schlafen–schlief、laufen–lief、lassen–ließ、halten–hielt）；ie→o（schließen–schloss、fliegen–flog、ziehen–zog）；o→a（kommen–kam）；u→a（tun–tat）。例句语序：并列句中第二个分句语序正常（und '
             'ich war...；aber letztes Jahr hatte ich...）。易错：弱变化动词过去时一、三人称单数是 '
             '-te（wohnte），不要与完成时混淆。\n'
             '\n'
             '🇬🇧 英语对照：英语过去时天天用（went/had）；德语过去时主攻书面语，口语让位给完成时。',
  'table': [['', '规则', '不规则'],
            ['结构', '词干 + te', '元音变化'],
            ['ich', 'machte', 'ging / gab'],
            ['du', 'machtest', 'gingst / gabst'],
            ['er', 'machte', 'ging / gab']],
  'examples': [['Ich bin jetzt Angestellter, und ich war im Jahr 2000 Student.',
                '我现在是职员，2000 年时是学生。'],
               ['Ich habe im Moment nur eine Tasche, aber letztes Jahr hatte ich drei Taschen.',
                '现在我只有一个包，但去年我有三个包。'],
               ['Er wohnt in China seit zehn Jahren, und wohnte vor zehn Jahren in den USA.',
                '他在中国住了十年，十年前住在美国。'],
               ['geben → gab（不规则过去时）', '给：课程变位表中的原始词形（ich/er gab）。']]},
 {'num': 'M01-09',
  'id': 'jishu',
  'cat': 'vokabel',
  'title': '基数词',
  'titleDe': 'Kardinalzahlen',
  'explain': '1–12 必须死记硬背，没有规律可推。13–19 = 个位 + zehn：sechzehn 中 6 去 s，siebzehn 中 7 去 en；vierzehn 中 '
             'vier 发短音是例外。整十数 = 数字 + zig：dreißig 中 3 变 ß，sechzig 中 6 去 s，siebzig 中 7 去 en。21–99 = '
             '个位 + und + 十位（个位在前、十位在后），10–20 之间不能加 und。加减法读法：plus（加）、minus（减）、ist gleich（等于）。eins '
             '后面接其他词时去掉 s（如 ein Apfel）。21–99 中 und 的 d 吞音（不读）。100 = (ein)hundert，1000 = '
             '(ein)tausend，10000 = zehntausend。\n'
             '\n'
             '🇬🇧 英语对照：英语 twenty-one（十位在前）；德语 einundzwanzig（个位在前），顺序反过来。',
  'table': [['数字', '德语', '备注'],
            ['0–12', 'null, eins, zwei … zwölf', '死记'],
            ['16 / 17', 'sechzehn / siebzehn', '6去s，7去en'],
            ['30', 'dreißig', '3变ß'],
            ['21', 'einundzwanzig', '个位+und+十位'],
            ['100 / 1000', '(ein)hundert / (ein)tausend', '']],
  'examples': [['Sieben plus drei ist gleich zehn.', '7+3=10'],
               ['Neun minus fünf ist gleich vier.', '9−5=4'],
               ['Vierundzwanzig plus siebzehn ist gleich einundvierzig.', '24+17=41'],
               ['Dreiundsiebzig minus dreizehn ist gleich sechzig.', '73−13=60']]},
 {'num': 'M01-10',
  'id': 'guoming',
  'cat': 'vokabel',
  'title': '国名、语言和国籍',
  'titleDe': 'Länder, Sprachen & Nationalitäten',
  'explain': '国名性别要单记：der Iran（阳性）；die USA、die Niederlande（复数）；die Türkei、die '
             'Schweiz（阴性）；其余大多中性。阳性（der）和阴性/复数（die）国名前冠词绝对不能省略；中性国名一般不加冠词，但形容词修饰等特定情况可加 '
             'das。国民词规律：中英法俄土耳其瑞典六国，男性国民词尾 -e（复数 +n），女性在男性基础上去 e 加 in（复数加 nen）；其他国家男性国民词尾 '
             '-er（复数不变），女性直接加 in（复数加 nen）。所有女性国民词复数一律加 -nen。语言名称词尾都是 -isch（印度 Hindi 例外）；国名形容词词尾也都是 '
             '-isch（包括 indisch）。国家、语言、形容词三者高度关联，连带记忆效率最高。发音细节：Syrien 的 s 在元音前发 [z]；Frankreich '
             '是复合词（Frank-reich），中间辅音不分开；Chinesin 中 i 是短音。\n'
             '\n'
             '🇬🇧 英语对照：英语 German 既是德国人又是德语还是形容词；德语 der Deutsche / Deutsch / deutsch 三个形式分工明确。',
  'table': [['国家', '语言', '国民（男/女）', '形容词'],
            ['Deutschland', 'Deutsch', 'der Deutsche / die Deutsche', 'deutsch'],
            ['China', 'Chinesisch', 'der Chinese / die Chinesin', 'chinesisch'],
            ['Frankreich', 'Französisch', 'der Franzose / die Französin', 'französisch'],
            ['die USA', 'Englisch', 'der Amerikaner / die Amerikanerin', 'amerikanisch'],
            ['Russland', 'Russisch', 'der Russe / die Russin', 'russisch'],
            ['Japan', 'Japanisch', 'der Japaner / die Japanerin', 'japanisch'],
            ['die Schweiz', '—', 'der Schweizer / die Schweizerin', 'schweizerisch'],
            ['die Türkei', 'Türkisch', 'der Türke / die Türkin', 'türkisch']],
  'examples': [['Deutschland — 德国', '国名（中性，无冠词）。'],
               ['die Universität — 大学', '阴性名词。'],
               ['der Koffer — 行李箱', '阳性名词。'],
               ['in der Stadt — 在城市', '在城市里。']]},
 {'num': 'M01-11',
  'id': 'xueye',
  'cat': 'vokabel',
  'title': '学业和职业',
  'titleDe': 'Studium & Beruf',
  'explain': 'lernen vs studieren：lernen 泛指"学习"（语言、技能）；studieren 专指大学及以上阶段的学习和研究。学习阶段名词配套：die '
             'Schule/der Schüler 指中小学；die Universität/der Student 指大学——两者不可混用。学科名词性别规律：-tik/-ik '
             '后缀几乎都是阴性（Mathematik、Physik、Musik），多源自希腊语；-tät/-ität 也是阴性（如 die Universität）；例外如 der '
             'Maschinenbau（阳性）要单独记。女性职业统一以 -in 结尾、复数加 -nen；男性职业复数：-er 结尾单复同形（Lehrer、Ingenieur），-t '
             '结尾加 en（Student、Assistent），-r 结尾加 e（Kommissar），另有变元音加 e '
             '的特殊形式（Koch→Köche、Arzt→Ärzte）。询问职业的常用表达：Was sind Sie von '
             'Beruf?（您是做什么工作的？）复合词拆分记忆：Betriebswirtschaft = Betrieb（企业）+ Wirtschaft（经济）。外来词发音：英语借词 '
             'Manager 中的 a 在德语里发 [ε] 而非 [æ]。\n'
             '\n'
             '🇬🇧 英语对照：英语 study 通吃；德语 lernen（学东西）vs studieren（上大学）分工明确。',
  'table': [['词', '中文'],
            ['die Schule / der Schüler', '中小学 / 中小学生'],
            ['die Universität / der Student', '大学 / 大学生'],
            ['Informatik / Medizin / Jura', '计算机科学 / 医学 / 法律'],
            ['der Ingenieur / der Arzt', '工程师 / 医生'],
            ['der Lehrer / der Koch', '老师 / 厨师'],
            ['Was sind Sie von Beruf?', '您是做什么工作的？']],
  'examples': [['die Schule / der Schüler — 中小学 / 中小学生', '学业阶段词。'],
               ['die Universität / der Student — 大学 / 大学生', '大学阶段词。'],
               ['der Ingenieur / der Arzt — 工程师 / 医生', '职业词。'],
               ['Was sind Sie von Beruf? — 您是做什么工作的？', '问职业的固定句。']]},
 {'num': 'M06-05',
  'id': 'yanse',
  'cat': 'vokabel',
  'title': '颜色的表达',
  'titleDe': 'Farben',
  'explain': '询问颜色的固定句型：Welche Farbe hat XXX? 回答：Das Auto ist '
             'rot.。两种词尾规则：德语自有颜色词（schwarz、weiß、rot、blau、grün、gelb、braun、grau）作定语要加词尾（einen '
             'schwarzen Tisch）；外来语颜色词（rosa、pink、lila、beige、orange、türkis）永远不加词尾（mein neues rosa '
             'Auto）。易错点："ein rosanes Auto""eine orangene Tasche" '
             '虽母语者也常说，但按规则是错误的——书面语和考试中必须用不变形式。hell-（浅）/dunkel-（深）作前缀直接复合（hellblau、dunkelblau）；hell '
             '可单独作形容词用（浅的、明亮的）。颜色形容词首字母大写即变成中性名词（das Gelb）；但 Türkis 情况特殊：der Türkis '
             '是阳性名词（绿松石），形容词形式 türkis 不变词尾。加了 -farbig/-farben 后缀（"……色的"）的词必须加词尾（türkisfarben → '
             'einen türkisfarbenen Tisch）。发音：beige 作表语读 [be:ʃ]，orange 读法语鼻音；die Farbe 是阴性名词，复数 '
             'Farben。\n'
             '\n'
             '🇬🇧 英语对照：英语 pink 作定语不变；德语自有颜色词要变，外来颜色词不变——看词源。',
  'table': [['颜色', '说明'],
            ['schwarz / weiß / rot', '黑色/白色/红色（加词尾）'],
            ['gelb / blau / grün', '黄色/蓝色/绿色（加词尾）'],
            ['braun / grau', '棕色/灰色（加词尾）'],
            ['rosa / pink / lila', '粉色/紫色（永不加词尾）'],
            ['beige / orange', '米色/橘红（永不加词尾）'],
            ['hellblau / dunkelblau', '浅蓝/深蓝（复合词）']],
  'examples': [['Welche Farbe hat das Auto?', '那辆车是什么颜色的？'],
               ['Das Auto ist rot.', '那辆车是红色的。'],
               ['Ich habe einen schwarzen Tisch.', '我有一张黑色的桌子。（加词尾）'],
               ['Du kannst mein neues rosa Auto fahren.', '你可以开我的新粉色车。（不加词尾）']]},
 {'num': 'M06-06',
  'id': 'siji',
  'cat': 'vokabel',
  'title': '一年四季',
  'titleDe': 'Jahreszeiten',
  'explain': '四季名称均为阳性：der Frühling、der Sommer、der Herbst、der Winter。天气动词用无人称主语 es：Es regnet.（下雨）/ '
             'Es schneit.（下雪）——表示天气现象时主语必须是 es。复数规律：der Frühling→Frühlinge；die Wolke→Wolken（-e 变 '
             '-n）；der Sturm→Stürme（变元音 + e）；das Gewitter→Gewitter（不变）。名词辨析：der Regen（雨，阳性）、der '
             'Nebel（雾，阳性）、das Eis（冰，中性）、die Kälte（寒冷，阴性）、der '
             'Frost（霜冻，阳性）——词性各不相同，需分别记忆。表示温度：Temperatur: 35 Grad（35 度）；Temperatur: minus 10 '
             'Grad（零下 10 度）。常用短句：Der Wind weht.（刮风了）/ Die Sonne scheint.（艳阳高照）/ Man friert.（人们挨冻）/ '
             'der blaue '
             'Himmel（蓝天）。按春夏秋冬的天气现象成组背单词：春（Regen、Wolke）、夏（Sonne、Hitze、Gewitter）、秋（Sturm、Nebel）、冬（Schnee、Eis、Kälte、Frost）。\n'
             '\n'
             '🇬🇧 英语对照：英语 It rains / It snows；德语 Es regnet / Es schneit，无人称 es 一一对应。',
  'table': [['季节/天气', '词'],
            ['春天/夏天/秋天/冬天', 'der Frühling / Sommer / Herbst / Winter（阳性）'],
            ['下雨/下雪', 'Es regnet. / Es schneit.'],
            ['云/风暴/雾', 'die Wolke / der Sturm / der Nebel'],
            ['冰/寒冷/霜冻', 'das Eis / die Kälte / der Frost']],
  'examples': [['Es regnet.', '下雨了。（无人称 es）'],
               ['Es schneit.', '下雪了。'],
               ['Der Wind weht.', '刮风了。'],
               ['Die Sonne scheint.', '艳阳高照。']]},
 {'num': 'M06-09',
  'id': 'wupin',
  'cat': 'vokabel',
  'title': '个人物品',
  'titleDe': 'Persönliche Gegenstände',
  'explain': 'Rucksack vs Mappe：背在背上的书包是 der Rucksack；Mappe 一般是夹在腋下的小包，更多时候指文件夹。西装细分：der Anzug '
             '指男士西装；der Hosenanzug 指配有长裤的成套女西装；das Kostüm 指配有半身裙的成套女西装。泳衣细分：der Badeanzug '
             '指连体泳衣、女士泳衣（泛指）；der Bikini 指比基尼（两截式）；die Badehose 指泳裤。复数要点：der Rucksack→Rucksäcke、der '
             'Anzug→Anzüge、der Mantel→Mäntel（变元音 + e）；das Hemd→Hemden（-en）；das '
             'Kleid→Kleider（-er）；英语借词复数加 -s（das T-Shirt→T-Shirts）。词性记忆：箱包类多为 der/die（der '
             'Koffer、die Handtasche），随身物品多为 der（der Pass、der Laptop、der Regenschirm），但 das '
             'Handy、die Kreditkarte、das Geld 例外。同义区分：der Schlafanzug（睡衣，阳性，分体式）与 das '
             'Nachthemd（睡衣，罩衫式）同义但词性不同。旅行必备词可与 Reise 主题联记：das Geld（钱）、der Führerschein（驾照）、der '
             'Fotoapparat（照相机）。\n'
             '\n'
             '🇬🇧 英语对照：英语 suit 通吃男女西装；德语 Anzug/Hosenanzug/Kostüm 按性别款式细分。',
  'table': [['词', '中文'],
            ['der Koffer / der Rucksack', '行李箱 / 背包'],
            ['die Handtasche', '手提包'],
            ['der Anzug / das Hemd', '男士西装 / 衬衫'],
            ['der Mantel / das Kleid', '大衣 / 连衣裙'],
            ['der Pass / die Kreditkarte', '护照 / 信用卡'],
            ['das Handy / der Laptop', '手机 / 笔记本电脑'],
            ['der Regenschirm / die Sonnenbrille', '雨伞 / 墨镜']],
  'examples': [['der Koffer / der Rucksack — 行李箱 / 背包', '旅行物品。'],
               ['der Anzug / das Hemd — 男士西装 / 衬衫', '服装。'],
               ['der Pass / die Kreditkarte — 护照 / 信用卡', '证件。'],
               ['der Regenschirm / die Sonnenbrille — 雨伞 / 墨镜', '随身物品。']]},
 {'num': 'M07-07',
  'id': 'jianzhu',
  'cat': 'vokabel',
  'title': '建筑、居家与方位',
  'titleDe': 'Gebäude, Wohnen & Richtung',
  'explain': '介词搭配：城市用 in（in der Stadt），农村用 auf（auf dem Land），郊区用 an（am '
             'Stadtrand）——记忆时把常用介词一起记。Keller 指地窖式昏暗地下室；Untergeschoss 指超市/商场地下一层（不昏暗，和其他楼层差不多）。Erde '
             'vs Boden：室外地面用 Erde，室内地面用 Boden；抽象的土地/耕地/土壤用 Boden，具体的泥土（如手捧的）用 '
             'Erde。卫生间细分：Bad/Badezimmer（带洗澡设施的浴室，餐厅里别说）；Toilette（通用卫生间，餐厅可用）；WC（water '
             'closet）；Klo（口语"厕所"，正式场合别用）。Balkon（小阳台）vs '
             'Terrasse（大平台/露台，一般在一楼地面或楼顶）。楼层词汇：Erdgeschoss（一楼地面层）、Obergeschoss（非地面层）、Dachgeschoss（顶层）、Untergeschoss/Keller（地下室）；Etage/Stock/Stockwerk/Geschoss '
             '都表"层"。复数：das Dach→Dächer；der Keller→Keller（不变）；der Stuhl→Stühle；der '
             'Fahrstuhl→Fahrstühle。\n'
             '\n'
             '🇬🇧 英语对照：英语 ground floor（英）/ first floor（美）各地不同；德语 Erdgeschoss（一楼）全国统一。',
  'table': [['表达', '中文'],
            ['in der Stadt / auf dem Land', '在城市 / 在农村'],
            ['am Stadtrand', '在郊区'],
            ['nach links / nach rechts', '左转 / 右转'],
            ['geradeaus gehen', '直走'],
            ['das Gebäude / das Hochhaus', '建筑物 / 高楼'],
            ['die Villa / das Reihenhaus', '别墅 / 联排别墅'],
            ['das Erdgeschoss', '一楼（地面层）'],
            ['der Aufzug / der Lift', '电梯'],
            ['das Wohnzimmer / das Schlafzimmer', '客厅 / 卧室']],
  'examples': [['in der Stadt / auf dem Land — 在城市 / 在农村', '方位表达。'],
               ['geradeaus gehen — 直走', '指路动词短语。'],
               ['das Erdgeschoss — 一楼（地面层）', '建筑词。'],
               ['das Wohnzimmer / das Schlafzimmer — 客厅 / 卧室', '房间词。']]},
 {'num': 'M07-08',
  'id': 'zhufang',
  'cat': 'vokabel',
  'title': '住房申请',
  'titleDe': 'Wohnungsbewerbung',
  'explain': 'Fragen zur Person 中 zu 表"针对、向"，表示方向：Fragen zur Person = 针对租客的问题；类似 Fragen zur '
             'Arbeit、ein Buch zum Thema。性别栏第三选项 divers（多样），适用于非男非女的申请人。"问题"的介词：一般只能用 zu（eine Frage '
             'zu + 三格），只有讨论深奥哲学问题时可用 nach（eine Frage nach dem Sinn des Lebens）。收入写法：2900,– Euro — '
             '德语小数点用逗号，,– 表示"整"（无小数）；不是英文式写法。Anzahl der Zimmer 可写成复合词 Zimmeranzahl（数量词 + '
             '名词复合），两者等价。Makler vs Agentur：Makler 可指个人也可指机构，Agentur 只能指机构不能指人——不可完全互换。表格实务：Etage '
             '填"nicht Erdgeschoss"表不租一楼；Lage 填"Stadtmitte/Osten"；Ausstattung 列所需设施（Bad, '
             'Balkon）；Miete 后"inkl. NK"表含附加费用。复合词拆分：Immobilienmaklerbüro = Immobilien（不动产）+ '
             'Makler（中介）+ Büro（办公室），德语复合名词拆分理解更高效。\n'
             '\n'
             '🇬🇧 英语对照：英语 2,900 euros（逗号分位）；德语 2900,– Euro（逗号小数点），写法反过来。',
  'table': [['词', '中文'],
            ['der Immobilienmakler', '房屋中介'],
            ['der Vorname / der Name', '名 / 姓'],
            ['das Geburtsdatum', '出生日期'],
            ['das Geschlecht', '性别（männlich/weiblich/divers）'],
            ['die Nationalität', '国籍'],
            ['der Arbeitgeber', '雇主'],
            ['das monatliche Einkommen', '月收入'],
            ['die Miete / die Nebenkosten', '房租 / 附加费用'],
            ['die Ausstattung', '设施配置']],
  'examples': [['der Immobilienmakler — 房屋中介', '租房申请相关。'],
               ['das Geburtsdatum — 出生日期', '申请表用词。'],
               ['die Miete / die Nebenkosten — 房租 / 附加费用', '租房费用。'],
               ['die Ausstattung — 设施配置', '房源描述词。']]},
 {'num': 'M08-02',
  'id': 'shenti',
  'cat': 'vokabel',
  'title': '身体部位',
  'titleDe': 'Körperteile',
  'explain': '身体部位词性各不相同，记忆时必须连冠词一起背。复数规律：die Hand→Hände、der Zahn→Zähne、der Fuß→Füße、der '
             'Kopf→Köpfe、der Hals→Hälse、der Mund→Münder（变元音 + e）；das Ohr→Ohren（+en）；das '
             'Auge→Augen（-en）；der Rücken、der Ellenbogen、der Finger（仅 +e 或不变）。复合词拆分：das '
             'Handgelenk（手腕）、das Fußgelenk（脚踝）——Gelenk（关节）通用。das Haar 单数指"一根头发"，常用复数 die Haare '
             '表"头发"。从头到脚顺序记忆：Kopf→Auge→Nase→Mund→Hals→Brust→Bauch→Rücken→Arm→Hand→Bein→Knie→Fuß。音近区分：das '
             'Haar（头发）与 der Hals（脖子）音近，注意区分；der Bauch（肚子）复数变元音 Bäuche。der Po（屁股）是口语常用词，正式场合可用 der '
             'Hintern 替代。\n'
             '\n'
             '🇬🇧 英语对照：英语 hand→hands 规则复数；德语身体部位复数多变元音（Hand→Hände），逐个记。',
  'table': [['词', '中文'],
            ['der Kopf / das Auge', '头 / 眼睛'],
            ['die Nase / der Mund', '鼻子 / 嘴巴'],
            ['der Hals / der Rücken', '脖子 / 后背'],
            ['der Arm / die Hand', '胳膊 / 手'],
            ['der Finger / das Handgelenk', '手指 / 手腕'],
            ['die Brust / der Bauch', '胸部 / 肚子'],
            ['das Bein / das Knie', '腿 / 膝盖'],
            ['der Fuß / die Zehe', '脚 / 脚趾']],
  'examples': [['der Kopf / das Auge — 头 / 眼睛', '身体部位。'],
               ['der Arm / die Hand — 胳膊 / 手', '身体部位。'],
               ['das Bein / das Knie — 腿 / 膝盖', '身体部位。'],
               ['der Fuß / die Zehe — 脚 / 脚趾', '身体部位。']]}]


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
