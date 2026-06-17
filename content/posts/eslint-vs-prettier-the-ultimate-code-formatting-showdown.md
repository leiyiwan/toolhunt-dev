---
title: "ESLint vs Prettier: The Ultimate Code Formatting Showdown"
date: 2026-06-17T18:03:43+08:00
draft: false
tags:

---

# ESLint vs Prettier：代码格式化的终极对决，我全都要

2023年，Stack Overflow的调查显示，87%的开发者使用代码格式化工具。但一个尴尬的现实是：超过一半的人分不清ESLint和Prettier的区别。打开GitHub，你总能看到类似的PR评论——“这是ESLint该管的吗？”“Prettier为什么报这个错？”

说白了，这两兄弟分工完全不同。一个管代码质量，一个管代码颜值。但很多人把它们混为一谈，导致配置文件写了一堆，该报的错一个没少。

## ESLint：代码质量的守门员

ESLint诞生于2013年，作者是Nicholas C. Zakas。它的核心能力是**静态分析**。什么意思？它能发现你没使用的变量、不安全的类型转换、甚至潜在的逻辑漏洞。

举个具体的例子。你写了一段代码：

```javascript
if (user = 'admin') {
  // 执行管理员操作
}
```

ESLint会立刻报错。因为这里应该是`===`而不是`=`。Prettier对这种错误完全无感，它只关心等号两边有没有空格。

据ESLint官方数据，它内置了超过200条规则。加上社区插件，这个数字能轻松破千。比如React项目的`eslint-plugin-react-hooks`，能在编译前就发现Hook使用顺序错误——这可是React官方认定的常见bug来源。

## Prettier：代码颜值的强迫症

Prettier是2016年才出现的后来者。它的理念很极端：**没有配置选项**。当然，后来迫于用户压力加了几个，但核心思想没变——你写代码，它管格式。

说真的，Prettier解决了一个很实际的问题：代码审查时，大家不再为“缩进用2空格还是4空格”吵架了。据GitHub的一项非正式统计，团队引入Prettier后，PR中关于格式的评论减少了约70%。

它怎么做到的？简单粗暴。你把代码扔给它，它解析成AST（抽象语法树），然后按照自己的规则重新打印出来。你的代码风格？不重要。Prettier的风格才是风格。

## 冲突现场：它们打架怎么办

现实很残酷。ESLint和Prettier在某些规则上会起冲突。最典型的是`max-len`（最大行长度）。ESLint会报错说“这一行超过80个字符了”，Prettier说“我帮你折行了，但ESLint还在报错”。

怎么办？社区给出了方案：`eslint-config-prettier`。这个配置包会关闭ESLint中所有与Prettier冲突的规则。据npm统计，这个包每周下载量超过1500万次，说明大家都遇到过这个问题。

另一个方案是`eslint-plugin-prettier`。它把Prettier当成ESLint的一条规则来运行。但有人反对这种做法，认为这让ESLint变慢了。Prettier的维护者James Long就明确说过：“Prettier应该独立运行，别塞进ESLint里。”

## 最佳实践：分工协作

经过大量团队实践，目前公认的方案是：

- **ESLint负责代码逻辑**：检查未使用变量、潜在错误、最佳实践
- **Prettier负责代码格式**：缩进、分号、引号、换行

具体怎么配置？以VS Code为例，打开settings.json，加上：

```json
"editor.formatOnSave": true,
"editor.defaultFormatter": "esbenp.prettier-vscode",
"editor.codeActionsOnSave": {
  "source.fixAll.eslint": true
}
```

保存文件时，Prettier先格式化，ESLint再修复。顺序不能反。有些团队会在CI/CD中再加一道检查：`npm run lint`和`npm run format:check`，确保代码提交前都通过。

## 不是选择题，是组合题

说穿了，ESLint和Prettier不是二选一的关系。ESLint管的是“代码对不对”，Prettier管的是“代码好不好看”。一个项目缺了ESLint，bug可能悄悄上线；缺了Prettier，代码审查变成辩论赛。

从npm下载量看，两者都在稳步增长。ESLint周下载量约3000万，Prettier约2000万。这个数字说明，绝大多数开发者已经接受了“质量+格式”双保险的思路。

最后说句实在话：别纠结选哪个。两个都装，让它们各司其职。你的代码会感谢你，你的同事也会。