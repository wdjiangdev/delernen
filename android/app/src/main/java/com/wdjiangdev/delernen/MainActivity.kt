package com.wdjiangdev.delernen

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import com.wdjiangdev.delernen.data.DataRepo
import com.wdjiangdev.delernen.data.ThemeStore
import com.wdjiangdev.delernen.data.WegProgress
import com.wdjiangdev.delernen.nav.AppRoot
import com.wdjiangdev.delernen.ui.theme.DelernenTheme
import com.wdjiangdev.delernen.ui.theme.ThemeState
import com.wdjiangdev.delernen.util.TtsHelper

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        DataRepo.init(applicationContext)
        WegProgress.init(applicationContext)
        // 主题偏好在首帧前读入（默认蓝色），避免启动时闪一下另一套配色
        ThemeState.light = ThemeStore.isLight(applicationContext)
        // TTS 绑定 applicationContext，进程级单例；提前初始化，旋转屏幕不重建
        TtsHelper.get(applicationContext)
        enableEdgeToEdge()
        setContent {
            DelernenTheme {
                AppRoot()
            }
        }
    }

    override fun onDestroy() {
        // 配置变更（旋转等）也会走 onDestroy：只有真正退出时才释放 TTS，
        // 避免把正在进行的「整页连读」打断、按钮短暂变灰。
        if (isFinishing && !isChangingConfigurations) {
            TtsHelper.release()
        }
        super.onDestroy()
    }
}
