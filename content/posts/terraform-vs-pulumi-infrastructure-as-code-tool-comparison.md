---
title: "Terraform vs Pulumi: Infrastructure as Code Tool Comparison"
date: 2026-07-16T18:05:12+08:00
draft: false
tags:

---

# Terraform vs Pulumi：谁才是基础设施即代码的王牌？

2023年，全球IaC市场规模突破16亿美元。HashiCorp的Terraform和Pulumi是两大主角。一个稳坐头把交椅，一个靠编程语言杀出重围。选谁？先别急着站队。

## 底层逻辑：声明式 vs 程序式

Terraform用HCL（HashiCorp Configuration Language）定义基础设施。你写“我想要一台EC2，配置是t2.micro”，Terraform就给你造出来。HCL是声明式的——你说结果，不管过程。

Pulumi反着来。它支持TypeScript、Python、Go、C#。你用Python写个for循环，就能创建100个AWS S3桶。代码逻辑直接控制资源创建。

**区别在哪？**  
Terraform适合“描述状态”，Pulumi适合“编写逻辑”。举个例子：你要创建10个不同配置的数据库。Terraform得写10个resource块，或者用count和for_each绕弯子。Pulumi一个for循环搞定，还能动态生成配置。

但声明式有好处：状态文件（state file）是Terraform的核心。它记录你所有资源的当前状态，每次运行先对比再执行。Pulumi不用状态文件？错了，它也有状态，但存在Pulumi Cloud或自托管后端里。

## 生态：谁的地盘谁做主

Terraform的Provider生态是护城河。截至2024年3月，官方注册表有超过3000个Provider。AWS、Azure、GCP、Kubernetes、Datadog……你想得到的都有。连一些冷门服务，比如Cloudflare、GitHub，也有社区维护的Provider。

Pulumi的Provider数量少一个量级。它原生支持AWS、Azure、GCP、Kubernetes，但长尾服务得靠社区贡献。官方数据：Pulumi有约200个核心Provider，而Terraform有3000+。

**但Pulumi有杀手锏：跨云编排。**  
Terraform每个Provider独立，A和B的资源互相不知道。Pulumi里，你用同一份代码同时调用AWS SDK和Azure SDK，逻辑上可以串起来。比如：先创建AWS的VPC，再根据结果创建Azure的虚拟机。Terraform得写两个模块，还得手动传递输出。

## 学习曲线：HCL vs 通用语言

Terraform的HCL是专门设计的。语法简单，但坑多。比如：循环只有count和for_each，条件判断只有count和三元运算符。写复杂逻辑时，HCL就像用螺丝刀撬钉子。

Pulumi用通用语言。Python程序员上手就能写。TypeScript开发者甚至能复用现有库。有个真实案例：某公司用Terraform管理Kubernetes集群，想加个自定义策略，得写HCL的locals和data块，折腾两天。换成Pulumi后，直接import一个Python包，两小时搞定。

**但通用语言也有代价。**  
Pulumi的代码里，你随时可能不小心触发API调用。比如在Python里写个`import pulumi_aws`，它不会立刻执行。但如果你在模块顶层的`__init__`里调用了`aws.ec2.get_ami()`，那每次import都会查AWS。Terraform的HCL只在`terraform apply`时才执行，本地跑`terraform plan`只是预览，不会动真格。

## 团队协作：状态管理谁更稳

Terraform的状态文件是单点故障。团队用远程后端（S3、Consul、Terraform Cloud），但锁机制有时会出问题。2022年有次事故：HashiCorp的Terraform Cloud宕机，导致大量用户无法`plan`和`apply`。

Pulumi的状态管理更灵活。它默认用Pulumi Cloud，支持加密、版本历史、审计日志。自托管的话，用AWS S3或Azure Blob Storage。Pulumi Cloud的免费层够小团队用，但大企业得付费。

**Pulumi有个独特功能：自动刷新。**  
Terraform的`terraform refresh`是手动命令，Pulumi在每次`pulumi up`前自动刷新。这意味着如果你手动改了AWS控制台，Pulumi会立刻发现差异。Terraform需要你记得跑`terraform plan`才能看到。

## 成本：开源 vs 商业

Terraform是开源的，但HashiCorp在2023年改了许可证：从MPL 2.0变成BSL 1.1。简单说：商业公司不能直接拿Terraform代码做竞品。但个人和小团队用免费版没问题。Terraform Cloud免费版有5个用户限制，更多用户得付费。

Pulumi也是开源的，许可证是Apache 2.0，更宽松。Pulumi Cloud免费版支持无限用户（但资源数有限制）。企业版按资源数收费，起步价约每月150美元。

**说真的，成本不是核心差异。**  
Terraform Cloud的企业版贵，但Pulumi Cloud的企业版也不便宜。真正差别在：Pulumi的开源版功能几乎和商业版一样，只是少了审计日志和团队协作的高级功能。Terraform的开源版缺了状态锁和远程后端的一些高级特性。

## 到底选谁？

**选Terraform，如果你：**  
- 管理的是传统基础设施，比如VM、网络、数据库  
- 团队已经熟悉HCL，不想折腾  
- 需要大量长尾Provider的支持  
- 追求稳定，不想频繁升级  

**选Pulumi，如果你：**  
- 团队有编程背景，Python/TS熟练  
- 需要跨云复杂编排  
- 想用代码测试框架（Pulumi支持单元测试）  
- 对状态管理有高要求，比如自动刷新  

一个小细节：据Pulumi官方2023年用户调研，约40%的用户是从Terraform迁移过来的。迁移原因前三：编程语言灵活性、更好的错误信息、更快的开发迭代。

**最后说句实话。**  
Terraform是行业标准，Pulumi是挑战者。如果你的场景是“用AWS做电商”，Terraform够了。如果是“用AWS+Azure+GCP做混合云，还要动态调整”，Pulumi更顺手。没有银弹，只有适合。