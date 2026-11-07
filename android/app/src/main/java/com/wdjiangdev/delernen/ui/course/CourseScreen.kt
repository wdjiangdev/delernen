package com.wdjiangdev.delernen.ui.course

import android.net.Uri
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
import com.wdjiangdev.delernen.data.DataRepo
import com.wdjiangdev.delernen.data.KursCard
import com.wdjiangdev.delernen.ui.components.CardSurface
import com.wdjiangdev.delernen.ui.components.PosChip
import com.wdjiangdev.delernen.ui.components.SectionHeader
import com.wdjiangdev.delernen.ui.theme.DelernenColors
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

/**
 * 页签 4：课程列表。kurs.json 94 张语法卡按等级分组（A1→C1 保持教学顺序），
 * 每行显示 num + 中文标题 + 德语标题 + 类别芯片，点行导航到 course/{num}。
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CourseScreen(navController: NavHostController) {
    val cards by produceState<List<KursCard>>(emptyList()) {
        value = withContext(Dispatchers.Default) { DataRepo.kursCards }
    }
    val grouped = remember(cards) { groupByLevel(cards) }

    Scaffold(topBar = { TopAppBar(title = { Text("课程") }) }) { padding ->
        if (cards.isEmpty()) {
            Box(Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                Text("暂无课程数据", color = DelernenColors.Text3)
            }
        } else {
            LazyColumn(
                contentPadding = PaddingValues(bottom = 24.dp),
                modifier = Modifier.fillMaxSize().padding(padding)
            ) {
                grouped.forEach { (level, list) ->
                    item { SectionHeader("$level（${list.size}）") }
                    items(list, key = { it.num }) { c ->
                        CourseRow(c) {
                            navController.navigate("course/${Uri.encode(c.num)}")
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun CourseRow(c: KursCard, onClick: () -> Unit) {
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
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(
                        c.num,
                        style = MaterialTheme.typography.labelMedium,
                        color = DelernenColors.Accent2
                    )
                    Spacer(Modifier.width(8.dp))
                    Text(
                        c.title,
                        style = MaterialTheme.typography.bodyLarge,
                        color = DelernenColors.Text
                    )
                }
                if (c.titleDe.isNotBlank()) {
                    Text(
                        c.titleDe,
                        style = MaterialTheme.typography.bodySmall,
                        color = DelernenColors.Text2
                    )
                }
            }
            PosChip(catLabel(c.cat))
        }
    }
}

/** 按等级分组并保持 A1→C1 顺序；未知等级追加在末尾按字母排。 */
private fun groupByLevel(cards: List<KursCard>): List<Pair<String, List<KursCard>>> {
    val byLevel = cards.groupBy { it.level }
    val known = LEVEL_ORDER.mapNotNull { lvl ->
        byLevel[lvl]?.takeIf { it.isNotEmpty() }?.let { lvl to it }
    }
    val rest = byLevel.filterKeys { it !in LEVEL_ORDER }.toList().sortedBy { it.first }
    return known + rest
}

private val LEVEL_ORDER = listOf("A1", "A2", "B1", "B2", "C1")

/** cat 是拼音键，展示成中文标签（与网站 kurs 页一致）；未知值原样显示。同包共享。 */
internal fun catLabel(cat: String): String = when (cat) {
    "yuyin" -> "语音"
    "mingci" -> "名词"
    "dongci" -> "动词"
    "xingrong" -> "形容词"
    "vokabel" -> "词汇"
    "pron" -> "代词"
    "jufa" -> "句式"
    "gejie" -> "介词"
    "ge" -> "格"
    "yufa" -> "语法"
    "congju" -> "从句"
    "tempus" -> "时态"
    "qita" -> "其他"
    "" -> ""
    else -> cat
}
