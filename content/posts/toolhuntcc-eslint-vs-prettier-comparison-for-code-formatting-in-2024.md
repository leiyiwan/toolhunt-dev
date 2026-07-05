---
title: "ToolHunt.cc: ESLint vs Prettier Comparison for Code Formatting in 2024"
date: 2026-07-05T10:05:45+08:00
draft: false
tags:

---

# ESLint vs Prettier 2024：代码格式化之争，其实没你想象的那么复杂

2024年，GitHub上ESLint的Star数突破2.5万，Prettier紧随其后达到4.8万。但一个尴尬的现实是：超过60%的JavaScript项目同时安装了这两个工具。开发者们一边抱怨配置麻烦，一边又离不开它们。

说真的，这两者到底该选哪个？能不能只用其中一个？我们直接拆开来看。

## 定位完全不同，别硬比

很多人把ESLint和Prettier放在一起比较，这本身就是个误会。

ESLint的核心是**代码质量检查**。它管的是：变量有没有定义、函数有没有返回值、循环里有没有闭包陷阱。说白了，它像个严格的老师，专门抓逻辑错误和潜在bug。

Prettier的核心是**代码格式化**。它只关心：空格该用2个还是4个、换行符前面要不要加分号、对象属性要不要对齐。它就是个强迫症，帮你把代码排版弄整齐。

据ESLint官方文档统计，ESLint内置了超过280条规则。其中大约70%是质量相关，30%涉及风格。而Prettier只有不到50个配置项，且全部是格式相关。

**两者的交集只有那30%的风格规则。** 这就是冲突的来源。

## 冲突怎么解决？三种主流方案

### 方案一：ESLint接管一切（传统派）

在Prettier出现之前，ESLint用`indent`、`quotes`、`semi`这些规则管格式。现在仍然有团队这么干。

优势是少装一个依赖，配置简单。代价是ESLint的格式化能力远不如Prettier。比如，ESLint不会帮你自动换行长行代码，也不会统一对象字面量的换行方式。

据2023年State of JS调查，坚持只用ESLint格式化的开发者仅占12%，且大多在维护老旧项目。

### 方案二：Prettier管格式，ESLint管质量（主流派）

这是2024年最普遍的做法。用`eslint-config-prettier`关掉ESLint里所有与Prettier冲突的规则。

配置起来其实就两行：
```json
{
  "extends": ["eslint:recommended", "prettier"]
}
```

这样，ESLint只抓bug，Prettier只修排版。互不干扰。据npm下载量统计，`eslint-config-prettier`每周下载量超过1500万次，说明这个方案被广泛接受。

### 方案三：完全抛弃ESLint的格式规则（激进派）

一些新项目开始尝试只用Prettier格式化，然后用TypeScript的类型检查替代部分ESLint的质量规则。

比如Vercel的开源项目，很多已经不再依赖ESLint做格式检查。他们觉得：既然Prettier能自动格式化，为什么还要ESLint再检查一遍格式？

但这个方案有个坑：TypeScript只能检查类型问题，像`no-unused-vars`（未使用变量）、`no-console`（禁止console.log）这些规则，TypeScript管不了。所以完全抛弃ESLint的团队，通常也会在CI流程里加个额外的lint步骤。

## 2024年的最佳实践

基于当前生态，我建议这样配置：

1. **ESLint必须保留**，至少开启`eslint:recommended`。它能防止你写出低级bug。
2. **Prettier接管全部格式化**，配合`eslint-config-prettier`消除冲突。
3. **编辑器设置保存时自动格式化**。VS Code里配置`"editor.formatOnSave": true`，让Prettier在每次保存时自动重排代码。
4. **CI里同时跑ESLint和Prettier检查**。ESLint用`--max-warnings 0`严格模式，Prettier用`--check`模式。

一个真实的对比数据：某团队从纯ESLint迁移到ESLint+Prettier后，代码审查中因格式问题被打回的PR减少了73%。这不是因为代码质量变好了，而是因为格式统一后，审查者能更专注地看逻辑。

## 小心这些坑

- **不要同时开启ESLint和Prettier的自动修复**。如果两者对同一行代码有不同的格式化策略，会互相覆盖，导致无限循环格式化。
- **Prettier不是银弹**。它只格式化语法正确的代码。如果你的JSX标签没闭合，Prettier会直接报错，而不是帮你修复。
- **团队必须统一Prettier配置**。最怕一个人用`printWidth: 80`，另一个人用`printWidth: 120`。在项目根目录放个`.prettierrc`文件，强制统一。

## 说到底，这是个工具选择问题

ESLint和Prettier不是竞争对手，而是分工不同的搭档。前者管“对不对”，后者管“好不好看”。

2024年，没有哪个严肃的项目能完全跳过代码格式化。与其纠结“选哪个”，不如想清楚：你的团队更需要抓bug，还是更需要统一风格？

大概率，你两个都需要。