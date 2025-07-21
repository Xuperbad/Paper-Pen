// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import {themes as prismThemes} from 'prism-react-renderer';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Paper-Pen',
  tagline: '纸和笔',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://xuperbad.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  // For local development, use '/' instead of '/Paper-Pen/'
  baseUrl: process.env.NODE_ENV === 'development' ? '/' : '/Paper-Pen/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'Xuperbad', // Usually your GitHub org/user name.
  projectName: 'Paper-Pen', // Usually your repo name.

  onBrokenLinks: 'warn', // 改为 warn 而不是 throw
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  markdown: {
    mermaid: true,
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
          remarkPlugins: [require('remark-math')],
          rehypePlugins: [require('rehype-katex')],
        },
        blog: {
          showReadingTime: true,
          blogSidebarTitle: '所有文章',
          blogSidebarCount: 'ALL', // 显示所有文章而不是默认的5篇
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
          // Useful options to enforce blogging best practices
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  plugins: [
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'notes',
        path: 'notes',
        routeBasePath: 'notes',
        sidebarPath: './sidebarNotes.js',
        editUrl: 'https://github.com/Xuperbad/Paper-Pen/tree/main/my-website/',
        remarkPlugins: [require('remark-math')],
        rehypePlugins: [require('rehype-katex')],
      },
    ],
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'history',
        path: 'history',
        routeBasePath: 'history',
        sidebarPath: './sidebarHistory.js',
        editUrl: 'https://github.com/Xuperbad/Paper-Pen/tree/main/my-website/',
        remarkPlugins: [require('remark-math')],
        rehypePlugins: [require('rehype-katex')],
      },
    ],
    [
      '@docusaurus/plugin-content-blog',
      {
        id: 'zhejiang',
        path: 'zhejiang',
        routeBasePath: 'zhejiang',
        showReadingTime: true,
        blogSidebarTitle: '浙江宣传',
        blogSidebarCount: 'ALL',
        feedOptions: {
          type: ['rss', 'atom'],
          xslt: true,
        },
        editUrl: 'https://github.com/Xuperbad/Paper-Pen/tree/main/my-website/',
        onInlineTags: 'warn',
        onInlineAuthors: 'warn',
        onUntruncatedBlogPosts: 'warn',
      },
    ],
    [
      '@docusaurus/plugin-content-blog',
      {
        id: 'fuxi',
        path: 'fuxi',
        routeBasePath: 'fuxi',
        showReadingTime: true,
        blogSidebarTitle: '复习资料',
        blogSidebarCount: 'ALL',
        feedOptions: {
          type: ['rss', 'atom'],
          xslt: true,
        },
        editUrl: 'https://github.com/Xuperbad/Paper-Pen/tree/main/my-website/',
        onInlineTags: 'warn',
        onInlineAuthors: 'warn',
        onUntruncatedBlogPosts: 'warn',
      },
    ],
    [
      '@docusaurus/plugin-content-blog',
      {
        id: 'zhenti',
        path: 'zhenti',
        routeBasePath: 'zhenti',
        showReadingTime: true,
        blogSidebarTitle: '真题练习',
        blogSidebarCount: 'ALL',
        feedOptions: {
          type: ['rss', 'atom'],
          xslt: true,
        },
        editUrl: 'https://github.com/Xuperbad/Paper-Pen/tree/main/my-website/',
        onInlineTags: 'warn',
        onInlineAuthors: 'warn',
        onUntruncatedBlogPosts: 'warn',
      },
    ],
  ],

  themes: ['@docusaurus/theme-mermaid'],

  stylesheets: [
    {
      href: 'https://cdn.jsdelivr.net/npm/katex@0.13.24/dist/katex.min.css',
      type: 'text/css',
      integrity:
        'sha384-odtC+0UGzzFL/6PNoE8rX/SPcQDXBJ+uRepguP4QkPCm2LBxH3FA3y+fKSiJ+AmM',
      crossorigin: 'anonymous',
    },
  ],

  scripts: [
    {
      src: '/js/password-protection.js',
      async: false,
    },
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      blog: {
        sidebar: {
          groupByYear: false, // 关闭按年分组
        },
      },
      navbar: {
        title: 'Paper-Pen',
        logo: {
          alt: 'Paper and Pen',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: '❤️Books',
          },
          {
            type: 'docSidebar',
            sidebarId: 'historySidebar',
            position: 'left',
            label: '🧡History',
            docsPluginId: 'history',
          },
          {
            type: 'docSidebar',
            sidebarId: 'notesSidebar',
            position: 'left',
            label: '💛Notes',
            docsPluginId: 'notes',
          },
          {to: '/blog', label: '💚Articles', position: 'left'},
          //暂时关闭Showcase功能
          // {to: '/showcase', label: 'Showcase', position: 'left'},
          // {
          //   href: 'https://github.com/Xuperbad/Paper-Pen',
          //   label: 'GitHub',
          //   position: 'right',
          // },
          {to: '/zhejiang', label: '💙Zhejiang', position: 'left'},
          {to: '/fuxi', label: '💜fuxi', position: 'left'},
          {to: '/zhenti', label: '🖤zhenti', position: 'left'},
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              {
                label: 'Books',
                to: '/docs/intro',
              },
              {
                label: 'Notes',
                to: '/notes/intro',
              },
              {
                label: 'History',
                to: '/history/intro',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Stack Overflow',
                href: 'https://stackoverflow.com/questions/tagged/docusaurus',
              },
              {
                label: 'Discord',
                href: 'https://discordapp.com/invite/docusaurus',
              },
              {
                label: 'X',
                href: 'https://x.com/docusaurus',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'Blog',
                to: '/blog',
              },
              {
                label: 'GitHub',
                href: 'https://github.com/facebook/docusaurus',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} My Project, Inc. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
      mermaid: {
        theme: {light: 'default', dark: 'dark'},
        options: {
          maxTextSize: 200000, // 增加到 200,000 字符
        },
      },
    }),
};

export default config;
