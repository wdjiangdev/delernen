package com.astemo.delernen.ui.course

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.Stop
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.produceState
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import com.astemo.delernen.data.DataRepo
import com.astemo.delernen.data.KursCard
import com.astemo.delernen.ui.components.PosChip
import com.astemo.delernen.ui.components.SectionHeader
import com.astemo.delernen.ui.components.TtsIconButton
import com.astemo.delernen.ui.theme.DelernenColors
import com.astemo.delernen.util.TtsHelper
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

/**
 * 课程详情 / 跟读页（路由 course/{num}）。
 * kurs 卡的跟读句子字段是 examples（[德语, 中文] 对，94 张卡全带）：
 * 标题区 + 讲解全文 + 逐句跟读（点句子或喇叭读单句德语）+ 整页连读 + 附表。
 * 若将来出现只有 explain、没有 examples 的卡，降级为讲解 + 标题朗读按钮。
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CourseDetailScreen(num: String, onBack: () -> Unit) {
    val context = LocalContext.current
    val tts = remember { TtsHelper.get(context) }
    // 离开课程详情时停止连读，避免在后台一直念
    DisposableEffect(Unit) { onDispose { tts.stop() } }

    val card by produceState<KursCard?>(null, key1 = num) {
        value = withContext(Dispatchers.Default) { DataRepo.kursByNum(num) }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(card?.title ?: "课程 $num") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "返回")
                    }
                }
            )
        }
    ) { padding ->
        val c = card
        if (c == null) {
            Box(Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                Text("未找到课程 $num", color = DelernenColors.Text3)
            }
        } else {
            Column(
                Modifier
                    .padding(padding)
                    .fillMaxSize()
                    .verticalScroll(rememberScrollState())
            ) {
                CourseHeader(c)
                SectionHeader("讲解")
                Text(
                    c.explain,
                    style = MaterialTheme.typography.bodyMedium,
                    color = DelernenColors.Text,
                    modifier = Modifier.padding(horizontal = 20.dp)
                )
                if (c.examples.isEmpty()) {
                    // 降级分支：无句子字段的卡只给标题朗读
                    Row(Modifier.padding(horizontal = 16.dp, vertical = 4.dp)) {
                        TtsIconButton(c.title)
                    }
                } else {
                    FollowReadSection(c, tts)
                }
                TableSection(c.table)
                Spacer(Modifier.height(32.dp))
            }
        }
    }
}

// ---------------------------------------------------------------- 标题区

@Composable
private fun CourseHeader(c: KursCard) {
    Column(Modifier.padding(horizontal = 16.dp, vertical = 8.dp)) {
        Text(
            c.title,
            style = MaterialTheme.typography.titleLarge,
            color = DelernenColors.Text
        )
        if (c.titleDe.isNotBlank()) {
            Text(
                c.titleDe,
                style = MaterialTheme.typography.titleMedium,
                color = DelernenColors.Accent2
            )
        }
        Spacer(Modifier.height(6.dp))
        Row(verticalAlignment = Alignment.CenterVertically) {
            PosChip(c.num)
            if (c.level.isNotBlank()) {
                PosChip(c.level)
            }
            PosChip(catLabel(c.cat))
        }
    }
}

// ---------------------------------------------------------------- 跟读区（examples = 德语 + 中文对）

@Composable
private fun FollowReadSection(c: KursCard, tts: TtsHelper) {
    SectionHeader("跟读（${c.examples.size} 句，点句子或喇叭朗读德语）")
    Row(
        Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 4.dp),
        horizontalArrangement = Arrangement.End
    ) {
        TextButton(
            onClick = { tts.speakAll(c.examples.map { sayLine(it.first) }) },
            enabled = tts.germanAvailable
        ) {
            Icon(Icons.Default.PlayArrow, contentDescription = null)
            Spacer(Modifier.width(4.dp))
            Text("整页连读")
        }
        TextButton(onClick = { tts.stop() }) {
            Icon(Icons.Default.Stop, contentDescription = null)
            Spacer(Modifier.width(4.dp))
            Text("停止")
        }
    }
    c.examples.forEach { (de, zh) ->
        ExampleRow(de, zh, onSpeak = { tts.speak(sayLine(de)) })
    }
}

@Composable
private fun ExampleRow(de: String, zh: String, onSpeak: () -> Unit) {
    Row(
        Modifier
            .fillMaxWidth()
            .clickable(onClick = onSpeak)
            .padding(horizontal = 16.dp, vertical = 6.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Column(Modifier.weight(1f)) {
            Text(de, style = MaterialTheme.typography.bodyLarge, color = DelernenColors.Text)
            if (zh.isNotBlank()) {
                Text(zh, style = MaterialTheme.typography.bodySmall, color = DelernenColors.Text2)
            }
        }
        // 朗读传入清洗后的德语（去掉音标注释），展示仍用原文
        TtsIconButton(sayLine(de))
    }
}

/**
 * 朗读预处理：语音卡（M01-01 / M01-02~04）的例句形如 "da [da:] —— dann [dan]"，
 * 去掉 [音标] 注释并按 —— 拆成词序列朗读；普通句子原样返回。
 */
private fun sayLine(de: String): String =
    de.split("——")
        .map { Regex("\\s*\\[[^\\]]*\\]\\s*").replace(it, " ").trim() }
        .filter { it.isNotBlank() }
        .joinToString(", ")

// ---------------------------------------------------------------- 附表

@Composable
private fun TableSection(table: List<List<String>>) {
    if (table.isEmpty()) return
    SectionHeader("表格")
    Column(
        Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp)
    ) {
        table.forEachIndexed { i, row ->
            if (i > 0) {
                HorizontalDivider(color = DelernenColors.Border2, thickness = 0.5.dp)
            }
            TableRow(row, isHeader = i == 0)
        }
    }
}

@Composable
private fun TableRow(cells: List<String>, isHeader: Boolean) {
    Row(
        Modifier
            .fillMaxWidth()
            .padding(horizontal = 4.dp, vertical = 6.dp)
    ) {
        cells.forEach { cell ->
            Text(
                cell,
                style = if (isHeader) MaterialTheme.typography.labelSmall
                else MaterialTheme.typography.bodySmall,
                color = if (isHeader) DelernenColors.Accent2 else DelernenColors.Text2,
                modifier = Modifier.weight(1f)
            )
        }
    }
}
