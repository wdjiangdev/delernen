package com.wdjiangdev.delernen.data

/** 与 assets/data 下各 JSON 一一对应的数据模型。字段以 scripts/build_android_data.py 输出为准。 */

// ---- nicos/{a1,a2,b1}/vocab.js -> nicos_<level>.json ----
data class NicosWord(
    val de: String,
    val en: String,
    val zh: String,
    val pos: String,
    val tip: String,
    val topic: String,
    val past: String = "",
    val pp: String = "",
    val k: String = ""
)

// ---- {a1a2,a1b2}/verb_groups.json ----
data class VerbMember(
    val verb: String,
    val prefix: String?,
    val count: Int,
    val def: String,
    val past: String,
    val pp: String,
    val zh: String,
    val level: String = ""
)

data class VerbGroup(
    val stem: String,
    val stemDef: String,
    val stemZh: String,
    val level: String = "",
    val members: List<VerbMember>,
    val inA1A2: Boolean = false
)

// ---- {a1a2,a1b2}/word_families.json ----
data class FamilyMember(
    val word: String,
    val pos: String,
    val zh: String,
    val past: String,
    val pp: String,
    val plural: String
)

data class WordFamily(
    val root: String,
    val members: List<FamilyMember>
)

// ---- {a1a2,a1b2}/grammar.json ----
data class GrammarMember(
    val word: String,
    val zh: String,
    val ex: String
)

data class GrammarGroup(
    val id: String,
    val title: String,
    val titleZh: String,
    val members: List<GrammarMember>,
    val learn: String = "",
    val learnTitle: String = "",
    val level: String = "",
    val inA1A2: Boolean = false
)

// ---- memorize/sep_*.js ----
data class SepWord(
    val de: String,
    val en: String,
    val zh: String,
    val pos: String,
    val tip: String,
    val topic: String,
    val prefix: String,
    val stem: String,
    val past: String,
    val pp: String,
    val k: String = ""
)

// ---- kurs/*/grammar*.json 合并 -> kurs.json ----
data class KursCard(
    val num: String,
    val id: String,
    val cat: String,
    val title: String,
    val titleDe: String,
    val explain: String,
    val examples: List<Pair<String, String>>,
    val table: List<List<String>>,
    val level: String
)

// ---- alice/*.html -> alice.json ----
data class AliceBlock(
    val type: String,   // h | p | li | vocab
    val text: String,
    val zh: String = ""
)

data class AliceNote(
    val title: String,
    val level: String,
    val blocks: List<AliceBlock>
)

// ---- 背单词 SRS 用的统一卡片（五选数据源归一化） ----
data class SrsCard(
    val source: String,
    val de: String,
    val en: String,
    val zh: String,
    val pos: String,
    val tip: String,
    val past: String,
    val pp: String,
    /** 进度主键：与网站 memorize 一致，取 w.k || w.de（k 为空时用 de）。 */
    val key: String = de
)

data class SrsSourceDef(
    val id: String,
    val name: String,
    val count: Int
)

// ---- Nicos Weg 加速课 -> weg.json（scripts/build_weg_data.py 生成） ----
data class WegFolge(
    val n: Int,
    val t: String,
    val d: String,
    /** DW 官方 YouTube 视频 ID，课页内 WebView 内嵌播放。 */
    val yt: String
)

data class WegWord(
    val de: String,
    val zh: String,
    val en: String
)

data class WegGrammar(
    val title: String,
    /** 语法卡正文纯文本（生成时已把 HTML 表格转成「单元格 | 单元格」行）。 */
    val text: String
)

data class WegQuiz(
    val q: String,
    val opts: List<String>,
    /** 正确选项下标。 */
    val a: Int
)

data class WegSpeaking(
    val intro: String,
    val lines: List<String>,
    val outro: String
)

data class WegLesson(
    val level: String,
    val num: Int,
    val thema: String,
    val zh: String,
    val duration: String,
    val folgen: List<WegFolge>,
    val cando: List<String>,
    val phrases: List<Pair<String, String>>,
    val dialogue: List<Pair<String, String>>,
    val dialogueNote: String,
    val grammar: List<WegGrammar>,
    val words: List<WegWord>,
    val quiz: List<WegQuiz>,
    val speaking: WegSpeaking
)
