package com.wdjiangdev.delernen.ui.notes

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.produceState
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.navigation.NavHostController
import com.wdjiangdev.delernen.data.AliceNote
import com.wdjiangdev.delernen.data.DataRepo
import com.wdjiangdev.delernen.ui.components.CardSurface
import com.wdjiangdev.delernen.ui.components.SectionHeader
import com.wdjiangdev.delernen.ui.theme.DelernenColors
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

/**
 * 页签 5：笔记列表。alice.json 17 篇按等级（A2/B1/C1）分组，显示标题；
 * 点行导航到 note/{数组下标}——分组展示时保留 alice.json 原数组下标。
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun NotesScreen(navController: NavHostController) {
    val notes by produceState<List<AliceNote>>(emptyList()) {
        value = withContext(Dispatchers.Default) { DataRepo.aliceNotes }
    }
    val grouped = remember(notes) { groupByLevel(notes) }

    Scaffold(topBar = { TopAppBar(title = { Text("笔记") }) }) { padding ->
        if (notes.isEmpty()) {
            Box(Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                Text("暂无笔记数据", color = DelernenColors.Text3)
            }
        } else {
            LazyColumn(
                contentPadding = PaddingValues(bottom = 24.dp),
                modifier = Modifier.fillMaxSize().padding(padding)
            ) {
                grouped.forEach { (level, list) ->
                    item { SectionHeader("$level（${list.size}）") }
                    items(list, key = { "note-${it.first}" }) { (idx, n) ->
                        NoteRow(idx, n) {
                            navController.navigate("note/$idx")
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun NoteRow(index: Int, n: AliceNote, onClick: () -> Unit) {
    CardSurface(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 4.dp),
        onClick = onClick
    ) {
        Row(
            Modifier
                .padding(horizontal = 14.dp, vertical = 10.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column(Modifier.weight(1f)) {
                Text(
                    n.title,
                    style = MaterialTheme.typography.bodyLarge,
                    color = DelernenColors.Text
                )
                Text(
                    "${n.blocks.size} 段 · 原文下标 #$index",
                    style = MaterialTheme.typography.bodySmall,
                    color = DelernenColors.Text3
                )
            }
            Spacer(Modifier.width(8.dp))
            Text(
                n.level,
                style = MaterialTheme.typography.labelMedium,
                color = DelernenColors.Accent2
            )
        }
    }
}

/** 按等级分组并保持 A1→C1 顺序；保留每篇在 alice.json 中的原数组下标。 */
private fun groupByLevel(notes: List<AliceNote>): List<Pair<String, List<Pair<Int, AliceNote>>>> {
    val byLevel = notes.mapIndexed { i, n -> i to n }.groupBy({ it.second.level }, { it })
    val known = LEVEL_ORDER.mapNotNull { lvl ->
        byLevel[lvl]?.takeIf { it.isNotEmpty() }?.let { lvl to it }
    }
    val rest = byLevel.filterKeys { it !in LEVEL_ORDER }.toList().sortedBy { it.first }
    return known + rest
}

private val LEVEL_ORDER = listOf("A1", "A2", "B1", "B2", "C1")
