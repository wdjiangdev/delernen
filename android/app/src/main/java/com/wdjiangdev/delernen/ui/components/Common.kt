package com.wdjiangdev.delernen.ui.components

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.VolumeUp
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.SegmentedButton
import androidx.compose.material3.SegmentedButtonDefaults
import androidx.compose.material3.SingleChoiceSegmentedButtonRow
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.wdjiangdev.delernen.ui.theme.DelernenColors
import com.wdjiangdev.delernen.util.TtsHelper

/** 单选分段切换（Material 3 SegmentedButton）。 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SegmentedRow(options: List<String>, selected: String, onSelect: (String) -> Unit) {
    SingleChoiceSegmentedButtonRow(
        modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 4.dp)
    ) {
        options.forEachIndexed { i, opt ->
            SegmentedButton(
                selected = opt == selected,
                onClick = { onSelect(opt) },
                shape = SegmentedButtonDefaults.itemShape(index = i, count = options.size),
                colors = SegmentedButtonDefaults.colors(
                    inactiveContainerColor = DelernenColors.Chip,
                    activeContainerColor = DelernenColors.AccentBg
                )
            ) {
                Text(opt, fontSize = 13.sp)
            }
        }
    }
}

/** 朗读按钮：TTS 德语不可用时静默禁用（不高亮、不崩溃）。 */
@Composable
fun TtsIconButton(text: String?, modifier: Modifier = Modifier) {
    val context = LocalContext.current
    val tts = remember { TtsHelper.get(context) }
    val enabled = !text.isNullOrBlank() && tts.germanAvailable
    IconButton(
        onClick = { tts.speak(text.orEmpty()) },
        enabled = enabled,
        modifier = modifier
    ) {
        Icon(
            Icons.Default.VolumeUp,
            contentDescription = "朗读",
            tint = if (enabled) DelernenColors.Accent2 else DelernenColors.Text3
        )
    }
}

/** 小节标题（词表 topic 分组、课程/笔记等级分组等）。 */
@Composable
fun SectionHeader(text: String, modifier: Modifier = Modifier) {
    Text(
        text,
        style = MaterialTheme.typography.labelLarge,
        color = DelernenColors.Accent2,
        modifier = modifier.padding(start = 20.dp, top = 14.dp, bottom = 4.dp)
    )
}

/** 小号统计卡（背单词顶部统计等）。 */
@Composable
fun StatCard(value: Int, label: String, tint: Color = DelernenColors.Accent2, modifier: Modifier = Modifier) {
    Surface(
        color = DelernenColors.BgCard,
        border = BorderStroke(1.dp, DelernenColors.Border),
        shape = MaterialTheme.shapes.medium,
        modifier = modifier
    ) {
        Row(
            modifier = Modifier.padding(vertical = 10.dp, horizontal = 8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                "$value",
                style = MaterialTheme.typography.titleMedium,
                color = tint
            )
            Spacer(Modifier.width(6.dp))
            Text(
                label,
                style = MaterialTheme.typography.labelSmall,
                color = DelernenColors.Text3
            )
        }
    }
}

/** 词性小芯片。 */
@Composable
fun PosChip(text: String) {
    if (text.isBlank()) return
    Surface(
        color = DelernenColors.Chip,
        shape = MaterialTheme.shapes.small
    ) {
        Text(
            text,
            fontSize = 10.sp,
            color = DelernenColors.Text3,
            modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
        )
    }
}

/** 与网站卡片一致的深色卡片容器；传 onClick 时整卡可点。 */
@Composable
fun CardSurface(
    modifier: Modifier = Modifier,
    onClick: (() -> Unit)? = null,
    content: @Composable () -> Unit
) {
    Surface(
        color = DelernenColors.BgCard,
        border = BorderStroke(1.dp, DelernenColors.Border2),
        shape = MaterialTheme.shapes.medium,
        modifier = modifier.clickable(enabled = onClick != null, onClick = onClick ?: {})
    ) {
        content()
    }
}
