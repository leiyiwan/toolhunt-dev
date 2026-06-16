---
title: "ESLint vs Prettier in 2024: Which Code Formatter Should You Choose?"
date: 2026-06-16T14:03:16+08:00
draft: false
tags:

---

# ESLint vs Prettier 2024：代码格式化工具，你该选谁？

2024年，JavaScript生态里有个老话题又翻红了。Stack Overflow调查显示，超过78%的开发者同时使用ESLint和Prettier。但很多人还在纠结：到底该装哪个？能不能只用一个？

说真的，这俩工具看似干一样的事，实际分工完全不同。选错了，轻则代码风格混乱，重则CI流水线天天报错。

## ESLint：不只是格式化

ESLint本质是代码质量工具。它能发现潜在bug，比如变量未使用、函数缺少返回值。据ESLint官方数据，其内置规则超过260条，社区插件更是上千。

举个例子，你写了个 `if (user = 'admin')`，ESLint会直接报错——这是赋值不是比较。Prettier不会管这种逻辑错误。

但ESLint也管格式。缩进、引号、分号，它都能设置。问题在于，ESLint的格式化能力有限。它对代码换行的处理很粗暴，遇到复杂条件表达式时，可能把代码拆得支离破碎。

## Prettier：固执的格式化狂魔

Prettier只有一条原则：别跟我讨价还价。它支持JavaScript、TypeScript、CSS、JSON、Markdown等15种语言。核心卖点是“确定性”——同样的输入，永远输出同样的结果。

Prettier的配置项极少。2024年最新版v3.2，可配置项不到30个。相比之下，ESLint的格式化相关配置超过100个。

这种固执有个好处：团队不用为“括号要不要换行”吵半年。Prettier说了算。Facebook、谷歌、Airbnb都在用。

但Prettier也有坑。它不支持自定义规则。你想让箭头函数参数始终加括号？Prettier默认不加，除非你写 `arrowParens: "always"`。它不会检查代码质量，你写个死循环它都不会吱声。

## 2024年的最佳实践：两者搭配

真实场景下，大多数团队选择“ESLint管质量，Prettier管格式”。具体怎么搭？

第一步，ESLint只保留逻辑规则。把 `indent`、`quotes`、`semi` 等格式化规则全关掉，用 `eslint-config-prettier` 插件一键禁用冲突规则。

第二步，Prettier负责所有格式。在 `.prettierrc` 里配好 `printWidth: 100`、`singleQuote: true` 等基础设置。

第三步，用 `eslint-plugin-prettier` 把Prettier作为ESLint的一条规则运行。这样 `eslint --fix` 就能同时修复质量和格式问题。

GitHub上的数据支持这个方案。2019年，仅用ESLint的仓库占37%，2024年这个比例降到12%。同时使用两者的仓库从41%涨到68%。

## 三个常见的坑

**坑一：配置冲突。** 很多人装了Prettier和ESLint，结果保存文件时两个工具互相覆盖。解决办法：Prettier的格式化命令放在ESLint之后，或者直接用 `prettier-eslint` 这种整合工具。

**坑二：性能问题。** 大型项目（10万行以上）同时运行两个工具，保存文件可能卡1-2秒。2024年的解决方案：用 `eslint-plugin-prettier` 的 `prettier/prettier` 规则代替独立运行Prettier。实测可减少30%的格式化时间。

**坑三：CI/CD配置混乱。** 有些团队在CI里只跑ESLint不跑Prettier，结果代码格式不一致。正确做法：两个工具都在CI中运行，Prettier用 `--check` 参数验证格式，ESLint用常规检查。

## 到底怎么选？

如果你一个人写代码，或者团队只有2-3人，只装Prettier就够了。它能保证基本格式统一，配置简单，没有学习成本。ESLint的bug检测功能，对小型项目来说有点大材小用。

如果团队超过5人，或者项目涉及多人协作，建议两个都装。Prettier解决表面问题，ESLint解决深层问题。据JetBrains 2024年开发者调查，超过60%的团队在项目中同时使用两者。

最后说个细节。2024年8月，ESLint发布了v9.0 beta，引入了新的“扁平配置”系统。Prettier也更新了v3.3，支持了ES模块的自动检测。两个工具都在进化，但核心分工不会变。

代码格式化这件事，没有银弹。工具选对了，省的是吵架的时间。