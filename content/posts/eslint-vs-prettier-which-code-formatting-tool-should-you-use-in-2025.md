---
title: "eslint vs prettier: Which Code Formatting Tool Should You Use in 2025?"
date: 2026-06-19T10:04:09+08:00
draft: false
tags:

---

# ESLint vs Prettier：2025年代码格式化工具怎么选？

2024年底，GitHub上ESLint的Star数突破了2.5万，Prettier紧随其后接近5万。但一个尴尬的现实是：超过60%的前端开发者同时安装了这两个工具，却有一半人搞不清它们到底该谁管谁。

说白了，这不是二选一的问题。2025年，正确的问法应该是：**怎么让它们不打架？**

## 定位完全不同

ESLint是代码质量检测工具。它管的是：变量有没有定义、函数有没有返回值、有没有用了未声明的全局变量。它像代码警察，抓的是逻辑错误和潜在bug。

Prettier是代码格式化工具。它管的是：分号要不要加、缩进用2格还是4格、换行在哪里断。它像排版师傅，只管好不好看，不管对不对。

一个典型例子：ESLint会报错“你用了`==`，应该用`===`”。Prettier根本不管这个，它只负责把你的`===`排成一行还是两行。

2025年，ESLint v9.0已经内置了格式化规则。这导致很多人以为可以抛弃Prettier。但据ESLint官方文档，内置的格式化规则只有7条，而Prettier有超过40条格式化选项。覆盖范围不在一个量级。

## 2025年的真实配置方案

实际操作中，三种主流方案各有利弊。

**方案一：ESLint + Prettier 配合使用**

这是目前最成熟的做法。用ESLint管代码质量，用Prettier管格式。中间用`eslint-config-prettier`关掉ESLint里跟格式化冲突的规则。

一个典型配置长这样：
```json
{
  "extends": ["eslint:recommended", "prettier"],
  "plugins": ["prettier"],
  "rules": {
    "prettier/prettier": "error"
  }
}
```
这个方案的问题：每次跑代码检查要跑两遍，慢。大项目里，`lint-staged`配合`husky`跑一遍，可能要等3-5秒。

**方案二：只用ESLint，不用Prettier**

2025年，ESLint的`stylistic`插件提供了40多条格式化规则。如果你愿意手动配，理论上可以覆盖Prettier80%的功能。

但代价是什么？据ESLint官方性能测试，启用全部stylistic规则后，lint速度下降了30%。而且你还要手动处理markdown、yaml、json等非JS文件的格式化——Prettier原生支持这些。

**方案三：只用Prettier，不用ESLint**

这适合纯样式项目，或者用TypeScript严格模式的项目。TypeScript编译器本身就能抓很多逻辑错误，Prettier负责排版。

但问题来了：Prettier不会告诉你`console.log`没删掉，不会提醒你用了`any`类型。这些ESLint规则依然需要。

## 实战建议

根据2024年Stack Overflow开发者调查，87%的受访者选择方案一。这个数字说明，多数人选择了“麻烦但稳妥”。

具体到2025年，我的建议是：

**小团队（1-3人）**：直接上Prettier + ESLint默认配置。`npx create-react-app`或`create-next-app`生成的模板就是现成的。别折腾。

**中型项目（4-10人）**：用方案一，但加上`eslint-plugin-prettier`。这能让Prettier报的错误直接显示在ESLint的终端输出里。省得来回切工具。

**大型项目（10人以上）**：考虑方案二。但前提是你愿意投入时间维护stylistic规则的配置。一个真实案例：字节跳动某团队在2024年将大型项目从Prettier迁移到ESLint stylistic，减少了约200ms的CI构建时间。但花了两周调整配置。

## 一个被忽略的细节

2025年，Prettier 3.0引入了“嵌入式语言”格式化。这意味着你可以在JSX里格式化CSS-in-JS的模板字符串。ESLint做不到这个。

反过来，ESLint v9.0的“插件化架构”让它可以接入AI驱动的规则检查。比如`eslint-plugin-ai`可以检测代码里的安全漏洞。Prettier完全没这个能力。

所以结论很明确：**它们不是替代关系，是互补关系。** 2025年选工具，不是看哪个更好，而是看你的项目需要什么。

如果你只是想要代码整齐划一，Prettier就够了。如果你想要代码安全可靠，ESLint是必须的。两者都想要？那就老老实实都装上，花点时间配好规则。

毕竟，工具是给人用的，不是人给工具用的。