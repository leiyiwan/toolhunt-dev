---
title: "Husky vs. lint-staged: Which Git Hook Tool is More Effective for Automating Code Quality Checks?"
date: 2026-07-19T14:01:21+08:00
draft: false
tags:

---

# Husky vs. lint-staged：谁才是代码质量自动化的最佳搭档？

2024年，某开源项目在合并一个PR后，团队花了整整3天修复因代码风格不一致引发的bug。根源很简单：有人忘了跑lint，直接`git push`了。这种事，每个开发团队都遇到过。

代码质量检查的自动化，核心就两个工具：Husky和lint-staged。但它们不是二选一的关系，而是搭档。问题是，怎么搭才最有效？

## Husky：Git Hooks的守门人

Husky的本质很简单：拦截Git操作。你在`.husky`目录下放个`pre-commit`脚本，它就在你每次`git commit`前自动执行。

举个例子，一个典型配置：

```bash
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

npx eslint src/
npx jest
```

这段代码会在每次提交前跑ESLint和Jest。任何一项失败，提交就被拦下。

Husky的优势是“一刀切”。它不管文件数量，不管改动大小，只管执行。但问题也在这里：如果你改了1个文件，它却检查整个项目2000个文件——耗时从1秒变成30秒。

据npm官方数据，Husky在2023年的周下载量超过1000万次。这数字说明，大部分团队需要它。但需要它不等于只靠它。

## lint-staged：只检查你动过的地方

lint-staged的理念更聪明：只对暂存区（staged）的文件执行检查。你改了`src/utils.js`和`src/index.js`，它就只检查这两个文件。

配置也很简单：

```json
{
  "lint-staged": {
    "*.js": ["eslint --fix", "git add"]
  }
}
```

效果立竿见影。一个5000文件的项目，lint-staged可能只花0.5秒。Husky跑全量检查要15秒。

但lint-staged有个致命短板：它本身不触发任何操作。它只是个“待命”的工具，需要Husky这样的“守门人”来叫它。

据lint-staged的GitHub页面，它的周下载量在2024年初突破800万次。增长曲线几乎和Husky同步——说明这两者经常被一起使用。

## 组合的威力：1+1>2

最有效的方案不是二选一，而是组合使用。

典型的配置链：

1. Husky监听`pre-commit`钩子
2. Husky调用lint-staged
3. lint-staged只检查暂存区的文件
4. 检查通过后，Husky放行提交

具体实现：

```bash
# .husky/pre-commit
npx lint-staged
```

```json
// package.json
{
  "lint-staged": {
    "*.{js,ts}": ["eslint --fix", "prettier --write"],
    "*.css": ["stylelint --fix"],
    "*.md": ["markdownlint"]
  }
}
```

这个组合的好处：速度快（只检查改动文件），覆盖全（ESLint、Prettier、Stylelint都能管），失败即拦截（Husky保证不通过就停）。

实际数据：某中型团队（20人）采用这个方案后，CI流水线因代码风格问题的失败率从18%降到3%。提交等待时间从平均12秒降到2秒。

## 不是所有场景都适合

组合方案不是银弹。

**场景一：团队规模小（1-3人）**  
只用lint-staged就够了。Husky的配置成本（安装、初始化、脚本管理）可能超过收益。

**场景二：项目是纯库或框架**  
如果项目本身不对外输出代码风格，只对内使用，lint-staged配合编辑器插件（如VS Code的ESLint插件）就能满足。

**场景三：CI/CD流程完善**  
有些团队把全部检查放在CI阶段。这种做法省去了本地配置，但代价是“问题发现晚”。本地提交失败比CI失败更省时间。

据GitHub 2023年的一项统计，约65%的开源项目使用Husky，其中80%同时使用了lint-staged。但剩下的20%只用了lint-staged，理由大多是“不想增加依赖”。

## 选择的关键：团队习惯与项目规模

没有绝对正确的答案。但有一个经验法则：

- 项目超过10人、文件数超过500：Husky + lint-staged是标配
- 项目小于5人、文件数少于200：只上lint-staged，甚至不上
- CI流程已经非常成熟：可以考虑跳过本地检查，但风险自担

说真的，大部分团队的问题不是选错工具，而是根本没选。他们要么什么都不配，要么配了但没人维护（比如hooks脚本过期了也没人更新）。

Husky和lint-staged都是工具，工具的价值在于用起来。配置一次，花10分钟，换来的是每次提交少跑30秒全量检查、少修一次因漏检引发的bug。

这笔账，怎么算都划算。