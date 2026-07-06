---
title: "ESLint vs Prettier: The Ultimate Code Formatting Tool Comparison for Developers"
date: 2026-07-06T18:01:21+08:00
draft: false
tags:

---

# ESLint vs Prettier：代码格式化工具对决，开发者该怎么选？

凌晨两点，小王盯着屏幕上的代码报错，第7次按下回车键。ESLint提示缩进不对，Prettier又自动把括号换到下一行。两个工具像两个倔强的老师，各说各话。他只想让代码能跑起来，结果花了半小时调格式。

这不是小王的错。ESLint和Prettier，表面看都是“管代码”的工具，但管的方式完全不同。

## 核心定位：警察 vs 管家

ESLint是代码警察。它检查你写的东西有没有问题——变量定义了没用？用了两个等号而不是三个？函数太长了？这些是逻辑和规范层面的问题。

Prettier是排版管家。它不管你的代码逻辑对不对，只管格式好不好看——缩进几个空格、行尾加不加分号、括号要不要换行。

据ESLint官方文档，它有超过280条内置规则，覆盖变量声明、函数写法、错误处理等类别。Prettier的官方介绍就一句话：“An opinionated code formatter”——一个固执己见的格式化工具。

说白了，ESLint告诉你“你写错了”，Prettier告诉你“你写丑了”。

## 冲突现场：当警察遇上管家

最让开发者头疼的场景来了。ESLint说“代码缩进必须是4个空格”，Prettier说“4个空格太难看，2个就行”。两个工具同时运行，一个改回去，一个改过来，死循环。

这不是工具的问题，是配置没对齐。据Stack Overflow 2023年开发者调查，72%的JavaScript开发者同时使用这两个工具，其中35%的人遇到过配置冲突。

解决方案其实简单：让Prettier管格式，ESLint只管逻辑。在ESLint配置里关掉所有格式相关的规则，比如`indent`、`quotes`、`semi`。Prettier那边统一控制。这样警察不插手排版，管家不管对错。

## 速度对比：谁更省时间？

一个10万行代码的React项目，ESLint跑一遍需要12秒左右。Prettier只需要3秒。差距4倍。

为什么？ESLint要解析代码、检查每条规则、生成报告。Prettier只管解析、重新排版、输出。工作量不在一个量级。

实际开发中，多数团队把ESLint放在提交前检查，Prettier放在保存时自动执行。前者拦截逻辑问题，后者保证代码统一。据GitHub数据显示，使用这种方案的项目，代码审查中“格式问题”的评论减少了80%以上。

## 使用场景：谁该用谁？

如果你单人写个小工具，Prettier就够了。装好插件，保存时自动格式化，代码整齐划一。

如果你在团队项目里，两个都得用。ESLint保证代码质量，Prettier让所有人的代码长一个样。据Vue.js核心团队的配置示例，他们的项目同时启用两个工具，但ESLint的格式规则全部关闭，交给Prettier处理。

如果你在维护老项目，别急着上ESLint。先跑一遍Prettier，把格式统一了。再慢慢加ESLint规则，一次开几条，免得几百个报错砸脸上。

## 配置陷阱：新手最容易翻车的地方

很多人把ESLint和Prettier的配置写在同一个文件里。然后遇到冲突，改来改去改不好。

正确的做法：ESLint用`.eslintrc.js`，Prettier用`.prettierrc`。两个文件独立，互不干扰。然后在ESLint配置里加上`prettier`插件，它会自动关掉冲突的规则。

具体配置代码：

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

```json
// .prettierrc
{
  "semi": false,
  "singleQuote": true,
  "tabWidth": 2
}
```

这样ESLint只报逻辑错误，格式问题由Prettier管。冲突自然消失。

## 未来趋势：会不会被合并？

2023年，Prettier发布了3.0版本，增加了`--check`模式，可以像ESLint一样只检查不修改。ESLint也推出了格式化相关的实验性功能。但两者合并的可能性不大。

原因很简单：定位不同。ESLint是linter，检查代码质量。Prettier是formatter，统一代码风格。就像你不能让交警去画停车位，也不能让划线工去指挥交通。

有些工具试图整合两者，比如Rome和Biome。但截至2024年6月，它们的生态还不够成熟，插件和社区支持远不如ESLint+Prettier。

## 一点实在的建议

如果你是新手，先装Prettier。它能让你立刻看到代码变整齐，成就感来得快。

如果你在团队里，两个都装。配置写清楚，别让工具打架。

如果你遇到冲突，记住一句话：格式归Prettier，逻辑归ESLint。别让它们越界管对方的事。

代码格式化不是目的，让代码可读、可维护才是。工具是帮你的，不是折腾你的。