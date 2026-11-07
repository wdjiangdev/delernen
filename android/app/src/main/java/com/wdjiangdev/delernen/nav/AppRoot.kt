package com.wdjiangdev.delernen.nav

import android.net.Uri
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Description
import androidx.compose.material.icons.filled.FormatListBulleted
import androidx.compose.material.icons.filled.MenuBook
import androidx.compose.material.icons.filled.Memory
import androidx.compose.material.icons.filled.Star
import androidx.compose.material3.Icon
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.NavigationBarItemDefaults
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.navigation.NavGraph.Companion.findStartDestination
import androidx.navigation.NavHostController
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import com.wdjiangdev.delernen.ui.course.CourseDetailScreen
import com.wdjiangdev.delernen.ui.course.CourseScreen
import com.wdjiangdev.delernen.ui.memorize.MemorizeScreen
import com.wdjiangdev.delernen.ui.notes.NoteDetailScreen
import com.wdjiangdev.delernen.ui.notes.NotesScreen
import com.wdjiangdev.delernen.ui.star.StarMapScreen
import com.wdjiangdev.delernen.ui.star.StarVerbScreen
import com.wdjiangdev.delernen.ui.theme.DelernenColors
import com.wdjiangdev.delernen.ui.vocab.VocabScreen

private const val SCREEN_STAR = "star"
private const val SCREEN_VOCAB = "vocab"
private const val SCREEN_MEMORIZE = "memorize"
private const val SCREEN_COURSE = "course"
private const val SCREEN_NOTES = "notes"

private val TOP_LEVEL = setOf(SCREEN_STAR, SCREEN_VOCAB, SCREEN_MEMORIZE, SCREEN_COURSE, SCREEN_NOTES)

private data class TabItem(val route: String, val label: String, val icon: ImageVector)

private val tabs = listOf(
    TabItem(SCREEN_STAR, "星图", Icons.Default.Star),
    TabItem(SCREEN_VOCAB, "词表", Icons.Default.FormatListBulleted),
    TabItem(SCREEN_MEMORIZE, "背单词", Icons.Default.Memory),
    TabItem(SCREEN_COURSE, "课程", Icons.Default.MenuBook),
    TabItem(SCREEN_NOTES, "笔记", Icons.Default.Description)
)

@Composable
fun AppRoot() {
    val navController = rememberNavController()
    val backStackEntry by navController.currentBackStackEntryAsState()
    val currentRoute = backStackEntry?.destination?.route
    val isTopLevel = currentRoute in TOP_LEVEL

    Scaffold(
        bottomBar = {
            if (isTopLevel) {
                NavigationBar(containerColor = DelernenColors.BgCard) {
                    val current = currentRoute.orEmpty()
                    tabs.forEach { tab ->
                        NavigationBarItem(
                            selected = current == tab.route,
                            onClick = {
                                navController.navigate(tab.route) {
                                    popUpTo(navController.graph.findStartDestination().id) {
                                        saveState = true
                                    }
                                    launchSingleTop = true
                                    restoreState = true
                                }
                            },
                            icon = { Icon(tab.icon, contentDescription = tab.label) },
                            label = { Text(tab.label) },
                            colors = NavigationBarItemDefaults.colors(
                                selectedIconColor = DelernenColors.Accent2,
                                selectedTextColor = DelernenColors.Accent2,
                                indicatorColor = DelernenColors.AccentDeep
                            )
                        )
                    }
                }
            }
        }
    ) { innerPadding ->
        NavHost(
            navController = navController,
            startDestination = SCREEN_STAR,
            modifier = Modifier.padding(innerPadding)
        ) {
            composable(SCREEN_STAR) { StarMapScreen(navController) }

            composable(
                "star/verb/{range}/{stem}",
                arguments = listOf(
                    navArgument("range") { type = NavType.StringType },
                    navArgument("stem") { type = NavType.StringType }
                )
            ) { entry ->
                StarVerbScreen(
                    range = entry.arguments?.getString("range") ?: "a1a2",
                    stem = Uri.decode(entry.arguments?.getString("stem") ?: ""),
                    onBack = { navController.popBackStack() }
                )
            }

            composable(SCREEN_VOCAB) { VocabScreen() }
            composable(SCREEN_MEMORIZE) { MemorizeScreen() }
            composable(SCREEN_COURSE) { CourseScreen(navController) }

            composable(
                "course/{num}",
                arguments = listOf(navArgument("num") { type = NavType.StringType })
            ) { entry ->
                CourseDetailScreen(
                    num = entry.arguments?.getString("num") ?: "",
                    onBack = { navController.popBackStack() }
                )
            }

            composable(SCREEN_NOTES) { NotesScreen(navController) }

            composable(
                "note/{index}",
                arguments = listOf(navArgument("index") { type = NavType.IntType })
            ) { entry ->
                val index = entry.arguments?.getInt("index") ?: 0
                NoteDetailScreen(index = index, onBack = { navController.popBackStack() })
            }
        }
    }
}
