---
title: "ESLint vs Prettier 2024: Which Code Formatting Tool Should You Choose?"
date: 2026-06-14T10:02:29+08:00
draft: false
tags:

---

# ESLint vs Prettier 2024：代码格式化工具选哪个？

2024年，一个前端开发者平均每天要花15分钟手动调整代码缩进、分号、引号。这不是段子。Stack Overflow 2024年调查显示，代码风格争议仍是团队协作中排名第三的痛点。于是ESLint和Prettier成了几乎所有项目的标配。但问题来了：这俩工具到底有什么不同？能不能只用一个？

## 它们根本不是一类东西

很多人以为ESLint和Prettier是竞品。错。它们解决的是不同维度的问题。

ESLint是代码质量检查工具。它关注的是“代码有没有bug”“变量是否声明未使用”“函数是否过于复杂”。它能在你写出`==`时警告你改用`===`，在循环里声明函数时提醒你潜在的内存泄漏。

Prettier是代码格式化工具。它只关心“代码长得好不好看”。它不管你的逻辑对不对，只管把缩进统一成2个空格，把单引号统一成双引号（或反过来），把超过80个字符的行自动换行。

说白了，ESLint是警察，管的是“能不能这么干”。Prettier是造型师，管的是“怎么干才好看”。

## 2024年两者的核心变化

ESLint在2024年最大的更新是扁平化配置（Flat Config）。以前你需要在`.eslintrc`里写一堆嵌套的`extends`和`plugins`，现在一个`eslint.config.js`就能搞定。这解决了一个老问题：配置继承带来的“幽灵规则”。

Prettier这边，2024年3.0版本后，支持了更多语言和框架。比如对Astro、Svelte的原生支持，对JSONC（带注释的JSON）的格式化。另外，Prettier的“无配置”哲学没变——它默认设置就够用，大部分人不需要改。

但有个细节：据ESLint官方数据，2024年仍有38%的团队同时使用两者，而不是二选一。

## 为什么需要一起用？

假设你只用ESLint。它能检查代码质量，但格式化能力很弱。ESLint的`--fix`参数虽然能自动修复一些格式问题，但只限于它能理解的规则。比如它没法智能换行，没法优雅地调整对象属性对齐。结果是，你写出来的代码在ESLint眼里没问题，但看起来还是乱糟糟。

假设你只用Prettier。它能让代码整齐划一，但不会提醒你变量未使用，不会警告你潜在的`undefined`错误。你可能会写出语法正确但逻辑有坑的代码。

所以最佳实践是：ESLint负责“对不对”，Prettier负责“美不美”。两者配合时，需要把ESLint中关于格式的规则关掉，比如`indent`、`quotes`、`semi`等，交给Prettier全权处理。

## 2024年推荐的配置方式

如果你用VSCode，安装两个插件：ESLint和Prettier。然后在项目根目录创建`eslint.config.js`和`.prettierrc`。

ESLint配置示例（扁平配置）：

```js
import js from '@eslint/js';
import prettier from 'eslint-config-prettier';

export default [
  js.configs.recommended,
  prettier,
  {
    rules: {
      'no-unused-vars': 'warn',
      'no-console': 'off',
    },
  },
];
```

Prettier配置示例（`.prettierrc`）：

```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "all"
}
```

关键在于`eslint-config-prettier`这个包。它能把ESLint中与Prettier冲突的规则全部禁用。否则你会遇到：ESLint要求分号，Prettier要求无分号，两个插件在编辑器里打架。

## 新趋势：Biome能取代它们吗？

2024年有个新工具叫Biome，它把ESLint和Prettier的功能合二为一。据Biome官方基准测试，它的格式化速度比Prettier快10倍，检查速度比ESLint快20倍。目前已经有像Next.js、Vite等项目开始尝试迁移。

但Biome的问题在于生态。ESLint有超过1000个插件，Prettier有超过200个插件。Biome的规则数量还不到ESLint的十分之一。如果你用React、TypeScript、Tailwind CSS，Biome目前覆盖不全。

## 怎么选？

看项目规模和个人偏好。

- **个人项目或小团队**：只装Prettier就够了。代码质量靠代码审查弥补。
- **中大型项目**：ESLint + Prettier组合，一个都不能少。
- **追求极致性能**：可以试试Biome，但要接受部分规则缺失。
- **对代码质量要求极高**：ESLint + Prettier + TypeScript严格模式，三管齐下。

2024年没有“最好”的工具，只有“最适合”的组合。别纠结，先装上，跑起来。代码风格统一比用什么工具重要一百倍。