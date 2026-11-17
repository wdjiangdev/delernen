# delernen Release 更新记录（存档）

> 2026-11-17 删除全部 GitHub Releases 后，按 tag 之间的提交记录重建。原 Release 正文删除前未保存，以下为各版本区间的提交标题原文（按版本倒序），仅供追溯，以代码历史为准。各 Release 均为 Android App 安装包（`delernen-*.apk`）。

## android-v1.9（2026-11-11）

（该版本区间无提交）

## android-v1.8（2026-11-11）

（该版本区间无提交）

## android-v1.7（2026-11-11）

- `816cac4` 课程讲解：①②③ 各起一行（网页 + Android）

## android-v1.6（2026-11-11）

- `2d11f7f` Android：背单词页加 TopAppBar，修复内容画到状态栏下面

## android-v1.5（2026-11-11）

- `59a86be` 词库按 2026-11-07 审查（vocab.md）全量修复：星图/背单词英译错译约 100 处（warten/öffnen/geben/legen/bezahlen/verstehen/arbeiten 等）、前缀 hervor/voraus/wahr、gelten 无前缀、a1b2 补 38 个 stemZh、27 个成员 zh/三形式、60 个空英文释义、sep_a1b2 补 13 条中文；Nicos：gestaubsaugt、haute ab、möchten→(wollte)、mit angepackt、der Elternteil、Bürokaufleute、15 个反身可分动词补 sich、erste Etage=二楼等；改 de 的条目保留旧 k；sep 版本 v5、Nicos 版本号+1；生成脚本同步校订表
- `b5d49c3` Web 审查修复（review-1107/web.md）：nginx 相对重定向、部署备份回滚、SW 目录/index.html 缓存、搜索→Nicos 深链、反身动词前缀等
- `96977df` 内容审校 2026-11-07 修复（101 条）：kurs A1–C1 语法卡（改源脚本并重新生成，ID 不变）、grammar_learn、a1a2/a1b2 星图语法例句按 Duden/DWDS 核对修正；Alice 17 篇换成原文照录 + 逐句中文译注 + ⚠ 纠错 + 中文要点，页首附原文链接与版权声明；build_alice.py 改为从仓库内 alice/src/*.md 构建，build_site 不发布 alice/src
- `bb35056` Android 评审修复（review-1107）：TTS、SRS 键与网站一致、防连点、release 构建与 CI 发版
- `309e8f3` Merge branch 'fix1111-web'
- `f628b02` Merge branch 'fix1111-content'
- `430b8b2` Merge branch 'fix1111-android'
- `6ddcd6d` Android 资产同步：按修复后的网站数据重新生成 13 个 JSON
- `ae23579` CI：签名校验步骤打印诊断，不再静默失败

## android-v1.0.0（2026-11-07）

- `bde0aa9` CI 修复轮1：Room 复合主键写法、Chip 配色参数、TTS 语言常量、weight 作用域、星图画布改 DrawScope+定位 Text 方案
- `56d5614` 修复 Models.kt 注释里 /* 触发 Kotlin 注释嵌套导致未闭合
- `3231301` 新增原生 Android App：Kotlin/Compose 五页签（星图/词表/背单词SRS/课程跟读/Alice笔记），数据离线打包，CI 固定签名打包发 Release
- `d97543b` 补齐审查修复遗漏：a1b2 halten/suchen/zeigen 成员 def、sep_a1b2 八条 en 残留错译；sep 版本号升 v4
- `29fc784` 按 2026-11-06 审查报告修复全部问题：星图英译错译（a1a2/a1b2 verb_groups、word_families 冠词、grammar 例句、背单词 sep 继承错译）、Nicos 动词形式 8 条（vorbereitet/staubsaugte/ritt/zubereitet/klang/反身 sich 等）、hervorheben 前缀、词干弹窗中文释义接 stemZh、Nicos 版本号参数对齐实际条数
- `41df14b` 配色收成共用 theme.css；浅色模式 der/die/das、绿/橙、次要文字对比度提到 WCAG AA；build_site 给 css 加内容哈希
- `3a5582e` 合并重复词条：A1 der Weg、A2 fest、B1 die Erde、das Asyl（词性/复数依 DWDS）；背单词自动把被删词条的进度并入保留词条
- `a163ab1` 修复：课程 A2–C1 搜索结果锚点跳转失效；课程/语法页手机端长文本撑宽页面；背单词记住所选范围、学习中计数包含刚见过的词、导入提示措辞；搜索支持多词组合、输入变元音时精确匹配
- `8ea9ad4` deploy.sh：nginx.conf 原地写入，容器内配置不一致时自动重建容器（修复单文件挂载导致配置不生效）
- `fa43a08` nginx：webmanifest 使用正确的 MIME 类型
- `7e4fec4` 背单词：乱序/先复习后新词/按词表三种出题顺序、进度导出导入、修复主题按钮变量冲突；新增全站搜索（单词/语法/星图/Alice 笔记，变元音可不打）；PWA 离线使用；构建脚本自动给 js/json 加内容哈希版本号并生成搜索索引与离线清单；deploy.sh 重载 nginx、清理旧文件、支持 --install-auto 自动部署
- `a907fe7` 词库：按 DWDS/Duden 修正 jemandem fehlen（被想念）、dazuzählen 释义、gratis 词性为副词
- `e4526dd` 词库全量审校：修正 A1/A2/B1 约 160 处错译/错词性/错别字（如 Weg 路、Essen food、Morgen morning、Bank bench、Sympathie 好感、Fernsehen 电视、fest/bar 形容词、der Grad、Bankkaufleute），vocab.js 版本号 +1
- `f1b49e0` 词库：A1/A2/B1 名词统一为“冠词 + 单数, 复数”（A2 899 条、B1 543 条、A1 102 条），不可数标 nur Sg./复数名词标 nur Pl.；修正 Guten Abend/Post/Vorgesetzte 等错译；词卡按 der/die/das 上色；背单词进度按旧词条 k 字段保留；nginx 改 no-cache+ETag，json 同规则
- `32e0be1` a1b2：标记与 a1a2 重复的内容（动词26/词族16/语法19，按钮加 A1·A2 徽标）
- `f0d0c20` Revert "a1a2 星图：46 个动词/名词加配图（Wikimedia），详情面板+词族卡片展示"
- `8b00572` a1a2 星图：46 个动词/名词加配图（Wikimedia），详情面板+词族卡片展示
- `741b573` 星图页：词族/语法分组栏也改换行
- `8275af7` 星图页：动词分组栏改换行显示，不再横滑
- `20d3368` 新增 /alice/ 分区：Alice Learn German 17 篇学习笔记（A2×2/B1×7/C1×8），首页入口卡片，deploy.sh 同步列表
- `dfc0e2d` Nicos词表补齐26个独立动词的过去式·过去分词（sein等7个情态动词+规则-ern/-eln+可分变体），das Essen/das Leben 改回名词
- `fb89f24` 修复Nicos页vforms模板缺少+导致JS语法错误
- `cd621bb` 背单词页：修正移除wiederholen后的词数
- `aa494f8` 动词加过去式及过去分词：可分动词50个+Nicos动词301条
- `c98e3e1` 背单词页：卡片点击来回翻转
- `e594e20` 背单词页：加撤销上次打分功能
- `6ffba1a` 背单词页：答案面保留德语原文
- `69b0a64` 背单词页：修复完成页返回按钮
- `61de61b` 背单词页：数据文件加版本号参数，绕过CDN缓存
- `5bb787d` nginx: js文件也不缓存，避免词库旧版本
- `0296d02` 背单词页：修复loadSource参数类型bug（传ID却按对象取file）
- `8775151` 背单词页：数据文件改绝对路径，避免相对路径404
- `b6ea40e` 背单词页：去掉eval改用window挂载，加可见错误提示
- `a30a591` nginx: 目录式URL的index.html也加无缓存头
- `d0e5663` 修复背单词页：eval作用域导致开始按钮无响应、清空进度按钮报错
- `e07e84d` deploy.sh: 同步 memorize 目录
- `632edb8` 新增背单词页：艾宾浩斯间隔重复，5种范围自选
- `49d9e2c` 新增 Nicos Weg A2(1732词)/B1(963词) 三语词汇页
- `b55fb5c` vocab.js 加版本号防缓存
- `55b7cc8` Nicos Weg A1 词汇升级为1726词完整三语版（原包1867笔记去重+补英文）
- `a695b67` deploy.sh: 同步 nicos 目录
- `8309103` 新增 Nicos Weg A1 词汇页：825词德英中三语+记忆提示+TTS发音
- `2f1606b` 前缀释义按Duden/DWDS核实修正: dar/ge/ver/er
- `9205353` 去掉body overflow-x: 与正常页面一致, 修iOS Chrome跳回顶部
- `3561bb8` 星空canvas: 只在横竖屏切换时重置, 工具栏resize不再触发(修iOS滚动丢失)
- `ed3a85f` 修iOS跳回顶部: body overflow-x:hidden改clip(避免创建滚动容器)
- `184ca36` 搜索跳转: 等iOS键盘收起视口恢复后再定位, 修跳回顶部
- `5b664a5` 搜索跳转: 平滑滚动改瞬时, 先收键盘再定位(修iOS跳动)
- `3d0cc1e` 星图页: 加全站搜索(动词/词族/语法), 点击跳转定位
- `6b4f6ee` 修a1a2动词详情构词解析重复显示
- `adef60c` 动词tab: 去掉级别徽章; 派生词详情加前缀构词解析
- `ea032b2` 语法tab: 29个语法点加级别徽章(A1/A2/B1/B2)
- `28a26b2` 星图页: 级别徽章文字改对比色(A1/B1/B2原字色与底色相同看不见)
- `51e2b35` 星图页: 浅色模式选中态tab/分组按钮改深色字
- `bf38d4c` 星图: a1a2副标题与a1b2格式统一; 图例上下居中
- `39ad85c` 星图页: 动词/名词/形容词图例在三个tab都显示, 两页统一
- `7fdbb89` 主页: DeLernen -> Deutsch Lernen, 副标题去掉 Nicos Weg
- `f1661f5` 总审计：A1 纯词汇卡例句换课程原词、praeteritum 补写例句换原词形、tiere 换原词；kurs 目录页+README 改为讲解原创例句选自课程原句
- `d805f75` C1 6 张卡片重写：讲解更细贴原文要点，例句换课程原文短句
- `fa92a2b` B2 11 张卡片重写：讲解更细贴原文要点，例句换课程原文短句
- `753260d` B1 18 张卡片重写：讲解更细贴原文要点，例句换课程原文短句
- `8691dfa` A2 18 张卡片重写：讲解更细贴原文要点，例句换课程原文短句
- `d2e0c23` A1 M05–M08+词汇课 21 张卡片重写：讲解更细贴原文要点，例句换课程原文短句
- `64a60b1` A1 M01–M04 20 张卡片重写：讲解更细贴原文要点，例句换课程原文短句
- `72344ca` 课程语法词汇部分加注：整理自 SharpLingo（kurs 目录页+五个级别页+README）
- `b98b481` README 同步最新结构：kurs/ 五级目录（94 张卡片），移除旧的 a1-kurs 等路径说明
- `342e77a` 移除 practice 刷题模块（用户要求卸载）
- `500fde8` 补 7 张词汇卡片：B1 三个词汇补充（动词/名词/其他类，M16）+ C1 四个词汇型课程（M21–M24）；B1 15→18 张，C1 2→6 张
- `392a54c` 首页五个课程卡片合并为一个 kurs/ 目录入口
- `5822544` 课程板块迁入二级目录 kurs/（a1/a2/b1/b2/c1），新增 kurs 目录索引页；首页卡片与 deploy.sh 同步
- `27a7a7e` practice 目录式 URL 加无缓存头（nginx index.html 正则命中不了目录 URL，客户端会缓存旧页面）
- `31b99f6` 补修 practice 里未加引号的绝对路径 href（/course/、/login、/sign-up 等漏网链接导致 404）
- `68080a2` 新增 C1 课程语法与词汇板块：2 张卡片（M21–M22，站内实际仅2节语法课上线，C1更新中），中英对照+例句，独立目录
- `330e33e` 新增 B2 课程语法与词汇板块：11 张卡片（M17–M20，3 语法+8 主题词汇），按站内实际顺序，中英对照+例句，独立目录
- `64a2770` 新增 B1 课程语法与词汇板块：15 张卡片（M13–M16，14 语法+1 缩写），按站内实际顺序，中英对照+例句，独立目录
- `5dea7c0` 修复 practice 刷题 baseUrl（/practice），否则 sapper 路由匹配不上导致 loading 卡死；service worker 注册路径修正
- `3898e53` 新增刷题练习模块：LibreLingo 刷题 /practice/（德语 A1 定制课 5 skill/281 题+真人发音），首页加卡片
- `404daff` 新增 A2 课程语法板块：18 张卡片按站内实际顺序，中英对照+例句，独立目录
- `e286fac` A1 课程板块加 9 张词汇卡片：基数词/国名/职业/颜色/四季/物品/建筑/租房/身体，新增词汇 tab
- `5406d5e` 按站内实际授课内容校准 A1 课程语法：32 点、模块编号、补发音拆分与比较级用法总结
- `428c103` 新增 A1 课程语法板块：30 个语法点按课程顺序，中英对照+例句，独立目录可拆分
- `602521d` 一键部署：deploy.sh + deploy/{docker-compose.yml,nginx.conf}，README 加换服务器说明
- `e0095dc` 浅色模式修复：例句德语行改用主题文字色，激活 tab 浅色下用深字
- `d264441` B2 四条目补中文讲解（konjunktiv1/partizip_attr/n_deklination/nominalisierung 释义+记忆要点+英语对照）
- `a3b53a3` B2 补第四例句：konjunktiv1 / partizip_attr / n_deklination / nominalisierung（28 个语法点全部 4 例句）
- `a9298f9` 加 scripts/：内容生成脚本（动词/词族/语法源数据），JSON 为构建产物
- `bc76778` DeLernen 德语学习整站：首页+A1-A2/A1-B2单词星图+语法学习页，相对路径

说明：`android-v1.0.0` 之后直接为 `android-v1.5`，中间无 Release。
