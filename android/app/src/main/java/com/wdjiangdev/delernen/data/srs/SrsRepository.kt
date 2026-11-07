package com.wdjiangdev.delernen.data.srs

import android.content.Context
import android.content.SharedPreferences
import com.wdjiangdev.delernen.data.db.AppDatabase
import com.wdjiangdev.delernen.data.db.SrsDao
import com.wdjiangdev.delernen.data.db.SrsWord
import org.json.JSONArray
import java.time.LocalDate

/** Room（SRS 进度）+ SharedPreferences（每日新词计数与设置）的薄封装。 */
class SrsRepository(context: Context) {

    private val dao: SrsDao = AppDatabase.get(context).srsDao()
    private val prefs: SharedPreferences =
        context.getSharedPreferences("delernen_srs", Context.MODE_PRIVATE)

    // ---------------- Room ----------------

    suspend fun word(source: String, de: String): SrsWord? = dao.get(source, de)

    suspend fun words(sources: List<String>): List<SrsWord> = dao.getWords(sources)

    suspend fun upsert(word: SrsWord) = dao.upsert(word)

    suspend fun delete(source: String, de: String) = dao.delete(source, de)

    suspend fun countDue(sources: List<String>, now: Long): Int = dao.countDue(sources, now)

    suspend fun countDueBetween(sources: List<String>, now: Long, until: Long): Int =
        dao.countDueBetween(sources, now, until)

    suspend fun countMastered(sources: List<String>): Int =
        dao.countMastered(sources, SrsRules.MASTER_BOX)

    suspend fun clearAll() = dao.clear()

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
    }
}
