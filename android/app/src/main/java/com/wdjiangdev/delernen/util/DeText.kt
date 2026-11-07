package com.wdjiangdev.delernen.util

import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.unit.sp
import com.wdjiangdev.delernen.ui.theme.DelernenColors

/**
 * 德语词条文本工具：与网站 memorize/index.html 的 deHtml/sayText 对齐。
 * - annotatedDe：给开头的定冠词着色（der 阳 g-m / die 阴 g-f / das 中 g-n），
 *   并把 (nur Sg.) / (meist Pl.) 这类注释缩小显示。
 * - sayText：朗读前去掉冠词与括号注释（TTS 用）。
 */
object DeText {

    private val ARTICLE_RE = Regex("(^|/ )(der/die|der/das|der|die|das)(?= )")
    private val NOTE_RE = Regex(" (\\((?:nur|meist) (?:Sg|Pl)\\.\\))")

    fun annotatedDe(de: String): AnnotatedString = buildAnnotatedString {
        var rest = de
        var guard = 0
        while (guard++ < 4) {
            val m = ARTICLE_RE.find(rest) ?: break
            append(rest.substring(0, m.range.first))
            val prefix = m.groupValues[1]
            val article = m.groupValues[2]
            append(prefix)
            val color = when (article) {
                "der" -> DelernenColors.GMasc
                "die" -> DelernenColors.GFem
                "das" -> DelernenColors.GNeut
                else -> DelernenColors.Purple
            }
            withStyle(SpanStyle(color = color)) { append(article) }
            rest = rest.substring(m.range.last + 1)
        }
        // 复数注释缩小（网站 .g-note）
        val noteMatch = NOTE_RE.find(rest)
        if (noteMatch != null) {
            append(rest.substring(0, noteMatch.range.first))
            withStyle(SpanStyle(fontSize = 11.sp, color = DelernenColors.Text3)) {
                append(noteMatch.groupValues[1])
            }
            append(rest.substring(noteMatch.range.last + 1))
        } else {
            append(rest)
        }
    }

    /** 朗读用：去掉冠词、括号注释，只取第一个释义（以逗号或 " / " 分割）。 */
    fun sayText(de: String): String {
        var s = Regex("[,]|( / )").split(de).firstOrNull() ?: de
        s = Regex("\\s*\\([^)]*\\)").replace(s, "")
        s = Regex("^(der/die|der/das|der|die|das)\\s+").replace(s, "")
        return s.trim()
    }
}
