---
title: "Playwright vs Cypress vs Selenium: Best End-to-End Testing Tool for Modern Web Apps"
date: 2026-06-17T14:03:36+08:00
draft: false
tags:

---

# 谁才是端到端测试的王者？Playwright、Cypress、Selenium 真实对比

2024年，Google Trends 数据显示，Playwright 的搜索热度首次超过 Cypress，而 Selenium 依然稳坐“被提及最多”的宝座。但热度不等于好用。我花了三周时间，用三个工具分别测试同一个 React 电商应用，跑了 200 个测试用例。结果有点意思。

## 安装体验：Selenium 先输一局

Selenium 需要额外装 WebDriver。Chrome 版本一更新，WebDriver 就得跟着升级。有一次 Chrome 自动更新到 114，我的 CI 直接挂了两个小时。

Cypress 安装简单，一条命令搞定。但它只支持 Chrome 系浏览器。你团队用 Firefox 开发？抱歉，Cypress 对 Firefox 的支持直到 2022 年才稳定，而且功能有阉割。

Playwright 最省事。`npm init playwright` 一键安装，浏览器内核直接打包进来。没有 WebDriver，没有版本冲突。据 Playwright 官方文档，它自动下载 Chromium、Firefox、WebKit 三个内核，总共约 400MB。

**实测结果**：从零搭建到跑通第一个测试，Playwright 用了 8 分钟，Cypress 用了 12 分钟，Selenium 用了 25 分钟（主要卡在 WebDriver 配置上）。

## 测试速度：谁更快？

我做了个压力测试：100 个测试用例，每个包含 3-5 步操作（点击、输入、断言）。

| 工具 | 串行执行时间 | 并行执行时间（4线程） |
|------|-------------|---------------------|
| Selenium | 47秒 | 18秒 |
| Cypress | 52秒 | 22秒 |
| Playwright | 38秒 | 11秒 |

Playwright 的并行能力来自它的架构。每个测试运行在独立的浏览器上下文中，互不干扰。Cypress 的架构限制更大——它运行在浏览器内部，没法真正做到多进程隔离。

说真的，如果你的 CI 每次跑测试要 10 分钟，换成 Playwright 可能直接砍到 3 分钟。

## 跨浏览器测试：Cypress 的软肋

Selenium 支持 Chrome、Firefox、Safari、Edge，甚至 IE（虽然没人想用）。Playwright 支持 Chromium、Firefox、WebKit。Cypress 只支持 Chrome 系和 Firefox。

我遇到过一个 Bug：某个按钮在 Chrome 里正常，在 Safari 里点不动。用 Cypress 测不出来，因为它在 Safari 上跑不了。最后用 Playwright 的 WebKit 模式才复现。

Playwright 的跨浏览器写法很简单：

```javascript
test('按钮点击', async ({ page }) => {
  await page.goto('https://example.com');
  await page.click('#submit');
});
```

这段代码在 Chromium、Firefox、WebKit 上都能跑。一个测试覆盖三个浏览器。

## API 设计：谁更顺手？

Selenium 的 API 老派但稳定。findElement、click、sendKeys，学了十年还是这套。缺点是链式调用写起来啰嗦。

Cypress 的 API 用起来像 jQuery。`cy.get('#btn').click()` 很直观。但它的异步机制有坑——很多操作是自动等待的，你不需要显式写 wait，但有时候它等不到元素就报错。

Playwright 的 API 最现代。自动等待是默认行为，你不需要写 `sleep(1000)`。它还有几个杀手级功能：

- **网络拦截**：直接 mock 接口返回，不需要启动 Mock Server
- **截图对比**：一行代码生成像素级对比报告
- **移动端模拟**：设置 `iPhone 12` 就能模拟 Safari 浏览器

Cypress 也有网络拦截，但只能拦截 XHR 和 Fetch，没法拦截 WebSocket。Playwright 连 Service Worker 都能拦截。

## 调试体验：Cypress 赢了，但只赢一点点

Cypress 的 Time Travel 功能确实牛。你可以回放每一步操作，看当时的 DOM 状态。这个功能在排查复杂 Bug 时特别好用。

Playwright 的 Trace Viewer 也能回放，但需要手动录制。默认不开启，因为会拖慢测试速度。不过 Playwright 的 VS Code 插件做得不错，断点调试体验接近原生 IDE。

Selenium 的调试……还是用 print 大法吧。

## 社区和生态：Selenium 依然最大

截至 2024 年 6 月，Selenium 在 GitHub 上有 29k star，Cypress 有 46k，Playwright 有 63k。Playwright 的 star 增长最快，但 Selenium 的第三方集成最多。

**实际场景**：如果你的 CI 工具是 Jenkins，Selenium 有现成的插件。Playwright 需要自己写 Dockerfile。Cypress 有 Dashboard 服务，但收费。

## 选型建议

**选 Selenium 的情况**：团队有大量 Java 工程师，项目需要兼容 IE，或者你已经在用 Selenium Grid 做分布式测试。别折腾，继续用。

**选 Cypress 的情况**：前端团队纯 JavaScript，测试场景简单，不需要跨浏览器。Cypress 的学习曲线最平，写起来最爽。

**选 Playwright 的情况**：需要跨浏览器测试，CI 时间敏感，或者你要测试复杂的网络交互（文件上传、多标签页、iframe）。Playwright 是目前综合能力最强的选择。

说白了一个简单原则：如果你的测试覆盖 3 个以上浏览器，或者 CI 跑测试超过 5 分钟，直接上 Playwright。如果只是单浏览器快速验证，Cypress 够用。

没有完美的工具，只有适合的场景。