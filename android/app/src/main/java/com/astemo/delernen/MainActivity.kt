package com.astemo.delernen

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import com.astemo.delernen.data.DataRepo
import com.astemo.delernen.nav.AppRoot
import com.astemo.delernen.ui.theme.DelernenTheme
import com.astemo.delernen.util.TtsHelper

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        DataRepo.init(applicationContext)
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
