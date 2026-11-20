package com.wdjiangdev.delernen.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.compose.ui.graphics.Color

/**
 * 主题状态：false = 蓝色（深色，默认），true = 白色（浅色）。
 * MainActivity 启动时从 ThemeStore（SharedPreferences）读入；顶栏切换按钮改这里并落盘。
 * [DelernenColors] 的每个 getter 都读它——在组合期读到即订阅，切换时全 App 即时重组换色。
 */
object ThemeState {
    var light by mutableStateOf(false)
}

private data class Palette(
    val Bg: Color, val BgCard: Color, val BgElev: Color, val BgDeep: Color,
    val Chip: Color, val Text: Color, val Text2: Color, val Text3: Color,
    val Border: Color, val Border2: Color,
    val Accent: Color, val Accent2: Color, val AccentBg: Color, val AccentDeep: Color,
    val Green: Color, val Orange: Color, val Red: Color, val Purple: Color, val Yellow: Color,
    val GMasc: Color, val GFem: Color, val GNeut: Color
)

/** 蓝色主题（深色）：取自网站 theme.css 的深色默认值（--bg 深蓝底 + 星图感强调色）。 */
private val DarkPalette = Palette(
    Bg = Color(0xFF0A0E1A), BgCard = Color(0xFF111830), BgElev = Color(0xFF141B30),
    BgDeep = Color(0xFF0D1326), Chip = Color(0xFF1A2340),
    Text = Color(0xFFE0E6F0), Text2 = Color(0xFFB0B8D0), Text3 = Color(0xFF8A93A8),
    Border = Color(0xFF2A3350), Border2 = Color(0xFF232C48),
    Accent = Color(0xFF4A7ACA), Accent2 = Color(0xFF6AB0FF),
    AccentBg = Color(0xFF2A4A8A), AccentDeep = Color(0xFF1A2A5A),
    Green = Color(0xFF7DD87D), Orange = Color(0xFFFFB84D), Red = Color(0xFFFF7D7D),
    Purple = Color(0xFF9D7BFF), Yellow = Color(0xFFFFD479),
    GMasc = Color(0xFF5A9CF0), GFem = Color(0xFFF06A7E), GNeut = Color(0xFF4CC28C)
)

/** 白色主题（浅色）：白卡 + 近白底，强调色仍是同一套蓝（加深以保证白底对比度）。 */
private val LightPalette = Palette(
    Bg = Color(0xFFF7F8FA), BgCard = Color(0xFFFFFFFF), BgElev = Color(0xFFFFFFFF),
    BgDeep = Color(0xFFEEF1F6), Chip = Color(0xFFE8EDF5),
    Text = Color(0xFF1B2334), Text2 = Color(0xFF4C5872), Text3 = Color(0xFF7C879E),
    Border = Color(0xFFD4DBE8), Border2 = Color(0xFFE0E5EF),
    Accent = Color(0xFF2F5DA8), Accent2 = Color(0xFF1668DC),
    AccentBg = Color(0xFFD9E7FB), AccentDeep = Color(0xFFBCD4F7),
    Green = Color(0xFF2F9E44), Orange = Color(0xFFE8890C), Red = Color(0xFFD64545),
    Purple = Color(0xFF7048E8), Yellow = Color(0xFFC77400),
    GMasc = Color(0xFF2B7CD3), GFem = Color(0xFFE05260), GNeut = Color(0xFF1F9D66)
)

/**
 * 全 App 唯一配色入口（调用点不变）：getter 按 [ThemeState] 返回当前主题的色值。
 * 在 @Composable 里读会订阅主题状态，切换即重组；非组合期读到的是当下值。
 */
object DelernenColors {
    private val p: Palette get() = if (ThemeState.light) LightPalette else DarkPalette
    val Bg: Color get() = p.Bg
    val BgCard: Color get() = p.BgCard
    val BgElev: Color get() = p.BgElev
    val BgDeep: Color get() = p.BgDeep
    val Chip: Color get() = p.Chip
    val Text: Color get() = p.Text
    val Text2: Color get() = p.Text2
    val Text3: Color get() = p.Text3
    val Border: Color get() = p.Border
    val Border2: Color get() = p.Border2
    val Accent: Color get() = p.Accent
    val Accent2: Color get() = p.Accent2
    val AccentBg: Color get() = p.AccentBg
    val AccentDeep: Color get() = p.AccentDeep
    val Green: Color get() = p.Green
    val Orange: Color get() = p.Orange
    val Red: Color get() = p.Red
    val Purple: Color get() = p.Purple
    val Yellow: Color get() = p.Yellow
    // 冠词性别色（网站 .g-m/.g-f/.g-n）
    val GMasc: Color get() = p.GMasc
    val GFem: Color get() = p.GFem
    val GNeut: Color get() = p.GNeut
}

private val DarkColorScheme = darkColorScheme(
    primary = DarkPalette.Accent2,
    onPrimary = DarkPalette.Bg,
    primaryContainer = DarkPalette.AccentBg,
    onPrimaryContainer = Color(0xFFDCEAFF),
    secondary = DarkPalette.Accent,
    onSecondary = DarkPalette.Text,
    secondaryContainer = DarkPalette.AccentDeep,
    onSecondaryContainer = DarkPalette.Accent2,
    tertiary = DarkPalette.Purple,
    onTertiary = DarkPalette.Bg,
    background = DarkPalette.Bg,
    onBackground = DarkPalette.Text,
    surface = DarkPalette.BgCard,
    onSurface = DarkPalette.Text,
    surfaceVariant = DarkPalette.Chip,
    onSurfaceVariant = DarkPalette.Text2,
    surfaceContainerLow = DarkPalette.BgCard,
    surfaceContainer = DarkPalette.BgElev,
    surfaceContainerHigh = DarkPalette.Chip,
    outline = DarkPalette.Border,
    outlineVariant = DarkPalette.Border2,
    error = DarkPalette.Red,
    onError = DarkPalette.Bg
)

private val LightColorScheme = lightColorScheme(
    primary = LightPalette.Accent2,
    onPrimary = Color.White,
    primaryContainer = LightPalette.AccentBg,
    onPrimaryContainer = Color(0xFF12294D),
    secondary = LightPalette.Accent,
    onSecondary = Color.White,
    secondaryContainer = LightPalette.AccentDeep,
    onSecondaryContainer = Color(0xFF12294D),
    tertiary = LightPalette.Purple,
    onTertiary = Color.White,
    background = LightPalette.Bg,
    onBackground = LightPalette.Text,
    surface = LightPalette.BgCard,
    onSurface = LightPalette.Text,
    surfaceVariant = LightPalette.Chip,
    onSurfaceVariant = LightPalette.Text2,
    surfaceContainerLow = LightPalette.BgCard,
    surfaceContainer = Color(0xFFF0F3F8),
    surfaceContainerHigh = LightPalette.Chip,
    outline = LightPalette.Border,
    outlineVariant = LightPalette.Border2,
    error = LightPalette.Red,
    onError = Color.White
)

@Composable
fun DelernenTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = if (ThemeState.light) LightColorScheme else DarkColorScheme,
        content = content
    )
}
