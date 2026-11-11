# Alice 笔记源文件

`NN-slug.md` 是 `/alice/NN-slug.html` 的源：Alice（alicelearngerman.medium.com）原文逐字照录，
`> 中：` 为中文译注、`> EN:` 为补充英文，⚠ 标出原文错误，文末 `# 中文要点` 为学习层小结。
原文版权归作者 Alice 所有，此处仅作个人学习整理。

重新生成页面和目录：

    python3 scripts/build_alice.py

文件头的 `<!-- title / level / desc -->` 决定页面标题、等级和目录导读（标题请保持不变，
Android 构建 `scripts/build_android_data.py` 会核对页面标题与目录一致）。
本目录不会被 `scripts/build_site.py` 发布到站点。
