package com.astemo.delernen.ui.memorize

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ColumnScope
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.RowScope
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Checkbox
import androidx.compose.material3.CheckboxDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ExposedDropdownMenuBox
import androidx.compose.material3.ExposedDropdownMenuDefaults
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import com.astemo.delernen.data.SrsCard
import com.astemo.delernen.data.srs.MemorizeViewModel
import com.astemo.delernen.data.srs.SrsRules
import com.astemo.delernen.ui.components.CardSurface
import com.astemo.delernen.ui.components.PosChip
import com.astemo.delernen.ui.components.StatCard
import com.astemo.delernen.ui.components.TtsIconButton
import com.astemo.delernen.ui.theme.DelernenColors
import com.astemo.delernen.util.DeText
import com.astemo.delernen.util.TtsHelper

/** 页签 3：背单词。SRS 规则与网站 memorize 完全一致（见 SrsRules / MemorizeViewModel）。 */
@Composable
fun MemorizeScreen() {
    val vm: MemorizeViewModel = viewModel()
    val mode by vm.mode.collectAsStateWithLifecycle()
    when (mode) {
        "study" -> StudyView(vm)
        "done" -> DoneView(vm)
        else -> SetupView(vm)
    }
}

// ---------------------------------------------------------------- 设置视图

@Composable
private fun SetupView(vm: MemorizeViewModel) {
    val stats by vm.stats.collectAsStateWithLifecycle()
    val selected by vm.selectedSources.collectAsStateWithLifecycle()
    val newPerDay by vm.newPerDay.collectAsStateWithLifecycle()
    val order by vm.order.collectAsStateWithLifecycle()
    val notice by vm.notice.collectAsStateWithLifecycle()
    val sourceDefs by vm.sourceDefs.collectAsStateWithLifecycle()
    val context = LocalContext.current
    val tts = remember { TtsHelper.get(context) }

    Column(
        Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(16.dp)
    ) {
        Text(
            "艾宾浩斯间隔重复：记得 → 间隔拉长（20分钟 → 1天 → 3天 → 7天 → 15天 → 30天 → 60天）；" +
                    "忘了 → 打回重学。每天先复习到期的，再学新词。进度保存在本机 Room。",
            style = MaterialTheme.typography.bodySmall,
            color = DelernenColors.Text3
        )

        Spacer(Modifier.height(12.dp))
        if (sourceDefs.isEmpty()) {
            LinearProgressIndicator(
                modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp),
                color = DelernenColors.Accent2,
                trackColor = DelernenColors.Chip
            )
        }
        sourceDefs.forEach { def ->
            SourceRow(
                name = def.name,
                count = def.count,
                checked = def.id in selected,
                onToggle = { vm.toggleSource(def.id) }
            )
        }

        Spacer(Modifier.height(8.dp))
        IntDropdown(
            label = "每天新词",
            options = listOf(10, 20, 30, 50),
            selected = newPerDay,
            onSelect = vm::setNewPerDay,
            format = { "$it 个" }
        )
        Spacer(Modifier.height(8.dp))
        StringDropdown(
            label = "出题顺序",
            options = listOf("mix", "split", "list"),
            labels = mapOf(
                "mix" to "全部乱序（复习和新词混在一起）",
                "split" to "先复习、再新词（各自乱序）",
                "list" to "按词表顺序"
            ),
            selected = order,
            onSelect = vm::setOrder
        )

        Spacer(Modifier.height(12.dp))
        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            StatCard(stats.total, "总数", DelernenColors.Accent2, Modifier.weight(1f))
            StatCard(stats.due, "待复习", DelernenColors.Orange, Modifier.weight(1f))
        }
        Spacer(Modifier.height(8.dp))
        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            StatCard(stats.learnedToday, "今日已学", DelernenColors.Accent2, Modifier.weight(1f))
            StatCard(stats.mastered, "已掌握", DelernenColors.Green, Modifier.weight(1f))
        }

        Spacer(Modifier.height(16.dp))
        Button(
            onClick = { vm.startSession() },
            enabled = selected.isNotEmpty(),
            modifier = Modifier.fillMaxWidth().height(52.dp),
            colors = ButtonDefaults.buttonColors(containerColor = DelernenColors.Accent)
        ) {
            Text(if (stats.due > 0) "开始复习（${stats.due} 个到期）" else "开始背单词")
        }

        if (tts.ready && tts.needsVoiceData) {
            Spacer(Modifier.height(8.dp))
            TextButton(onClick = { tts.installVoiceData(context) }) {
                Text("🔈 未安装德语语音数据，朗读不可用 —— 点此安装", color = DelernenColors.Orange)
            }
        }

        if (!notice.isNullOrEmpty()) {
            Spacer(Modifier.height(8.dp))
            Text(notice!!, style = MaterialTheme.typography.bodySmall, color = DelernenColors.Orange)
        }

        Spacer(Modifier.height(16.dp))
        Text(
            "💡 三档自评：忘了 = 完全想不起来，打回重学；模糊 = 犹豫/猜对，维持当前进度再巩固一次；" +
                    "记得 = 干脆答对，进入下一间隔。诚实打分效果最好。",
            style = MaterialTheme.typography.bodySmall,
            color = DelernenColors.Text3
        )
    }
}

