package com.wdjiangdev.delernen.ui.star
import com.wdjiangdev.delernen.ui.components.ThemeToggleButton

import android.net.Uri
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
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.produceState
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.navigation.NavHostController
import com.wdjiangdev.delernen.data.DataRepo
import com.wdjiangdev.delernen.data.GrammarGroup
import com.wdjiangdev.delernen.data.VerbGroup
import com.wdjiangdev.delernen.data.WordFamily
import com.wdjiangdev.delernen.ui.components.CardSurface
import com.wdjiangdev.delernen.ui.components.PosChip
import com.wdjiangdev.delernen.ui.components.SectionHeader
import com.wdjiangdev.delernen.ui.components.SegmentedRow
import com.wdjiangdev.delernen.ui.theme.DelernenColors
import com.wdjiangdev.delernen.util.DeText
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

/** 页签 1：星图。顶部 A1-A2 / A1-B2，内部 动词 / 词族 / 语法 三段（与网站结构一致）。 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun StarMapScreen(navController: NavHostController) {
    var range by rememberSaveable { mutableStateOf("a1a2") }
    var segment by rememberSaveable { mutableStateOf("动词") }

    val verbGroups by produceState<List<VerbGroup>>(emptyList(), key1 = range) {
        value = withContext(Dispatchers.Default) { DataRepo.verbGroups(range) }
    }
    val families by produceState<List<WordFamily>>(emptyList(), key1 = range) {
        value = withContext(Dispatchers.Default) { DataRepo.wordFamilies(range) }
    }
    val grammar by produceState<List<GrammarGroup>>(emptyList(), key1 = range) {
        value = withContext(Dispatchers.Default) { DataRepo.grammarGroups(range) }
    }

    Scaffold(topBar = { TopAppBar(title = { Text("星图") }, actions = { ThemeToggleButton() }) }) { padding ->
        Column(Modifier.padding(padding).fillMaxSize()) {
            SegmentedRow(
                options = listOf("A1-A2", "A1-B2"),
                selected = if (range == "a1a2") "A1-A2" else "A1-B2"
            ) { range = if (it == "A1-A2") "a1a2" else "a1b2" }
            SegmentedRow(
                options = listOf("动词", "词族", "语法"),
                selected = segment
            ) { segment = it }

            when (segment) {
                "动词" -> VerbGroupList(verbGroups, range, navController, padding)
                "词族" -> FamilyList(families, padding)
                else -> GrammarList(grammar, padding)
            }
        }
    }
}

// ---------------------------------------------------------------- 动词分组

@Composable
private fun VerbGroupList(
    groups: List<VerbGroup>,
    range: String,
    navController: NavHostController,
    padding: PaddingValues
) {
    if (groups.isEmpty()) return
    LazyColumn(
        contentPadding = PaddingValues(bottom = 24.dp),
        modifier = Modifier.fillMaxSize()
    ) {
        items(groups, key = { "${range}:${it.stem}" }) { g ->
            CardSurface(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 4.dp),
                onClick = {
                    navController.navigate("star/verb/$range/${Uri.encode(g.stem)}")
                }
            ) {
                Column(Modifier.padding(14.dp)) {
                    Row(verticalAlignment = androidx.compose.ui.Alignment.CenterVertically) {
                        Text(
                            g.stem,
                            style = MaterialTheme.typography.titleMedium,
                            color = DelernenColors.Accent2
                        )
                        Spacer(Modifier.weight(1f))
                        Text(
                            "${g.members.size} 个成员",
                            style = MaterialTheme.typography.labelSmall,
                            color = DelernenColors.Text3
                        )
                    }
                    if (g.stemDef.isNotBlank()) {
                        Text(g.stemDef, style = MaterialTheme.typography.bodySmall, color = DelernenColors.Text3)
                    }
                    if (g.stemZh.isNotBlank()) {
                        Text(g.stemZh, style = MaterialTheme.typography.bodySmall, color = DelernenColors.Text2)
                    }
                }
            }
        }
    }
}

// ---------------------------------------------------------------- 词族

@Composable
private fun FamilyList(families: List<WordFamily>, padding: PaddingValues) {
    LazyColumn(
        contentPadding = PaddingValues(bottom = 24.dp),
        modifier = Modifier.fillMaxSize()
    ) {
        items(families, key = { it.root }) { f ->
            CardSurface(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 4.dp)
            ) {
                Column(Modifier.padding(14.dp)) {
                    Row(verticalAlignment = androidx.compose.ui.Alignment.CenterVertically) {
                        Text(
                            f.root,
                            style = MaterialTheme.typography.titleMedium,
                            color = DelernenColors.Accent2
                        )
                        Spacer(Modifier.weight(1f))
                        Text(
                            "${f.members.size} 个成员",
                            style = MaterialTheme.typography.labelSmall,
                            color = DelernenColors.Text3
                        )
                    }
                    f.members.forEach { m ->
                        Column(Modifier.padding(top = 8.dp)) {
                            Row(verticalAlignment = androidx.compose.ui.Alignment.CenterVertically) {
                                Text(
                                    DeText.annotatedDe(m.word),
                                    style = MaterialTheme.typography.bodyLarge,
                                    color = DelernenColors.Text,
                                    modifier = Modifier.weight(1f)
                                )
                                PosChip(m.pos)
                            }
                            if (m.pos == "v" && (m.past.isNotEmpty() || m.pp.isNotEmpty())) {
                                Text(
                                    "${m.past} · ${m.pp}",
                                    style = MaterialTheme.typography.bodySmall,
                                    color = DelernenColors.Accent2
                                )
                            }
                            if (m.zh.isNotBlank()) {
                                Text(m.zh, style = MaterialTheme.typography.bodySmall, color = DelernenColors.Text2)
                            }
                            if (m.plural.isNotBlank()) {
                                Text(
                                    "复数 ${m.plural}",
                                    style = MaterialTheme.typography.bodySmall,
                                    color = DelernenColors.Text3
                                )
                            }
                        }
                        if (m !== f.members.last()) {
                            HorizontalDivider(color = DelernenColors.Border2, thickness = 0.5.dp)
                        }
                    }
                }
            }
        }
    }
}

// ---------------------------------------------------------------- 语法

@Composable
private fun GrammarList(groups: List<GrammarGroup>, padding: PaddingValues) {
    LazyColumn(
        contentPadding = PaddingValues(bottom = 24.dp),
        modifier = Modifier.fillMaxSize()
    ) {
        items(groups, key = { it.id }) { g ->
            CardSurface(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 4.dp)
            ) {
                Column(Modifier.padding(14.dp)) {
                    Text(
                        g.title,
                        style = MaterialTheme.typography.titleMedium,
                        color = DelernenColors.Accent2
                    )
                    if (g.titleZh.isNotBlank()) {
                        Text(g.titleZh, style = MaterialTheme.typography.bodySmall, color = DelernenColors.Text2)
                    }
                    if (g.learnTitle.isNotBlank()) {
                        Text(
                            "关联：${g.learnTitle}",
                            style = MaterialTheme.typography.labelSmall,
                            color = DelernenColors.Text3
                        )
                    }
                    g.members.forEach { m ->
                        Column(Modifier.padding(top = 8.dp)) {
                            Row {
                                Text(
                                    m.word,
                                    style = MaterialTheme.typography.bodyLarge,
                                    color = DelernenColors.Text,
                                    modifier = Modifier.weight(1f)
                                )
                                Text(
                                    m.zh,
                                    style = MaterialTheme.typography.bodySmall,
                                    color = DelernenColors.Text2
                                )
                            }
                            if (m.ex.isNotBlank()) {
                                Text(
                                    m.ex,
                                    style = MaterialTheme.typography.bodySmall,
                                    color = DelernenColors.Text3
                                )
                            }
                        }
                    }
                }
            }
        }
    }
}
