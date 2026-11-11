package com.astemo.delernen.ui.vocab

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.produceState
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.astemo.delernen.data.DataRepo
import com.astemo.delernen.data.NicosWord
import com.astemo.delernen.ui.components.CardSurface
import com.astemo.delernen.ui.components.PosChip
import com.astemo.delernen.ui.components.SectionHeader
import com.astemo.delernen.ui.components.SegmentedRow
import com.astemo.delernen.ui.components.TtsIconButton
import com.astemo.delernen.ui.theme.DelernenColors
import com.astemo.delernen.util.DeText
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.delay
import kotlinx.coroutines.withContext

/** 页签 2：词表。三册切换 A1/A2/B1；topic 分组 + 顶部搜索（de/zh/en 子串）。 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun VocabScreen() {
    var level by rememberSaveable { mutableStateOf("a1") }
    var query by rememberSaveable { mutableStateOf("") }
    var selected by remember { mutableStateOf<NicosWord?>(null) }

    // 每册只算一次检索串（de/zh/en 小写 + ä/ö/ü/ß 折叠），不再每次按键对每条做 3 次 lowercase()
    val indexed by produceState<List<Pair<NicosWord, String>>>(emptyList(), key1 = level) {
        value = withContext(Dispatchers.Default) {
            DataRepo.nicos(level).map { it to foldSearch("${it.de}\u0000${it.zh}\u0000${it.en}") }
        }
    }
    val words: List<NicosWord> = remember(indexed) { indexed.map { it.first } }

    // 过滤放到 Default 上，并做 150ms 去抖：连续输入时只算最后一次
    val filtered by produceState<List<NicosWord>>(words, indexed, query) {
        val q = foldSearch(query.trim())
        if (q.isEmpty()) {
            value = words
        } else {
            delay(150)
            value = withContext(Dispatchers.Default) {
                indexed.filter { it.second.contains(q) }.map { it.first }
            }
        }
    }
    val grouped: Map<String, List<NicosWord>> = remember(filtered) { filtered.groupBy { it.topic } }

    Scaffold(topBar = { TopAppBar(title = { Text("词表") }) }) { padding ->
        Column(Modifier.padding(padding).fillMaxSize()) {
            SegmentedRow(
                options = listOf("A1", "A2", "B1"),
                selected = level.uppercase()
            ) { level = it.lowercase() }

            OutlinedTextField(
                value = query,
                onValueChange = { query = it },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 6.dp),
                singleLine = true,
                placeholder = { Text("搜索 de / zh / en", color = DelernenColors.Text3) },
                leadingIcon = {
                    Icon(Icons.Default.Search, contentDescription = null, tint = DelernenColors.Text3)
                },
                trailingIcon = {
                    if (query.isNotEmpty()) {
                        IconButton(onClick = { query = "" }) {
                            Icon(Icons.Default.Close, contentDescription = "清空", tint = DelernenColors.Text3)
                        }
                    }
                },
                colors = OutlinedTextFieldDefaults.colors(
                    focusedBorderColor = DelernenColors.Accent,
                    unfocusedBorderColor = DelernenColors.Border,
                    focusedTextColor = DelernenColors.Text,
                    unfocusedTextColor = DelernenColors.Text,
                    cursorColor = DelernenColors.Accent2,
                    focusedPlaceholderColor = DelernenColors.Text3,
                    unfocusedPlaceholderColor = DelernenColors.Text3
                )
            )

            if (filtered.isEmpty()) {
                Column(
                    Modifier.fillMaxSize().padding(24.dp),
                    verticalArrangement = Arrangement.Center,
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Text(
                        if (words.isEmpty()) "本册暂无数据" else "无匹配单词",
                        color = DelernenColors.Text3
                    )
                }
            } else {
                LazyColumn(
                    contentPadding = PaddingValues(bottom = 24.dp),
                    modifier = Modifier.fillMaxSize()
                ) {
                    grouped.forEach { (topic, ws) ->
                        item(contentType = "header") { SectionHeader("$topic（${ws.size}）") }
                        items(ws, key = { w -> "${w.de}|${w.topic}" }, contentType = { "word" }) { w ->
                            WordRow(w, onClick = { selected = w })
                        }
                    }
                }
            }
        }
    }

    selected?.let { w ->
        WordDetailDialog(w, onDismiss = { selected = null })
    }
}

@Composable
private fun WordRow(w: NicosWord, onClick: () -> Unit) {
    Row(
        Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick)
            .padding(horizontal = 20.dp, vertical = 10.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Column(Modifier.weight(1f)) {
            Text(
                DeText.annotatedDe(w.de),
                style = MaterialTheme.typography.bodyLarge,
                color = DelernenColors.Text
            )
            if (w.zh.isNotBlank()) {
                Text(w.zh, style = MaterialTheme.typography.bodySmall, color = DelernenColors.Text2)
            }
            if (w.en.isNotBlank()) {
                Text(w.en, style = MaterialTheme.typography.bodySmall, color = DelernenColors.Text3)
            }
        }
        PosChip(posLabel(w.pos))
    }
}

@Composable
private fun WordDetailDialog(w: NicosWord, onDismiss: () -> Unit) {
    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text(DeText.annotatedDe(w.de), style = MaterialTheme.typography.titleLarge) },
        text = {
            Column {
                if (w.en.isNotBlank()) {
                    Text(w.en, style = MaterialTheme.typography.bodyLarge, color = DelernenColors.Green)
                }
                if (w.zh.isNotBlank()) {
                    Text(w.zh, style = MaterialTheme.typography.bodyLarge, color = DelernenColors.Text)
                }
                Spacer(Modifier.height(6.dp))
                Row(verticalAlignment = Alignment.CenterVertically) {
                    PosChip(posLabel(w.pos))
                    if (w.topic.isNotBlank()) {
                        PosChip(w.topic)
                    }
                }
                if (w.pos == "verb" && (w.past.isNotEmpty() || w.pp.isNotEmpty())) {
                    Text(
                        "过去式 ${w.past} · 过去分词 ${w.pp}",
                        style = MaterialTheme.typography.bodyMedium,
                        color = DelernenColors.Accent2
                    )
                }
                if (w.tip.isNotBlank()) {
                    Text(
                        w.tip,
                        style = MaterialTheme.typography.bodySmall,
                        color = DelernenColors.Orange
                    )
                }
            }
        },
        confirmButton = {
            Row {
                TtsIconButton(DeText.sayText(w.de))
                TextButton(onClick = onDismiss) { Text("关闭") }
            }
        }
    )
}

private fun posLabel(pos: String): String = when (pos) {
    "noun" -> "名词"
    "verb" -> "动词"
    "adj" -> "形容词"
    "adv" -> "副词"
    "" -> ""
    else -> pos
}

/** 检索串折叠：小写，ä→ae ö→oe ü→ue ß→ss（输入 strasse 也能搜到 Straße）。 */
private fun foldSearch(s: String): String =
    s.lowercase()
        .replace("ä", "ae")
        .replace("ö", "oe")
        .replace("ü", "ue")
        .replace("ß", "ss")
