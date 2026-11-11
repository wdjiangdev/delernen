package com.astemo.delernen.data

import android.content.Context
import org.json.JSONArray
import org.json.JSONObject

/**
 * 从 assets/data/ 读取 build_android_data.py 产出的 JSON，解析成模型。
 * 全部懒加载且进程内缓存；解析在调用线程执行，UI 侧请用 Dispatchers.Default。
 */
object DataRepo {
    private const val DIR = "data"

    @Volatile
    private var appContext: Context? = null

    fun init(context: Context) {
        if (appContext == null) appContext = context.applicationContext
    }

    private fun ctx(): Context = appContext ?: error("DataRepo.init(context) 未调用")

    private fun loadJson(name: String): String =
        ctx().assets.open("$DIR/$name").bufferedReader().use { it.readText() }

    private fun optStr(o: JSONObject, key: String): String =
        if (o.isNull(key)) "" else o.optString(key, "")

    // ---------------- nicos ----------------

    private fun parseNicos(name: String): List<NicosWord> {
        val arr = JSONArray(loadJson(name))
        return (0 until arr.length()).map { i ->
            val o = arr.getJSONObject(i)
            NicosWord(
                de = o.getString("de"),
                en = optStr(o, "en"),
                zh = optStr(o, "zh"),
                pos = optStr(o, "pos"),
                tip = optStr(o, "tip"),
                topic = optStr(o, "topic"),
                past = optStr(o, "past"),
                pp = optStr(o, "pp"),
                k = optStr(o, "k")
            )
        }
    }

    val nicosA1: List<NicosWord> by lazy { parseNicos("nicos_a1.json") }
    val nicosA2: List<NicosWord> by lazy { parseNicos("nicos_a2.json") }
    val nicosB1: List<NicosWord> by lazy { parseNicos("nicos_b1.json") }

    fun nicos(level: String): List<NicosWord> = when (level) {
        "a1" -> nicosA1
        "a2" -> nicosA2
        "b1" -> nicosB1
        else -> emptyList()
    }

    // ---------------- 可分动词分组 ----------------

    private fun parseVerbGroups(name: String): List<VerbGroup> {
        val arr = JSONObject(loadJson(name)).getJSONArray("groups")
        return (0 until arr.length()).map { i ->
            val g = arr.getJSONObject(i)
            val memArr = g.getJSONArray("members")
            val members = (0 until memArr.length()).map { j ->
                val m = memArr.getJSONObject(j)
                VerbMember(
                    verb = m.getString("verb"),
                    prefix = if (m.isNull("prefix")) null else m.optString("prefix", ""),
                    count = m.optInt("count", 1),
                    def = optStr(m, "def"),
                    past = optStr(m, "past"),
                    pp = optStr(m, "pp"),
                    zh = optStr(m, "zh"),
                    level = optStr(m, "level")
                )
            }
            VerbGroup(
                stem = g.getString("stem"),
                stemDef = optStr(g, "stemDef"),
                stemZh = optStr(g, "stemZh"),
                level = optStr(g, "level"),
                members = members,
                inA1A2 = g.optBoolean("inA1A2", false)
            )
        }
    }

    val verbGroupsA1A2: List<VerbGroup> by lazy { parseVerbGroups("verb_groups_a1a2.json") }
    val verbGroupsA1B2: List<VerbGroup> by lazy { parseVerbGroups("verb_groups_a1b2.json") }

    fun verbGroups(range: String): List<VerbGroup> = when (range) {
        "a1b2" -> verbGroupsA1B2
        else -> verbGroupsA1A2
    }

    // ---------------- 词族 ----------------

    private fun parseWordFamilies(name: String): List<WordFamily> {
        val arr = JSONObject(loadJson(name)).getJSONArray("families")
        return (0 until arr.length()).map { i ->
            val f = arr.getJSONObject(i)
            val memArr = f.getJSONArray("members")
            val members = (0 until memArr.length()).map { j ->
                val m = memArr.getJSONObject(j)
                FamilyMember(
                    word = m.getString("word"),
                    pos = optStr(m, "pos"),
                    zh = optStr(m, "zh"),
                    past = optStr(m, "past"),
                    pp = optStr(m, "pp"),
                    plural = optStr(m, "plural")
                )
            }
            WordFamily(root = f.getString("root"), members = members)
        }
    }

