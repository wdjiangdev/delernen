package com.wdjiangdev.delernen.util

import android.content.Context
import android.speech.tts.TextToSpeech
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import java.util.Locale

/**
 * 全局唯一的 TTS 封装：Locale.GERMAN；不可用时各按钮静默禁用，不崩溃。
 */
class TtsHelper private constructor(context: Context) {

    var ready by mutableStateOf(false)
    var germanAvailable by mutableStateOf(false)
        private set

    private var tts: TextToSpeech? = null

    init {
        try {
            tts = TextToSpeech(context.applicationContext) { status ->
                if (status == TextToSpeech.SUCCESS) {
                    val r = tts?.isLanguageAvailable(Locale.GERMAN) ?: TextToSpeech.LANG_NOT_SUPPORTED
                    germanAvailable = r != TextToSpeech.LANG_MISSING_DATA &&
                            r != TextToSpeech.LANG_NOT_SUPPORTED
                }
                ready = true
            }
        } catch (_: Exception) {
            ready = true
            germanAvailable = false
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

        fun release() {
            instance?.shutdown()
            instance = null
        }
    }
}
