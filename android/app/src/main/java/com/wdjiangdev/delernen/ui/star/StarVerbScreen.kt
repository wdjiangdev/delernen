package com.wdjiangdev.delernen.ui.star

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Canvas
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.produceState
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.onSizeChanged
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.wdjiangdev.delernen.data.VerbGroup
import com.wdjiangdev.delernen.data.VerbMember
import com.wdjiangdev.delernen.data.DataRepo
import com.wdjiangdev.delernen.ui.components.SectionHeader
import com.wdjiangdev.delernen.ui.components.TtsIconButton
import com.wdjiangdev.delernen.ui.theme.DelernenColors
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlin.math.cos
import kotlin.math.min
import kotlin.math.sin

/**
 * 星图详情：Compose Canvas 放射图 —— 中心词干圆，成员按角度环绕、连线；
 * 点成员弹详情（verb/def/zh/past/pp + 朗读），点中心弹词干详情（stemDef + stemZh）。
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun StarVerbScreen(range: String, stem: String, onBack: () -> Unit) {
    val groups by produceState<List<VerbGroup>>(emptyList(), key1 = range) {
        value = withContext(Dispatchers.Default) { DataRepo.verbGroups(range) }
    }
    val group = groups.firstOrNull { it.stem == stem }

    var member by remember { mutableStateOf<VerbMember?>(null) }
    var showStem by remember { mutableStateOf(false) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(stem) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "返回")
                    }
                }
            )
        }
    ) { padding ->
        if (group == null) {
            Box(Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                Text("未找到词干 $stem", color = DelernenColors.Text3)
            }
        } else {
            val g = group!!
            Column(
                Modifier
                    .padding(padding)
                    .fillMaxSize()
                    .verticalScroll(rememberScrollState())
            ) {
                Column(Modifier.padding(horizontal = 16.dp, vertical = 8.dp)) {
                    if (g.stemDef.isNotBlank()) {
                        Text(g.stemDef, style = MaterialTheme.typography.bodySmall, color = DelernenColors.Text3)
                    }
                    if (g.stemZh.isNotBlank()) {
                        Text(g.stemZh, style = MaterialTheme.typography.bodySmall, color = DelernenColors.Text2)
                    }
                }

                StarGraph(
                    group = g,
                    onMember = { member = it },
                    onStem = { showStem = true }
                )

                SectionHeader("成员（${g.members.size}）—— 点任意成员看详情")
                g.members.forEach { m ->
                    MemberRow(m, onClick = { member = m })
                }
                Spacer(Modifier.height(32.dp))
            }
        }
    }

    member?.let { m ->
        AlertDialog(
            onDismissRequest = { member = null },
            title = { Text(m.verb) },
            text = {
                Column {
                    m.prefix?.let {
                        Text(
                            "前缀 $it-",
                            style = MaterialTheme.typography.labelMedium,
                            color = DelernenColors.Purple
                        )
                    }
                    if (m.def.isNotBlank()) {
                        Text(m.def, style = MaterialTheme.typography.bodySmall, color = DelernenColors.Text3)
                    }
                    if (m.zh.isNotBlank()) {
                        Text(m.zh, style = MaterialTheme.typography.bodyMedium, color = DelernenColors.Text)
                    }
                    if (m.past.isNotEmpty() || m.pp.isNotEmpty()) {
                        Text(
                            "过去式 ${m.past} · 过去分词 ${m.pp}",
                            style = MaterialTheme.typography.bodySmall,
                            color = DelernenColors.Accent2
                        )
                    }
                    if (m.level.isNotBlank()) {
                        Text("等级 ${m.level}", style = MaterialTheme.typography.bodySmall, color = DelernenColors.Text3)
                    }
                    Text("本组出现 ${m.count} 次", style = MaterialTheme.typography.bodySmall, color = DelernenColors.Text3)
                }
            },
            confirmButton = {
                Row(Modifier.fillMaxWidth(), horizontalArrangement = androidx.compose.foundation.layout.Arrangement.End) {
                    TtsIconButton(m.verb)
                    TextButton(onClick = { member = null }) { Text("关闭") }
                }
            }
        )
    }

    if (showStem && group != null) {
        val g = group!!
        AlertDialog(
            onDismissRequest = { showStem = false },
            title = { Text(g.stem) },
            text = {
                Column {
                    if (g.stemDef.isNotBlank()) {
                        Text(g.stemDef, style = MaterialTheme.typography.bodySmall, color = DelernenColors.Text3)
                    }
                    if (g.stemZh.isNotBlank()) {
                        Text(g.stemZh, style = MaterialTheme.typography.bodyMedium, color = DelernenColors.Text)
                    }
                    Text(
                        "成员 ${g.members.size} 个",
                        style = MaterialTheme.typography.bodySmall,
                        color = DelernenColors.Text3
                    )
                }
            },
            confirmButton = {
                Row(Modifier.fillMaxWidth(), horizontalArrangement = androidx.compose.foundation.layout.Arrangement.End) {
                    TtsIconButton(g.stem)
                    TextButton(onClick = { showStem = false }) { Text("关闭") }
                }
            }
        )
    }
}

// ---------------------------------------------------------------- 放射图

@Composable
private fun StarGraph(
    group: VerbGroup,
    onMember: (VerbMember) -> Unit,
    onStem: () -> Unit
) {
    val n = group.members.size
    var boxSize by remember { mutableStateOf(Size.Zero) }

    // 成员按角度环绕（同一公式用于绘制与点击命中检测）
    val positions: List<Offset> = remember(n, boxSize.width, boxSize.height) {
        if (boxSize.width == 0f || boxSize.height == 0f || n == 0) {
            emptyList()
        } else {
            val cx = boxSize.width / 2f
            val cy = boxSize.height / 2f
            val r = min(cx, cy) - 24.dp.toPx()
            (0 until n).map { i ->
                val a = 2 * Math.PI * i / n - Math.PI / 2
                Offset(
                    (cx + r * cos(a)).toFloat(),
                    (cy + r * 0.82f * sin(a)).toFloat()
                )
            }
        }
    }

    Box(
        Modifier
            .fillMaxWidth()
            .height(300.dp)
            .padding(horizontal = 8.dp)
            .onSizeChanged { boxSize = it }
            .pointerInput(n, positions) {
                detectTapGestures { off ->
                    var bestIdx = -1
                    var bestD = Float.MAX_VALUE
                    positions.forEachIndexed { i, p ->
                        val d = (p - off).getDistance()
                        if (d < bestD) {
                            bestD = d
                            bestIdx = i
                        }
                    }
                    if (bestIdx >= 0 && bestD <= 34.dp.toPx()) {
                        onMember(group.members[bestIdx])
                    }
                }
            }
    ) {
        Canvas(Modifier.fillMaxSize()) {
            val cx = size.width / 2f
            val cy = size.height / 2f
            val r = min(cx, cy) - 24.dp.toPx()

            // 星轨
            drawCircle(
                color = DelernenColors.Accent.copy(alpha = 0.18f),
                radius = r,
                style = Stroke(width = 1.dp.toPx())
            )
            drawCircle(
                color = DelernenColors.Accent.copy(alpha = 0.08f),
                radius = r * 0.55f
            )

            // 连线 + 成员节点
            positions.forEach { p ->
                drawLine(
                    color = DelernenColors.Accent.copy(alpha = 0.45f),
                    start = Offset(cx, cy),
                    end = p,
                    strokeWidth = 1.dp.toPx()
                )
                drawCircle(color = DelernenColors.Accent2, radius = 6.dp.toPx(), center = p)
            }

            // 中心词干圆
            drawCircle(color = DelernenColors.Accent2.copy(alpha = 0.22f), radius = 34.dp.toPx(), center = Offset(cx, cy))
            drawCircle(color = DelernenColors.Accent2, radius = 26.dp.toPx(), center = Offset(cx, cy))

            // 标签
            drawIntoCanvas { c ->
                val paint = android.graphics.Paint().apply {
                    isAntiAlias = true
                    textAlign = android.graphics.Paint.Align.CENTER
                }
                if (n <= 14) {
                    paint.textSize = 11.dp.toPx()
                    paint.color = DelernenColors.Text.toArgb()
                    positions.forEachIndexed { i, p ->
                        val a = 2 * Math.PI * i / n - Math.PI / 2
                        val lx = p.x + (18.dp.toPx() * cos(a)).toFloat()
                        val ly = p.y + (18.dp.toPx() * sin(a)).toFloat() + 4.dp.toPx()
                        c.nativeCanvas.drawText(group.members[i].verb, lx, ly, paint)
                    }
                } else {
                    // 成员过多时画编号，避免重叠（下方列表可按编号对照）
                    paint.textSize = 10.dp.toPx()
                    paint.color = DelernenColors.Text3.toArgb()
                    positions.forEachIndexed { i, p ->
                        c.nativeCanvas.drawText("#${i + 1}", p.x, p.y - 12.dp.toPx(), paint)
                    }
                }
            }
        }

        // 中心词干（可点 → 词干详情）
        Box(
            Modifier
                .align(Alignment.Center)
                .size(52.dp)
                .clip(CircleShape)
                .background(DelernenColors.Accent2)
                .clickable { onStem() },
            contentAlignment = Alignment.Center
        ) {
            Text(
                group.stem,
                color = DelernenColors.Bg,
                fontWeight = FontWeight.Bold,
                fontSize = 12.sp,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
        }
    }
}

// ---------------------------------------------------------------- 成员行

@Composable
private fun MemberRow(m: VerbMember, onClick: () -> Unit) {
    Row(
        Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick)
            .padding(horizontal = 20.dp, vertical = 10.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Column(Modifier.weight(1f)) {
            Text(
                m.verb,
                style = MaterialTheme.typography.bodyLarge,
                color = DelernenColors.Text
            )
            if (m.def.isNotBlank()) {
                Text(m.def, style = MaterialTheme.typography.bodySmall, color = DelernenColors.Text3)
            }
        }
        Text(
            m.zh,
            style = MaterialTheme.typography.bodySmall,
            color = DelernenColors.Text2
        )
    }
}
