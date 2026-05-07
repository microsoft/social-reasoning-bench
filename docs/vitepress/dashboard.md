---
sidebar: false
aside: false
layout: page
footer: false
---

<div class="dashboard-wrapper">
  <iframe src="/dashboard-app.html?load=/dashboard-data/"></iframe>
</div>

<style scoped>
.dashboard-wrapper {
  width: 100vw;
  height: calc(100vh - var(--vp-nav-height, 64px));
  margin-left: calc(-50vw + 50%);
  overflow: hidden;
}
.dashboard-wrapper iframe {
  width: 100%;
  height: 100%;
  border: none;
  display: block;
}
</style>
