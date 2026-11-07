# delernen Android

离线德语学习 App（Jetpack Compose + Room SRS）。数据全量打包在 `app/src/main/assets/data/`（13 个 JSON，由 `scripts/build_android_data.py` 生成），Manifest 不申请 INTERNET 权限，完全离线。

## 构建

**CI 为主（推荐）**：`.github/workflows/android.yml` 在 push 到 master 且改动路径含 `android/**`（或手动 workflow_dispatch）时自动执行 `assembleDebug`，用固定签名打出 APK 并发布到 Release：

- tag：`android-v1.0.0`
- name：`delernen Android v1.0.0`
- 附件：`delernen-1.0.0.apk`

**arm02 备用**：本沙箱无 Gradle 时，在 arm02 构建机（129.159.200.32，环境在 `/opt/build/`：Temurin JDK 17 + android-sdk platform 34 / build-tools 34）同步 `android/` 源码后执行：

```bash
gradle -p android assembleDebug        # 若已生成 wrapper，等价于 ./gradlew assembleDebug
```

产物：`android/app/build/outputs/apk/debug/app-debug.apk`。

**本地 Android Studio**：直接打开 `android/` 目录 Run 即可；`android/debug.keystore` 不存在时自动回退默认 debug 签名，不影响编译。

## 数据更新流程

1. 改完网站源数据（仓库根的 `nicos/`、`kurs/`、`alice/`、`a1a2/`、`a1b2/`、`memorize/` 等目录）；
2. 重跑生成脚本：

   ```bash
   python3 scripts/build_android_data.py
   ```

   它会重新生成 `android/app/src/main/assets/data/` 下 13 个 JSON（nicos×3、sep×2、动词组×2、词族×2、语法×2、kurs、alice）。脚本带条数断言（nicos 1725/1731/961、sep 27/49、动词组 66/154、kurs 94、alice 17），**新增课程卡/笔记后必须先同步更新脚本里的 `EXPECTED`**，否则脚本报错不产出；
3. 把 `assets/data/` 的变动随源码一起提交。App 端零代码改动——`DataRepo` 按文件名懒加载assets。

## 版本号修改位置（发版需同步两处）

1. `android/app/build.gradle.kts` → `defaultConfig` 里的 `versionCode` / `versionName`（当前 1 / "1.0.0"）；
2. `.github/workflows/android.yml` → 三处硬编码：产物名 `delernen-1.0.0.apk`、Release tag `android-v1.0.0`、Release name `delernen Android v1.0.0`。

发版流程：两处同步改完 → 推 master（改动落在 `android/**`）→ CI 自动构建并发 Release。

## 签名说明

- `app/build.gradle.kts` 里定义了 `debugFixed` 签名配置：storeFile 指向 `android/debug.keystore`（`rootProject.file("debug.keystore")`），口令 `android`、别名 `androiddebugkey`。**仅当该文件存在时**，`debug` 构建类型才启用它；不存在则回退 Android 默认 debug 签名，所以本地无密钥也能编译。
- CI 在构建前把仓库 Secret `ANDROID_KEYSTORE_BASE64`（keystore 文件的 base64）解码写入 `android/debug.keystore`，从而产出固定签名的 APK——覆盖安装即可更新，不用卸载旧版。
- keystore 本体不入库（仓库里没有该文件），只存在于 CI Secret 与构建机上；Secret 轮换后重新部署即可。

## 代码结构速览

```
android/app/src/main/java/com/wdjiangdev/delernen/
├── MainActivity.kt            # Application 入口：DataRepo.init + TtsHelper.release
├── nav/AppRoot.kt             # Navigation Compose：5 个页签 + star/verb、course/{num}、note/{index} 详情路由
├── data/
│   ├── Models.kt              # 与 assets/data/*.json 一一对应的数据类
│   ├── DataRepo.kt            # assets JSON 解析（懒加载、进程内缓存）
│   ├── db/                    # Room SRS 数据库
│   └── srs/                   # SRS 仓库/ViewModel/间隔规则
├── ui/
│   ├── star/                  # 页签 1 星图（StarMapScreen / StarVerbScreen）
│   ├── vocab/                 # 页签 2 词表
│   ├── memorize/              # 页签 3 背单词（SRS）
│   ├── course/                # 页签 4 课程列表 + 详情/跟读（本目录）
│   ├── notes/                 # 页签 5 笔记列表 + 详情（本目录）
│   ├── components/Common.kt   # 通用组件（CardSurface / SectionHeader / TtsIconButton / SegmentedRow / PosChip）
│   └── theme/Theme.kt         # DelernenColors 深色配色（对齐网站 theme.css）
└── util/                      # TtsHelper（德语 TTS）、DeText（词条文本工具）
```
