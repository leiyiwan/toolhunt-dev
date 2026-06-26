---
title: "ESLint vs Prettier vs Biome: Choosing the Right Code Formatter and Linter"
date: 2026-06-26T14:02:38+08:00
draft: false
tags:

---

# ESLint、Prettier、Biome：代码格式化工具怎么选？

2024年，一个前端项目平均要装12个npm包才能跑起来。其中ESLint和Prettier几乎是标配，但最近冒出来的Biome号称能一个打俩。这三个工具到底该怎么选？

## 它们到底在干什么

先说清楚职能。ESLint是代码检查工具，抓逻辑错误和风格问题。Prettier纯粹做格式化，不管逻辑。Biome则是新玩家，想一口气把检查和格式化都干了。

拿个具体例子说明。你写了个 `if (x = 1)`，ESLint会报错：你这是赋值不是比较。Prettier不管这个，它只关心你写的空格和换行符对不对。Biome两者都管。

## ESLint：老大哥的烦恼

ESLint从2013年活到现在，生态最成熟。社区有上万个规则，TypeScript、React、Vue都有专属插件。据npm统计，ESLint周下载量超过3000万次。

但问题也在这。一个典型项目要配 `.eslintrc.js`、`.prettierrc`，还得装 `eslint-config-prettier` 来防止两者打架。配置文件的嵌套能让你怀疑人生。我见过一个项目，光ESLint配置就写了200行。

## Prettier：简单但不够用

Prettier的口号是“opinionated”，意思是你别跟我犟，按我的来。它只有十几个配置项，开箱即用。周下载量同样超过3000万次。

但Prettier只管格式，不管业务逻辑。你写了个 `var x = 1`，它不会提醒你用 `const`。这就意味着你还是要装ESLint。两个工具一起跑，CI时间至少翻倍。

## Biome：新来的挑战者

Biome是2023年开源的，用Rust写的。它的卖点就一个：快。据官方测试，格式化速度是Prettier的10倍，检查速度是ESLint的5倍。

更关键的是，Biome把格式化和检查合二为一。你只需要装一个包，配一个文件。它原生支持TypeScript、JSX，不需要额外插件。

但代价是生态不成熟。Biome目前的规则只有ESLint的十分之一。你常用的 `no-console`、`no-alert` 虽然有，但像 `react-hooks/exhaustive-deps` 这种高级规则，暂时没有。据GitHub数据显示，Biome目前有1.2万stars，而ESLint是2.5万。

## 怎么选

看项目规模。小项目或个人项目，Biome完全够用。配置简单，跑得快，省心。

大项目或企业项目，ESLint+Prettier还是更稳妥。生态成熟，遇到问题社区能解决。但要做好配置管理，别让配置文件占代码量的10%。

说句实在话，Biome还在快速迭代。2024年4月刚发布了1.7版本，新增了 `noUnusedVariables` 规则。如果它能保持这个速度，两年后可能真能取代ESLint。

但眼下，选哪个取决于你对“省事”和“省时间”的权衡。省事选Biome，省时间选ESLint。没有绝对正确，只有适合。