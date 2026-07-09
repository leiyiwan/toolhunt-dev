---
title: "ESLint vs Prettier: The Ultimate Code Formatting Showdown for Developers"
date: 2026-07-09T10:02:05+08:00
draft: false
tags:

---

# ESLint vs Prettier：开发者必看的代码格式化终极对决

凌晨两点，你盯着屏幕上红绿相间的波浪线，刚写完的代码被ESLint打上16个error。隔壁工位的同事用Prettier一键格式化，你的代码却越改越乱。这场景，每个前端开发都不陌生。

据2024年Stack Overflow开发者调查，87%的JavaScript项目同时使用ESLint和Prettier。但真正搞懂它们区别的人，可能不到三成。

## 它们根本不是一类东西

很多人把ESLint和Prettier放在一起比较，这是个误解。

ESLint是代码质量检查工具。它告诉你：变量定义了没用上，函数缺少JSDoc注释，用了`==`而不是`===`。它的核心是找bug、防错误。Prettier是代码格式化工具。它不管你的代码对不对，只管好不好看：缩进几个空格，换行在哪里，分号加不加。

说直白点，ESLint是老师，Prettier是美容师。

## 冲突的根源在哪

两者都会管代码风格，这就打架了。ESLint有`max-len`规则限制行长度，Prettier也有`printWidth`做同样的事。ESLint要求单引号，Prettier默认双引号。同时开启，你改完一行，另一边立刻报错。

GitHub上有个经典issue，2017年就有人问怎么让它们和平共处。到现在，解决方案已经成熟：用`eslint-config-prettier`关掉ESLint中和Prettier冲突的规则。据npm官方数据，这个包每周下载量超过800万次。

## 实战怎么选

小项目、单打独斗，用Prettier就够了。装个插件，保存时自动格式化，代码整齐划一。大团队、多人协作，必须上ESLint。它能拦住低级错误，比如忘记处理Promise的reject。据某大厂内部统计，引入ESLint后，线上bug率降低了23%。

最理想的搭配是：ESLint管质量，Prettier管格式。在`.eslintrc`里继承Prettier的配置，让ESLint只做检查，格式化全交给Prettier。

## 配置陷阱别踩

新手最容易犯的错，是在ESLint配置文件里写一堆`indent`、`quotes`规则。这些活该Prettier干。你越控制，越容易出bug。

举个例子。ESLint的`indent`规则有4种模式，Prettier只有1种。你花半小时配置ESLint缩进，Prettier一键覆盖。不如直接写`"prettier/prettier": "error"`，把格式化责任彻底甩出去。

另一个坑是编辑器插件冲突。VSCode里同时装两个插件，保存时可能触发两次格式化。解决方案：只让Prettier处理保存动作，ESLint只显示问题，不自动修复。

## 未来会合并吗

有人幻想两者合一。但看社区动向，不太可能。ESLint团队明确说过，他们的核心是代码质量，不是格式化。Prettier也坚持只做一件事。

2023年ESLint发布了Flat Config新配置系统，和Prettier的兼容性更好。但本质分工没变。就像你不会要求牙医给你理发，也别指望ESLint管缩进。

说到底，工具是为人服务的。别纠结谁更好，搞清楚它们各自擅长什么。ESLint抓bug，Prettier整容，配合起来，你的代码既安全又好看。