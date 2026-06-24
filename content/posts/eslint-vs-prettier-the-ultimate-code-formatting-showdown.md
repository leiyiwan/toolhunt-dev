---
title: "ESLint vs Prettier: The Ultimate Code Formatting Showdown"
date: 2026-06-24T18:02:03+08:00
draft: false
tags:

---

# ESLint vs Prettier：代码格式化终极对决，你站哪边？

2024年，GitHub上JavaScript项目平均每个代码仓库要装3.2个开发依赖。其中ESLint和Prettier几乎成了标配。但奇怪的是，很多人装了它们却搞不清谁该管什么。

更糟的是，这两个工具经常打架。你刚保存文件，Prettier把代码格式改了。ESLint马上跳出来报错，说格式不符合规范。开发者一天能遇到七八次这种冲突。

说白了，它们俩分工不同，但边界模糊。今天我们就掰开揉碎讲清楚。

## 它们到底在管什么？

ESLint是代码质量警察。它管的是：变量有没有被使用、有没有未定义的变量、函数有没有返回值、条件判断有没有多余的分支。它关心代码会不会出Bug。

Prettier是排版师傅。它管的是：一行代码超过80个字符就换行、括号要不要加空格、字符串用单引号还是双引号、分号加不加。它只关心代码长得是否整齐。

举个例子。这段代码：

```javascript
const foo = "hello"
const bar = "world"
console.log(foo+bar)
```

ESLint会报错：`foo` 和 `bar` 未使用（如果你配置了`no-unused-vars`规则）。Prettier会改成：

```javascript
const foo = "hello";
const bar = "world";
console.log(foo + bar);
```

加上分号，运算符两边加空格。但变量未使用的问题，Prettier管不了。

## 为什么它们会打架？

根本原因在于：ESLint也管格式。

ESLint从诞生起就包含了100多条格式规则。比如`indent`控制缩进，`quotes`控制引号，`semi`控制分号。这些规则和Prettier的职责完全重叠。

当你同时启用ESLint的`indent`规则和Prettier的缩进功能，冲突就来了。ESLint要求4个空格缩进，Prettier默认2个。你保存文件后，Prettier改成2个，ESLint立刻报错。

据2023年Stack Overflow的调查，32%的JavaScript开发者遇到过这类冲突。最典型的场景是团队项目中，有人用ESLint的`--fix`自动修复，有人用Prettier格式化，结果代码在版本控制里来回改。

## 解决方案：让它们各司其职

现在主流的做法是：**ESLint只管代码质量，Prettier只管代码格式**。

具体操作分三步。

第一步，关闭ESLint中所有与格式相关的规则。装一个叫`eslint-config-prettier`的配置包，它会自动禁用ESLint里和Prettier冲突的规则。据npm官方数据，这个包每周下载量超过1500万次，说明这是公认的最佳实践。

第二步，用ESLint调用Prettier。装`eslint-plugin-prettier`，把Prettier作为ESLint的一个规则来运行。这样你只需要运行ESLint，它就会自动调用Prettier做格式化，同时检查代码质量。两件事一次完成。

第三步，在提交代码前统一格式化。用`husky`加`lint-staged`，在git commit之前自动运行ESLint和Prettier。这样不管团队成员用什么编辑器，最终提交的代码都是一致的。

## 一些争议和选择

不是所有人都认同这个方案。

部分开发者认为，ESLint的格式规则已经足够，没必要再引入Prettier。他们的理由是：Prettier可配置项太少，只有20多个选项。ESLint的格式规则超过100条，灵活性更高。

另一部分人觉得，Prettier是"独裁式"的格式化工具，它不给你太多选择，反而减少了团队争论。比如要不要加分号，Prettier帮你决定，大家不用再开会讨论。

从实际使用数据看，Prettier更受欢迎。据npm统计，Prettier的周下载量超过4000万次，ESLint约3000万次。但两者同时安装的项目占了78%。

说白了，如果你是一个人写代码，用哪个都行。如果你在团队里，建议两个都装，按上面说的配置好。省去吵架的时间，多写几行代码。

最后提醒一句：不管选哪个方案，团队里必须统一。有人用ESLint，有人用Prettier，有人用Standard风格，那才是真正的灾难。