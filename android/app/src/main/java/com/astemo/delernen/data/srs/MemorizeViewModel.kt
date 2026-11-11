package com.astemo.delernen.data.srs

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.astemo.delernen.data.DataRepo
import com.astemo.delernen.data.SrsCard
import com.astemo.delernen.data.SrsSourceDef
import com.astemo.delernen.data.db.SrsWord
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

/**
 * 背单词页签。SRS 规则与网站 memorize/index.html 完全一致（见 SrsRules）：
 * 记得 → box+1 进入下一间隔（封顶 Box 7）；忘了 → box=0、10 分钟后重来；
 * 模糊 → box 维持、按当前间隔再巩固。每天先复习到期的，再学新词（受每日新词上限约束）。
 */
class MemorizeViewModel(app: Application) : AndroidViewModel(app) {

    data class Stats(val total: Int, val due: Int, val learnedToday: Int, val mastered: Int)

    data class SessionSummary(
        val done: Int,
        val dueReviewed: Int,
        val freshLearned: Int,
        val forgot: Int,
        val dueTomorrow: Int
    )

    private data class UndoEntry(
        val source: String,
        val key: String,
        val prev: SrsWord?,
        val newCount: Int,
        val index: Int,
        val done: Int,
        val forgot: Int
    )

    private val repo = SrsRepository(app)

    /** 五个可多选数据源（与网站一致）。在 Dispatchers.Default 上加载，避免主线程解析 JSON。 */
    private val _sourceDefs = MutableStateFlow<List<SrsSourceDef>>(emptyList())
    val sourceDefs: StateFlow<List<SrsSourceDef>> = _sourceDefs.asStateFlow()

    /** 正在处理一次打分/撤销：期间打分按钮禁用，重复点击直接忽略。 */
    private val _busy = MutableStateFlow(false)
    val busy: StateFlow<Boolean> = _busy.asStateFlow()

    private val _selectedSources = MutableStateFlow<List<String>>(emptyList())
    val selectedSources: StateFlow<List<String>> = _selectedSources.asStateFlow()

    private val _newPerDay = MutableStateFlow(20)
    val newPerDay: StateFlow<Int> = _newPerDay.asStateFlow()

    private val _order = MutableStateFlow("mix")
    val order: StateFlow<String> = _order.asStateFlow()

    private val _stats = MutableStateFlow(Stats(0, 0, 0, 0))
    val stats: StateFlow<Stats> = _stats.asStateFlow()

    private val _mode = MutableStateFlow("setup") // setup | study | done
    val mode: StateFlow<String> = _mode.asStateFlow()

    private val _queue = MutableStateFlow<List<SrsCard>>(emptyList())
    val queue: StateFlow<List<SrsCard>> = _queue.asStateFlow()

    private val _index = MutableStateFlow(0)
    val index: StateFlow<Int> = _index.asStateFlow()

    val current: SrsCard? get() = _queue.value.getOrNull(_index.value)

    private val _flipped = MutableStateFlow(false)
    val flipped: StateFlow<Boolean> = _flipped.asStateFlow()

    private val _canUndo = MutableStateFlow(false)
    val canUndo: StateFlow<Boolean> = _canUndo.asStateFlow()

    private val _summary = MutableStateFlow(SessionSummary(0, 0, 0, 0, 0))
    val summary: StateFlow<SessionSummary> = _summary.asStateFlow()

    private val _notice = MutableStateFlow<String?>(null)
    val notice: StateFlow<String?> = _notice.asStateFlow()

    private val undoStack = ArrayDeque<UndoEntry>()

    private var sessDue = 0
    private var sessFresh = 0
    private var sessDone = 0
    private var sessForgot = 0

