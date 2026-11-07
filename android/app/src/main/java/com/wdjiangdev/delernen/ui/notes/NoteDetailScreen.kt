package com.wdjiangdev.delernen.ui.notes

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.produceState
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.wdjiangdev.delernen.data.AliceBlock
import com.wdjiangdev.delernen.data.AliceNote
import com.wdjiangdev.delernen.data.DataRepo
import com.wdjiangdev.delernen.ui.components.CardSurface
import com.wdjiangdev.delernen.ui.theme.DelernenColors
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

/**
 * 笔记详情（路由 note/{index}，index 为 alice.json 数组下标）。
 * blocks 原生渲染：h 标题样式 / p 正文（"---" 渲染为分隔线）/ li 列表项 / vocab 强调卡片。
 * 严禁 WebView——全部用基础 Composable 画出。
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun NoteDetailScreen(index: Int, onBack: () -> Unit) {
    val note by produceState<AliceNote?>(null, key1 = index) {
        value = withContext(Dispatchers.Default) { DataRepo.aliceNotes.getOrNull(index) }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(note?.title ?: "笔记 #$index") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "返回")
                    }
                }
            )
        }
    ) { padding ->
        val n = note
        if (n == null) {
            Box(Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                Text("未找到笔记 #$index", color = DelernenColors.Text3)
            }
        } else {
            LazyColumn(
                contentPadding = PaddingValues(bottom = 24.dp),
                modifier = Modifier.fillMaxSize().padding(padding)
            ) {
                itemsIndexed(n.blocks) { _, b ->
                    BlockView(b)
                }
            }
        }
    }
}

@Composable
private fun BlockView(b: AliceBlock) {
    when (b.type) {
        "h" -> Text(
            b.text,
            style = MaterialTheme.typography.titleSmall,
            color = DelernenColors.Accent2,
            modifier = Modifier.padding(start = 20.dp, top = 18.dp, bottom = 4.dp)
        )
        "li" -> Row(
            Modifier
                .fillMaxWidth()
                .padding(start = 20.dp, top = 3.dp, end = 16.dp, bottom = 3.dp)
        ) {
            Text("• ", style = MaterialTheme.typography.bodyMedium, color = DelernenColors.Accent2)
            Text(
                b.text,
                style = MaterialTheme.typography.bodyMedium,
                color = DelernenColors.Text,
                modifier = Modifier.weight(1f)
            )
        }
        "vocab" -> VocabCard(b)
        else -> { // p 正文
            if (b.text == "---") {
                HorizontalDivider(
                    color = DelernenColors.Border2,
                    thickness = 0.5.dp,
                    modifier = Modifier.padding(horizontal = 20.dp, vertical = 8.dp)
                )
            } else {
                Text(
                    b.text,
                    style = MaterialTheme.typography.bodyMedium,
                    color = DelernenColors.Text,
                    modifier = Modifier.padding(horizontal = 20.dp, vertical = 2.dp)
                )
            }
        }
    }
}

/** vocab 块：德语词条 + 中文释义，卡片强调样式。 */
@Composable
private fun VocabCard(b: AliceBlock) {
    CardSurface(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 4.dp)
    ) {
        Column(Modifier.padding(horizontal = 14.dp, vertical = 10.dp)) {
            Text(
                b.text,
                style = MaterialTheme.typography.bodyLarge,
                color = DelernenColors.Accent2
            )
            if (b.zh.isNotBlank()) {
                Text(
                    b.zh,
                    style = MaterialTheme.typography.bodySmall,
                    color = DelernenColors.Text2
                )
            }
        }
    }
}