@Composable
private fun SourceRow(name: String, count: Int, checked: Boolean, onToggle: () -> Unit) {
    Row(
        Modifier
            .fillMaxWidth()
            .clickable(onClick = onToggle)
            .padding(vertical = 4.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Checkbox(
            checked = checked,
            onCheckedChange = { onToggle() },
            colors = CheckboxDefaults.colors(
                checkedColor = DelernenColors.Accent2,
                uncheckedColor = DelernenColors.Border
            )
        )
        Column(Modifier.weight(1f)) {
            Text(name, style = MaterialTheme.typography.bodyLarge, color = DelernenColors.Text)
            Text(
                "艾宾浩斯间隔重复 · 进度本机保存",
                style = MaterialTheme.typography.labelSmall,
                color = DelernenColors.Text3
            )
        }
        Text(
            "$count 词",
            style = MaterialTheme.typography.labelMedium,
            color = DelernenColors.Accent2,
            fontWeight = FontWeight.Bold
        )
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun IntDropdown(
    label: String,
    options: List<Int>,
    selected: Int,
    onSelect: (Int) -> Unit,
    format: (Int) -> String
) {
    var expanded by remember { mutableStateOf(false) }
    ExposedDropdownMenuBox(expanded = expanded, onExpandedChange = { expanded = !expanded }) {
        OutlinedTextField(
            value = format(selected),
            onValueChange = {},
            readOnly = true,
            label = { Text(label, color = DelernenColors.Text3) },
            trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) },
            modifier = Modifier.menuAnchor().fillMaxWidth(),
            colors = OutlinedTextFieldDefaults.colors(
                focusedBorderColor = DelernenColors.Accent,
                unfocusedBorderColor = DelernenColors.Border,
                focusedTextColor = DelernenColors.Text,
                unfocusedTextColor = DelernenColors.Text
            )
        )
        ExposedDropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
            options.forEach { v ->
                androidx.compose.material3.DropdownMenuItem(
                    text = { Text(format(v)) },
                    onClick = {
                        onSelect(v)
                        expanded = false
                    }
                )
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun StringDropdown(
    label: String,
    options: List<String>,
    labels: Map<String, String>,
    selected: String,
    onSelect: (String) -> Unit
) {
    var expanded by remember { mutableStateOf(false) }
    ExposedDropdownMenuBox(expanded = expanded, onExpandedChange = { expanded = !expanded }) {
        OutlinedTextField(
            value = labels[selected] ?: selected,
            onValueChange = {},
            readOnly = true,
            label = { Text(label, color = DelernenColors.Text3) },
            trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) },
            modifier = Modifier.menuAnchor().fillMaxWidth(),
            colors = OutlinedTextFieldDefaults.colors(
                focusedBorderColor = DelernenColors.Accent,
                unfocusedBorderColor = DelernenColors.Border,
                focusedTextColor = DelernenColors.Text,
                unfocusedTextColor = DelernenColors.Text
            )
        )
        ExposedDropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
            options.forEach { v ->
                androidx.compose.material3.DropdownMenuItem(
                    text = { Text(labels[v] ?: v) },
                    onClick = {
                        onSelect(v)
                        expanded = false
                    }
                )
            }
        }
    }
}

// ---------------------------------------------------------------- 学习视图

@Composable
private fun StudyView(vm: MemorizeViewModel) {
    val queue by vm.queue.collectAsStateWithLifecycle()
    val index by vm.index.collectAsStateWithLifecycle()
    val flipped by vm.flipped.collectAsStateWithLifecycle()
    val canUndo by vm.canUndo.collectAsStateWithLifecycle()
    val busy by vm.busy.collectAsStateWithLifecycle()
    val card = vm.current

    Column(Modifier.fillMaxSize().padding(16.dp)) {
        val progress = if (queue.isEmpty()) 0f else index.toFloat() / queue.size
        LinearProgressIndicator(
            progress = { progress },
            modifier = Modifier.fillMaxWidth(),
            color = DelernenColors.Accent2,
            trackColor = DelernenColors.Chip
        )
        Text(
            "${minOf(index + 1, queue.size)} / ${queue.size}",
            style = MaterialTheme.typography.labelSmall,
            color = DelernenColors.Text3,
            modifier = Modifier.align(Alignment.CenterHorizontally).padding(vertical = 6.dp)
        )

        if (card != null) {
            StudyCard(card, flipped, onFlip = { vm.flip() })
        }

        Spacer(Modifier.weight(1f))

        if (flipped) {
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                GradeButton("忘了", DelernenColors.Red, enabled = !busy, onClick = { vm.grade(SrsRules.GRADE_FORGOT) })
                GradeButton("模糊", DelernenColors.Orange, enabled = !busy, onClick = { vm.grade(SrsRules.GRADE_FUZZY) })
                GradeButton("记得", DelernenColors.Green, enabled = !busy, onClick = { vm.grade(SrsRules.GRADE_GOT) })
            }
        }

        Row(
            Modifier.fillMaxWidth().padding(top = 12.dp),
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            TextButton(onClick = { vm.undo() }, enabled = canUndo && !busy) {
                Text("↩ 撤销上次打分", color = DelernenColors.Text3)
            }
            TextButton(onClick = { vm.quitSession() }) {
                Text("结束本次", color = DelernenColors.Text3)
            }
        }
    }
}