    init {
        viewModelScope.launch {
            withContext(Dispatchers.Default) {
                _sourceDefs.value = DataRepo.srsSources
            }
            withContext(Dispatchers.IO) {
                // v1→v2：旧的 de 键迁到 k||de（只跑一次）
                runCatching { repo.migrateKeys(DataRepo.srsSourceIds) { DataRepo.srsWords(it) } }
                val stored = repo.selectedSources
                val known = DataRepo.srsSourceIds
                _selectedSources.value =
                    if (stored.isEmpty()) listOf("nicos_a1") else stored.filter { it in known }
                _newPerDay.value = repo.newPerDay
                _order.value = repo.order
            }
            refreshStats()
        }
    }

    // ---------------- 设置 ----------------

    fun toggleSource(id: String) {
        val cur = _selectedSources.value.toMutableList()
        if (cur.remove(id)) {
            // 移除
        } else {
            cur.add(id)
        }
        _selectedSources.value = cur
        viewModelScope.launch {
            withContext(Dispatchers.IO) { repo.selectedSources = cur }
            refreshStats()
        }
    }

    fun setNewPerDay(v: Int) {
        _newPerDay.value = v
        viewModelScope.launch { repo.newPerDay = v }
    }

    fun setOrder(v: String) {
        _order.value = v
        viewModelScope.launch { repo.order = v }
    }

    fun clearNotice() {
        _notice.value = null
    }

    // ---------------- 统计 ----------------

    /** 只统计当前数据里存在的键（孤儿行不计入「待复习」，与出题逻辑一致）。 */
    private suspend fun validRows(sel: List<String>): List<SrsWord> =
        withContext(Dispatchers.IO) {
            val rows = repo.words(sel)
            val valid = sel.associateWith { src -> DataRepo.srsWords(src).mapTo(HashSet()) { it.key } }
            rows.filter { valid[it.source]?.contains(it.key) == true }
        }

    private suspend fun refreshStats() {
        val sel = _selectedSources.value
        if (sel.isEmpty()) {
            _stats.value = Stats(0, 0, 0, 0)
            return
        }
        val now = System.currentTimeMillis()
        val total = withContext(Dispatchers.Default) { sel.sumOf { DataRepo.srsWords(it).size } }
        val rows = validRows(sel)
        val due = rows.count { it.dueAt <= now }
        val mastered = rows.count { it.box >= SrsRules.MASTER_BOX }
        val learnedToday = withContext(Dispatchers.IO) { repo.newCountToday }
        _stats.value = Stats(total, due, learnedToday, mastered)
    }

    // ---------------- 会话 ----------------

    fun startSession() {
        viewModelScope.launch {
            val sel = _selectedSources.value
            if (sel.isEmpty()) {
                _notice.value = "请至少选择一个单词范围"
                return@launch
            }
            val now = System.currentTimeMillis()
            val dbRows = withContext(Dispatchers.IO) { repo.words(sel) }
            val newCountToday = withContext(Dispatchers.IO) { repo.newCountToday }
            val order = _order.value
            val newPerDay = _newPerDay.value

            // 构建队列放在 Default 上（遍历数千词条）
            val built = withContext(Dispatchers.Default) {
                val dbMap = dbRows.associateBy { "${it.source}|${it.key}" }
                val dueList = mutableListOf<Pair<SrsCard, Long>>()
                val freshList = mutableListOf<SrsCard>()
                val seen = HashSet<String>()
                for (src in sel) {
                    for (w in DataRepo.srsWords(src)) {
                        val k = "$src|${w.key}"
                        // 同一个键只出一次（与网站 store.words[k] 一致）
                        if (!seen.add(k)) continue
                        val st = dbMap[k]
                        if (st == null) {
                            freshList += w
                        } else if (st.dueAt <= now) {
                            dueList += w to st.dueAt
                        }
                    }
                }
                val allowed = maxOf(0, newPerDay - newCountToday)
                // 与网站一致：list 按词表顺序取前 N；mix/split 从全部新词里随机抽 N 个
                val fresh = if (order == "list") {
                    freshList.take(allowed)
                } else {
                    freshList.shuffled().take(allowed)
                }

                val queue = when (order) {
                    "split" -> dueList.map { it.first }.shuffled() + fresh
                    "list" -> dueList.map { it.first } + fresh
                    else -> (dueList.map { it.first } + fresh).shuffled()
                }
                Triple(queue, dueList.size, fresh.size)
            }
            val (queue, dueCount, freshCount) = built

            sessDue = dueCount
            sessFresh = freshCount
            sessDone = 0
            sessForgot = 0
            undoStack.clear()
            _canUndo.value = false

            if (queue.isEmpty()) {
                _notice.value = "🎉 太棒了！所选范围内今日没有到期的单词。"
            } else {
                _queue.value = queue
                _index.value = 0
                _flipped.value = false
                _mode.value = "study"
                _notice.value = null
            }
        }
    }

