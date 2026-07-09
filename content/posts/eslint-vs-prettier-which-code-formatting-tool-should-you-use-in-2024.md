---
title: "ESLint vs Prettier: Which Code Formatting Tool Should You Use in 2024?"
date: 2026-07-09T14:02:13+08:00
draft: false
tags:

---

# ESLint vs Prettier 2024：别再二选一了，这才是正确用法

2023年Stack Overflow调查显示，87.6%的开发者使用代码格式化工具。但一个尴尬的现实是：很多人还在纠结ESLint和Prettier该用哪个。

两个工具我都用了五年，踩过坑，也见过团队因为选错工具导致代码风格混乱。今天直接说结论：**不是二选一，而是各司其职**。

## 它们根本就不是一个东西

很多人把ESLint和Prettier混为一谈，这是最大的误解。

ESLint是**代码质量工具**。它检查的是：变量是否定义了但没使用、有没有写了死循环的风险、异步操作是否正确处理。说白了，它抓的是**逻辑错误**。

Prettier是**代码格式化工具**。它只关心：括号要不要换行、缩进用2空格还是4空格、字符串用单引号还是双引号。它不关心你的代码能不能跑，只关心好不好看。

一个抓bug，一个整容。你见过让整形医生去做体检的吗？

## 2024年的最佳实践

经过多个项目的实践，现在最稳妥的方案是：

**用ESLint做代码质量检查，用Prettier做代码格式化。** 两者用配置文件明确分工。

具体操作分三步：

第一，安装ESLint和Prettier，以及`eslint-config-prettier`这个插件。它的作用是把ESLint中和格式相关的规则全部关掉，避免和Prettier打架。

第二，在ESLint配置里只保留逻辑检查规则。比如：
```json
{
  "rules": {
    "no-unused-vars": "error",
    "no-console": "warn"
  }
}
```

第三，Prettier负责所有格式问题。比如单引号、行宽、末尾逗号这些。

曾经有个团队，ESLint配置了200多条规则，每次提交代码要等30秒检查。后来砍掉格式规则，只保留逻辑检查，速度提升到5秒。

## 一个容易忽略的坑

就算配置好了，还有个常见问题：**保存代码时自动格式化**。

很多人习惯在VS Code里设置"保存时自动格式化"，结果ESLint和Prettier同时启动，一个要加空格，一个要删空格，代码来回跳。

正确做法是：只让Prettier在保存时自动格式化。ESLint只在提交前检查，或者手动运行。

具体在VS Code的settings.json里：
```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "eslint.formatOnSave": false
}
```

这样保存时Prettier整理格式，提交时ESLint抓逻辑问题，互不干扰。

## 特殊情况怎么处理

有些场景需要调整策略。

如果项目是TypeScript，建议用`@typescript-eslint/parser`替换ESLint默认解析器。Prettier不需要额外配置，它原生支持TS。

如果是React项目，ESLint加`eslint-plugin-react`检查JSX里的逻辑。Prettier会自动格式化JSX的缩进和换行。

如果是多人协作的大型项目，建议在CI/CD里加一个步骤：`eslint --max-warnings 0`，超过警告数直接拒绝合并。Prettier用`--check`参数只检查不修改，确保所有人格式一致。

## 别被工具绑架

说到底，代码格式化工具是为了减少沟通成本，不是增加负担。

我见过最离谱的案例：一个团队花了三周时间争论用2空格还是4空格，最后决定用3空格。结果Prettier根本不支持3空格缩进，又吵了一周。

工具是服务人的。2024年的最佳选择不是二选一，而是让ESLint和Prettier各管各的。一个保质量，一个保整洁，加起来才是好代码。

如果你还在纠结，直接按上面的方案配置。半小时搞定，剩下的时间好好写代码。