package com.wdjiangdev.delernen.ui.weg

import android.content.ActivityNotFoundException
import android.content.Context
import android.content.Intent
import android.net.Uri
import androidx.compose.foundation.BorderStroke
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
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateMapOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.produceState
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import com.wdjiangdev.delernen.data.DataRepo
import com.wdjiangdev.delernen.data.WegLesson
import com.wdjiangdev.delernen.data.WegProgress
import com.wdjiangdev.delernen.ui.components.CardSurface
import com.wdjiangdev.delernen.ui.components.PosChip
import com.wdjiangdev.delernen.ui.components.SectionHeader
import com.wdjiangdev.delernen.ui.components.TtsIconButton
import com.wdjiangdev.delernen.ui.theme.DelernenColors
import com.wdjiangdev.delernen.util.TtsHelper
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

/**
 * 加速课课详情（路由 weg/{level}/{num}），与网页端课页同结构：
 * 目标 → 视频（跳 YouTube 打开，App 本身不联网）→ 核心句型（可朗读/连读）→
 * 对话（可朗读/连读）→ 语法卡（纯文本）→ 核心词（可朗读）→ 自测（点选判分）→
 * 口语任务 → 标记学完（WegProgress 持久化）。
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun WegLessonScreen(level: String, num: Int, onBack: () -> Unit) {
    val context = LocalContext.current
    val tts = remember { TtsHelper.get(context) }
    DisposableEffect(Unit) { onDispose { tts.stop() } }

    val lesson by produceState<WegLesson?>(null, level, num) {
        value = withContext(Dispatchers.Default) { DataRepo.wegLesson(level, num) }
    }
    var done by remember(level, num) { mutableStateOf(WegProgress.isDone(level, num)) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(lesson?.let { "第 ${it.num} 课 · ${it.thema}" } ?: "加速课") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "返回")
                    }
                }
            )
        }
    ) { padding ->
        val les = lesson
        if (les == null) {
            Box(Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                Text("未找到这一课", color = DelernenColors.Text3)
            }
        } else {
            Column(
                Modifier
                    .padding(padding)
                    .fillMaxSize()
                    .verticalScroll(rememberScrollState())
            ) {
                Header(les, done)
                CandoSection(les)
                VideoSection(les, context)
                SpeakListSection(
                    title = "💬 核心句型（${les.phrases.size} 句）",
                    lines = les.phrases,
                    tts = tts
                )
                DialogueSection(les, tts)
                GrammarSection(les)
                WordsSection(les)
                QuizSection(les)
                SpeakingSection(les)
                Button(
                    onClick = {
                        done = !done
                        WegProgress.setDone(les.level, les.num, done)
                    },
                    colors = ButtonDefaults.buttonColors(
                        containerColor = if (done) DelernenColors.AccentDeep else DelernenColors.AccentBg
                    ),
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp, vertical = 8.dp)
                ) {
                    Text(if (done) "✓ 本课已学完（点此取消）" else "标记本课已学完")
                }
                Spacer(Modifier.height(32.dp))
            }
        }
    }
}

// ---------------------------------------------------------------- 标题区

@Composable
private fun Header(les: WegLesson, done: Boolean) {
    Column(Modifier.padding(horizontal = 16.dp, vertical = 8.dp)) {
        Text(les.zh, style = MaterialTheme.typography.titleLarge, color = DelernenColors.Text)
        Text(
            les.thema,
            style = MaterialTheme.typography.titleMedium,
            color = DelernenColors.Accent2
        )
        Spacer(Modifier.height(6.dp))
        Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
            PosChip(les.level.uppercase())
            PosChip(les.duration)
            PosChip("视频 ${les.folgen.size} 集")
            if (done) PosChip("已学完")
        }
    }
}

// ---------------------------------------------------------------- 目标

@Composable
private fun CandoSection(les: WegLesson) {
    SectionHeader("🎯 学完这课，你能做到")
    CardSurface(Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 4.dp)) {
        Column(Modifier.padding(horizontal = 14.dp, vertical = 10.dp)) {
            les.cando.forEach { c ->
                Text(
                    "• $c",
                    style = MaterialTheme.typography.bodyMedium,
                    color = DelernenColors.Text,
                    modifier = Modifier.padding(vertical = 2.dp)
                )
            }
        }
    }
}

// ---------------------------------------------------------------- 视频（跳 YouTube）

@Composable
private fun VideoSection(les: WegLesson, context: Context) {
    SectionHeader("🎬 视频（${les.folgen.size} 集，点开在 YouTube 播放）")
    Text(
        "视频是 DW 官方 YouTube 源，打开时需要联网；课内文字、发音都离线可用。",
        style = MaterialTheme.typography.bodySmall,
        color = DelernenColors.Text3,
        modifier = Modifier.padding(horizontal = 20.dp, vertical = 2.dp)
    )
    les.folgen.forEach { f ->
        CardSurface(
            modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 4.dp),
            onClick = { openYouTube(context, f.yt) }
        ) {
            Row(
                Modifier.padding(horizontal = 14.dp, vertical = 10.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column(Modifier.weight(1f)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(
                            "Folge ${f.n}",
                            style = MaterialTheme.typography.labelMedium,
                            color = DelernenColors.Accent2
                        )
                        Spacer(Modifier.width(8.dp))
                        Text(
                            f.t,
                            style = MaterialTheme.typography.bodyLarge,
                            color = DelernenColors.Text
                        )
                    }
                    if (f.d.isNotBlank()) {
                        Text(
                            f.d,
                            style = MaterialTheme.typography.bodySmall,
                            color = DelernenColors.Text2
                        )
                    }
                }
                Icon(
                    Icons.Default.PlayArrow,
                    contentDescription = "在 YouTube 播放",
                    tint = DelernenColors.Accent2
                )
            }
        }
    }
}

private fun openYouTube(context: Context, videoId: String) {
    if (videoId.isBlank()) return
    try {
        context.startActivity(
            Intent(Intent.ACTION_VIEW, Uri.parse("https://www.youtube.com/watch?v=$videoId"))
        )
    } catch (_: ActivityNotFoundException) {
        // 没有浏览器/YouTube 可处理：静默忽略
    }
}

// ---------------------------------------------------------------- 可朗读句列（句型/对话共用行样式）

@Composable
private fun SpeakListSection(title: String, lines: List<Pair<String, String>>, tts: TtsHelper) {
    SectionHeader(title)
    ReadAllRow(lines.map { it.first }, tts)
    lines.forEach { (de, zh) ->
        SpeakRow(de, zh) { tts.speak(de) }
    }
}

@Composable
private fun DialogueSection(les: WegLesson, tts: TtsHelper) {
    SectionHeader("🗣 跟读对话")
    ReadAllRow(les.dialogue.map { it.second }, tts)
    les.dialogue.forEach { (who, line) ->
        Row(
            Modifier
                .fillMaxWidth()
                .clickable { tts.speak(line) }
                .padding(horizontal = 16.dp, vertical = 6.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column(Modifier.weight(1f)) {
                Text(
                    who,
                    style = MaterialTheme.typography.labelMedium,
                    color = DelernenColors.Accent2
                )
                Text(line, style = MaterialTheme.typography.bodyLarge, color = DelernenColors.Text)
            }
            TtsIconButton(line)
        }
    }
    if (les.dialogueNote.isNotBlank()) {
        Text(
            les.dialogueNote,
            style = MaterialTheme.typography.bodySmall,
            color = DelernenColors.Text2,
            modifier = Modifier.padding(horizontal = 20.dp, vertical = 4.dp)
        )
    }
}

@Composable
private fun ReadAllRow(lines: List<String>, tts: TtsHelper) {
    Row(
        Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 2.dp),
        horizontalArrangement = Arrangement.End
    ) {
        TextButton(onClick = { tts.speakAll(lines) }, enabled = tts.germanAvailable) {
            Icon(Icons.Default.PlayArrow, contentDescription = null)
            Spacer(Modifier.width(4.dp))
            Text("整段连读")
        }
        TextButton(onClick = { tts.stop() }) {
            Icon(Icons.Default.Stop, contentDescription = null)
            Spacer(Modifier.width(4.dp))
            Text("停止")
        }
    }
}

@Composable
private fun SpeakRow(de: String, zh: String, onSpeak: () -> Unit) {
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
        TtsIconButton(de)
    }
}

// ---------------------------------------------------------------- 语法

@Composable
private fun GrammarSection(les: WegLesson) {
    SectionHeader("📐 语法一页讲透")
    les.grammar.forEach { g ->
        CardSurface(Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 4.dp)) {
            Column(Modifier.padding(horizontal = 14.dp, vertical = 10.dp)) {
                if (g.title.isNotBlank()) {
                    Text(
                        g.title,
                        style = MaterialTheme.typography.labelLarge,
                        color = DelernenColors.Accent2,
                        modifier = Modifier.padding(bottom = 6.dp)
                    )
                }
                Text(
                    g.text,
                    style = MaterialTheme.typography.bodyMedium,
                    color = DelernenColors.Text
                )
            }
        }
    }
}

// ---------------------------------------------------------------- 核心词

@Composable
private fun WordsSection(les: WegLesson) {
    SectionHeader("🔤 核心词（${les.words.size} 个）")
    les.words.forEach { w ->
        Row(
            Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp, vertical = 5.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column(Modifier.weight(1f)) {
                Text(w.de, style = MaterialTheme.typography.bodyLarge, color = DelernenColors.Text)
                if (w.en.isNotBlank()) {
                    Text(
                        w.en,
                        style = MaterialTheme.typography.bodySmall,
                        color = DelernenColors.Text3
                    )
                }
            }
            if (w.zh.isNotBlank()) {
                Text(
                    w.zh,
                    style = MaterialTheme.typography.bodyMedium,
                    color = DelernenColors.Text2,
                    modifier = Modifier.padding(end = 4.dp)
                )
            }
            TtsIconButton(w.de)
        }
    }
}

// ---------------------------------------------------------------- 自测

@Composable
private fun QuizSection(les: WegLesson) {
    SectionHeader("✍️ 自测（${les.quiz.size} 题）")
    val answers = remember(les.level, les.num) { mutableStateMapOf<Int, Int>() }
    val correct = les.quiz.indices.count { answers[it] == les.quiz[it].a }
    val allDone = answers.size == les.quiz.size

    les.quiz.forEachIndexed { qi, q ->
        Column(Modifier.padding(horizontal = 16.dp, vertical = 6.dp)) {
            Text(
                q.q,
                style = MaterialTheme.typography.bodyMedium,
                color = DelernenColors.Text,
                modifier = Modifier.padding(bottom = 6.dp)
            )
            q.opts.forEachIndexed { oi, opt ->
                val chosen = answers[qi]
                val answered = chosen != null
                val isAnswer = oi == q.a
                val border = when {
                    answered && isAnswer -> DelernenColors.Green
                    answered && chosen == oi -> DelernenColors.Red
                    else -> DelernenColors.Border2
                }
                val fg = when {
                    answered && isAnswer -> DelernenColors.Green
                    answered && chosen == oi -> DelernenColors.Red
                    else -> DelernenColors.Text
                }
                Surface(
                    color = DelernenColors.BgCard,
                    border = BorderStroke(1.dp, border),
                    shape = MaterialTheme.shapes.small,
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 3.dp)
                        .clickable(enabled = !answered) { answers[qi] = oi }
                ) {
                    Text(
                        opt + when {
                            answered && isAnswer -> " ✓"
                            answered && chosen == oi -> " ✗"
                            else -> ""
                        },
                        style = MaterialTheme.typography.bodyMedium,
                        color = fg,
                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 9.dp)
                    )
                }
            }
        }
    }
    if (allDone) {
        Row(
            Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp, vertical = 6.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                "得分 $correct / ${les.quiz.size}" + if (correct == les.quiz.size) "，全对，过关！" else "，错题回上面几步再看一遍。",
                style = MaterialTheme.typography.bodyMedium,
                color = if (correct == les.quiz.size) DelernenColors.Green else DelernenColors.Orange,
                modifier = Modifier.weight(1f)
            )
            OutlinedButton(onClick = { answers.clear() }) { Text("重做") }
        }
    }
}

// ---------------------------------------------------------------- 口语任务

@Composable
private fun SpeakingSection(les: WegLesson) {
    val sp = les.speaking
    if (sp.intro.isBlank() && sp.lines.isEmpty()) return
    SectionHeader("🎙 口语任务（过关标准）")
    CardSurface(Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 4.dp)) {
        Column(Modifier.padding(horizontal = 14.dp, vertical = 10.dp)) {
            if (sp.intro.isNotBlank()) {
                Text(sp.intro, style = MaterialTheme.typography.bodyMedium, color = DelernenColors.Text)
            }
            sp.lines.forEach { ln ->
                Text(
                    "• $ln",
                    style = MaterialTheme.typography.bodyMedium,
                    color = DelernenColors.Text,
                    modifier = Modifier.padding(vertical = 2.dp)
                )
            }
            if (sp.outro.isNotBlank()) {
                Text(
                    sp.outro,
                    style = MaterialTheme.typography.bodySmall,
                    color = DelernenColors.Text2,
                    modifier = Modifier.padding(top = 6.dp)
                )
            }
        }
    }
}
