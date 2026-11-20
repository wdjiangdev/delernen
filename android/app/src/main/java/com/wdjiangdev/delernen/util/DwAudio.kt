package com.wdjiangdev.delernen.util

import android.content.Context
import android.media.MediaPlayer
import org.json.JSONObject
import java.io.File
import java.net.HttpURLConnection
import java.net.URL
import java.util.Locale
import java.util.concurrent.Executors

/**
 * DW 原版单词录音（与网站同一批 Akamai mp3、同一张映射表 dw_audio.json）：
 * 点读时先查本地缓存（cacheDir/dw-audio），没有就联网下载、存缓存再播，
 * 之后再点同一个词直接播本地文件、不走网络；下载失败回退系统 TTS。
 * DW 只录了单词和少数固定短语，句型/对话整句查不到映射，自动走 TTS——与网站行为一致。
 */
object DwAudio {
    private const val BASE =
        "https://radiodownloaddw-a.akamaihd.net/Events/dwelle/deutschkurse/nicosweg/wortschatz/"

    @Volatile
    private var appContext: Context? = null

    @Volatile
    private var map: Map<String, String>? = null

    private val executor = Executors.newSingleThreadExecutor()
    private var player: MediaPlayer? = null

    fun init(context: Context) {
        if (appContext == null) {
            appContext = context.applicationContext
            executor.execute { audioMap() } // 后台预解析映射表，点读时不卡顿
        }
    }

    private fun audioMap(): Map<String, String> {
        map?.let { return it }
        synchronized(this) {
            map?.let { return it }
            val ctx = appContext ?: return emptyMap()
            val m = HashMap<String, String>()
            try {
                val text = ctx.assets.open("data/dw_audio.json")
                    .bufferedReader().use { it.readText() }
                val obj = JSONObject(text)
                val keys = obj.keys()
                while (keys.hasNext()) {
                    val k = keys.next()
                    m[k] = obj.getString(k)
                }
            } catch (_: Exception) {
                // 资产缺失/损坏：当作无录音，全部回退 TTS
            }
            map = m
            return m
        }
    }

    /** 与网站 dwKey 完全一致的归一化键（三处必须同步改）。 */
    fun dwKey(t: String): String {
        var s = t.split(',')[0].split(" / ")[0]
        s = s.replace(Regex("\\s*\\([^)]*\\)"), "").replace("|", "")
        s = s.replace(Regex("[.!?;:]"), "").trim().lowercase(Locale.ROOT)
        s = s.replace(Regex("^(der/die|der/das|der|die|das|den|dem|ein|eine)\\s+"), "")
        return s.trim()
    }

    fun hasAudio(text: String): Boolean = audioMap()[dwKey(text)] != null

    /** 点读入口：DW 录音优先（缓存 → 下载），其余情况 TTS。 */
    fun speak(text: String, tts: TtsHelper) {
        val file = audioMap()[dwKey(text)]
        val ctx = appContext
        if (file == null || ctx == null) {
            stop()
            tts.speak(text)
            return
        }
        tts.stop()
        executor.execute {
            val dir = File(ctx.cacheDir, "dw-audio").apply { mkdirs() }
            val local = File(dir, file)
            if (!local.exists()) {
                try {
                    val tmp = File(dir, "$file.tmp")
                    val conn = URL(BASE + file).openConnection() as HttpURLConnection
                    conn.connectTimeout = 10_000
                    conn.readTimeout = 10_000
                    conn.instanceFollowRedirects = true
                    conn.inputStream.use { input ->
                        tmp.outputStream().use { input.copyTo(it) }
                    }
                    if (!tmp.renameTo(local)) tmp.delete()
                } catch (_: Exception) {
                    // 下载失败：下面走 TTS 兜底
                }
            }
            if (local.exists() && local.length() > 0) {
                play(local)
            } else {
                tts.speak(text)
            }
        }
    }

    fun stop() {
        executor.execute { releasePlayer() }
    }

    private fun play(file: File) {
        releasePlayer()
        try {
            val mp = MediaPlayer()
            mp.setDataSource(file.absolutePath)
            mp.setOnCompletionListener { done ->
                done.release()
                if (player === done) player = null
            }
            mp.setOnErrorListener { bad, _, _ ->
                bad.release()
                if (player === bad) player = null
                true
            }
            mp.prepare()
            player = mp
            mp.start()
        } catch (_: Exception) {
            releasePlayer()
        }
    }

    private fun releasePlayer() {
        try {
            player?.release()
        } catch (_: Exception) {
        }
        player = null
    }
}