    fun flip() {
        _flipped.value = !_flipped.value
    }

    /**
     * g: 0=忘了 1=模糊 2=记得（与网站 grade() 一致）。
     * 防连点：[busy] 为 true 时直接忽略（主线程上同步判断+置位，协程跑完才放开），
     * 因此每次有效打分只压一条撤销记录、index 只前进一次。
     */
    fun grade(g: Int) {
        if (_busy.value || _mode.value != "study") return
        val card = current ?: return
        val idx = _index.value
        _busy.value = true
        viewModelScope.launch {
            try {
                val now = System.currentTimeMillis()
                val prev = withContext(Dispatchers.IO) { repo.word(card.source, card.key) }
                val newCount = withContext(Dispatchers.IO) { repo.newCountToday }
                undoStack.addLast(
                    UndoEntry(
                        source = card.source,
                        key = card.key,
                        prev = prev,
                        newCount = newCount,
                        index = idx,
                        done = sessDone,
                        forgot = sessForgot
                    )
                )
                _canUndo.value = true

                val res = SrsRules.grade(prev?.box ?: 0, now, g)
                withContext(Dispatchers.IO) {
                    repo.upsert(
                        SrsWord(
                            source = card.source,
                            key = card.key,
                            box = res.box,
                            dueAt = res.dueAt,
                            lastSeen = now,
                            lastGrade = g,
                            createdAt = prev?.createdAt ?: now
                        )
                    )
                    if (prev == null) repo.newCountToday = newCount + 1
                }
                if (g == SrsRules.GRADE_FORGOT) sessForgot++
                sessDone++

                if (idx + 1 >= _queue.value.size) {
                    finishSession()
                } else {
                    _index.value = idx + 1
                    _flipped.value = false
                }
                refreshStats()
            } finally {
                _busy.value = false
            }
        }
    }

    private suspend fun finishSession() {
        val now = System.currentTimeMillis()
        val dueTomorrow = withContext(Dispatchers.IO) {
            val until = now + 24 * 3600 * 1000L
            validRows(_selectedSources.value).count { it.dueAt in (now + 1)..until }
        }
        _summary.value = SessionSummary(
            done = sessDone,
            dueReviewed = minOf(sessDone, sessDue),
            freshLearned = maxOf(0, sessDone - minOf(sessDone, sessDue)),
            forgot = sessForgot,
            dueTomorrow = dueTomorrow
        )
        _mode.value = "done"
    }

    fun undo() {
        if (_busy.value) return
        val u = undoStack.removeLastOrNull() ?: return
        _busy.value = true
        viewModelScope.launch {
            try {
                withContext(Dispatchers.IO) {
                    if (u.prev == null) repo.delete(u.source, u.key) else repo.upsert(u.prev)
                    repo.newCountToday = u.newCount
                }
                _index.value = u.index
                sessDone = u.done
                sessForgot = u.forgot
                _flipped.value = false
                _mode.value = "study"
                _canUndo.value = undoStack.isNotEmpty()
                refreshStats()
            } finally {
                _busy.value = false
            }
        }
    }

    fun quitSession() {
        _mode.value = "setup"
        viewModelScope.launch { refreshStats() }
    }

    fun backToSetup() {
        _mode.value = "setup"
        viewModelScope.launch { refreshStats() }
    }
}