@Composable
private fun ColumnScope.StudyCard(card: SrsCard, flipped: Boolean, onFlip: () -> Unit) {
    CardSurface(
        modifier = Modifier
            .fillMaxWidth()
            .weight(1f, fill = false)
            .heightIn(min = 280.dp),
        onClick = onFlip
    ) {
        if (!flipped) {
            // 正面：de + tip
            Column(
                Modifier.fillMaxSize().padding(16.dp),
                verticalArrangement = Arrangement.Center,
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Text(
                    DeText.annotatedDe(card.de),
                    style = MaterialTheme.typography.displaySmall,
                    color = DelernenColors.Text
                )
                if (card.tip.isNotBlank()) {
                    Text(
                        card.tip,
                        style = MaterialTheme.typography.bodySmall,
                        color = DelernenColors.Orange,
                        modifier = Modifier.padding(top = 10.dp)
                    )
                }
                TtsIconButton(DeText.sayText(card.de), Modifier.padding(top = 16.dp))
                Text(
                    "点击卡片翻面",
                    style = MaterialTheme.typography.labelSmall,
                    color = DelernenColors.Text3,
                    modifier = Modifier.padding(top = 12.dp)
                )
            }
        } else {
            // 翻面：en / zh / past / pp
            Column(
                Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(16.dp),
                verticalArrangement = Arrangement.Center,
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Text(
                    DeText.annotatedDe(card.de),
                    style = MaterialTheme.typography.headlineSmall,
                    color = DelernenColors.Text
                )
                if (card.past.isNotEmpty() || card.pp.isNotEmpty()) {
                    Text(
                        "${card.past} · ${card.pp}",
                        style = MaterialTheme.typography.titleSmall,
                        color = DelernenColors.Accent2,
                        modifier = Modifier.padding(top = 6.dp)
                    )
                }
                if (card.en.isNotBlank()) {
                    Text(
                        card.en,
                        style = MaterialTheme.typography.titleMedium,
                        color = DelernenColors.Green,
                        fontWeight = FontWeight.Bold,
                        modifier = Modifier.padding(top = 10.dp)
                    )
                }
                if (card.zh.isNotBlank()) {
                    Text(
                        card.zh,
                        style = MaterialTheme.typography.titleSmall,
                        color = DelernenColors.Text,
                        modifier = Modifier.padding(top = 4.dp)
                    )
                }
                if (card.tip.isNotBlank()) {
                    Surface(
                        color = DelernenColors.Chip,
                        shape = MaterialTheme.shapes.small,
                        modifier = Modifier.padding(top = 10.dp)
                    ) {
                        Text(
                            card.tip,
                            style = MaterialTheme.typography.bodySmall,
                            color = DelernenColors.Orange,
                            modifier = Modifier.padding(horizontal = 10.dp, vertical = 6.dp)
                        )
                    }
                }
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier.padding(top = 8.dp)
                ) {
                    PosChip(posLabel(card.pos))
                    TtsIconButton(DeText.sayText(card.de))
                }
            }
        }
    }
}

