package com.wdjiangdev.delernen.data.srs

/**
 * 艾宾浩斯间隔重复规则 —— 与网站 memorize/index.html 完全一致：
 * NEXT=[0,20分钟,1天,3天,7天,15天,30天,60天]（毫秒），封顶 60 天；
 * 记得 → box+1 进入下一间隔；忘了 → box=0 且 10 分钟后重来；
 * 模糊 → box 维持，按当前间隔再巩固一次（box=0 时按 10 分钟）。
 */
object SrsRules {
    /** 各 box 的复习间隔（毫秒），下标即 box。 */
    val NEXT: List<Long> = listOf(
        0L,
        20 * 60 * 1000L,
        86400 * 1000L,
        3 * 86400 * 1000L,
        7 * 86400 * 1000L,
        15 * 86400 * 1000L,
        30 * 86400 * 1000L,
        60 * 86400 * 1000L
    )

    const val MASTER_BOX = 7
    const val FORGET_DELAY_MS = 10 * 60 * 1000L

    const val GRADE_FORGOT = 0
    const val GRADE_FUZZY = 1
    const val GRADE_GOT = 2

    data class GradeResult(val box: Int, val dueAt: Long)

    fun grade(prevBox: Int, now: Long, grade: Int): GradeResult = when (grade) {
        GRADE_FORGOT -> GradeResult(0, now + FORGET_DELAY_MS)
        GRADE_FUZZY -> GradeResult(prevBox, now + (if (prevBox > 0) NEXT[prevBox] else FORGET_DELAY_MS))
        else -> {
            val box = minOf(MASTER_BOX, prevBox + 1)
            GradeResult(box, now + NEXT[box])
        }
    }

    fun boxName(box: Int): String = if (box >= MASTER_BOX) "已掌握" else "Box $box"
}
