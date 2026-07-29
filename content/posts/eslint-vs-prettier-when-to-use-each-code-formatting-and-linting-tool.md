---
title: "ESLint vs Prettier: When to Use Each Code Formatting and Linting Tool"
date: 2026-07-29T10:05:52+08:00
draft: false
tags:

---

# ESLint vs Prettier：代码格式化和质量检查，到底该用谁？

2024年，GitHub上JavaScript项目里，ESLint的下载量超过4亿次，Prettier也突破了1.5亿。两个工具几乎成了前端开发的标配。但很多人搞不清：它们到底有什么区别？能不能只用一个？

说白了，ESLint和Prettier干的不是同一件事。一个抓逻辑错误，一个管代码长相。

## 核心分歧：抓虫 vs 整容

ESLint本质上是个“代码警察”。它检查的是你写没写错——变量定义了没用上，函数里有未处理的Promise，用了`==`而不是`===`。这些是实打实的逻辑风险，跑起来可能出Bug。

Prettier则是个“理发师”。它只关心代码长得是否整齐：缩进是2个空格还是4个，行尾要不要分号，对象花括号前后有没有空格。它不管你的代码对不对，只管好不好看。

一个真实的例子：你用`var a = 1`，ESLint会警告“请用`let`或`const`”。Prettier则沉默不语，因为它只负责把`var a = 1`排版成`var a = 1`（如果配置了分号，就加个分号）。逻辑问题它不碰。

据ESLint官方文档，它内置了超过200条规则，覆盖常见错误、最佳实践、代码风格。Prettier的规则则少得多，大约20条左右，全是关于格式的。

## 重叠地带：它们确实会打架

问题出在“代码风格”这个领域。ESLint也管一些格式问题，比如缩进、引号、逗号。Prettier也管。于是两把尺子量同一根线，结果经常不一样。

举个例子：ESLint默认要求字符串用单引号，Prettier默认用双引号。你保存文件时，Prettier把单引号改成双引号，ESLint又报错说“应该用单引号”。死循环。

更常见的冲突是缩进。ESLint规则`indent`要求4个空格，Prettier配置了2个空格。每次格式化，Prettier把缩进改成2，ESLint立刻报红。团队里有人装Prettier插件，有人不装，代码提交时一片混乱。

据Stack Overflow 2023年调查，超过40%的前端开发者遇到过ESLint和Prettier的配置冲突。这不是小概率事件。

## 怎么选：看场景，不是看名气

**纯逻辑检查场景，选ESLint就够了。** 比如你写Node.js后端脚本，不需要团队统一格式，只求代码没Bug。这时候ESLint的`no-unused-vars`、`no-console`这些规则就够用。Prettier反而多余。

**多人协作项目，必须两个一起上。** 但得让它们“分工明确”。业内主流做法是：Prettier负责所有格式规则，ESLint关闭所有与格式相关的规则（比如`indent`、`quotes`、`semi`），专心抓逻辑问题。

具体怎么配？用`eslint-config-prettier`这个包，它能一键关闭ESLint里和Prettier冲突的规则。据npm数据，这个包每周下载量超过800万次，说明这是行业共识。

**单文件快速格式化，Prettier更顺手。** 你改完一个文件，按Ctrl+S，Prettier自动把整段代码排整齐。ESLint的自动修复功能（`--fix`）也能做类似事，但它更保守，只修它认为“错误”的格式，不修“不美观”的格式。

## 一个常见误区：用了Prettier就不需要ESLint

这种想法很危险。Prettier不检查未定义变量、不检查潜在类型错误、不检查异步代码的Promise链。你把代码写得再整齐，如果逻辑有洞，上线照样崩。

反过来，只用ESLint也不行。ESLint的格式规则写得再细，也比不上Prettier的“无脑统一”。Prettier的策略是“不给你选择”，团队里所有人都用同一套格式，省去争论。ESLint的格式规则允许自定义，结果就是A用4空格，B用2空格，C用Tab——都在规则范围内，但看着就是乱。

据Google的JavaScript风格指南建议，团队应该统一使用Prettier处理格式，ESLint只处理逻辑。这是一个被验证过的组合。

## 实际配置建议

如果你从零开始，可以这样搭：

1. 安装ESLint和Prettier，以及`eslint-config-prettier`。
2. 在`.eslintrc`里继承`prettier`配置，关闭格式规则。
3. 在`.prettierrc`里定义团队统一的格式（比如单引号、无分号、2空格）。
4. 用`eslint-plugin-prettier`（可选），让ESLint把Prettier作为规则运行。这样你运行`eslint --fix`时，会同时修逻辑和格式。

据GitHub上的开源项目统计，React、Vue、Next.js的官方脚手架都默认集成了这个方案。说明它是经过大规模验证的。

## 结尾

ESLint和Prettier不是竞争对手，是互补工具。一个管“别写错”，一个管“别乱写”。单用哪个都会留下盲区。

团队配置时，别让它们打架。让Prettier管长相，ESLint管脑子。代码既不会崩，也不会丑。