---
title: "LocalStack vs AWS SAM: Which Serverless Development Tool is Right for You?"
date: 2026-06-25T18:02:24+08:00
draft: false
tags:

---

# LocalStack vs AWS SAM：你的无服务开发该选谁？

2023年，AWS Lambda每天处理超过10万亿次请求。但真正让开发者头疼的，不是Lambda本身，而是本地调试。一个Bug在云端反复部署测试，光等反馈就能耗掉半天。于是，LocalStack和AWS SAM成了两把钥匙。

但选哪把？我们来拆开看。

## 一个模拟，一个框架

LocalStack做的事很简单——在你的电脑上跑一个假的AWS。它用Docker容器模拟S3、DynamoDB、Lambda等40多项服务。你写代码，它假装是AWS，返回一样的结果。说白了，它是个本地玩具版AWS。

AWS SAM则不同。它是AWS官方出的框架，帮你定义、构建、部署无服务应用。它用CloudFormation模板描述架构，本地用Docker模拟Lambda和API Gateway。但它的核心目标不是模拟，而是帮你把代码打包推上云端。

一个偏测试，一个偏部署。这是根本区别。

## 速度与真实感，你选哪个？

LocalStack启动很快。一条命令 `localstack start`，30秒内你的电脑就变成了一台迷你AWS。你可以直接调用 `aws s3 ls` 操作本地模拟的S3。据LocalStack官方数据，它的API兼容性覆盖了AWS服务95%以上的功能。

但问题来了——95%不是100%。某个S3的冷启动策略，或者DynamoDB的最终一致性，可能和真实AWS有偏差。你本地跑得欢，一上生产就翻车。

AWS SAM在这方面更老实。它用真实Lambda运行时（比如Python 3.9的Docker镜像），行为更接近生产。但它启动慢。一个包含3个Lambda和1个DynamoDB的项目，SAM本地启动可能要2分钟。而且它只支持Lambda、API Gateway、DynamoDB等少数服务，想测SQS？对不起，没门。

## 谁在用它？

我翻了翻GitHub。LocalStack有5.2万颗星，社区活跃，Issue回复快。它的Pro版（收费）支持更多服务，还提供Web界面看日志。很多创业公司用它做CI/CD测试——在GitHub Action里跑LocalStack，每次提交自动测Lambda逻辑，省下真AWS的费用。

AWS SAM是官方亲儿子。更新快，和AWS控制台、CloudWatch日志无缝对接。大公司更爱它。据AWS官方博客，某金融公司用SAM管理500多个Lambda的部署，CI/CD流水线一天跑200次。SAM的 `sam deploy --guided` 交互式部署，对新手友好。

但社区吐槽也不少。LocalStack的Pro版一年要3000美元，小团队嫌贵。SAM的本地调试体验被骂“像用锤子砸核桃”——日志不清晰，断点难设置。

## 场景决定选择

如果你的工作流是**频繁本地迭代+测试**，LocalStack是首选。举个例子：你写一个处理S3图片上传的Lambda，每次改完代码，本地启动LocalStack，上传一张假图片，看Lambda返回什么。10秒一轮。用SAM，你得先 `sam build` 再 `sam local invoke`，至少40秒。

但如果你要**部署到生产+管理复杂架构**，SAM更稳。它的 `sam package` 和 `sam deploy` 帮你处理好IAM角色、API Gateway配置、Lambda版本管理。LocalStack的部署靠你自己写脚本。

还有第三种选择——两个都用。白天用LocalStack快速写代码，晚上用SAM做集成测试。一个朋友在Slack上跟我说：“LocalStack是跑鞋，SAM是登山靴。跑鞋快，但爬山得换靴子。”

## 一个细节决定成败

我试过用LocalStack测一个依赖SQS的Lambda。代码里调用了 `sqs.receive_message()`，本地跑得好好的。部署到真实AWS后，发现SQS消息可见性超时的行为不一样——LocalStack默认30秒，真实AWS是12秒。排查了两小时。

这个教训是：LocalStack适合测逻辑，不适合测行为。如果你依赖AWS服务的特定时间窗口或一致性模型，一定要在真实环境验证。

## 没有银弹

选LocalStack还是SAM，取决于你的痛点。如果你痛恨部署等待，选LocalStack。如果你痛恨部署失败，选SAM。如果你两个都痛，那就两个都用。

无服务开发已经够复杂了。工具是拿来省事的，不是拿来折腾的。先搞清楚你想解决什么问题，再选工具。别让工具定义你的工作流。

最后说一句：不管你选哪个，记得在CI里跑一遍真实AWS的测试。本地再像，也不是真的。