import React from 'react';
import Layout from '@theme/Layout';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

const FeatureList = [
  {
    title: '易于使用',
    description: (
      <>
        Docusaurus 从一开始就被设计为易于安装和使用，
        让你快速启动并运行你的网站。
      </>
    ),
  },
  {
    title: '专注于重要的事情',
    description: (
      <>
        Docusaurus 让你专注于你的文档，我们来处理其他事务。
        只需将你的文档移动到 <code>docs</code> 目录中。
      </>
    ),
  },
  {
    title: '基于 React 构建',
    description: (
      <>
        通过重用 React 来扩展或自定义你的网站布局。
        Docusaurus 可以在重用相同页眉和页脚的同时进行扩展。
      </>
    ),
  },
];

function Feature({title, description}) {
  return (
    <div className="col col--4">
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function Features() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title="功能特性"
      description="了解 Docusaurus 的主要功能特性">
      <header className="hero hero--primary">
        <div className="container">
          <h1 className="hero__title">功能特性</h1>
          <p className="hero__subtitle">探索 Docusaurus 的强大功能</p>
        </div>
      </header>
      <main>
        <section className="features">
          <div className="container">
            <div className="row">
              {FeatureList.map((props, idx) => (
                <Feature key={idx} {...props} />
              ))}
            </div>
          </div>
        </section>
        
        <section className="padding-vert--lg">
          <div className="container">
            <div className="row">
              <div className="col col--8 col--offset-2">
                <h2>更多功能</h2>
                <ul>
                  <li><strong>搜索功能</strong>：集成 Algolia DocSearch</li>
                  <li><strong>版本控制</strong>：支持文档版本管理</li>
                  <li><strong>国际化</strong>：多语言支持</li>
                  <li><strong>主题系统</strong>：可自定义外观</li>
                  <li><strong>插件生态</strong>：丰富的插件扩展</li>
                  <li><strong>SEO 优化</strong>：搜索引擎友好</li>
                </ul>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
