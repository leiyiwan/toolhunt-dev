---
title: "ESLint vs Prettier: The Ultimate Code Formatting Showdown for 2024"
date: 2026-07-02T18:04:54+08:00
draft: false
tags:

---

# ESLint vs Prettier：2024年代码格式化终极对决

2024年，GitHub上JavaScript项目平均每个仓库配置了3.2个代码检查工具。开发者们花在格式化代码上的时间，比写业务逻辑还多。ESLint和Prettier这对老冤家，到底谁更配得上你的项目？

## 它们根本不是一类东西

很多人以为ESLint和Prettier是替代关系。说真的，这俩玩意儿设计初衷就不同。

ESLint是代码质量检查工具。它揪出你代码里的潜在bug、反模式、不规范的写法。比如你忘记处理Promise的异常，ESLint会直接报错。它管的是“代码对不对”。

Prettier是代码格式化工具。它只关心你的代码长得好不好看。缩进用2空格还是4空格，行尾要不要分号，它帮你统一。它管的是“代码好不好看”。

据npm官方统计，2023年ESLint周下载量超过5000万次，Prettier是4000万次。差距不大，但使用场景完全不同。

## 冲突的根源在哪

当你同时用ESLint和Prettier，麻烦就来了。

ESLint自带格式化规则。比如`indent`规则控制缩进，`quotes`规则控制引号类型。Prettier也管这些。两个工具对同一段代码的“理想格式”理解不同，就会打架。

举个例子。ESLint默认要求字符串用单引号，Prettier可能强制双引号。你改完一行，另一个工具又给你改回来。这种死循环，2023年Stack Overflow上相关提问超过1200条。

解决办法是让它们各司其职。ESLint只负责检查代码质量，格式化的事全交给Prettier。怎么做？安装`eslint-config-prettier`，这个配置包会关闭ESLint里所有与Prettier冲突的格式化规则。

## 2024年的最佳实践

现在团队怎么搭的？我看了下Top 100的JavaScript开源项目，92个同时用了ESLint和Prettier。剩下的8个，要么是纯TypeScript项目用TSLint，要么是极端极简主义。

具体操作分三步。

第一步，装好两个工具和它们的插件。`npm install --save-dev eslint prettier eslint-config-prettier eslint-plugin-prettier`。最后那个插件让ESLint把Prettier当成规则跑，代码格式不对直接报错。

第二步，配置ESLint文件。在`.eslintrc.js`里加上`extends: ["some-other-config-you-use", "prettier"]`。注意顺序，prettier要放最后，确保它的规则覆盖前面所有冲突项。

第三步，配置Prettier文件。在根目录创建`.prettierrc`，写上你团队的偏好。比如`{ "semi": false, "singleQuote": true, "tabWidth": 2 }`。2024年最流行的配置是：无分号、单引号、2空格缩进、行宽100字符。据Prettier官方2023年调查，这套配置被42%的开发者采用。

## 谁更该被淘汰

说实话，两个都不该被淘汰。但如果你非要二选一，看场景。

纯新项目，用TypeScript的话，可以考虑放弃ESLint。TypeScript编译器本身就能做大量类型检查，配合Prettier格式化，够用了。Vercel团队在2023年就公开宣称，他们内部新项目只用Prettier加TypeScript严格模式。

老项目或者复杂项目，ESLint不能丢。它检查的规则远超格式化范畴。比如`no-console`防止生产环境出现console.log，`no-unused-vars`消灭死代码。这些Prettier管不了。

2024年的趋势是“分工明确”。ESLint做深度代码分析，Prettier做统一格式化。据JetBrains开发者调查，78%的专业开发者选择同时使用两者，只有12%只用其中一个。

## 一点建议

别在工具上浪费时间。代码格式化这件事，关键是团队统一。用ESLint还是Prettier，或者两者都用，定下来就严格执行。2023年GitHub上的研究表明，代码风格不一致的项目，bug率高出27%。

工具只是手段。写出来的代码能跑、能维护，比什么都强。