    val wordFamiliesA1A2: List<WordFamily> by lazy { parseWordFamilies("word_families_a1a2.json") }
    val wordFamiliesA1B2: List<WordFamily> by lazy { parseWordFamilies("word_families_a1b2.json") }

    fun wordFamilies(range: String): List<WordFamily> = when (range) {
        "a1b2" -> wordFamiliesA1B2
        else -> wordFamiliesA1A2
    }

    // ---------------- 语法 ----------------

    private fun parseGrammarGroups(name: String): List<GrammarGroup> {
        val arr = JSONObject(loadJson(name)).getJSONArray("groups")
        return (0 until arr.length()).map { i ->
            val g = arr.getJSONObject(i)
            val memArr = g.getJSONArray("members")
            val members = (0 until memArr.length()).map { j ->
                val m = memArr.getJSONObject(j)
                GrammarMember(
                    word = m.getString("word"),
                    zh = optStr(m, "zh"),
                    ex = optStr(m, "ex")
                )
            }
            GrammarGroup(
                id = g.getString("id"),
                title = g.getString("title"),
                titleZh = g.getString("titleZh"),
                members = members,
                learn = optStr(g, "learn"),
                learnTitle = optStr(g, "learnTitle"),
                level = optStr(g, "level"),
                inA1A2 = g.optBoolean("inA1A2", false)
            )
        }
    }

    val grammarGroupsA1A2: List<GrammarGroup> by lazy { parseGrammarGroups("grammar_a1a2.json") }
    val grammarGroupsA1B2: List<GrammarGroup> by lazy { parseGrammarGroups("grammar_a1b2.json") }

    fun grammarGroups(range: String): List<GrammarGroup> = when (range) {
        "a1b2" -> grammarGroupsA1B2
        else -> grammarGroupsA1A2
    }

    // ---------------- sep 可分动词（背单词数据源） ----------------

    private fun parseSep(name: String): List<SepWord> {
        val arr = JSONArray(loadJson(name))
        return (0 until arr.length()).map { i ->
            val o = arr.getJSONObject(i)
            SepWord(
                de = o.getString("de"),
                en = optStr(o, "en"),
                zh = optStr(o, "zh"),
                pos = optStr(o, "pos"),
                tip = optStr(o, "tip"),
                topic = optStr(o, "topic"),
                prefix = optStr(o, "prefix"),
                stem = optStr(o, "stem"),
                past = optStr(o, "past"),
                pp = optStr(o, "pp"),
                k = optStr(o, "k")
            )
        }
    }

    val sepA1A2: List<SepWord> by lazy { parseSep("sep_a1a2.json") }
    val sepA1B2: List<SepWord> by lazy { parseSep("sep_a1b2.json") }

    // ---------------- kurs 课程卡 ----------------

    val kursCards: List<KursCard> by lazy {
        val arr = JSONArray(loadJson("kurs.json"))
        (0 until arr.length()).map { i ->
            val c = arr.getJSONObject(i)
            val exArr = c.optJSONArray("examples")
            val examples = (0 until (exArr?.length() ?: 0)).map { j ->
                val row = exArr!!.getJSONArray(j)
                row.optString(0, "") to (if (row.length() > 1) row.optString(1, "") else "")
            }
            val tArr = c.optJSONArray("table")
            val table = (0 until (tArr?.length() ?: 0)).map { j ->
                val row = tArr!!.getJSONArray(j)
                (0 until row.length()).map { k -> row.optString(k, "") }
            }
            KursCard(
                num = c.getString("num"),
                id = optStr(c, "id"),
                cat = optStr(c, "cat"),
                title = c.getString("title"),
                titleDe = optStr(c, "titleDe"),
                explain = optStr(c, "explain"),
                examples = examples,
                table = table,
                level = optStr(c, "level")
            )
        }
    }

