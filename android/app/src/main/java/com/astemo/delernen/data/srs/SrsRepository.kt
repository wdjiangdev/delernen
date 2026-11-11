package com.astemo.delernen.data.srs

import android.content.Context
import android.content.SharedPreferences
import androidx.room.withTransaction
import com.astemo.delernen.data.SrsCard
import com.astemo.delernen.data.db.AppDatabase
import com.astemo.delernen.data.db.SrsDao
import com.astemo.delernen.data.db.SrsWord
import org.json.JSONArray
import java.time.LocalDate

/** Room（SRS 进度）+ SharedPreferences（每日新词计数与设置）的薄封装。 */
class SrsRepository(context: Context) {

    private val db: AppDatabase = AppDatabase.get(context)
    private val dao: SrsDao = db.srsDao()
    private val prefs: SharedPreferences =
        context.getSharedPreferences("delernen_srs", Context.MODE_PRIVATE)

    // ---------------- Room ----------------

    suspend fun word(source: String, key: String): SrsWord? = dao.get(source, key)

    suspend fun words(sources: List<String>): List<SrsWord> = dao.getWords(sources)

    suspend fun upsert(word: SrsWord) = dao.upsert(word)

    suspend fun delete(source: String, key: String) = dao.delete(source, key)

    suspend fun clearAll() = dao.clear()

    /**
     * 把 v1 时代按 de 存的进度行迁到 k||de 键上（与网站一致），并照搬网站 memorize 的 ALIAS 合并。
     * 需要解析数据文件，必须在后台线程调用。每个 [KEY_MIGRATION_VERSION] 只跑一次；
     * 以后网站 ALIAS 表有新增时，把它同步到 [ALIAS] 并把版本号 +1。
     *
     * 合并规则同网站 migrate()：目标键已有进度时，保留 box 更高的；box 相同保留 dueAt 更晚的。
     * 无法映射的孤儿行保留在库里，但统计/出题只认当前数据里存在的键，不会再计入「待复习」。
     */
    suspend fun migrateKeys(sourceIds: List<String>, wordsOf: (String) -> List<SrsCard>) {
        if (prefs.getInt(KEY_KEY_MIGRATION, 0) >= KEY_MIGRATION_VERSION) return
        val rows = dao.getAll()
        if (rows.isNotEmpty()) {
            db.withTransaction {
                val bySource = rows.groupBy { it.source }
                for ((src, srcRows) in bySource) {
                    if (src !in sourceIds) continue
                    val cards = wordsOf(src)
                    val validKeys = cards.mapTo(HashSet()) { it.key }
                    val deToKey = HashMap<String, String>()
                    for (c in cards) if (c.key != c.de) deToKey.putIfAbsent(c.de, c.key)
                    val current = srcRows.associateByTo(HashMap()) { it.key }
                    for (row in srcRows) {
                        if (row.key in validKeys) continue
                        val target = ALIAS["$src|${row.key}"]?.substringAfter('|')
                            ?: deToKey[row.key]
                            ?: continue
                        if (target !in validKeys) continue
                        val existing = current[target]
                        val keepOld = existing == null || row.box > existing.box ||
                                (row.box == existing.box && row.dueAt > existing.dueAt)
                        if (keepOld) {
                            val moved = row.copy(key = target)
                            dao.upsert(moved)
                            current[target] = moved
                        }
                        dao.delete(src, row.key)
                        current.remove(row.key)
                    }
                }
            }
        }
        prefs.edit().putInt(KEY_KEY_MIGRATION, KEY_MIGRATION_VERSION).apply()
    }

    // ---------------- 设置与每日计数 ----------------

    var newPerDay: Int
        get() = prefs.getInt(KEY_NEW_PER_DAY, 20)
        set(v) = prefs.edit().putInt(KEY_NEW_PER_DAY, v).apply()

    /** 出题顺序：mix | split | list（与网站一致） */
    var order: String
        get() = prefs.getString(KEY_ORDER, "mix") ?: "mix"
        set(v) = prefs.edit().putString(KEY_ORDER, v).apply()

    var selectedSources: List<String>
        get() {
            val s = prefs.getString(KEY_SELECTED_SOURCES, null) ?: return emptyList()
            return try {
                val arr = JSONArray(s)
                (0 until arr.length()).map { arr.getString(it) }
            } catch (_: Exception) {
                emptyList()
            }
        }
        set(v) = prefs.edit().putString(KEY_SELECTED_SOURCES, JSONArray(v).toString()).apply()

    private fun todayEpochDay(): Long = LocalDate.now().toEpochDay()

    /** 今日已学新词数（跨天自动清零）。 */
    var newCountToday: Int
        get() {
            if (prefs.getLong(KEY_NEW_DATE, Long.MIN_VALUE) != todayEpochDay()) return 0
            return prefs.getInt(KEY_NEW_COUNT, 0)
        }
        set(v) = prefs.edit()
            .putLong(KEY_NEW_DATE, todayEpochDay())
            .putInt(KEY_NEW_COUNT, v)
            .apply()

    companion object {
        private const val KEY_NEW_PER_DAY = "newPerDay"
        private const val KEY_ORDER = "order"
        private const val KEY_SELECTED_SOURCES = "selectedSources"
        private const val KEY_NEW_DATE = "newDate"
        private const val KEY_NEW_COUNT = "newCount"
        private const val KEY_KEY_MIGRATION = "keyMigrationVersion"
        private const val KEY_MIGRATION_VERSION = 1

        /** 照搬网站 memorize/index.html 的 ALIAS（"源|旧键" → "源|新键"）。 */
        val ALIAS: Map<String, String> = mapOf(
            "nicos_a1|der Weg, die Wege" to "nicos_a1|weg",
            "nicos_a2|feste" to "nicos_a2|Fest",
            "nicos_b1|Erde (f., hier nur Singular)" to "nicos_b1|Erde, -n (f., meist Singular)",
            "nicos_b1|Asyl (n., selten im Plural)" to "nicos_b1|Asyl, -e (n., meist Singular)"
        )
    }
}
