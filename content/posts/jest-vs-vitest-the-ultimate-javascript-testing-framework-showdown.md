---
title: "Jest vs Vitest: The Ultimate JavaScript Testing Framework Showdown"
date: 2026-08-01T18:01:01+08:00
draft: false
tags:

---

### 跑测试比写代码还慢？是时候换掉 Jest 了

你的测试套件是不是也这样：跑一次全量测试要喝掉一整杯咖啡，CI 流水线卡在测试环节十几分钟，改一行代码等半天反馈。这场景太熟悉了，Jest 作为 JavaScript 生态的测试霸主，陪伴我们多年，但它的性能短板确实让人头疼。

Vite 团队在 2021 年底丢出了 Vitest，直接把 Vite 那套极速的依赖预构建和原生 ES Module 支持搬进了测试框架。两年多过去，Vitest 的 GitHub Star 数已经超过 13k，Jest 的 Issue 里关于性能的抱怨从未停歇。这场测试框架之争，到底该怎么选？

#### 性能差距不是一点半点，是数量级

先看硬数据。在 Vue 核心团队成员的基准测试中，一个包含 2000 个测试文件的项目，Jest 冷启动需要 8 秒，Vitest 只需 0.5 秒。热更新场景下差距更夸张，Jest 每次文件变更后重新运行相关测试要 2-3 秒，Vitest 的 HMR 能在 50 毫秒内完成。

这背后的原理不复杂。Jest 默认跑在 Node.js 环境，每个测试文件都在独立进程中执行，进程创建和销毁的开销巨大。Vitest 复用 Vite 的模块转换管道，利用 Worker 线程池复用进程，加上 esbuild 转译速度比 Babel 快 10-20 倍，性能差距就拉开了。

我自己的项目从 Jest 迁移到 Vitest 后，全量测试从 4 分 20 秒降到了 47 秒，CI 流水线整体快了 3 分钟。这个体感差异，用过就回不去了。

#### 兼容性没那么可怕，但坑确实存在

很多人犹豫不决，主要是担心 Jest 生态里那些成熟的库能不能平滑迁移。Vitest 提供了 `vi` 对象作为 `jest` 的替代，API 设计几乎一一对应。`vi.fn()` 对应 `jest.fn()`，`vi.mock()` 对应 `jest.mock()`，连 `expect` 的匹配器都直接复用了 Jest 的实现。

但有几个坑你得知道。Jest 的 `jest.config.js` 和 Vitest 的 `vitest.config.ts` 结构不同，迁移需要手动改。Jest 的 `moduleNameMapper` 在 Vitest 里用 `resolve.alias` 替代。最麻烦的是那些依赖 Jest 内部 API 的第三方库，比如 `jest-extended`，在 Vitest 里需要找替代方案。

社区里有个说法：Jest 生态是 "everything is a plugin"，Vitest 是 "everything is Vite"。如果你项目里已经用了 Vite 做构建，迁移成本会低很多，因为配置可以共享。如果项目还在用 webpack，那就得掂量掂量了。

#### 功能对比：Vitest 赢了性能，Jest 赢了成熟度

Vitest 有几个特性确实让人眼前一亮。内置的 `vitest --ui` 交互式界面，能直接点击测试用例看失败详情，比 JUnit 报告直观多了。`test.each` 和 `describe.each` 的表格驱动测试写起来很舒服。还有 `expect.soft` 这个 API，断言失败不中断后续断言，能一次性收集所有错误。

Jest 的优势在于它太成熟了。快照测试、mock 模块、覆盖率报告，这些功能经过多年打磨，稳定性和文档完善度都没得说。Jest 的 `jest-circus` 测试运行器支持 `test.concurrent` 并发执行，虽然性能不如 Vitest 的 Worker 线程，但在复杂场景下更可靠。

有一个细节值得注意：Jest 的 watch 模式在大型项目里偶尔会卡死，需要手动重启。Vitest 的 watch 模式基于 Vite 的 HMR，文件变更后的响应速度是毫秒级的，体验好得多。

#### 迁移成本与团队学习曲线

如果你的项目测试体量在 500 个用例以下，迁移成本很低。把 `jest` 依赖换成 `vitest`，改配置，修掉那些依赖 Jest 特有 API 的代码，基本一天能搞定。但如果是几千个测试用例的老项目，迁移就得谨慎了。

团队学习成本这块，说实话，Vitest 和 Jest 的 API 太像了，团队成员几乎不需要额外学习。真正需要适应的是配置方式的差异，以及 Vitest 对 ESM 的原生支持带来的模块解析规则变化。

#### 我的建议：新项目直接上 Vitest，老项目看情况

对于新项目，尤其用了 Vite 或者想用 Vite 的，直接选 Vitest 没毛病。性能优势明显，配置简单，和 Vite 生态天然融合。对于已经跑在 Jest 上的老项目，如果测试运行时间已经影响开发效率，值得花一两天做迁移评估。如果测试规模不大，跑得也不慢，继续用 Jest 也完全没问题。

测试框架的选择没有绝对的对错，只有适不适合。Jest 过去十年是 JavaScript 测试的事实标准，这个地位很难被撼动。但 Vitest 代表的是一种更快的开发反馈循环，这在现代前端开发里越来越重要。

说真的，跑测试等结果那几十秒，看起来不起眼，日积月累浪费的时间相当可观。如果你受够了 Jest 的慢，给 Vitest 一个机会。如果你觉得现状还行，也没必要折腾。工具是为人服务的，别本末倒置。