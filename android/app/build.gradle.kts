plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("org.jetbrains.kotlin.plugin.compose")
    id("com.google.devtools.ksp")
}

// ---- 版本号：CI 用 GitHub run number，本地默认 1 ----
// versionCode = run number；versionName = 1.<VERSION_MINOR>.<run>；发布 tag = android-v1.<run>
val versionMinor = 1
val runNumber: Int = System.getenv("GITHUB_RUN_NUMBER")?.toIntOrNull() ?: 1

// ---- 签名：keystore 路径与口令全部来自环境变量 / GitHub Secrets，仓库里不放任何明文 ----
// ANDROID_KEYSTORE_PATH（默认 android/signing.keystore）、ANDROID_KEYSTORE_PASSWORD、
// ANDROID_KEY_ALIAS、ANDROID_KEY_PASSWORD。缺任何一项（或 keystore 为空文件）时不配签名：
// debug 回退默认 debug key，release 产出未签名包（CI 会在构建前显式检查并失败）。
val signingStoreFile: File = System.getenv("ANDROID_KEYSTORE_PATH")?.let { file(it) }
    ?: rootProject.file("signing.keystore")
val signingStorePassword: String? = System.getenv("ANDROID_KEYSTORE_PASSWORD")?.takeIf { it.isNotEmpty() }
val signingKeyAlias: String? = System.getenv("ANDROID_KEY_ALIAS")?.takeIf { it.isNotEmpty() }
val signingKeyPassword: String? = System.getenv("ANDROID_KEY_PASSWORD")?.takeIf { it.isNotEmpty() }
val hasSigning: Boolean = signingStoreFile.exists() && signingStoreFile.length() > 0 &&
        signingStorePassword != null && signingKeyAlias != null && signingKeyPassword != null

android {
    namespace = "com.astemo.delernen"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.astemo.delernen"
        minSdk = 26
        targetSdk = 35
        versionCode = runNumber
        versionName = "1.$versionMinor.$runNumber"
    }

    signingConfigs {
        if (hasSigning) {
            create("shared") {
                storeFile = signingStoreFile
                storePassword = signingStorePassword
                keyAlias = signingKeyAlias
                keyPassword = signingKeyPassword
            }
        }
    }

    buildTypes {
        debug {
            if (hasSigning) {
                signingConfig = signingConfigs.getByName("shared")
            }
        }
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            isDebuggable = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
            if (hasSigning) {
                signingConfig = signingConfigs.getByName("shared")
            }
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }

    buildFeatures {
        compose = true
    }
}

// Room schema 导出到 app/schemas（随代码提交，供迁移校验 / AutoMigration 使用）
ksp {
    arg("room.schemaLocation", "$projectDir/schemas")
}

dependencies {
    val composeBom = platform("androidx.compose:compose-bom:2024.12.01")
    implementation(composeBom)
    androidTestImplementation(composeBom)

    implementation("androidx.core:core-ktx:1.15.0")
    implementation("androidx.activity:activity-compose:1.9.3")

    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.material:material-icons-extended")

    implementation("androidx.navigation:navigation-compose:2.8.5")
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.8.7")
    implementation("androidx.lifecycle:lifecycle-runtime-compose:2.8.7")

    implementation("androidx.room:room-runtime:2.6.1")
    implementation("androidx.room:room-ktx:2.6.1")
    ksp("androidx.room:room-compiler:2.6.1")

    debugImplementation("androidx.compose.ui:ui-tooling")
}
