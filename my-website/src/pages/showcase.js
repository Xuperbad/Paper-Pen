import React from 'react';
import Layout from '@theme/Layout';

// 书籍数据
const booksData = [
  {
    title: 'JavaScript 高级程序设计',
    cover: '/img/books/js-advanced.jpg',
    link: '/docs/javascript-advanced',
  },
  {
    title: 'React 技术揭秘',
    cover: '/img/books/react-secrets.jpg',
    link: '/docs/react-secrets',
  },
  {
    title: 'Node.js 实战',
    cover: '/img/books/nodejs-practice.jpg',
    link: '/docs/nodejs-practice',
  },
  {
    title: 'TypeScript 编程',
    cover: '/img/books/typescript.jpg',
    link: '/docs/typescript',
  },
  {
    title: 'Vue.js 设计与实现',
    cover: '/img/books/vue-design.jpg',
    link: '/docs/vue-design',
  },
  {
    title: 'Python 编程快速上手',
    cover: '/img/books/python-automate.jpg',
    link: '/docs/python-automate',
  },
  {
    title: 'CSS 权威指南',
    cover: '/img/books/css-guide.jpg',
    link: '/docs/css-guide',
  },
  {
    title: 'HTML5 与 CSS3 实战',
    cover: '/img/books/html5-css3.jpg',
    link: '/docs/html5-css3',
  },
  {
    title: 'Git 版本控制管理',
    cover: '/img/books/git-version.jpg',
    link: '/docs/git-version',
  },
  {
    title: 'Docker 容器技术',
    cover: '/img/books/docker.jpg',
    link: '/docs/docker',
  },
  {
    title: 'MongoDB 权威指南',
    cover: '/img/books/mongodb.jpg',
    link: '/docs/mongodb',
  },
  {
    title: 'Redis 设计与实现',
    cover: '/img/books/redis.jpg',
    link: '/docs/redis',
  },
];

function BookCard({title, cover, link}) {
  return (
    <div className="col col--2 margin-bottom--lg" style={{display: 'flex', justifyContent: 'center'}}>
      <a href={link} style={{textDecoration: 'none', color: 'inherit'}}>
        <div style={{
          transition: 'transform 0.2s',
          cursor: 'pointer',
          textAlign: 'center'
        }}
             onMouseEnter={(e) => e.currentTarget.style.transform = 'translateY(-2px)'}
             onMouseLeave={(e) => e.currentTarget.style.transform = 'translateY(0)'}>
          {/* 书籍封面 */}
          <div
            style={{
              width: '120px',
              height: '180px',
              backgroundColor: '#f8f9fa',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '14px',
              color: '#6c757d',
              border: '2px dashed #dee2e6',
              borderRadius: '8px',
              marginBottom: '12px',
              flexDirection: 'column',
              gap: '8px'
            }}>
            <div style={{fontSize: '24px'}}>📚</div>
            <div style={{fontSize: '12px', textAlign: 'center', padding: '0 8px'}}>
              {title.length > 10 ? title.substring(0, 10) + '...' : title}
            </div>
          </div>
          {/* 书名 */}
          <div style={{
            fontSize: '14px',
            fontWeight: '500',
            maxWidth: '120px',
            lineHeight: '1.3',
            wordBreak: 'break-word'
          }}>
            {title}
          </div>
        </div>
      </a>
    </div>
  );
}

export default function Showcase() {
  return (
    <Layout
      title="书库"
      description="精选技术书籍和学习资源">

      <main className="margin-vert--lg">
        <div className="container">
          {/* 页面标题 - 参考 Blog 页面位置 */}
          <div className="row margin-bottom--lg">
            <div className="col text--center">
              <h1 style={{
                fontSize: '2.5rem',
                fontWeight: 'bold',
                margin: '1rem 0 2rem 0',
                color: 'var(--ifm-heading-color)'
              }}>
                书库
              </h1>
            </div>
          </div>

          {/* 书籍列表 - 6列2行布局 */}
          <div className="row" style={{justifyContent: 'center'}}>
            {booksData.map((book, idx) => (
              <BookCard key={idx} {...book} />
            ))}
          </div>
        </div>
      </main>
    </Layout>
  );
}
