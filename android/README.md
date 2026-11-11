# delernen Android

离线德语学习 App（Jetpack Compose + Room SRS）。数据全量打包在 `app/src/main/assets/data/`（13 个 JSON，由 `scripts/build_android_data.py` 生成），Manifest 不申请 INTERNET 权限，完全离线。

## 构建

**CI 为主（推荐）**：`.github/workflows/android.yml` 在 push 到 master 且改动路径含 `android/**` 或该 workflow 本身（或手动 workflow_dispatch）时执行 `assembleRelease`（R8 混淆 + 资源压缩，debuggable=false），用固定证书签名并发布到 Release。每次构建都是一个新版本，不覆盖旧的：

- versionCode：`GITHUB_RUN_NUMBER`
- versionName：`1.1.<run>`（`app/build.gradle.kts` 里的 `versionMinor` 控制中间那位）
- tag：`android-v1.<run>`，附件：`delernen-1.1.<run>.apk`
- 有 `concurrency: android-release`，连续 push 只保留最新一次构建。
- CI 会校验 APK 证书 SHA-256 必须等于既有证书（`2308e396…438164`），不一致直接失败。

**arm02 备用**：在 arm02 构建机（129.159.200.32，环境在 `/opt/build/`）同步 `android/` 后执行 `gradle -p android assembleDebug`（release 需要先导出下面的签名环境变量）。注意 compileSdk 是 35，构建机需要 platform 35。

**本地 Android Studio**：直接打开 `android/` 目录 Run 即可；没设签名环境变量时 debug 回退默认 debug 签名，不影响编译。

## 数据更新流程

1. 改完网站源数据（仓库根的 `nicos/`、`kurs/`、`alice/`、`a1a2/`、`a1b2/`、`memorize/` 等目录）；
2. 重跑生成脚本：

   ```bash
   python3 scripts/build_android_data.py
   ```

   它会重新生成 `android/app/src/main/assets/data/` 下 13 个 JSON（nicos×3、sep×2、动词组×2、词族×2、语法×2、kurs、alice）。脚本带条数断言（nicos 1725/1731/961、sep 27/49、动词组 66/154、kurs 94、alice 17），**新增课程卡/笔记后必须先同步更新脚本里的 `EXPECTED`**，否则脚本报错不产出；
3. 把 `assets/data/` 的变动随源码一起提交。App 端零代码改动——`DataRepo` 按文件名懒加载assets。

## 版本号

不用手改：versionCode / versionName / tag 都由 CI 的 run number 自动生成（见上）。要升中间位时改 `app/build.gradle.kts` 的 `versionMinor` 和 workflow 里的 `VERSION_NAME`。

## 签名说明

- 证书：与 TriCloud App 共用的固定 key（CN=Android Debug，SHA-256 `2308e396…438164`），保证已安装用户覆盖升级、无需卸载。
- 仓库里**没有**任何 keystore 或口令。`app/build.gradle.kts` 只从环境变量读取：
  `ANDROID_KEYSTORE_PATH`（默认 `android/signing.keystore`）、`ANDROID_KEYSTORE_PASSWORD`、`ANDROID_KEY_ALIAS`、`ANDROID_KEY_PASSWORD`。缺任一项或 keystore 为空文件时不配置签名。
- CI 从仓库 Secrets 取值：`ANDROID_KEYSTORE_BASE64`（keystore 的 base64，解码到 `$RUNNER_TEMP`）、`ANDROID_KEYSTORE_PASSWORD`、`ANDROID_KEY_ALIAS`、`ANDROID_KEY_PASSWORD`；任一为空则构建直接失败。
- 根目录 `.gitignore` 忽略 `*.keystore` / `*.jks` / `build/` / `.gradle/` / `local.properties` 等。

## Room 数据库

- `exportSchema = true`，schema 输出到 `android/app/schemas/`。CI 会把生成的 schema 作为 artifact 上传（`room-schemas-<run>`），**请把其中的 `2.json` 提交进仓库**，以后改表才能用 AutoMigration / 迁移校验。
- v2：主键改为 `(source, wkey)`，`wkey = w.k || w.de`，与网站 memorize 完全一致。`MIGRATION_1_2` 做结构迁移，启动时 `SrsRepository.migrateKeys()` 再把旧的 de 键映射到 k 键，并照搬网站 `ALIAS` 合并规则（网站 ALIAS 有新增时同步过来并把 `KEY_MIGRATION_VERSION` +1）。
- 迁移策略：每次改表 version+1 并写显式 `Migration` 加进 `ALL_MIGRATIONS`；**不要**用 `fallbackToDestructiveMigration`。

## 代码结构速览

```
android/app/src/main/java/com/astemo/delernen/
├── MainActivity.kt            # 入口：DataRepo.init + TTS 预热（只在真正退出时释放）
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