    fun kursByLevel(level: String): List<KursCard> = kursCards.filter { it.level == level }

    fun kursByNum(num: String): KursCard? = kursCards.firstOrNull { it.num == num }

    // ---------------- alice 笔记 ----------------

    val aliceNotes: List<AliceNote> by lazy {
        val arr = JSONArray(loadJson("alice.json"))
        (0 until arr.length()).map { i ->
            val n = arr.getJSONObject(i)
            val blocksArr = n.getJSONArray("blocks")
            val blocks = (0 until blocksArr.length()).map { j ->
                val b = blocksArr.getJSONObject(j)
                AliceBlock(
                    type = b.getString("type"),
                    text = b.getString("text"),
                    zh = optStr(b, "zh")
                )
            }
            AliceNote(
                title = n.getString("title"),
                level = optStr(n, "level"),
                blocks = blocks
            )
        }
    }

    fun aliceByLevel(level: String): List<AliceNote> = aliceNotes.filter { it.level == level }

    // ---------------- 背单词数据源归一化 ----------------

    /** 网站 memorize 的 SRS_SOURCES 等价物（不触发 JSON 解析，词数在首次 srsWords() 之后才准确）。 */
    val srsSourceIds: List<String> = listOf("sep_a1a2", "sep_a1b2", "nicos_a1", "nicos_a2", "nicos_b1")

    /**
     * 五个数据源及词数。会解析全部 JSON（约 0.8 MB），**只能在后台线程调用**
     * （MemorizeViewModel 在 Dispatchers.Default 上读取）。
     */
    val srsSources: List<SrsSourceDef> by lazy {
        listOf(
            SrsSourceDef("sep_a1a2", "A1-A2 可分动词", sepA1A2.size),
            SrsSourceDef("sep_a1b2", "A1-B2 可分动词", sepA1B2.size),
            SrsSourceDef("nicos_a1", "Nicos Weg A1 单词", nicosA1.size),
            SrsSourceDef("nicos_a2", "Nicos Weg A2 单词", nicosA2.size),
            SrsSourceDef("nicos_b1", "Nicos Weg B1 单词", nicosB1.size)
        )
    }

    /** 进度键：与网站 memorize 的 key(id, w.k||w.de) 一致。 */
    private fun srsKey(k: String, de: String): String = k.ifBlank { de }

    private val srsCache = java.util.concurrent.ConcurrentHashMap<String, List<SrsCard>>()

    /** 某数据源的背单词卡片（已缓存；首次调用会解析 JSON，请在后台线程调用）。 */
    fun srsWords(sourceId: String): List<SrsCard> = srsCache.getOrPut(sourceId) {
        when (sourceId) {
            "sep_a1a2" -> sepA1A2.map {
                SrsCard("sep_a1a2", it.de, it.en, it.zh, it.pos, it.tip, it.past, it.pp, srsKey(it.k, it.de))
            }
            "sep_a1b2" -> sepA1B2.map {
                SrsCard("sep_a1b2", it.de, it.en, it.zh, it.pos, it.tip, it.past, it.pp, srsKey(it.k, it.de))
            }
            "nicos_a1" -> nicosA1.map {
                SrsCard("nicos_a1", it.de, it.en, it.zh, it.pos, it.tip, it.past, it.pp, srsKey(it.k, it.de))
            }
            "nicos_a2" -> nicosA2.map {
                SrsCard("nicos_a2", it.de, it.en, it.zh, it.pos, it.tip, it.past, it.pp, srsKey(it.k, it.de))
            }
            "nicos_b1" -> nicosB1.map {
                SrsCard("nicos_b1", it.de, it.en, it.zh, it.pos, it.tip, it.past, it.pp, srsKey(it.k, it.de))
            }
            else -> emptyList()
        }
    }
}
