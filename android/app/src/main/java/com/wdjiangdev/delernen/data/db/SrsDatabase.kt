package com.wdjiangdev.delernen.data.db

import android.content.Context
import androidx.room.Dao
import androidx.room.Database
import androidx.room.Entity
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Room
import androidx.room.RoomDatabase

/**
 * 背单词进度。实体按 source+de 唯一键，存 box、dueAt、lastSeen 等。
 * SRS 规则见 data/srs/SrsRules.kt（与网站 memorize 完全一致）。
 */
@Entity(tableName = "srs_words", primaryKeys = ["source", "de"])
data class SrsWord(
    val source: String,
    val de: String,
    val box: Int,
    val dueAt: Long,
    val lastSeen: Long,
    val lastGrade: Int,
    val createdAt: Long
)

@Dao
interface SrsDao {
    @Query("SELECT * FROM srs_words WHERE source = :source AND de = :de")
    suspend fun get(source: String, de: String): SrsWord?

    @Query("SELECT * FROM srs_words WHERE source IN (:sources)")
    suspend fun getWords(sources: List<String>): List<SrsWord>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsert(word: SrsWord)

    @Query("DELETE FROM srs_words WHERE source = :source AND de = :de")
    suspend fun delete(source: String, de: String)

    /** 待复习：到期时间 <= 现在 */
    @Query("SELECT COUNT(*) FROM srs_words WHERE source IN (:sources) AND dueAt <= :now")
    suspend fun countDue(sources: List<String>, now: Long): Int

    /** 未来一段时间内到期（now < dueAt <= until） */
    @Query("SELECT COUNT(*) FROM srs_words WHERE source IN (:sources) AND dueAt > :now AND dueAt <= :until")
    suspend fun countDueBetween(sources: List<String>, now: Long, until: Long): Int

    /** 已掌握：达到最高级 box >= MASTER_BOX */
    @Query("SELECT COUNT(*) FROM srs_words WHERE source IN (:sources) AND box >= :masterBox")
    suspend fun countMastered(sources: List<String>, masterBox: Int): Int

    @Query("DELETE FROM srs_words")
    suspend fun clear()
}

@Database(entities = [SrsWord::class], version = 1, exportSchema = false)
abstract class AppDatabase : RoomDatabase() {
    abstract fun srsDao(): SrsDao

    companion object {
        @Volatile
        private var INSTANCE: AppDatabase? = null

        fun get(context: Context): AppDatabase =
            INSTANCE ?: synchronized(this) {
                INSTANCE ?: Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "delernen.db"
                ).build().also { INSTANCE = it }
            }
    }
}
