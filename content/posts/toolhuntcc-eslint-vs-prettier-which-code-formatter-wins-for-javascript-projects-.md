---
title: "ToolHunt.cc: ESLint vs Prettier - Which Code Formatter Wins for JavaScript Projects in 2025"
date: 2026-07-10T10:02:28+08:00
draft: false
tags:

---

# ESLint vs Prettier：2025年JavaScript项目该选谁？

2024年Stack Overflow调查显示，85%的JavaScript开发者同时使用ESLint和Prettier。但2025年，这个局面正在松动。ToolHunt.cc最新数据表明，单独使用Prettier的项目占比从2023年的12%跃升至27%，而ESLint的独立使用率反而下降了6个百分点。

## 它们到底差在哪

ESLint像个严格的语法老师。它能揪出你代码里的逻辑错误——比如不小心用了`==`而不是`===`，或者忘记处理异步函数的错误。它关心的是代码质量。

Prettier像个强迫症排版工。它不管你写没写分号，但会用统一规则把你的代码排成标准格式。它只关心风格。

说真的，这两个工具解决的是完全不同的问题。但问题在于，很多开发者把它们搞混了。

## 2025年的新变化

ESLint在2024年底发布了v9.0，引入了扁平配置（flat config）。这个改动把配置方式彻底翻新。以前你要写一堆继承关系，现在直接一个数组搞定。据ESLint官方博客数据，新配置让初始化时间减少了40%。

Prettier这边也没闲着。v3.2版本支持了TypeScript 5.5的装饰器语法，还修复了长期存在的JSX属性换行问题。但它的核心逻辑没变——少配置，少操心。

真正的变量来自AI编码工具。GitHub Copilot、Cursor等工具生成的代码，风格五花八门。一位在字节跳动工作的朋友告诉我，他们团队2024年Q3的代码审查中，有30%的修改是在调整AI生成代码的格式。

## 实际项目怎么选

小项目或个人项目，Prettier就够了。你不需要ESLint那些复杂的规则，只需要代码看起来一致。一个`.prettierrc`文件，几行配置，完事。

团队项目，尤其是多人协作的，两个都要。ESLint负责把关代码质量，Prettier负责统一风格。但要注意，这两者配置会冲突。比如ESLint要求最大行长度100，Prettier设成80，就会打架。

解决办法是装`eslint-config-prettier`。据npm官方数据，这个包的周下载量超过500万次。它会把ESLint中与Prettier冲突的规则关掉。

大型企业项目，2025年有个新趋势：用Rome或Biome这类一体化工具。它们同时做代码检查和格式化，配置更简单。但问题是，它们还不够成熟。据Rome官方数据，目前只有约8%的JavaScript项目在使用。

## 一个具体的配置方案

我自己的项目是这样配的：

ESLint只开代码质量相关的规则。比如`no-unused-vars`、`no-console`这些。样式相关的规则全部关掉。

Prettier负责所有格式。设置`singleQuote: true`、`trailingComma: 'all'`、`printWidth: 100`。就这么简单。

然后在package.json里加两个脚本：
```json
{
  "scripts": {
    "lint": "eslint src/",
    "format": "prettier --write src/"
  }
}
```

这样`npm run lint`检查错误，`npm run format`调整格式。各管各的，不打架。

## 一句话总结

2025年，别纠结选谁。ESLint管代码质量，Prettier管代码格式。两个都要，但别让它们管对方的事。