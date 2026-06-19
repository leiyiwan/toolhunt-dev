---
title: "ESLint vs Prettier: The Ultimate Code Formatting Showdown for JavaScript Developers"
date: 2026-06-19T14:04:16+08:00
draft: false
tags:

---

# ESLint vs Prettier：JavaScript 开发者该选谁？一场代码格式的终极对决

2024 年 Stack Overflow 调查显示，87% 的 JavaScript 开发者同时使用 ESLint 和 Prettier。但很多人搞不清：这两个工具到底有什么不同？能不能只用一个？

说真的，这个问题困扰过每一个前端新手。甚至一些老手，在配置项目时也会纠结——到底该装哪个？两个都装会不会打架？

## 它们不是同一个东西

ESLint 诞生于 2013 年，最初定位是代码质量检查工具。它像个严格的审查员，会告诉你：“这里有个未使用的变量”、“这个函数太长了”、“你用了 `==` 而不是 `===`”。

Prettier 晚了两年，2015 年才出现。它是个格式化工具，只关心外观：“你的代码缩进是 2 个空格还是 4 个？”、“这行超过 80 个字符了，我帮你换行”。

本质区别：ESLint 抓逻辑错误，Prettier 管排版美观。

举个例子，下面这段代码：

```javascript
const foo = "hello"
if(foo=='world')console.log('hi')
```

ESLint 会报错：`foo` 变量未使用、用了 `==` 建议改成 `===`、`if` 后缺少空格。Prettier 会把它格式化成：

```javascript
const foo = "hello";
if (foo == "world") console.log("hi");
```

看到了吗？Prettier 不会告诉你 `==` 有问题，它只负责让代码看起来整齐。

## 冲突不可避免

当你同时使用两个工具，冲突就来了。

ESLint 有 `max-len` 规则控制行长度，Prettier 也有 `printWidth`。ESLint 的 `indent` 规则控制缩进，Prettier 的 `tabWidth` 也管这个。

据 GitHub 上的 eslint-config-prettier 项目统计，ESLint 核心规则中至少有 40 条与 Prettier 直接冲突。这就是为什么你经常看到开发者配置了半天的规则，一跑 Prettier 全给改了。

解决办法很简单：让 ESLint 只管代码质量，格式的事全交给 Prettier。用 `eslint-config-prettier` 关掉 ESLint 中所有与格式相关的规则。

## 实战中的选择策略

**小团队或个人项目**：只装 Prettier 就够了。Prettier 配置简单，开箱即用。它能保证代码风格统一，对新手友好。你不需要记住该用单引号还是双引号，Prettier 帮你搞定。

**中大型项目**：两个都要。ESLint 能捕获潜在 bug，Prettier 保证风格一致。配置方式推荐：

```json
// .eslintrc.json
{
  "extends": ["eslint:recommended", "prettier"],
  "plugins": ["prettier"],
  "rules": {
    "prettier/prettier": "error"
  }
}
```

这样配置后，运行 ESLint 时它会自动调用 Prettier 检查格式。Prettier 格式不对的，ESLint 会报错。

**TypeScript 项目**：加上 `@typescript-eslint/parser` 和 `@typescript-eslint/eslint-plugin`。Prettier 对 TypeScript 支持也很好，不用额外配置。

## 一些实用建议

1. 在提交代码前自动格式化。用 husky + lint-staged，在 git commit 前自动跑 Prettier 和 ESLint。据 npm 下载数据显示，lint-staged 周下载量超过 800 万次，说明这是行业标准做法。

2. 编辑器里设置“保存时自动格式化”。VS Code 用户装好 ESLint 和 Prettier 插件，在 settings.json 里加：

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  }
}
```

3. 团队统一配置。把 `.prettierrc` 和 `.eslintrc` 文件放在项目根目录，用 CI 流程确保每个人提交的代码都经过检查。别让格式化问题变成 code review 的争论点。

## 未来会怎样？

ESLint 团队在 2022 年宣布了 ESLint v9 的重大改动，计划引入类似 Prettier 的格式化功能。Prettier 也在探索代码质量检查能力。两者边界正在模糊。

但短期内，它们还是各司其职更好。就像你不会让厨师同时干收银的活，让工具做自己擅长的事。

最后说句实在话：别在工具选择上花太多时间。两个都装上，配置好，然后就忘了它们的存在。把精力留给真正需要思考的业务逻辑。