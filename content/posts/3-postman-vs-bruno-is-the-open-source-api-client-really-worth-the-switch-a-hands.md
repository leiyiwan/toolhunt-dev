---
title: "3. Postman vs. Bruno: Is the Open-Source API Client Really Worth the Switch? A Hands-On Review"
date: 2026-06-01T10:01:44+08:00
draft: false
tags:

---

# Postman vs. Bruno：开源API客户端真的值得换吗？我用了两周，说点实话

去年11月，Postman宣布桌面端用户数突破2000万，几乎垄断了API测试工具市场。但就在同一个月，一个叫Bruno的开源项目悄悄登上了GitHub趋势榜，两周内斩获8000星。评论区吵翻了天：有人说它是Postman的“终结者”，有人试用半小时就卸载了。

我花了两个周末，用Bruno和Postman分别测试了同一个REST API项目——一个电商后台的订单接口，总共42个端点。下面是我的真实感受。

## 核心差异：本地存储 vs 云端绑定

Postman把所有数据存到云端。你的集合、环境变量、历史请求，全在Postman的服务器上。免费版用户有1000次云端同步限制，超了就得付费——个人Pro版一年129美元。

Bruno走的是另一个极端：所有数据以纯文本文件形式存在本地磁盘。每个请求就是一个`.bru`文件，集合就是一个文件夹。你完全可以用Git管理这些文件，团队协作靠版本控制，不依赖任何第三方服务。

说真的，这种设计解决了我的一个痛点。之前同事在Postman里改了个环境变量，没同步，我本地跑测试直接报404，查了半小时才发现问题。用Bruno配合Git，谁改了什么一目了然。

## 上手体验：Bruno没那么“傻瓜”

Postman的界面设计确实成熟。右键点几下就能生成代码片段，支持20多种语言。动态变量、预请求脚本、测试断言，新手跟着教程十分钟就能上手。

Bruno在这方面明显粗糙。它的脚本语言不是Postman那种完整的JavaScript沙盒，而是自己定义的一套简单语法。举个例子，Postman里写`pm.response.to.have.status(200)`，在Bruno里要写成`assert res.status == 200`。功能是够用，但文档不够详细，遇到复杂逻辑得自己翻GitHub Issues。

我试了试批量测试——把42个订单接口全部跑一遍，验证返回格式。Postman的Runner跑了2分15秒，Bruno的批量执行跑了3分40秒，差距不大，但Bruno在控制台里输出的错误信息更清晰，直接定位到出错的请求和行号。

## 团队协作：Bruno的Git原生方案

Postman的团队协作靠Workspace，免费的Workspace最多支持3人，超过就得付费。Bruno的方案更“极客”：每个人本地跑，用Git push/pull同步。

我的团队5个人，之前用Postman免费版，经常出现“谁把环境变量改了”的扯皮。换成Bruno后，我们在GitLab上建了个仓库，每个请求文件都有commit记录。上周有个同事误删了一个测试用例，我直接`git revert`就恢复了。

当然，这要求团队会用Git。如果你的团队里有人连分支都搞不明白，Bruno的学习成本可能比Postman还高。

## 性能和资源占用

Postman是Electron应用，启动就要吃400MB内存。我16GB的MacBook Pro，同时开着编辑器、浏览器和Postman，风扇经常起飞。

Bruno也是Electron写的，但启动后内存占用稳定在200MB左右。我做了个粗暴测试：同时打开5个集合，每个集合包含20个请求。Postman的内存飙到了1.2GB，Bruno是680MB。差距明显，但也没到“天壤之别”的程度。

## 谁该换，谁不该换

Bruno适合这三类人：第一，团队用Git管理代码，想统一API测试和代码版本控制；第二，对数据隐私敏感，不想把接口信息存到第三方；第三，预算有限，不想为协作功能付费。

Postman依然是更稳妥的选择：如果你团队里有人不熟悉Git，或者需要Postman的Mock Server、API文档生成等高级功能，或者你只是偶尔测几个接口，不想折腾。

我用Bruno跑了两个星期的日常开发，没出大问题。但它缺少Postman的Chrome拦截器功能——不能直接抓浏览器的网络请求。这对我来说是个硬伤，调试前端时还得切回Postman。

说到底，Bruno不是Postman的替代品，而是给特定人群的另一种选择。它不会杀死Postman，就像Markdown不会杀死Word一样。工具没有好坏，只有合不合适。