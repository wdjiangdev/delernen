package com.astemo.delernen.util

import android.content.ActivityNotFoundException
import android.content.Context
import android.content.Intent
import android.speech.tts.TextToSpeech
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import java.util.Locale

/**
 * 进程级唯一的 TTS 封装（绑定 applicationContext，旋转屏幕不会重建）。
 * onInit 里真正调用 setLanguage(Locale.GERMAN)，用返回值决定德语是否可用；
 * 缺语音数据时 [needsVoiceData] 为 true，可调用 [installVoiceData] 引导安装。
 * 不可用时各朗读按钮静默禁用，不崩溃。
 * 注意：Android 11+ 需要 Manifest 里的 <queries> TTS_SERVICE 才能绑定到引擎。
 */
class TtsHelper private constructor(context: Context) {

    var ready by mutableStateOf(false)
        private set
    var germanAvailable by mutableStateOf(false)
        private set
    /** 引擎在，但缺德语语音数据（LANG_MISSING_DATA）。 */
    var needsVoiceData by mutableStateOf(false)
        private set

    private var tts: TextToSpeech? = null

    init {
        try {
            tts = TextToSpeech(context.applicationContext) { status -> onInit(status) }
        } catch (_: Exception) {
            ready = true
            germanAvailable = false
        }
    }

    private fun onInit(status: Int) {
        if (status == TextToSpeech.SUCCESS) {
            val r = runCatching { tts?.setLanguage(Locale.GERMAN) }.getOrNull()
                ?: TextToSpeech.LANG_NOT_SUPPORTED
            needsVoiceData = r == TextToSpeech.LANG_MISSING_DATA
            germanAvailable = r == TextToSpeech.LANG_AVAILABLE ||
                    r == TextToSpeech.LANG_COUNTRY_AVAILABLE ||
                    r == TextToSpeech.LANG_COUNTRY_VAR_AVAILABLE
        } else {
            germanAvailable = false
        }
        ready = true
    }

    /** 打开系统「安装语音数据」页面（缺德语语音包时用）。 */
    fun installVoiceData(context: Context) {
        val intent = Intent(TextToSpeech.Engine.ACTION_INSTALL_TTS_DATA)
            .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        try {
            context.startActivity(intent)
        } catch (_: ActivityNotFoundException) {
            // 没有可处理的引擎设置页：静默忽略
        } catch (_: SecurityException) {
        }
    }

    /** 朗读单个德语词/句（打断当前播放）。不可用时静默无操作。 */
    fun speak(text: String) {
        if (!germanAvailable) return
        runCatching {
            tts?.speak(text, TextToSpeech.QUEUE_FLUSH, null, "delernen-w-${text.hashCode()}")
        }
    }

    /** 顺序连读多个德语句子（整页连读）。 */
    fun speakAll(lines: List<String>) {
        if (!germanAvailable) return
        runCatching {
            tts?.stop()
            lines.forEachIndexed { i, t ->
                if (t.isNotBlank()) {
                    tts?.speak(t, TextToSpeech.QUEUE_ADD, null, "delernen-s-$i-${t.hashCode()}")
                }
            }
        }
    }

    fun stop() {
        runCatching { tts?.stop() }
    }

    fun shutdown() {
        runCatching {
            tts?.stop()
            tts?.shutdown()
        }
        tts = null
    }

    companion object {
        @Volatile
        private var instance: TtsHelper? = null

        fun get(context: Context): TtsHelper = instance ?: synchronized(this) {
            instance ?: TtsHelper(context.applicationContext).also { instance = it }
        }

        /** 只在真正退出 App 时调用（Activity isFinishing 且非配置变更）。 */
        fun release() {
            synchronized(this) {
                instance?.shutdown()
                instance = null
            }
        }
    }
}
