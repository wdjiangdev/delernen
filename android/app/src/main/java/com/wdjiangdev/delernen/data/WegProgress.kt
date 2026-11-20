package com.wdjiangdev.delernen.data

import android.content.Context
import android.content.SharedPreferences

/**
 * 加速课「已学完」标记：SharedPreferences 布尔键 "<level>-<num>"
 * （如 "a1-3"），与网页端 localStorage 的 nicosweg-<level>-<NN>-done 口径一致。
 */
object WegProgress {
    @Volatile
    private var prefs: SharedPreferences? = null

    fun init(context: Context) {
        if (prefs == null) {
            prefs = context.applicationContext
                .getSharedPreferences("weg_progress", Context.MODE_PRIVATE)
        }
    }

    private fun key(level: String, num: Int) = "$level-$num"

    fun isDone(level: String, num: Int): Boolean =
        prefs?.getBoolean(key(level, num), false) ?: false

    fun setDone(level: String, num: Int, done: Boolean) {
        prefs?.edit()?.putBoolean(key(level, num), done)?.apply()
    }
}
