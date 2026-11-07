package com.wdjiangdev.delernen

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import com.wdjiangdev.delernen.data.DataRepo
import com.wdjiangdev.delernen.nav.AppRoot
import com.wdjiangdev.delernen.ui.theme.DelernenTheme
import com.wdjiangdev.delernen.util.TtsHelper

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        DataRepo.init(applicationContext)
        enableEdgeToEdge()
        setContent {
            DelernenTheme {
                AppRoot()
            }
        }
    }

    override fun onDestroy() {
        TtsHelper.release()
        super.onDestroy()
    }
}
