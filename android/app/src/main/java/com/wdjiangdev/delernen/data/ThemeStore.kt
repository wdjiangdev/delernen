package com.wdjiangdev.delernen.data

import android.content.Context

/** 主题偏好落盘：只存一个布尔（白色主题开/关），默认关 = 蓝色主题。 */
object ThemeStore {
    private const val KEY_LIGHT = "light_theme"

    private fun prefs(context: Context) =
        context.applicationContext.getSharedPreferences("app_theme", Context.MODE_PRIVATE)

    fun isLight(context: Context): Boolean = prefs(context).getBoolean(KEY_LIGHT, false)

    fun setLight(context: Context, light: Boolean) {
        prefs(context).edit().putBoolean(KEY_LIGHT, light).apply()
    }
}
