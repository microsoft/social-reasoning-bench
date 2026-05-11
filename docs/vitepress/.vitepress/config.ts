import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'SocialReasoningBench',
  description: 'Evaluate the social reasoning capabilities of LLM agents in multi-agent environments',
  base: '/social-reasoning-bench/',

  head: [
    ['link', { rel: 'icon', href: '/favicon.ico' }],
  ],

  themeConfig: {
    nav: [
      { text: 'Quick Start', link: '/' },
      { text: 'Installation', link: '/installation' },
      { text: 'Benchmarks', link: '/running-benchmarks' },
      { text: 'Experiments', link: '/experiments' },
      { text: 'Data Generation', link: '/generating-data' },
      { text: 'LLMs', link: '/llm' },
      { text: 'Results', link: '/results' },
      { text: 'GitHub', link: 'https://github.com/microsoft/social-reasoning-bench' },
    ],

    sidebar: [
      {
        text: 'Get Started',
        items: [
          { text: 'Quick Start', link: '/' },
          { text: 'Installation', link: '/installation' },
        ],
      },
      {
        text: 'User Guide',
        items: [
          { text: 'Running benchmarks', link: '/running-benchmarks' },
          { text: 'Designing experiments', link: '/experiments' },
          { text: 'Generating data', link: '/generating-data' },
          { text: 'LLMs', link: '/llm' },
          { text: 'Results', link: '/results' },
        ],
      },
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/microsoft/social-reasoning-bench' },
    ],

    search: {
      provider: 'local',
    },

    outline: {
      level: [2, 3],
    },

    editLink: {
      pattern: 'https://github.com/microsoft/social-reasoning-bench/edit/main/docs/vitepress/:path',
      text: 'Edit this page on GitHub',
    },

    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright 2024-2026 Microsoft Corporation',
    },
  },
})
