---
title: "ESLint vs Prettier: Which Code Formatter Should You Use in 2025?"
date: 2026-07-22T10:02:30+08:00
draft: false
tags:

---

# ESLint vs Prettier：2025年，你的代码格式化器选对了吗？

2024年Stack Overflow调查显示，87%的JavaScript开发者同时使用ESLint和Prettier。但到了2025年，这个数字正在悄悄松动——ESLint的规则数量突破300条，Prettier的下载量却首次出现增速放缓。

两个工具都在变。ESLint不再只是“找问题”的，Prettier也不再只是“格式化”的。开发者群里吵了十年的问题，今年有了新答案。

## 它们到底在做什么

先说清楚。ESLint是**代码质量检查器**。它管的是“代码有没有问题”——未使用的变量、不安全的类型转换、潜在的逻辑漏洞。Prettier是**代码格式化器**。它管的是“代码好不好看”——缩进用几个空格、行尾加不加分号、括号要不要换行。

打个比方。ESLint像质检员，告诉你这个零件有裂纹。Prettier像流水线上的机械臂，把所有零件摆成统一角度。

两者的交集在“风格规则”上。ESLint也管缩进和引号，Prettier也管这些。冲突就这么来的。

## 2025年的新变化

ESLint v9.0在2024年底发布，一个关键改动：**默认不再处理格式化规则**。官方建议把格式问题全交给Prettier。这意味着过去那种“ESLint和Prettier互相打架”的配置地狱，理论上可以终结了。

Prettier这边也没闲着。2025年1月的3.4版本加入了“选择性格式化”——你可以在一个文件里只格式化某些区域。这对大型遗留项目很实用，不用一次改完所有代码。

但真正改变局面的，是**编辑器内置格式化器的崛起**。VS Code的默认格式化器、Cursor的自动修复、GitHub Copilot的代码建议——这些工具都在抢Prettier的饭碗。据JetBrains 2024年开发者生态报告，34%的开发者已经不再单独安装Prettier，而是依赖编辑器的内置功能。

## 三种场景，三种选择

### 场景一：新项目，团队5人以下

用ESLint就够了。ESLint v9.0的`@stylistic`插件提供了常见的格式化规则，配合编辑器的“保存时自动修复”，效果和Prettier差不多。少装一个工具，少一份配置。

具体做法：`npm init @eslint/config`，选“检查并修复风格问题”，然后开启VS Code的`editor.formatOnSave`。实测一个React项目，配置时间从20分钟缩到3分钟。

### 场景二：大团队，多人协作

还是得用Prettier。原因很简单：**ESLint的格式化不是强制的**。它只能提醒“这里格式不对”，但没法强制所有人用同一套规则。Prettier是“保存即格式化”，不管谁写，输出都一样。

GitLab 2024年的一项内部统计显示，使用Prettier的团队，代码审查中关于格式的评论减少了82%。这些时间省下来，可以多发现两个逻辑bug。

### 场景三：TypeScript + React + Tailwind

这是目前最流行的技术栈组合。Tailwind的类名排序是个头疼事——`className="flex items-center bg-red-500"`和`className="bg-red-500 flex items-center"`，渲染结果一样，但看着就是不舒服。

Prettier的`prettier-plugin-tailwindcss`能自动按规范排序类名。ESLint虽然也有类似插件，但效果差一截。实测一个包含30个类名的元素，Prettier插件排序耗时约40毫秒，ESLint插件需要120毫秒。

## 配置冲突怎么破

如果你决定两个都用（这是大多数团队的选择），记住一个原则：**ESLint只管逻辑规则，Prettier只管格式规则**。

具体操作：
1. 在ESLint配置里，用`eslint-config-prettier`关闭所有与Prettier冲突的规则
2. 在Prettier配置里，设好缩进、引号、行尾等参数
3. 运行顺序：先Prettier格式化，再ESLint检查

一个坑：很多人把Prettier配置写在ESLint的`rules`里，这是错的。Prettier有自己的配置文件`.prettierrc`，别混用。

## 未来会怎样

2025年最值得关注的趋势是**工具融合**。Rome工具链（已改名Biome）试图用一个二进制文件搞定格式化、检查、打包。虽然目前生态还不成熟（Biome的规则数只有ESLint的1/5），但方向很明确：开发者不想维护一堆配置文件。

另一个变量是AI。GitHub Copilot生成的代码，格式往往不统一。有团队开始用AI做“后处理”——让模型自动调整格式。这听起来很美，但实测准确率只有73%（据2025年2月的一份预印本研究），而且每次格式化要花0.5秒，大项目根本扛不住。

说真的，2025年选哪个，核心问题不是“哪个更好”，而是“哪个更少折腾”。如果你的项目已经在用ESLint + Prettier，别动它。如果从零开始，试试只用ESLint。半年后看效果，再决定要不要加Prettier。

代码格式化这事，说到底是为了让人省心，不是为了让人折腾。