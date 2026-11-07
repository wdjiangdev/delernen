package com.wdjiangdev.delernen.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

/**
 * 配色取自网站 theme.css 的深色默认值（--bg 深蓝底 + 星图感强调色）。
 * 原始值：--bg:#0a0e1a --bg-card:#111830 --bg-elev:#141b30 --bg-deep:#0d1326
 * --chip:#1a2340 --text:#e0e6f0 --text2:#b0b8d0 --text3:#8a93a8
 * --border:#2a3350 --border2:#232c48 --accent:#4a7aca --accent2:#6ab0ff
 * --accentbg:#2a4a8a --accentdeep:#1a2a5a --green:#7dd87d --orange:#ffb84d
 * --red:#ff7d7d --purple:#9d7bff --yellow:#ffd479 --g-m:#5a9cf0 --g-f:#f06a7e --g-n:#4cc28c
 */
object DelernenColors {
    val Bg = Color(0xFF0A0E1A)
    val BgCard = Color(0xFF111830)
    val BgElev = Color(0xFF141B30)
    val BgDeep = Color(0xFF0D1326)
    val Chip = Color(0xFF1A2340)
    val Text = Color(0xFFE0E6F0)
    val Text2 = Color(0xFFB0B8D0)
    val Text3 = Color(0xFF8A93A8)
    val Border = Color(0xFF2A3350)
    val Border2 = Color(0xFF232C48)
    val Accent = Color(0xFF4A7ACA)
    val Accent2 = Color(0xFF6AB0FF)
    val AccentBg = Color(0xFF2A4A8A)
    val AccentDeep = Color(0xFF1A2A5A)
    val Green = Color(0xFF7DD87D)
    val Orange = Color(0xFFFFB84D)
    val Red = Color(0xFFFF7D7D)
    val Purple = Color(0xFF9D7BFF)
    val Yellow = Color(0xFFFFD479)
    // 冠词性别色（网站 .g-m/.g-f/.g-n）
    val GMasc = Color(0xFF5A9CF0)
    val GFem = Color(0xFFF06A7E)
    val GNeut = Color(0xFF4CC28C)
}

private val DarkColorScheme = darkColorScheme(
    primary = DelernenColors.Accent2,
    onPrimary = DelernenColors.Bg,
    primaryContainer = DelernenColors.AccentBg,
    onPrimaryContainer = Color(0xFFDCEAFF),
    secondary = DelernenColors.Accent,
    onSecondary = DelernenColors.Text,
    secondaryContainer = DelernenColors.AccentDeep,
    onSecondaryContainer = DelernenColors.Accent2,
    tertiary = DelernenColors.Purple,
    onTertiary = DelernenColors.Bg,
    background = DelernenColors.Bg,
    onBackground = DelernenColors.Text,
    surface = DelernenColors.BgCard,
    onSurface = DelernenColors.Text,
    surfaceVariant = DelernenColors.Chip,
    onSurfaceVariant = DelernenColors.Text2,
    surfaceContainerLow = DelernenColors.BgCard,
    surfaceContainer = DelernenColors.BgElev,
    surfaceContainerHigh = DelernenColors.Chip,
    outline = DelernenColors.Border,
    outlineVariant = DelernenColors.Border2,
    error = DelernenColors.Red,
    onError = DelernenColors.Bg
)

@Composable
fun DelernenTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = DarkColorScheme,
        content = content
    )
}
