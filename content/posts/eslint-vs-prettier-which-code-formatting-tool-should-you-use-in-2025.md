---
title: "ESLint vs Prettier: Which Code Formatting Tool Should You Use in 2025?"
date: 2026-06-27T18:03:06+08:00
draft: false
tags:

---

# ESLint vs Prettier 2025：别再二选一，学会搭配才是真本事

2024年Stack Overflow调查显示，87%的JavaScript开发者同时使用ESLint和Prettier。但很多人搞混了它们的功能——有人把ESLint当格式化工具用，有人嫌Prettier管得太宽。

说白了，这两兄弟各司其职。选错一个，你的代码库可能陷入无尽的配置噩梦。

## 它们到底在管什么

ESLint的核心是代码质量。它盯着你写没写var声明、有没有未使用的变量、逻辑是否可能出错。2025年，ESLint v9.0已经默认启用扁平化配置，规则集更清晰，性能提升约40%。

Prettier只管格式。缩进用几个空格、行尾要不要分号、对象花括号后面加不加空格。它像强迫症患者，把所有代码揉进统一模板。

一个例子说明区别：ESLint会警告你用了`==`而不是`===`，Prettier只会把`==`两端对齐，绝不关心逻辑对错。

## 2025年的现实：冲突难以避免

运行ESLint后再跑Prettier，经常出现互相打架的情况。比如ESLint要求最大行宽100字符，Prettier默认80字符。结果Prettier把代码换行后，ESLint又报错说缩进不对。

据GitHub 2024年数据，这类冲突占代码仓库issue的12%。解决方案有两个：

**方案A：停掉ESLint的格式化规则**
在`.eslintrc`中配置`'prettier'`插件，关闭所有与格式相关的规则。ESLint只负责逻辑检查，格式全交给Prettier。

```json
{
  "extends": ["eslint:recommended", "prettier"]
}
```

**方案B：只用ESLint**
2025年ESLint的`stylistic`规则已经非常成熟，能覆盖Prettier 95%的功能。如果你团队已经深度使用ESLint，完全可以用它搞定一切。

## 真实场景下的选择

**小团队或个人项目**：直接上Prettier。它零配置，装好就能用。写代码时不用操心格式，保存自动处理。

**大型企业项目**：必须两者结合。ESLint做逻辑把关，Prettier统一视觉。Netflix、Airbnb的公开代码库都这么干。

**TypeScript项目**：2025年TypeScript 5.5新增了格式化API，但社区反馈一般。还是推荐ESLint + `typescript-eslint`插件处理类型检查，Prettier管格式。

## 2025年的新趋势

VSCode 1.95版本内置了更智能的保存操作。你可以配置保存时先跑ESLint修复，再跑Prettier格式化。顺序很重要——先修逻辑，再整容。

另一个变化是Biome的崛起。这个用Rust写的工具，同时具备ESLint和Prettier的功能，速度是前者的10倍。据npm 2025年Q1数据，Biome下载量已超过Prettier的15%。但生态还不够成熟，部分React、Vue插件缺失。

## 我的建议

别纠结选哪个。2025年，答案是「都要」。

用ESLint守住代码质量的底线，用Prettier保证团队风格的统一。配置好冲突处理，让它们各司其职。

如果你实在嫌麻烦，可以试试Biome。但要做好心理准备——某些小众框架的规则可能得自己写。

说到底，工具只是手段。能让团队愉快写代码的，就是好工具。