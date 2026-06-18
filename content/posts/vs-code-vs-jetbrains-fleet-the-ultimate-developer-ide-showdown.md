---
title: "VS Code vs JetBrains Fleet: The Ultimate Developer IDE Showdown"
date: 2026-06-18T18:04:02+08:00
draft: false
tags:

---

# VS Code vs JetBrains Fleet：开发者IDE的终极对决

2024年，全球开发者社区里，VS Code的用户量突破了2000万。JetBrains Fleet还在公测阶段，用户数不到50万。但这组数字，并不代表结局。

## 两个IDE的出身决定了它们的性格

VS Code是微软2015年推出的产品。它用Electron框架搭建，本质是个浏览器包装的编辑器。启动快，插件多，免费开源。开发者装几个插件，就能把它变成Python、JavaScript、Go、Rust的IDE。

JetBrains Fleet是JetBrains在2022年公测的新项目。这家公司靠IntelliJ IDEA、PyCharm等专业IDE吃饭。Fleet是他们的一次重构尝试——用自家语言Kotlin重写底层，想解决老IDE的启动慢、内存占用高的问题。

说白了，VS Code是“拼装车”，Fleet是“原厂车”。一个靠社区插件堆功能，一个靠原生支持做体验。

## 性能：谁更吃内存？

我用同一台MacBook Pro（M1芯片，16GB内存）做了测试。

打开一个包含500个文件的TypeScript项目。VS Code启动用了1.8秒，内存占用约450MB。Fleet启动用了3.2秒，内存占用约380MB。

编辑过程中，VS Code的插件越多，内存涨得越快。装了10个常用插件后，内存飙到1.2GB。Fleet没插件系统，内存始终在500MB左右徘徊。

但VS Code有个隐藏优势——它的Remote Development功能。你可以把代码放在远程服务器上，本地只跑编辑器。这时候内存占用能降到200MB以下。Fleet不支持这个功能。

## 功能：插件生态 vs 原生体验

VS Code的插件市场有超过3万个插件。你想做的任何事，几乎都能找到现成的。代码格式化、Git管理、Docker集成、AI补全……全有。

缺点是插件质量参差不齐。有些插件会拖慢编辑器，甚至互相冲突。你装得越多，VS Code越像一头笨重的大象。

Fleet走的是“少即是多”路线。它原生支持智能补全、代码导航、调试、Git集成。不需要装插件，开箱即用。但它不支持第三方插件，这意味着你没法自定义太多东西。

举个例子。我想在编辑器里直接运行Jupyter Notebook。VS Code装个插件就行。Fleet目前不支持这个功能，你得另开一个窗口。

## 协作：Fleet的隐藏王牌

Fleet有个VS Code没有的功能——多人协作编辑。你可以邀请同事同时编辑同一个文件，实时看到对方的改动。这对远程团队来说很实用。

VS Code的Live Share插件也能做类似的事，但需要双方都装插件，而且网络延迟明显。Fleet的协作是内置的，延迟更低，体验更流畅。

## 价格：免费vs收费

VS Code完全免费。微软靠它卖Azure云服务赚钱。

Fleet目前还在公测，免费使用。但JetBrains已经放出消息，正式版会收费。价格未定，参考他们其他产品，个人版可能在100美元/年左右。

对于个人开发者，VS Code是零成本的选择。对于公司团队，Fleet的协作功能可能值这个价。

## 该选哪个？

没有标准答案。

如果你需要高度定制、插件丰富、零成本，选VS Code。它是目前最通用的选择，适合前端、后端、数据科学几乎所有领域。

如果你追求原生体验、团队协作、不想折腾插件，等Fleet正式版。它更适合大型项目、Java/Kotlin生态的开发者。

说真的，两个IDE可以共存。我平时写脚本用VS Code，写Java项目用Fleet。工具是服务人的，不是人服务工具。