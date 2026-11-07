package com.wdjiangdev.delernen.data.srs

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.wdjiangdev.delernen.data.DataRepo
import com.wdjiangdev.delernen.data.SrsCard
import com.wdjiangdev.delernen.data.SrsSourceDef
import com.wdjiangdev.delernen.data.db.SrsWord
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
        val de: String,
        val prev: SrsWord?,
        val newCount: Int,
        val index: Int,
        val done: Int,
        val forgot: Int
    )

    private val repo = SrsRepository(app)

    /** 五个可多选数据源（与网站一致）。 */
    val sourceDefs: List<SrsSourceDef> = DataRepo.srsSources

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
            val stored = repo.selectedSources
            val known = DataRepo.srsSources.map { it.id }
            _selectedSources.value =
                if (stored.isEmpty()) listOf("nicos_a1") else stored.filter { it in known }
            _newPerDay.value = repo.newPerDay
            _order.value = repo.order
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
            repo.selectedSources = cur
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

    private suspend fun refreshStats() {
        val sel = _selectedSources.value
        if (sel.isEmpty()) {
            _stats.value = Stats(0, 0, 0, 0)
            return
        }
        val now = System.currentTimeMillis()
        val total = DataRepo.srsSources.filter { it.id in sel }.sumOf { it.count }
        val due = withContext(Dispatchers.IO) { repo.countDue(sel, now) }
        val mastered = withContext(Dispatchers.IO) { repo.countMastered(sel) }
        _stats.value = Stats(total, due, repo.newCountToday, mastered)
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
            val dbMap = withContext(Dispatchers.IO) { repo.words(sel) }
                .associateBy { "${it.source}|${it.de}" }

            val dueList = mutableListOf<Pair<SrsCard, Long>>()
            val freshList = mutableListOf<SrsCard>()
            for (src in sel) {
                for (w in DataRepo.srsWords(src)) {
                    val st = dbMap["$src|${w.de}"]
                    if (st == null) {
                        freshList += w
                    } else if (st.dueAt <= now) {
                        dueList += w to st.dueAt
                    }
                }
            }
            val allowed = maxOf(0, _newPerDay.value - repo.newCountToday)
            val fresh = freshList.take(allowed)

            val queue = when (_order.value) {
                "split" -> dueList.map { it.first }.shuffled() + fresh.shuffled()
                "list" -> dueList.sortedBy { it.second }.map { it.first } + fresh
                else -> (dueList.map { it.first } + fresh).shuffled()
            }

            sessDue = dueList.size
            sessFresh = fresh.size
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

    /** g: 0=忘了 1=模糊 2=记得（与网站 grade() 一致）。 */
    fun grade(g: Int) {
        val card = current ?: return
        viewModelScope.launch {
            val now = System.currentTimeMillis()
            val prev = withContext(Dispatchers.IO) { repo.word(card.source, card.de) }
            undoStack.addLast(
                UndoEntry(
                    source = card.source,
                    de = card.de,
                    prev = prev,
                    newCount = repo.newCountToday,
                    index = _index.value,
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
                        de = card.de,
                        box = res.box,
                        dueAt = res.dueAt,
                        lastSeen = now,
                        lastGrade = g,
                        createdAt = prev?.createdAt ?: now
                    )
                )
            }
            if (prev == null) repo.newCountToday = repo.newCountToday + 1
            if (g == SrsRules.GRADE_FORGOT) sessForgot++
            sessDone++

            if (_index.value + 1 >= _queue.value.size) {
                finishSession()
            } else {
                _index.value += 1
                _flipped.value = false
            }
            refreshStats()
        }
    }

    private suspend fun finishSession() {
        val now = System.currentTimeMillis()
        val dueTomorrow = withContext(Dispatchers.IO) {
            repo.countDueBetween(_selectedSources.value, now, now + 24 * 3600 * 1000L)
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
        val u = undoStack.removeLastOrNull() ?: return
        viewModelScope.launch {
            withContext(Dispatchers.IO) {
                if (u.prev == null) repo.delete(u.source, u.de) else repo.upsert(u.prev)
            }
            repo.newCountToday = u.newCount
            _index.value = u.index
            sessDone = u.done
            sessForgot = u.forgot
            _flipped.value = false
            _mode.value = "study"
            _canUndo.value = undoStack.isNotEmpty()
            refreshStats()
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
