package com.astemo.delernen.data.db

import android.content.Context
import androidx.room.ColumnInfo
import androidx.room.Dao
import androidx.room.Database
import androidx.room.Entity
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Room
import androidx.room.RoomDatabase
import androidx.room.migration.Migration
import androidx.sqlite.db.SupportSQLiteDatabase

/**
 * 背单词进度。主键 = (source, wkey)，wkey 与网站 memorize 的 key(id, w.k||w.de) 完全一致
 * （v1 用的是 de，v2 起改为 k||de，见 [MIGRATION_1_2] 与 SrsRepository.migrateKeys）。
 * SRS 规则见 data/srs/SrsRules.kt（与网站 memorize 完全一致）。
 *
 * 迁移策略：schema 导出到 android/app/schemas（exportSchema = true），每次改表必须 version+1
 * 并写显式 Migration 加到 [ALL_MIGRATIONS]；**禁止** fallbackToDestructiveMigration（会清空进度）。
 */
@Entity(tableName = "srs_words", primaryKeys = ["source", "wkey"])
data class SrsWord(
    val source: String,
    /** 进度键：w.k ?: w.de */
    @ColumnInfo(name = "wkey") val key: String,
    val box: Int,
    val dueAt: Long,
    val lastSeen: Long,
    val lastGrade: Int,
    val createdAt: Long
)

@Dao
interface SrsDao {
    @Query("SELECT * FROM srs_words WHERE source = :source AND wkey = :key")
    suspend fun get(source: String, key: String): SrsWord?

    @Query("SELECT * FROM srs_words WHERE source IN (:sources)")
    suspend fun getWords(sources: List<String>): List<SrsWord>

    @Query("SELECT * FROM srs_words")
    suspend fun getAll(): List<SrsWord>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsert(word: SrsWord)

    @Query("DELETE FROM srs_words WHERE source = :source AND wkey = :key")
    suspend fun delete(source: String, key: String)

    @Query("DELETE FROM srs_words")
    suspend fun clear()
}

@Database(entities = [SrsWord::class], version = 2, exportSchema = true)
abstract class AppDatabase : RoomDatabase() {
    abstract fun srsDao(): SrsDao

    companion object {
        /**
         * v1 → v2：主键列 de → wkey。这里只做结构迁移（原样把 de 复制到 wkey）；
         * 带 k 的词需要数据文件才能把 de 映射到 k，由 SrsRepository.migrateKeys() 在启动时
         * （后台线程）完成，并照搬网站的 ALIAS 合并规则。
         */
        val MIGRATION_1_2 = object : Migration(1, 2) {
            override fun migrate(db: SupportSQLiteDatabase) {
                db.execSQL(
                    "CREATE TABLE IF NOT EXISTS `srs_words_new` (" +
                            "`source` TEXT NOT NULL, `wkey` TEXT NOT NULL, `box` INTEGER NOT NULL, " +
                            "`dueAt` INTEGER NOT NULL, `lastSeen` INTEGER NOT NULL, " +
                            "`lastGrade` INTEGER NOT NULL, `createdAt` INTEGER NOT NULL, " +
                            "PRIMARY KEY(`source`, `wkey`))"
                )
                db.execSQL(
                    "INSERT OR REPLACE INTO `srs_words_new` " +
                            "(`source`, `wkey`, `box`, `dueAt`, `lastSeen`, `lastGrade`, `createdAt`) " +
                            "SELECT `source`, `de`, `box`, `dueAt`, `lastSeen`, `lastGrade`, `createdAt` " +
                            "FROM `srs_words`"
                )
                db.execSQL("DROP TABLE `srs_words`")
                db.execSQL("ALTER TABLE `srs_words_new` RENAME TO `srs_words`")
            }
        }

        val ALL_MIGRATIONS: Array<Migration> = arrayOf(MIGRATION_1_2)

        @Volatile
        private var INSTANCE: AppDatabase? = null

        fun get(context: Context): AppDatabase =
            INSTANCE ?: synchronized(this) {
                INSTANCE ?: Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "delernen.db"
                )
                    .addMigrations(*ALL_MIGRATIONS)
                    .build()
                    .also { INSTANCE = it }
            }
    }
}
