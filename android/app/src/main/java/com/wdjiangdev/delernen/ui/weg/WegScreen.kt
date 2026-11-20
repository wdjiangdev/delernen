package com.wdjiangdev.delernen.ui.weg
import com.wdjiangdev.delernen.ui.components.ThemeToggleButton

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
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.produceState
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.navigation.NavHostController
import androidx.navigation.compose.currentBackStackEntryAsState
import com.wdjiangdev.delernen.data.DataRepo
import com.wdjiangdev.delernen.data.WegLesson
import com.wdjiangdev.delernen.data.WegProgress
import com.wdjiangdev.delernen.ui.components.CardSurface
import com.wdjiangdev.delernen.ui.components.PosChip
import com.wdjiangdev.delernen.ui.components.SegmentedRow
import com.wdjiangdev.delernen.ui.theme.DelernenColors
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

/**
 * 加速课页签：Nicos Weg 56 课（A1 18 / A2 19 / B1 19），与网页端 nicos/weg 同内容。
 * 分级切换 + 每课一行（主题/中文/集数/学完标记），点行进 weg/{level}/{num}。
 * 「已学完」读 WegProgress（SharedPreferences）；用当前导航条目做 remember 键，
 * 从课详情返回时条目变化会触发重读，标记即时刷新。
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun WegScreen(navController: NavHostController) {
    var level by rememberSaveable { mutableStateOf("a1") }
    val lessons by produceState<List<WegLesson>>(emptyList()) {
        value = withContext(Dispatchers.Default) { DataRepo.wegLessons }
    }
    val entry by navController.currentBackStackEntryAsState()
    val doneSet = remember(entry, lessons) {
        lessons.filter { WegProgress.isDone(it.level, it.num) }
            .map { it.level to it.num }.toSet()
    }
    val levelLessons = remember(lessons, level) { lessons.filter { it.level == level } }
    val doneCount = levelLessons.count { (it.level to it.num) in doneSet }

    Scaffold(topBar = { TopAppBar(title = { Text("加速课 · Nicos Weg") }, actions = { ThemeToggleButton() }) }) { padding ->
        Column(Modifier.fillMaxSize().padding(padding)) {
            SegmentedRow(
                options = listOf("A1", "A2", "B1"),
                selected = level.uppercase(),
                onSelect = { level = it.lowercase() }
            )
            Text(
                "${level.uppercase()} 共 ${levelLessons.size} 课 · 已学完 $doneCount 课",
                style = MaterialTheme.typography.bodySmall,
                color = DelernenColors.Text3,
                modifier = Modifier.padding(horizontal = 20.dp, vertical = 4.dp)
            )
            if (lessons.isEmpty()) {
                Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Text("暂无课程数据", color = DelernenColors.Text3)
                }
            } else {
                LazyColumn(
                    contentPadding = PaddingValues(bottom = 24.dp),
                    modifier = Modifier.fillMaxSize()
                ) {
                    items(levelLessons, key = { it.num }) { les ->
                        WegRow(les, done = (les.level to les.num) in doneSet) {
                            navController.navigate("weg/${les.level}/${les.num}")
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun WegRow(les: WegLesson, done: Boolean, onClick: () -> Unit) {
    CardSurface(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 4.dp),
        onClick = onClick
    ) {
        Row(
            Modifier.padding(horizontal = 14.dp, vertical = 10.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column(Modifier.weight(1f)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(
                        "第 ${les.num} 课",
                        style = MaterialTheme.typography.labelMedium,
                        color = DelernenColors.Accent2
                    )
                    Spacer(Modifier.width(8.dp))
                    Text(
                        les.thema,
                        style = MaterialTheme.typography.bodyLarge,
                        color = DelernenColors.Text
                    )
                }
                Text(
                    "${les.zh} · ${les.duration}",
                    style = MaterialTheme.typography.bodySmall,
                    color = DelernenColors.Text2
                )
            }
            if (done) {
                Text(
                    "✓ 已学完",
                    style = MaterialTheme.typography.labelMedium,
                    color = DelernenColors.Green
                )
            } else {
                PosChip("${les.folgen.size} 集")
            }
        }
    }
}
