---
title: "VS Code Dev Containers vs GitHub Codespaces: Best Remote Development Setup"
date: 2026-06-29T10:03:34+08:00
draft: false
tags:

---

# VS Code Dev Containers vs GitHub Codespaces：远程开发到底选哪个？

2024年，GitHub官方数据显示，超过300万开发者使用Codespaces。与此同时，VS Code的Dev Containers扩展下载量突破8000万。这两个工具都在解决同一个问题：让开发环境像代码一样可复现、可共享。但它们是替代关系，还是互补关系？我花了两个月时间，在两个工具之间反复横跳，今天说点实在的。

## 核心区别：一个本地跑，一个云上跑

Dev Containers是在你本地机器上跑Docker容器。你装好Docker，装好VS Code扩展，然后打开一个项目，它会自动构建一个容器环境。说白了，就是把你本机变成了一个“容器宿主机”。

Codespaces是GitHub的云端服务。你点一下浏览器里的按钮，GitHub会给你分配一台云虚拟机，上面跑着VS Code Server，你通过浏览器或者本地VS Code连接上去。环境也是容器化的，但机器是GitHub的。

这个区别决定了所有后续体验。本地跑，你控制一切，但消耗你的硬件。云上跑，你不用管硬件，但网络延迟和账单会找上门。

## 启动速度：谁更快？

Dev Containers首次启动要下载镜像、构建容器。一个Node.js项目大概2-5分钟。但第二次启动，因为镜像缓存，10秒内就能用。我测试了一个包含PostgreSQL、Redis的微服务项目，首次构建花了11分钟。之后每次重启都在15秒以内。

Codespaces首次创建也要构建，但GitHub有预构建（Prebuilds）功能。如果你配置了预构建，点开项目到进入编辑器，平均25秒。没有预构建的话，和Dev Containers差不多。

有个细节：Codespaces的机器配置是可以选的。2核8GB的机器启动快，但跑起大型项目会卡。16核64GB的机器启动慢，但编译速度翻倍。Dev Containers完全取决于你本机的性能。我同事的MacBook Pro M3 Max（64GB内存）启动一个大型Java项目只要40秒，而我的Intel Mac要3分钟。

## 成本：谁更省钱？

Dev Containers的成本为零。你只需要有Docker和VS Code。但你的电量、硬盘磨损、内存占用是隐形成本。我跑一个完整的微服务集群（6个服务+3个数据库），本机内存直接飙到32GB，风扇转得像飞机起飞。

Codespaces按使用时长收费。免费用户每月有60小时2核8GB的额度。超过后，2核8GB每小时0.18美元，4核16GB每小时0.36美元。听起来不多，但如果你每天用8小时，一个月就是43.2美元（按2核算）。团队5个人，一个月216美元。

有个小技巧：Codespaces不活跃时会自动暂停，不会继续计费。我设置30分钟无操作自动暂停，一个月实际使用时间只有计费时长的60%左右。

## 协作体验：谁更适合团队？

Dev Containers的协作能力基本为零。你只能自己用。如果你要和同事一起调试，得用Live Share扩展，但那只是共享编辑器，不是共享环境。

Codespaces天生就是为协作设计的。你可以把Codespaces的URL直接发给同事，对方点开就能进入和你完全一样的环境。GitHub还支持“并行开发”，两个人可以同时在一个空间中工作，看到彼此的终端输出。

我团队有个案例：一个前端bug在本地复现不了，但在CI环境里必现。我用Codespaces创建了一个和CI配置一致的环境，把链接发给同事，他进去10分钟就定位了问题。如果用Dev Containers，得让他拉代码、装Docker、配置一样的环境，至少半小时。

## 网络依赖：谁更可靠？

Dev Containers完全离线可用。你在飞机上、地铁里、甚至没网的咖啡馆都能干活。只要项目文件在本地，容器就能跑。

Codespaces依赖网络。我测试过，200ms延迟下，打字都有明显卡顿。100ms以内基本无感。但如果你用的是4G热点或者公共WiFi，体验会打折扣。

有个极端情况：GitHub在2024年3月发生了一次持续4小时的宕机。那天所有Codespaces用户都干不了活。而Dev Containers用户完全不受影响。

## 场景选择：什么情况用哪个？

如果你满足以下任意一条，Dev Containers更适合：
- 经常在无网或弱网环境工作
- 团队规模小（1-3人），不需要频繁协作
- 本机性能足够（16GB以上内存，SSD）
- 对成本敏感，不想每个月多花几十美元

如果你满足以下任意一条，Codespaces更适合：
- 团队需要快速共享开发环境
- 本机性能不足（8GB内存以下的MacBook）
- 需要和CI/CD环境保持完全一致
- 愿意为省时间付费

我自己的方案是混合使用：日常写代码用Dev Containers，需要和同事协作或复现CI环境时用Codespaces。两个工具的配置文件（devcontainer.json）是通用的，所以切换成本很低。

## 最后说一句

没有完美的工具。Dev Containers省钱但费电，Codespaces省心但费钱。选哪个，取决于你更缺钱还是更缺时间。

（数据来源：GitHub 2024年开发者报告、VS Code Marketplace下载统计、个人使用记录）