@Composable
private fun RowScope.GradeButton(label: String, tint: Color, enabled: Boolean, onClick: () -> Unit) {
    Surface(
        onClick = onClick,
        enabled = enabled,
        shape = MaterialTheme.shapes.medium,
        border = BorderStroke(1.dp, tint),
        color = tint.copy(alpha = 0.15f),
        modifier = Modifier.weight(1f).height(52.dp)
    ) {
        Box(contentAlignment = Alignment.Center) {
            Text(label, fontWeight = FontWeight.Bold, color = tint)
        }
    }
}

// ---------------------------------------------------------------- 完成视图

@Composable
private fun DoneView(vm: MemorizeViewModel) {
    val summary by vm.summary.collectAsStateWithLifecycle()
    Column(
        Modifier
            .fillMaxSize()
            .padding(24.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text("🎉", fontSize = 48.sp)
        Text(
            "本轮完成！",
            style = MaterialTheme.typography.headlineSmall,
            color = DelernenColors.Text
        )
        Spacer(Modifier.height(16.dp))
        SummaryRow("本轮完成", summary.done)
        SummaryRow("其中复习", summary.dueReviewed)
        SummaryRow("其中新学", summary.freshLearned)
        SummaryRow("没记住", summary.forgot)
        SummaryRow("未来24小时到期", summary.dueTomorrow)
        Spacer(Modifier.height(20.dp))
        Button(
            onClick = { vm.backToSetup() },
            modifier = Modifier.fillMaxWidth().height(52.dp),
            colors = ButtonDefaults.buttonColors(containerColor = DelernenColors.Accent)
        ) {
            Text("返回")
        }
    }
}

@Composable
private fun SummaryRow(label: String, value: Int) {
    Row(
        Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp),
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        Text(label, style = MaterialTheme.typography.bodyMedium, color = DelernenColors.Text3)
        Text("$value", style = MaterialTheme.typography.titleMedium, color = DelernenColors.Text)
    }
}

private fun posLabel(pos: String): String = when (pos) {
    "noun" -> "名词"
    "verb" -> "动词"
    "adj" -> "形容词"
    "adv" -> "副词"
    "" -> ""
    else -> pos
}
