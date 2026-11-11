# DeLernen 德语学习站

德语学习整站源码（Nicos Weg 词汇 + 语法 A1–B2），纯静态页面，无需构建，直接用浏览器打开 `index.html` 即可。

在线访问：https://delernen.6668800.xyz/

## 栏目

| 路径 | 内容 |
|------|------|
| `/` | 首页：四个栏目入口 |
| `/a1a2/` | A1-A2 单词星图：26 组动词词干 + 16 组词族 + 19 组语法星图 |
| `/a1b2/` | A1-B2 单词星图：82 组动词词干 + 28 组词族 + 29 组语法星图，A1/A2/B1/B2 级别徽章 |
| `/grammatik/` | 德语语法 A1-B2：28 个语法点，中文讲解 + 规则表 + 例句（德+中）+ 英语对照 |
| `/kurs/` | 德语课程语法与词汇 A1–C1：94 张卡片（A1 41 / A2 18 / B1 18 / B2 11 / C1 6），按站内课程实际顺序 M01–M24（已登录核验），中文讲解 + 英语对照 + 例句，整理自 SharpLingo 德语课程（讲解为原创重写，例句选自课程原句；视频除外）；C1 仍在更新、持续补充 |

## 功能

- **动词星图**：按词干分组（如 ziehen → ausziehen / einziehen / umziehen），每个动词有中文、过去式、过去分词、英文释义
- **词族**：同一词根的名词/动词/形容词（如 fahr → fahren / die Fahrt / der Fahrer），名词带复数
- **语法星图**：介词格、情态动词、可分前缀、连词、人称代词、句型语序、句框结构、固定搭配、虚拟式等；分组下方有"📖 系统讲解"深链，可跳到语法页对应条目
- **深色/浅色模式**：右上角按钮切换，可手动选或自动跟随系统

## 文件

- `index.html`：首页
- `a1a2/`、`a1b2/`：`index.html`（星图页面）+ `verb_groups.json`（动词）+ `word_families.json`（词族）+ `grammar.json`（语法星图）
- `grammatik/`：`index.html`（语法学习页）+ `grammar_learn.json`（28 个语法点数据）
- `kurs/`：课程索引页 + `a1/`/`a2/`/`b1/`/`b2/`/`c1/` 五个级别子目录，各含 `index.html` + 语法/词汇 JSON（共 94 张卡片：A1 41、A2 18、B1 18、B2 11、C1 6）
- `scripts/`：内容生成脚本（动词提取/词族/语法点源数据），JSON 为构建产物，可直接改 JSON

## 数据来源

- 动词/对话脚本：[lightsongjs/DW-Nicos-Weg](https://github.com/lightsongjs/DW-Nicos-Weg)（Nicos Weg A1+A2）
- B2 动词：歌德 B2 考纲常见词汇
- 词性校验：TU Chemnitz ding 德英词典（GPL-2.0+）
- 词族、语法例句、三形式：手工整理核对

## 一键部署（换服务器）

在新服务器上以 root 执行一条命令即可（Debian/Ubuntu；会自动装 docker）：

```bash
curl -fsSL https://raw.githubusercontent.com/wdjiangdev/delernen/master/deploy.sh | bash
```

做完的事：下载本站文件 → 构建（`scripts/build_site.py`：给页面引用的 js/json 自动加内容哈希版本号、生成全站搜索索引、生成离线缓存清单）→ 写入 `/opt/docker/delernen`（`conf/nginx.conf` + `www/`）→ 启动 `delernen-web` 容器（nginx:alpine，监听 `127.0.0.1:18095`）→ 健康检查。

最后一步手动做：在 Cloudflare Tunnel 里加一条 Public Hostname，Service 指向 `http://127.0.0.1:18095`。

- 换端口：`PORT=18096 bash deploy.sh`
- 换目录：`DEPLOY_DIR=/srv/delernen bash deploy.sh`
- 重新执行即更新站点文件并重载 nginx（幂等）。
- 开启自动部署（每 5 分钟检查 GitHub master，有新提交自动更新，日志 `/var/log/delernen-deploy.log`）：
  `curl -fsSL https://raw.githubusercontent.com/wdjiangdev/delernen/master/deploy.sh | bash -s -- --install-auto`
- 关闭自动部署：同上，参数换成 `--remove-auto`。
- 改词库/数据后**不需要**手动改 `?v=`，构建时按文件内容自动生成。
- 本地预览构建结果：`python3 scripts/build_site.py . /tmp/dist && cd /tmp/dist && python3 -m http.server`
