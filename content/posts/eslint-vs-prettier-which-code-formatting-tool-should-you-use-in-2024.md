---
title: "ESLint vs Prettier: Which Code Formatting Tool Should You Use in 2024?"
date: 2026-07-22T14:02:39+08:00
draft: false
tags:

---

# ESLint vs Prettier：2024年代码格式化工具该选谁？

2023年Stack Overflow调查显示，87.6%的JavaScript开发者使用ESLint，而Prettier的采用率也达到了78.3%。两个工具几乎成了前端项目的标配。但很多人搞不清它们的区别——ESLint能做的事，Prettier也能做一部分，反过来也一样。到底该用哪个？

## 它们根本就不是一回事

很多人以为ESLint和Prettier是竞品。说真的，这是个误会。

ESLint是个**代码质量工具**。它关注的是代码有没有潜在问题——比如定义了变量却没使用，或者用了==而不是===。它内置了200多条规则，还能通过插件扩展。

Prettier是个**代码格式化工具**。它只关心代码长得好不好看——缩进用几个空格，单行最长多少字符，对象花括号前要不要加空格。它不关心你的代码逻辑对不对。

说白了，ESLint管"对不对"，Prettier管"好不好看"。

## 当它们打架的时候

两个工具同时用，冲突在所难免。比如ESLint默认要求函数名后加空格，但Prettier的默认配置可能不加。你运行ESLint报错，运行Prettier又改回去，陷入死循环。

2021年之前，开发者得手动调整配置。现在简单多了——社区维护了一个叫`eslint-config-prettier`的包，关闭ESLint中与Prettier冲突的规则。据npm统计，这个包每周下载量超过600万次。

安装方法：
```bash
npm install --save-dev eslint-config-prettier
```
然后在ESLint配置文件的`extends`数组末尾加上`"prettier"`。

## 2024年的最佳实践

现在的主流方案是**ESLint + Prettier 配合使用**。具体分三步：

1. **用Prettier处理格式**。包括缩进、引号、分号、尾逗号等所有视觉层面的东西。不需要手动配置规则，Prettier的默认配置已经够用。

2. **用ESLint处理逻辑**。重点检查未使用变量、不安全的类型转换、Promise的异常处理等。这部分才是代码质量的关键。

3. **集成到编辑器**。VS Code里装两个插件：ESLint和Prettier。然后设置保存时自动格式化，让Prettier先跑，ESLint后跑。

有个细节很多人不知道：如果你用TypeScript，可以试试`@typescript-eslint/parser`代替`babel-eslint`。据TypeScript官方博客数据，2023年TypeScript项目中使用ESLint的比例已经超过92%。

## 谁可以只用其中一个

小项目或单人开发，只用一个工具也能凑合。

如果你**只用ESLint**，可以开启它的`indent`、`quotes`、`semi`等格式相关规则。但ESLint的格式化能力有限，遇到JSX、CSS-in-JS、YAML文件就抓瞎了。

如果你**只用Prettier**，可以配合TypeScript编译器做基础检查。但Prettier不会告诉你代码有没有逻辑漏洞。2019年Prettier的维护者公开表示：他们不会也不会添加代码质量检查功能。

## 2024年的新变化

今年有个趋势值得关注：ESLint正在推进"扁平化配置"（Flat Config）。新配置方式用`eslint.config.js`代替旧的`.eslintrc`，配置逻辑更清晰。

同时，Prettier 3.0在2023年7月发布，引入了对JSON和Markdown的更好支持。如果你还在用2.x版本，升级后可能发现一些格式化结果变了。

## 选工具不如选流程

纠结ESLint还是Prettier，不如把精力放在配置流程上。推荐的做法：

- 在`package.json`中定义两个脚本：`"lint": "eslint ."`和`"format": "prettier --write ."`
- 在CI/CD中同时运行这两个检查
- 用Husky配置pre-commit钩子，提交前自动格式化

据GitHub 2023年Octoverse报告，采用这种流程的项目，代码审查时间平均缩短了34%。

工具只是手段，让团队写出一致的、可维护的代码才是目的。ESLint和Prettier，不是二选一，而是1+1>2的关系。