---
sidebar_position: 2
---

# 页面布局示例

这个页面展示了 Docusaurus 中不同的页面布局和组件。

## 文档页面布局（当前页面）

你现在看到的就是**文档页面布局**：

- **左侧**：文档导航树（侧边栏）
- **中间**：文档内容（你正在阅读的部分）
- **右侧**：页面目录（TOC）

## 内容组件示例

### 提示框组件

:::tip 提示
这是一个提示框，用于显示有用的信息。
:::

:::info 信息
这是一个信息框，用于显示一般信息。
:::

:::warning 警告
这是一个警告框，用于显示需要注意的内容。
:::

:::danger 危险
这是一个危险提示框，用于显示重要警告。
:::

### 代码块

```javascript title="示例代码"
function HelloWorld() {
  return <h1>Hello, World!</h1>;
}
```

```bash title="命令行"
npm start
npm run build
npm run serve
```

### 标签页组件

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<Tabs>
  <TabItem value="npm" label="npm" default>
    ```bash
    npm install
    npm start
    ```
  </TabItem>
  <TabItem value="yarn" label="Yarn">
    ```bash
    yarn install
    yarn start
    ```
  </TabItem>
  <TabItem value="pnpm" label="pnpm">
    ```bash
    pnpm install
    pnpm start
    ```
  </TabItem>
</Tabs>

### 可折叠内容

<details>
<summary>点击展开详细信息</summary>

这里是折叠的内容。你可以在这里放置：

- 详细的技术说明
- 长篇的代码示例
- 可选的配置信息
- 故障排除步骤

</details>

## 其他页面类型

### 1. 博客页面
- 访问 `/blog` 查看博客列表页面
- 点击任意文章查看博客文章页面

### 2. 自定义页面
- 访问 `/about` 查看 Markdown 自定义页面
- 访问 `/features` 查看 React 自定义页面

### 3. 首页
- 访问 `/` 查看自定义首页布局

## 响应式设计

所有页面都支持响应式设计：

- **桌面端**：完整的三栏或两栏布局
- **平板端**：侧边栏可折叠
- **手机端**：单栏布局，导航菜单折叠

## 自定义布局

你可以通过以下方式自定义布局：

1. **修改现有组件**：编辑 `src/components/` 中的组件
2. **创建新页面**：在 `src/pages/` 中添加新的页面文件
3. **自定义样式**：编辑 `src/css/custom.css`
4. **使用插件**：安装和配置 Docusaurus 插件
