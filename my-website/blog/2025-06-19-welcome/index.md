---
slug: welcome
title: 欢迎
tags: [hello]
---

[Docusaurus 的博客功能](https://docusaurus.io/docs/blog)是由[博客插件](https://docusaurus.io/docs/api/plugins/@docusaurus/plugin-content-blog)驱动的。

以下是一些你可能会觉得有用的小提示。

<!-- truncate -->

1. 只需将 Markdown 文件（或文件夹）添加到 `blog` 目录即可。
2. 博客作者信息可以添加到 `authors.yml` 文件中。
3. 博文的发布日期可以从文件名中提取，例如：
   1. `2019-05-30-welcome.md`
   2. `2019-05-30-welcome/index.md`
4. 使用博文文件夹来存放相关的图片会很方便：
![Docusaurus 毛绒玩具](./docusaurus-plushie-banner.jpeg)
5. 博客也支持标签功能！
6. 使用 `<!--` `truncate` `-->` 来控制在博客列表页面中显示的内容长度。
7. 博文信息配置如下：
```markdown
---
slug: welcome
title: 欢迎
authors: 作者
tags: [hello]
---
```

**如果你不想要博客功能**：只需删除此目录，并在你的 Docusaurus 配置文件中设置 `blog: false` 即可。