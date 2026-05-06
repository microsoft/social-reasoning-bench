import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'SRBench-Benchmark',
  description: 'Evaluating social reasoning capabilities of LLM agents',
  base: '/srbench/',

  head: [
    ['link', { rel: 'icon', href: '/srbench/favicon.ico' }],
  ],

  themeConfig: {
    nav: [
      { text: 'Introduction', link: '/introduction' },
      { text: 'Results', link: '/results' },
      { text: 'Dashboard', link: '/dashboard' },
      {
        text: 'Packages',
        items: [
          { text: 'srbench', link: '/running-benchmarks' },
          { text: 'srbench-data-gen', link: '/generating-data' },
          { text: 'WhimsyGen', link: '/whimsygen' },
          { text: 'Privacy Judge', link: '/privacy-judge' },
        ],
      },
      { text: 'GitHub', link: 'https://github.com/microsoft/srbench' },
    ],

    sidebar: [
      {
        text: 'Report',
        items: [
          { text: 'Introduction', link: '/introduction' },
          { text: 'Benchmarks', link: '/benchmarks' },
          { text: 'Evaluation', link: '/evaluation' },
          { text: 'Results', link: '/results' },
        ],
      },
      {
        text: 'Guide',
        items: [
          { text: 'Installation', link: '/installation' },
          { text: 'Reproduction', link: '/reproduction' },
          { text: 'Running Benchmarks', link: '/running-benchmarks' },
          { text: 'Experiments', link: '/new-experiments' },
          { text: 'Data Generation', link: '/generating-data' },
          { text: 'WhimsyGen', link: '/whimsygen' },
          { text: 'Privacy Judge', link: '/privacy-judge' },
        ],
      },
      {
        text: 'Internals',
        items: [
          { text: 'Architecture', link: '/architecture' },
          { text: 'Calendar Scheduling', link: '/calendar-internals' },
          { text: 'Form Filling', link: '/form-filling-internals' },
          { text: 'Marketplace', link: '/marketplace-internals' },
          { text: 'Adding a Benchmark', link: '/new-benchmarks' },
        ],
      },
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/microsoft/srbench' },
    ],

    search: {
      provider: 'local',
    },

    outline: {
      level: [2, 3],
    },

    editLink: {
      pattern: 'https://github.com/microsoft/srbench/edit/main/docs/vitepress/:path',
      text: 'Edit this page on GitHub',
    },

    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright 2024-2026 Microsoft Corporation',
    },
  },
})
