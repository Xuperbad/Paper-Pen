# Paper-Pen 文档站

基于 [Docusaurus](https://docusaurus.io/) 构建的现代化文档网站，支持 Markdown 编写、自动部署和多种功能扩展。

## 🌐 在线访问

- **线上地址**: https://xuperbad.github.io/Paper-Pen/
- **本地开发**: http://localhost:3000

## 📁 项目结构

```
my-website/
├── blog/                    # 博客文章目录
│   ├── authors.yml         # 作者信息配置
│   ├── tags.yml           # 标签配置
│   └── *.md               # 博客文章（Markdown 格式）
├── docs/                   # 文档页面目录
│   ├── intro.md           # 介绍页面
│   ├── getting-started.md # 快速开始
│   ├── tutorial-basics/   # 基础教程
│   └── tutorial-extras/   # 进阶教程
├── src/                    # 源代码目录
│   ├── components/        # React 组件
│   ├── css/              # 自定义样式
│   └── pages/            # 自定义页面
├── static/                 # 静态资源目录
│   └── img/              # 图片资源
├── docusaurus.config.js   # 主配置文件
├── sidebars.js            # 侧边栏配置
└── package.json           # 项目依赖
```

## 🚀 快速开始

### 环境要求
- Node.js 18+
- npm 或 yarn

### 本地开发

```bash
# 1. 克隆项目
git clone https://github.com/Xuperbad/Paper-Pen.git
cd Paper-Pen/my-website

# 2. 安装依赖
npm install
# 或者使用 yarn
yarn

# 3. 启动开发服务器
npm start
# 或者使用 yarn
yarn start
```

开发服务器启动后会自动打开浏览器，访问 http://localhost:3000

### 构建和部署

```bash
# 构建生产版本
npm run build
# 或者使用 yarn
yarn build

# 本地预览构建结果
npm run serve
# 或者使用 yarn
yarn serve
```

## ✍️ 内容创作指南

### 📝 编写博客文章

1. **创建博客文件**
   在 `blog/` 目录下创建 Markdown 文件，文件名格式：`YYYY-MM-DD-标题.md`

2. **博客文章模板**
   ```markdown
   ---
   slug: my-blog-post
   title: 我的博客标题
   authors: [admin]
   tags: [docusaurus, 教程]
   ---

   # 博客标题

   这里是博客内容...

   <!--truncate-->

   这里是展开后的详细内容...
   ```

3. **配置作者信息**
   编辑 `blog/authors.yml` 添加作者：
   ```yaml
   admin:
     name: 你的名字
     title: 职位
     url: https://github.com/yourusername
     image_url: https://github.com/yourusername.png
   ```

### 📚 编写文档页面

1. **创建文档文件**
   在 `docs/` 目录下创建 `.md` 文件

2. **文档页面模板**
   ```markdown
   ---
   sidebar_position: 1
   ---

   # 文档标题

   文档内容...

   ## 二级标题

   更多内容...
   ```

3. **配置侧边栏**
   编辑 `sidebars.js` 自定义侧边栏结构：
   ```javascript
   const sidebars = {
     tutorialSidebar: [
       'intro',
       'getting-started',
       {
         type: 'category',
         label: '教程',
         items: ['tutorial-basics/create-a-document'],
       },
     ],
   };
   ```

### 📄 Markdown 语法指南

支持标准 Markdown 语法和 Docusaurus 扩展：

```markdown
# 一级标题
## 二级标题

**粗体** *斜体* `代码`

- 无序列表
1. 有序列表

[链接](https://docusaurus.io)

![图片](./img/image.png)

```代码块
console.log('Hello World');
```

:::tip 提示
这是一个提示框
:::

:::warning 警告
这是一个警告框
:::

:::danger 危险
这是一个危险提示框
:::
```

## 🎨 自定义配置

### 修改网站基本信息

编辑 `docusaurus.config.js`：

```javascript
const config = {
  title: '你的网站标题',
  tagline: '网站标语',
  url: 'https://yourusername.github.io',
  baseUrl: '/your-repo-name/',
  // ...
};
```

### 修改主页内容

编辑 `src/pages/index.js` 修改首页布局和内容

### 自定义样式

编辑 `src/css/custom.css` 添加自定义样式：

```css
:root {
  --ifm-color-primary: #2e8555;
  --ifm-color-primary-dark: #29784c;
}
```

### 添加导航菜单

在 `docusaurus.config.js` 的 `navbar.items` 中添加：

```javascript
navbar: {
  items: [
    {
      type: 'docSidebar',
      sidebarId: 'tutorialSidebar',
      position: 'left',
      label: '文档',
    },
    {to: '/blog', label: '博客', position: 'left'},
    {
      href: 'https://github.com/yourusername/your-repo',
      label: 'GitHub',
      position: 'right',
    },
  ],
}
```

## 🔄 多人协作开发

### 在其他电脑上开发

**是的！** 你可以在任何电脑上克隆项目并进行开发：

```bash
# 1. 克隆项目到新电脑
git clone https://github.com/Xuperbad/Paper-Pen.git
cd Paper-Pen/my-website

# 2. 安装依赖
npm install

# 3. 开始开发
npm start

# 4. 提交更改
git add .
git commit -m "feat: 添加新内容"
git push origin main
```

### 自动部署机制

✅ **每次推送到 `main` 分支都会自动触发部署**

- GitHub Actions 会自动构建网站
- 部署到 GitHub Pages
- 通常 2-3 分钟后网站更新

### 协作工作流

1. **拉取最新代码**: `git pull origin main`
2. **创建功能分支**: `git checkout -b feature/new-content`
3. **开发和测试**: 本地修改并测试
4. **提交更改**: `git commit -m "描述"`
5. **推送分支**: `git push origin feature/new-content`
6. **创建 Pull Request**: 在 GitHub 上创建 PR
7. **合并到主分支**: 审核后合并，自动部署

## 🛠️ 常用命令

```bash
# 开发相关
npm start          # 启动开发服务器
npm run build      # 构建生产版本
npm run serve      # 预览构建结果
npm run clear      # 清理缓存

# Git 相关
git status         # 查看文件状态
git add .          # 添加所有更改
git commit -m ""   # 提交更改
git push origin main # 推送到远程仓库
git pull origin main # 拉取最新代码
```

## 🎯 进阶功能

- **搜索功能**: 集成 Algolia DocSearch
- **版本控制**: 支持文档版本管理
- **国际化**: 多语言支持
- **插件系统**: 丰富的插件生态
- **SEO 优化**: 自动生成 sitemap 和 meta 标签

## 📞 获取帮助

- [Docusaurus 官方文档](https://docusaurus.io/docs)
- [Markdown 语法指南](https://www.markdownguide.org/)
- [GitHub Actions 文档](https://docs.github.com/en/actions)

---

**Happy Writing! 🎉**
