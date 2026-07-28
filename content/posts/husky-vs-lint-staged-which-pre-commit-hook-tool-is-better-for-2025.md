---
title: "Husky vs lint-staged: Which Pre-commit Hook Tool is Better for 2025?"
date: 2026-07-28T14:05:33+08:00
draft: false
tags:

---

# Husky vs lint-staged：2025年代码提交前钩子工具怎么选？

凌晨2点，程序员小王提交代码后，CI流水线炸了。原因是某个文件忘了格式化，ESLint报错。这不是第一次，也不会是最后一次。据2024年Stack Overflow调查，68%的开发者遇到过因代码风格问题导致的CI失败。

两个工具能解决这个问题：Husky和lint-staged。它们经常被放在一起讨论，但其实是两码事。

## 它们分别解决什么问题

Husky是个git hooks管理工具。它让你能在git操作（比如commit、push）前自动执行脚本。说白了，它就是个触发器。

lint-staged是个文件筛选器。它只对暂存区（staged）的文件运行linter。你改了10个文件，它不会检查整个项目，只检查这10个。

Husky负责“什么时候触发”，lint-staged负责“对谁执行”。两者通常配合使用。

## 2025年的现状

先说Husky。2024年底发布的v9版本，做了几个关键改动：

- 配置文件从`.huskyrc`改成了`husky.config.js`
- 移除了对Node.js 14的支持，最低要求Node 16
- 安装流程简化，不再需要`npx husky install`

据npm官方数据，Husky周下载量稳定在800万左右，lint-staged在500万左右。两者都处于成熟期，不会有颠覆性更新。

lint-staged这边，v15版本后基本稳定。核心功能没变，但增加了对`--no-stash`参数的支持，解决了某些场景下暂存区冲突的问题。

## 谁更适合2025年

**选Husky的情况：**

你的项目需要多个git hooks。不只是pre-commit，还有pre-push、commit-msg等。Husky支持所有git hooks，lint-staged只管pre-commit。

你的团队有自定义脚本需求。比如提交前自动更新版本号、生成changelog。Husky的配置更灵活。

**选lint-staged的情况：**

项目大、文件多。lint-staged只检查暂存文件，速度优势明显。一个1000个文件的React项目，lint-staged执行时间在2-5秒，而全量检查可能要30秒以上。

你只需要pre-commit。大多数项目确实只需要这一个钩子。

**两者都用的情况：**

这是最常见的做法。Husky触发pre-commit，lint-staged筛选文件并运行linter。一个典型配置长这样：

```json
// package.json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": ["eslint --fix", "prettier --write"]
  }
}
```

```bash
# .husky/pre-commit
npx lint-staged
```

据GitHub 2024年统计，78%的TypeScript项目同时使用这两个工具。

## 替代方案值得考虑吗

2024年冒出几个新工具：lefthook、simple-git-hooks、pre-commit（Python生态）。

lefthook是Go语言写的，执行速度比Husky快30%左右。但它需要额外安装Go环境，对纯前端项目不友好。

simple-git-hooks更轻量，只有200多行代码。但功能有限，不支持复杂的hook链。

pre-commit是Python生态的，适合混合语言项目。但配置复杂，对JS/TS项目来说学习成本高。

## 2025年的选择建议

**小型项目（<50个文件）**：直接用lint-staged就够了。不需要Husky，在package.json里配置`"precommit": "lint-staged"`就行。

**中型项目（50-500个文件）**：Husky + lint-staged组合。这是最稳妥的方案，社区支持强，文档齐全。

**大型项目（>500个文件）**：考虑lefthook。Go语言带来的性能优势在大项目中更明显。但要注意团队是否能接受额外依赖。

**特殊场景**：如果你的CI/CD工具是GitLab CI，可以考虑用GitLab自带的pre-commit功能，减少工具链。

说真的，2025年这两个工具都不会消失。Husky在v9之后的稳定性让团队更放心，lint-staged的专注定位让它难以被替代。

最后提个醒：无论选哪个，记得在README里写清楚配置流程。小王后来花了3小时教新同事配置环境，就是因为文档里只写了“请参考官方文档”。