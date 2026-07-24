---
title: "ESLint vs Prettier: Should You Use Both or Just One"
date: 2026-07-24T10:03:25+08:00
draft: false
tags:

---

# ESLint vs Prettier：两个都要，还是二选一？

2023年，Stack Overflow的调查显示，87%的专业开发者都在项目里用上了代码格式化工具。但一个老问题始终没解决：ESLint和Prettier，到底该一起用，还是只选一个？

说真的，我第一次接触这两个工具时，也被搞晕了。ESLint报红色波浪线，Prettier又自动改格式，两个插件在VSCode里打架。最后项目跑不起来，我只能一个个关掉重来。

## 它们到底有什么不同？

ESLint出生在2013年，目标是揪出代码里的逻辑错误。比如你写了个未使用的变量，或者不小心用了`==`而不是`===`，它都会跳出来提醒你。说白了，它是个代码质量检查员。

Prettier晚了两年，2015年才出现。它不关心你的代码逻辑对不对，只管格式好不好看。引号统一用单引号还是双引号，行尾要不要加分号，这些琐事都由它说了算。

据ESLint官方文档统计，ESLint有超过280条内置规则，而Prettier只有20个左右的配置选项。一个管得宽，一个管得专，分工完全不同。

## 冲突的根源在哪？

问题出在重叠区域。ESLint也能管格式，比如缩进用2格还是4格。Prettier也管格式，但它有自己的标准。两个工具同时管同一件事，不打架才怪。

我见过一个真实案例：某团队在React项目里同时用了ESLint的`indent`规则和Prettier的默认缩进。结果ESLint要求4格缩进，Prettier自动改成2格。每次保存文件，两个插件来回改，代码像在跳探戈。

社区里有个经典方案：用`eslint-config-prettier`关掉ESLint里所有和Prettier冲突的规则。据npm下载数据显示，这个配置包每周下载量超过600万次，说明大家都遇到过这个问题。

## 两个都要的理由

如果你问Prettier的创始人James Long，他会建议你两个都用。Prettier负责格式，ESLint负责逻辑，各管各的。

这种分工有个好处：ESLint的格式规则被关掉后，它就能专心抓真正的bug。Prettier则保证团队代码风格统一，新人来了不用纠结要不要加分号。

具体配置其实很简单。装好`eslint-config-prettier`后，在ESLint配置文件里加上`extends: ["prettier"]`就行。Prettier那边基本不用动，它默认就能和ESLint和平共处。

## 只用一个会怎样？

有人觉得两个工具太麻烦，想只留一个。选ESLint的话，你得手动配置所有格式规则，工作量不小。选Prettier的话，逻辑错误就没人管了。

GitHub上有位开发者分享过经验：他只用Prettier，结果代码格式很漂亮，但上线后发现一个变量没声明，直接报错。因为Prettier不检查这个，他也没用TypeScript。

反过来，只用ESLint的团队，代码格式经常不统一。有人喜欢在箭头函数参数加括号，有人不加。ESLint虽然能管，但配置起来比Prettier复杂得多。

## 一个折中方案

现在有些团队开始用`@stylistic/eslint-plugin`，这个插件把ESLint的格式规则单独拆出来维护。理论上，你可以用它替代Prettier，只用一个工具搞定所有事。

但据我了解，这个插件的下载量只有Prettier的零头。大多数开发者还是愿意用两个工具，毕竟Prettier的格式化速度比ESLint快得多。据基准测试数据，Prettier处理1000行代码平均只要0.3秒，ESLint需要1.2秒。

## 我的建议

如果你在做新项目，两个都装上。Prettier负责格式，ESLint配合`eslint-config-prettier`负责质量。这个组合已经被无数项目验证过，稳得很。

如果你嫌配置麻烦，可以试试VSCode的`Format on Save`功能，配合`.vscode/settings.json`文件。这样每次保存文件，Prettier自动格式化，ESLint自动检查，你只管写代码。

说到底，工具是为人服务的。别为了选工具浪费太多时间，把精力花在写代码上才是正事。