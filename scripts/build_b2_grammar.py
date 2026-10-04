# B2 课程语法+词汇（按站内实际模块顺序，11 个卡片）
# 数据源：站内课程目录+课件要点（已登录核验）；讲解为原创重写（贴近原文要点），例句采用课程原文短句，不含视频内容
# 生成：python3 scripts/build_b2_grammar.py -> kurs/b2/grammar_b2.json
import json, os

GRAMMAR_POINTS = [{'num': 'M17-01',
  'id': 'zu_passiv',
  'cat': 'yufa',
  'title': '带 zu 不定式的被动含义',
  'titleDe': 'Infinitiv mit zu (passivisch)',
  'explain': '带 zu 不定式的被动含义。① "带 zu 不定式"作表语/主语成分时可带被动含义，引导它的动词语义相当于情态动词 können / müssen / '
             'sollen，具体是哪个要看上下文。② sein + zu + 不定式：相当于 können、müssen 或 sollen（Die Anträge sind im '
             'Rathaus abzuholen）。③ bleiben + zu + 不定式：相当于 müssen（Vieles bleibt zu erledigen）。④ '
             'gehen + zu + 不定式：相当于 können，常用于否定句（Das Bild geht nicht zu befestigen）。⑤ stehen + zu '
             '+ 不定式：相当于 müssen，主语一般是 es，且通常只与 befürchten（担心）和 erwarten（预计）搭配（Es steht zu '
             'befürchten, dass…）。⑥ es gibt + zu + 不定式：相当于 müssen（Es gibt noch vieles zu tun）。⑦ '
             '易错点：改写成 sein zu 结构时，若原句的不定式带有直接宾语（有动作执行者），要先删掉该宾语，否则结构错误。\n'
             '\n'
             '🇬🇧 英语对照：英语 These applications are to be collected；德语 sind abzuholen，sein+zu '
             '表被动含义，路数一样。',
  'table': [['结构', '相当于', '例子'],
            ['sein + zu', 'können/müssen/sollen', 'Die Anträge sind abzuholen.'],
            ['bleiben + zu', 'müssen', 'Es bleibt zu hoffen.'],
            ['gehen + zu', 'können', 'Das geht nicht zu ändern.'],
            ['stehen + zu', 'müssen', 'es steht zu erwarten'],
            ['es gibt + zu', 'müssen', 'Es gibt viel zu tun.']],
  'examples': [['Die Anträge sind im Rathaus abzuholen.', '这些申请须到市政厅领取。（sein+zu）'],
               ['Diese Frage ist noch zu erörtern.', '这个问题还有待讨论。'],
               ['Vieles bleibt zu erledigen.', '还有许多事有待完成。（bleiben+zu≈müssen）'],
               ['Es steht zu befürchten, dass sich die Vorfälle häufen.',
                '恐怕这些事件会越来越多。（stehen+zu，只与 befürchten/erwarten 搭配）']]},
 {'num': 'M19-08',
  'id': 'konjunktiv1',
  'cat': 'yufa',
  'title': '第一虚拟式',
  'titleDe': 'Konjunktiv I',
  'explain': '第一虚拟式（Konjunktiv I）。① 主要用来引述第三方的话，强调所说的话不是说话人自己说的、体现中立态度，因此多出现在新闻、广播、电视、报纸等媒体语体中。② '
             '构成：在原型词干上加 e 词尾（如 sei、habe、fehle、zerstöre）；记忆技巧：一虚在"原型词干"上变化，二虚在"过去式"上变化，词尾一样。③ '
             '当一虚变位与直陈式现在时相同时，必须改用二虚代替（如 sie würden fehlen），否则听者无法判断是虚拟式还是直陈式——这是最易错的点。④ '
             '一虚的第二人称几乎不用、第一人称很少用，因为转述的本质是"别人说的"，绝大多数句子的主语都是第三人称。⑤ 过去时构成：一虚和二虚都是"haben/sein 的虚拟式 + '
             '过去分词"（er sei in Frankreich gewesen）。⑥ 口语中要避免使用一虚，引用别人的话时用直陈式或二虚（Paul hat gesagt, er '
             'kommt nicht）。⑦ 易错辨析：als sei 不表示主观感受（那该用二虚 wäre），它强调的是从对方刚才说的话中可以听出来的客观事实，而非作者的主观理解。\n'
             '\n'
             '🇬🇧 英语对照：英语间接引语用时态回退；德语第一虚拟式专管"引述"，sei/habe/fehle 一眼可辨。',
  'table': [['用法', '例子'],
            ['转述（中立）', 'Er sagt, er sei krank.'],
            ['与直陈式相同时改用二虚', 'sie würden fehlen'],
            ['口语中避免', '口语用直陈式或二虚']],
  'examples': [['Die Ergebnisse seien alarmierend.', '据称结果令人担忧。'],
               ['Von den Tätern fehle jede Spur.', '据称作案者毫无踪迹。'],
               ['Der Minister sagte, er sei in Frankreich gewesen.', '部长说他曾在法国。（一虚过去时）'],
               ['Paul hat gesagt, er kommt nicht.', 'Paul 说他不来。（口语用直陈式）']]},
 {'num': 'M20-01',
  'id': 'dopp_akk',
  'cat': 'yufa',
  'title': '支配两个四格宾语的动词',
  'titleDe': 'Verben mit zwei Akkusativobjekten',
  'explain': '支配两个四格宾语的动词。① 德语中支配两个四格宾语的动词分四类：(1) kosten/lehren；(2) abfragen/abhören；(3) '
             'fragen/bitten；(4) angehen。② kosten 和 lehren 支配两个四格宾语（表示人 + 表示事）：Der Flug hat meinen '
             'Vater 5000 Euro gekostet.。③ 口语中 kosten/lehren 后表示人的四格有时被说成三格（如 Das kann ihn/ihm den '
             'Hals kosten），但这种说法在书面语中要尽量避免——口语/书面语分界的易错点。④ abfragen/abhören '
             '表示人的宾语可用三格或四格；但如果表示人的宾语是句中唯一的宾语，必须用四格（Der Lehrer hat ihn abgefragt）。⑤ fragen 和 '
             'bitten 后的表示人的间接宾语要用四格（Hast du ihn etwas gefragt? / Das möchte ich dich bitten）。⑥ '
             'bitten 很少接双宾语，更常见用法是"表示人的四格宾语 + um + 介词宾语"（Ich möchte dich darum bitten）或"表示人的四格宾语 + '
             '带 zu 不定式"。⑦ angehen 固定结构：表示人的四格 + nichts/etwas 等表示不确定数量或程度的四格名词/不定代词（Das geht dich '
             'nichts an 这不关你的事；Das geht mich einen Dreck an 这跟我有个毛的关系）。⑧ 德国北部一些地区会把 angehen '
             '结构中表示人的第四格换成第三格，但这种说法未被标准德语接受。\n'
             '\n'
             '🇬🇧 英语对照：英语 teach sb sth 无介词；德语 lehren/fragen/bitten 四类动词直接带两个四格，整批背。',
  'table': [['动词', '结构', '例子'],
            ['kosten/lehren', '四格 + 四格', 'Das kostet mich viel Zeit.'],
            ['abfragen/abhören', '人三/四格 + 物四格', 'Er fragt ihn die Vokabeln ab.'],
            ['fragen/bitten', '人四格', 'Ich frage dich etwas.'],
            ['angehen', '人四格 + nichts/etwas', 'Das geht dich nichts an.']],
  'examples': [['Der Flug hat meinen Vater 5000 Euro gekostet.', '这趟航班花了我父亲 5000 欧元。（kosten+双四格）'],
               ['Sie hat mich Deutsch gelehrt.', '她教我德语。'],
               ['Der Lehrer hat ihn die englischen Vokabeln abgefragt.', '老师抽查了他英语单词。（唯一宾语必须四格）'],
               ['Das geht dich nichts an.', '这不关你的事。（angehen 固定结构）']]},
 {'num': 'M17-08',
  'id': 'personen',
  'cat': 'vokabel',
  'title': 'Personen und Lebensläufe（人物与简历）',
  'titleDe': 'Personen und Lebensläufe',
  'explain': '主题词汇：人物与简历（Personen und Lebensläufe）。① '
             '本课六大主题：个人信息、学校与教育（上学时/毕业后）、简历与工作经历、人际关系（两节）、名人事迹，覆盖求职与自我介绍场景。② Schule 指中小学阶段，Studium '
             '指大学阶段："上学"用 zur Schule gehen；大学学业用 Studium beginnen / unterbrechen / weiterführen / '
             'abschließen。③ 考试词汇：通过用 bestehen，挂科用 durch eine Prüfung fallen；升学用 versetzt '
             'werden，留级用 sitzen bleiben。④ 简历写作固定搭配：sich bewerben 接 um/auf/für 三个介词都行；Erfahrungen '
             'sammeln（积累经验）；über Fachkenntnisse verfügen（具备专业知识）；verantwortlich für … sein（负责……）。⑤ '
             '名人事迹表达：einen Beitrag leisten（做出贡献）、eine Theorie entwickeln（提出理论）、etwas '
             'entdecken/erfinden（发现/发明）、einen Staat gründen（建立国家）。⑥ 人际关系：sich in jn. '
             'verlieben（四格反身动词）、eine Ehe schließen（结婚）。⑦ 老师强调：erarbeiten 多用于企业团队语境（高级词汇），个人小计划用 '
             'machen 就够了；anführen 强调"带领/冲在第一线"，führen/leiten 是抽象的"领导"。⑧ '
             '记忆技巧：词汇按人生时间线编排——个人信息→学校→求职→工作→婚恋→名人事迹，可按时间顺序记忆。\n'
             '\n'
             '🇬🇧 英语对照：英语 résumé/CV；德语 der Lebenslauf，求职自我介绍词汇按人生时间线背。',
  'table': [['词', '中文'],
            ['das Abitur', '高中毕业考/高考'],
            ['sitzen bleiben', '留级'],
            ['ledig', '单身（未婚）'],
            ['die Bewerbung', '申请/求职信'],
            ['anführen', '率领（冲锋在前）'],
            ['erarbeiten', '（协作）制定']],
  'examples': [['Ich habe die (deutsche) Staatsbürgerschaft.', '我拥有（德国）公民身份。'],
               ['das Abitur machen / ablegen', '取得高中毕业证书。'],
               ['sich um / auf / für eine Stelle bewerben', '申请工作岗位。'],
               ['sich in jemanden verlieben', '爱上某人。（四格反身）']]},
 {'num': 'M17-13',
  'id': 'daheim',
  'cat': 'vokabel',
  'title': 'Daheim und unterwegs（家与旅途）',
  'titleDe': 'Daheim und unterwegs',
  'explain': '主题词汇：家与旅途（Daheim und unterwegs）。① 本课四大场景：居住（租房）、德国城市、旅行、酒店，词汇围绕生活服务展开。② 德国租房特色词：die '
             'Kaution（押金）、die Kaltmiete（冷租）、die Nebenkosten（附加费用）；老师答疑：Miete 单数指每次支付的租金，Mieten '
             '指多次支付的总和。③ einbehalten 的固定主语是房东：Der Vermieter hat die Kaution '
             'einbehalten（房东扣押了押金），固定说法要背下来。④ beklagen '
             '可作及物动词，表示"为……而惋惜/痛惜"（如发帖呼吁改变现状），不等同于普通"抱怨"。⑤ 旅行谚语：die Katze im Sack '
             'kaufen（瞎买/买不了解的东西）、tief in die Tasche greifen（大把花钱/掏腰包）；sich an Stränden sonnen '
             '是日光浴（泛指多个沙滩，am Strand 则特指某一个沙滩）。⑥ Wert auf Akk legen 译作"重视/善用、利用好"（auf ein '
             'kostenloses Frühstück Wert legen）。⑦ 城市描写搭配：besuchen（去某地）、besichtigen（参观景点）、den '
             'Grundstein für etw. legen（为……奠基）。\n'
             '\n'
             '🇬🇧 英语对照：英语 rent/deposit；德语 Kaution/Kaltmiete/Nebenkosten，租房词汇是德国生活必备。',
  'table': [['词', '中文'],
            ['die Miete, -n', '房租'],
            ['der Preisaufschlag', '涨价/加价'],
            ['die Frühstückspension', '供早餐的民宿'],
            ['der Wellnessbereich', '康乐区'],
            ['Wert auf Akk. legen', '重视…']],
  'examples': [['bei Mietbeginn eine Kaution bezahlen', '租赁开始时支付押金。'],
               ['die Kaltmiete / die Nebenkosten beträgt…', '冷租/附加费用是……'],
               ['die Katze im Sack kaufen', '瞎买（买不了解的东西）。'],
               ['für den Urlaub tief in die Tasche greifen', '为度假掏腰包。']]},
 {'num': 'M18-08',
  'id': 'kulturen',
  'cat': 'vokabel',
  'title': 'Zwischen den Kulturen（文化之间）',
  'titleDe': 'Zwischen den Kulturen',
  'explain': '主题词汇：文化之间（Zwischen den Kulturen）。① 本课分五部分：欧洲与德国人、海外冒险、文化差异、认识索布人（两节）。② '
             '第一节是"统计数据"主题词汇：Wirtschaftsdaten（经济数据）、im Mittelfeld liegen / an der Spitze / unter '
             'dem Durchschnitt / einsam vorn（中游/顶端/低于平均/单独领先）；统计报道固定句 der Statistik zufolge / '
             'statistisch gesehen。③ 易错点：unterhalb 与 unter 意思一样，但 unterhalb 是非常书面的说法。④ '
             '第二节海外工作/生活词汇：Ausschau halten nach（寻找机会）、sich an + Akk gewöhnen（适应）、sich mit seiner '
             'Heimat verbunden fühlen（感受到与祖国的联系）、von einem besseren Leben träumen（憧憬更好的生活）；成对记忆 '
             'ins Ausland ziehen（迁往国外）vs an die Heimat denken（思乡）。⑤ 第三节跨文化商务礼仪：sich über die '
             'Gewohnheiten informieren（了解习惯）、Aufforderungen nicht direkt, immer höflich '
             'formulieren（委婉提要求）、核心价值观 Bescheidenheit（谦逊）与 Kompromissbereitschaft（妥协意愿）、Die '
             'Hierarchien sind ausgeprägt/flach（层级分明/扁平）。⑥ 第四、五节介绍德国少数民族索布人：Minderheit（少数群体）、sich '
             'ansiedeln（定居）、die Eigenständigkeit bewahren（保持独立）、die Entwicklung der Sprache und '
             'Kultur fördern（促进语言文化发展）。⑦ 记忆技巧：成群记忆动词组合，如 begrüßen/empfangen/willkommen '
             'heißen（接待）、pflegen/begehen/feiern（庆祝节日）；或按"反义词对"串联记忆。\n'
             '\n'
             '🇬🇧 英语对照：英语 cross-cultural；德语 Zwischen den Kulturen，统计句式+商务礼仪成组背。',
  'table': [['词', '中文'],
            ['der Statistik zufolge', '据统计'],
            ['im Mittelfeld liegen', '处于中游'],
            ['das Heimweh', '思乡'],
            ['die Minderheit', '少数民族'],
            ['unterhalb（书面）', '在…之下']],
  'examples': [['Die Deutschen liegen im Mittelfeld.', '德国人处于中游。'],
               ['der Statistik zufolge', '据统计。'],
               ['auf Höflichkeit Wert legen', '重视礼貌。'],
               ['traditionelle Feste pflegen / begehen / feiern', '维持/庆祝传统节日。']]},
 {'num': 'M18-15',
  'id': 'arbeit',
  'cat': 'vokabel',
  'title': 'Arbeit und Studium（工作与学习）',
  'titleDe': 'Arbeit und Studium',
  'explain': '主题词汇：工作与学习（Arbeit und Studium）。① 本课分八部分：打电话（16 '
             '个子场景）、日常工作、工作续、电子邮件、会议、大学、商务信函、信件称呼与问候。② '
             '电话场景按通话流程组织：接电话→找人→转接/问名→人不在→提供帮助→留言→询问事由→说明事由→索取信息→约人→提议时间→回应提议→取消预约→承诺跟进→结束（Danke '
             'für Ihren Anruf / Auf Wiederhören）。③ 易错细节：Wie war Ihr Name?（来电者已说过名字时复述确认）vs Wie ist '
             'Ihr Name?（来电者还没说名字时询问）——过去时与现在时的礼貌分工。④ 电话留言常用虚拟二式委婉句：Könnten Sie Herrn … ausrichten, '
             'dass …? / Könnten Sie Herrn … bitte sagen, er/sie soll mich zurückrufen.。⑤ '
             '约会时间表达群：Geht/Ginge es am … um … Uhr? / Passt es Ihnen am …? / Hätten Sie nächste '
             'Woche Zeit?；回应：Der Termin kommt mir sehr gelegen. / Das trifft sich gut. / Mir ist '
             'leider etwas dazwischengekommen（临时有事）。⑥ 工作生活词汇：die E-Mail-Flut（邮件泛滥）、ständig '
             'erreichbar sein（随时在线）与保护员工的对策对应（nach Arbeitsende keine E-Mails mehr weiterleiten '
             '下班后不再转发邮件）；会议效率表达 als Zeitfresser gelten（被视为时间杀手）、einen Zeitpuffer '
             'einplanen（预留缓冲时间）。⑦ 大学场景：sich für ein Studienfach '
             'entscheiden（选专业）、BAföG（国家助学金）是德国特有概念。⑧ 信件称呼三档：正式 Sehr geehrte Damen und Herren（Sie '
             '大写）、半正式 Liebe Frau (Müller) + Mit besten Grüßen、非正式 Liebe Petra + Mit herzlichen '
             'Grüßen；正式称呼的 Sie/Ihnen 必须大写。\n'
             '\n'
             '🇬🇧 英语对照：英语 make an appointment；德语 einen Termin vereinbaren/absagen，电话流程按 16 步背。',
  'table': [['词', '中文'],
            ['der Zeitfresser', '时间杀手（低效会议）'],
            ['das BAföG', '助学金'],
            ['die Frist', '截止日期'],
            ['weiterleiten', '转接（电话）'],
            ['Sehr geehrte/r …', '尊敬的…']],
  'examples': [['Ich würde gern mit Ihnen einen Termin vereinbaren.', '我想与您预约。'],
               ['Ich muss den Termin leider absagen.', '遗憾的是我必须取消预约。'],
               ['die E-Mail-Flut bewältigen', '应对大量邮件。'],
               ['sich an einer Universität einschreiben', '注册入学。']]},
 {'num': 'M19-07',
  'id': 'zeit',
  'cat': 'vokabel',
  'title': 'Zeit und Tätigkeit（时间与活动）',
  'titleDe': 'Zeit und Tätigkeit',
  'explain': '主题词汇：时间与活动（Zeit und Tätigkeit）。① 本课分四部分：时间与活动、休闲与阅读、运动时间、特别活动与爱好。② 第一节是时间管理词汇群：die '
             'Zeiteinteilung（时间划分）、die Zeit verschwenden/vergeuden（浪费时间）、etwas raubt jemandem die '
             'Zeit（某事占用时间）；时间拟人短句 Die Zeit läuft/drängt/geht vorbei（时间流逝/紧迫）。③ 第二节休闲趋势：an '
             'Bedeutung gewinnen（重要性增加）、fließende Grenzen zwischen Arbeitszeit und '
             'Freizeit（工作与休闲界限模糊）、Angst haben, etwas zu verpassen（害怕错过）——与社交媒体时代语境相连。④ 第三节运动词汇：球类用 '
             'spielen（Fußball spielen）、an einer Weltmeisterschaft teilnehmen（参加世锦赛）、einen '
             'Weltrekord aufstellen（创世界纪录）、Mitglied der Nationalmannschaft sein（国家队成员）。⑤ '
             '第四节"小众爱好"词汇：Wasserski fahren（滑水）、Honig schleudern（取蜜）、der Imker（养蜂人）、die '
             'Geheimschrift（密码）；动词搭配 sich für das Außergewöhnliche begeistern（对非凡事物充满热情）。⑥ '
             '记忆技巧：按"动词+名词"固定搭配成组记，如 Trends feststellen（确定趋势）、Regeln festlegen（制定规则）、einen '
             'Fußballverband gründen（成立足协）。\n'
             '\n'
             '🇬🇧 英语对照：英语 waste time；德语 die Zeit verschwenden/vergeuden，动词+名词固定搭配成组背。',
  'table': [['词', '中文'],
            ['der Stau', '堵车'],
            ['Zeit verschwenden', '浪费时间'],
            ['der Weltrekord', '世界纪录'],
            ['das Bienenvolk', '蜂群'],
            ['die Freizeitgestaltung', '休闲安排']],
  'examples': [['die Zeit verschwenden / vergeuden', '浪费时间。'],
               ['sich die Zeit einteilen', '安排时间。'],
               ['im Schichtdienst arbeiten', '轮班工作。'],
               ['einen Weltrekord aufstellen', '创造世界纪录。']]},
 {'num': 'M19-41',
  'id': 'spannung',
  'cat': 'vokabel',
  'title': 'Spannung und Entspannung（紧张与放松）',
  'titleDe': 'Spannung und Entspannung',
  'explain': '主题词汇：紧张与放松（Spannung und Entspannung）。① '
             '本课分四部分：世界新闻、电视犯罪剧、政治、犯罪——"紧张"主题贯穿新闻价值与犯罪话题；注意：标题中的"Entspannung"（放松）并未单独成节，本课内容实际偏向"紧张/刺激"一侧。② '
             '新闻价值八要素（本课核心清单）：Aktualität（时事性）、Überraschung（惊喜性）、Bekanntheit（熟悉性）、Personalisierung（个性化）、Spannung（紧张性）、Kuriosität（好奇性）、Nähe（亲近性）、Identifikation（认同感）——成串记忆。③ '
             '犯罪剧词汇群：den Tatort untersuchen（调查现场）、Beweise sammeln（收集证据）、den Täter '
             'überführen（给凶手定罪）、das Geständnis ablegen（坦白）；固定搭配 dem Täter auf der Spur '
             'sein（追踪凶手）。④ 犯罪统计表达：die Kriminalitätsrangliste anführen（犯罪率排名第一）、die '
             'Aufklärungsquote（破案率）、aus der Polizeilichen Kriminalstatistik (PKS) '
             'hervorgehen（出自警方犯罪统计）。⑤ 反腐词汇群：den Kampf gegen die Korruption antreten（打响反腐斗争）、Macht '
             'missbrauchen（滥用权力）、Bestechungsgelder zahlen/annehmen（行贿/受贿）、das Vertrauen in die '
             'staatliche Verwaltung verlieren（失去对政府的信任）。⑥ 政治冷漠表达：die '
             'Politikverdrossenheit（厌恶政治）、Das politische Interesse sinkt/steigt/bleibt gleich；生动比喻 '
             'auf eine Mauer des Schweigens stoßen（碰到沉默之墙）、sich um mehr Transparenz '
             'bemühen（努力提高透明度）。\n'
             '\n'
             '🇬🇧 英语对照：英语 crime drama；德语 der Tatort/die Aufklärungsquote，新闻价值八要素成串背。',
  'table': [['词', '中文'],
            ['der Tatort', '犯罪现场（刑侦剧）'],
            ['aufklären', '查明/破案'],
            ['die Politikverdrossenheit', '政治冷漠'],
            ['die Bestechung', '贿赂'],
            ['die Einschaltquote', '收视率']],
  'examples': [['dem Täter auf der Spur sein', '追踪凶手。'],
               ['ein Verbrechen verüben / begehen', '犯罪。'],
               ['Neugier erregen / wecken', '引起好奇心。'],
               ['Bestechungsgelder zahlen / annehmen', '行贿/受贿。']]},
 {'num': 'M20-62',
  'id': 'technik',
  'cat': 'vokabel',
  'title': 'Technik und Trends（技术与趋势）',
  'titleDe': 'Technik und Trends',
  'explain': '主题词汇：技术与趋势（Technik und Trends）。① 本课分四块主题：日常生活中的设备与产品（含计划性报废 '
             'Obsoleszenz）、电脑安全、新旧学习技巧、发明专利。② '
             '设备操作词汇群：benutzen/einschalten/ausschalten/bedienen（使用/打开/关闭/操作）；部件词 '
             'Knopf/Schalter/Hebel/Taste；位置描述固定句式"befindet sich an der '
             'linken/rechten/oberen/unteren Seite"。③ Obsoleszenz（计划性报废）是本课关键词：eingebaute '
             'Fehler（内置缺陷）、nach einer bestimmten Zeit den Geist aufgeben（到时停止运转）、den Verkauf '
             'ankurbeln（刺激销量）；对立面词汇 schärfere Vorschriften fordern / Maßnahmen '
             'ergreifen（要求更严格规定/采取措施）。④ 产品命名与市场：Die Nachfrage nach einem unverwechselbaren Namen '
             'wächst（对独特名称的需求增长）、注重性价比 auf das Preis-Leistungs-Verhältnis achten、sich auf dem '
             'Markt durchsetzen（市场胜出）。⑤ '
             '电脑安全词汇群：Schädling（恶意软件）、infizieren（感染）、einnisten（潜入）、verschlüsseln（加密）、Passwort '
             'knacken（破解密码）；防范表达 sich durch Anti-Viren-Programme schützen（用杀毒软件保护自己）。⑥ '
             '学习技巧部分强调记忆与大脑：Hippocampus（海马体）、mit stärkeren Emotionen verknüpft sein（与更强烈的情绪相连）。⑦ '
             '发明专利词汇：Erfindung（发明）与 Entdeckung（发现）要区分；Die Patentanmeldung wird beim Patentamt '
             'eingereicht（向专利局提交申请）、Das Patent wird seinem Erfinder zugesprochen（专利被授予发明人）。\n'
             '\n'
             '🇬🇧 英语对照：英语 planned obsolescence；德语 die Obsoleszenz，本课关键词，设备+安全+专利三块背。',
  'table': [['词', '中文'],
            ['die Obsoleszenz', '计划报废'],
            ['büffeln', '死记硬背'],
            ['die Datensicherung', '数据备份'],
            ['das Patent', '专利'],
            ['die Firewall', '防火墙']],
  'examples': [['Der Knopf befindet sich an der linken Seite.', '旋钮位于左侧。'],
               ['den Verkauf ankurbeln', '增加销量。'],
               ['sich auf dem Markt durchsetzen', '在市场上获得成功。'],
               ['Daten verschlüsseln', '加密数据。']]},
 {'num': 'M20-70',
  'id': 'gesundheit',
  'cat': 'vokabel',
  'title': 'Gesundheit und Umwelt（健康与环境）',
  'titleDe': 'Gesundheit und Umwelt',
  'explain': '主题词汇：健康与环境（Gesundheit und Umwelt）。① 本课分五部分：健康生活、健康问题、食物与环境、环境问题与人类负担、健康睡眠。② '
             '健康生活核心句型群：Krankheiten vermeiden/verhindern（避免/预防疾病）、sich ausgewogen '
             'ernähren（均衡饮食）、auf Zigaretten und Alkohol verzichten（戒烟酒）；危险因素用 Risikofaktor '
             '串联（falsche Ernährung / mangelnde Bewegung）。③ 就医表达易错点：an (einer Krankheit) leiden（患病用 '
             'an）与 unter (Schmerzen) leiden（遭受痛苦用 unter）的介词区别；Schulmedizin（主流医学）与 alternative '
             'Heilmethoden（替代疗法）对应。④ 食物与环境部分多为警示短句：Die Alarmglocken sollten läuten（警钟应响起）、der '
             'Raubbau an der Natur（过度开发自然）、Die Tierbestände müssen sich regenerieren（动物种群必须再生）、Die '
             'Nachfrage übersteigt das Angebot（需求超过供应）。⑤ 环境政策动词群：Plastiktüten '
             'verbieten（禁用塑料袋）、mehr Hausmüll recyceln（回收更多生活垃圾）、herkömmliche Busse durch '
             'Elektrobusse ersetzen（电动公交取代传统公交）、Fördermittel zur Verfügung stellen（提供资助资金）。⑥ '
             '健康睡眠文化点：午睡在德国名声不好（in Deutschland einen schlechten Ruf haben / als schwach oder faul '
             'gelten）；Schlafstörungen/Schlafmangel 与 die Konzentrationsfähigkeit '
             'beeinträchtigen（损害注意力）搭配。⑦ 记忆技巧：按"问题—对策"成对记忆，如 Gesundheitliche Beschwerden nehmen '
             'zu（问题）与 Initiativen zum Schutz der Mitarbeiter starten（对策）。\n'
             '\n'
             '🇬🇧 英语对照：英语 suffer from；德语 an (Krankheit) leiden vs unter (Schmerzen) leiden，介词分工记牢。',
  'table': [['词', '中文'],
            ['die Krankenkasse', '医保/健康保险公司'],
            ['die Zivilisationskrankheit', '文明病'],
            ['die Innenstadtmaut', '市中心通行费'],
            ['die Erhebung', '征收'],
            ['die Überfischung', '过度捕捞']],
  'examples': [['Die Meere sind überfischt.', '海洋被过度捕捞。'],
               ['Die Luftverschmutzung bleibt nach wie vor ein Gefahrenherd.', '空气污染仍然是一个危险。'],
               ['Es kommt zu einem Engpass.', '出现短缺。'],
               ['an einer Krankheit leiden / unter Schmerzen leiden', '患病/遭受痛苦。（介词分工）']]}]


def main():
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'kurs', 'b2')
    os.makedirs(out_dir, exist_ok=True)
    data = []
    for p in GRAMMAR_POINTS:
        data.append({
            'num': p['num'], 'id': p['id'], 'cat': p['cat'],
            'title': p['title'], 'titleDe': p['titleDe'],
            'explain': p['explain'], 'table': p.get('table', []),
            'examples': [list(e) for e in p['examples']],
        })
    out = os.path.join(out_dir, 'grammar_b2.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f'wrote {out} ({len(data)} points)')

if __name__ == '__main__':
    main()
