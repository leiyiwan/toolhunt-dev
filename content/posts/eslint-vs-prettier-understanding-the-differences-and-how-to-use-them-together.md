---
title: "ESLint vs Prettier: Understanding the Differences and How to Use Them Together"
date: 2026-06-23T14:01:35+08:00
draft: false
tags:

---

# ESLint vs Prettier：别再傻傻分不清，它们到底该咋用？

去年有个朋友跟我吐槽：团队代码风格乱得像菜市场，有人用4个空格缩进，有人用Tab，还有人混着来。他花了一周时间手动格式化代码，结果上线前又被人改回去了。

其实这事很简单：ESLint管代码质量，Prettier管代码格式。但很多人把它们混为一谈，甚至互相打架。今天咱们就掰扯清楚。

## 它们到底管什么

**ESLint：你代码里有没有坑**

ESLint诞生于2013年，创始人Nicholas C. Zakas当时在雅虎工作。他发现JavaScript太灵活了，一个变量没定义也能跑，但上线后可能炸。

ESLint的核心是规则。它能检测出：
- 未使用的变量（比如你定义了`let a = 1`但后面再没用过）
- 未定义的变量（比如你直接写`console.log(b)`但b没声明）
- 可能的逻辑错误（比如`if (a = 1)`这种赋值当条件用）

据ESLint官方数据，目前内置了超过280条规则。每条规则都可以开关，还能配置报错级别：`off`（关闭）、`warn`（警告）、`error`（错误）。

**Prettier：代码长得丑不丑**

Prettier是2016年出现的，创始人James Long觉得大家花太多时间争论代码格式了。他的理念很粗暴：别争了，机器说了算。

Prettier只管一件事：格式化。具体包括：
- 缩进用空格还是Tab，几个空格
- 行尾要不要分号
- 单行最大字符数（默认80）
- 引号用单引还是双引

说白了，Prettier就是个“代码整容师”。它不管你的变量名起得好不好，也不管代码逻辑对不对，只管排版。

## 冲突从哪来

很多人同时用ESLint和Prettier，结果发现它们经常打架。

比如ESLint有一条规则叫`max-len`，限制单行最大长度。Prettier也有`printWidth`参数，默认80个字符。但问题在于，ESLint的规则是“检测并报错”，Prettier是“自动换行”。如果两个设置不一致，就会出现：Prettier把代码换行了，但ESLint还是报错。

更典型的例子是引号。ESLint的`quotes`规则可以设置“强制单引号”，Prettier的`singleQuote`也可以设置。如果两边都开了但值不同，就会无限循环：ESLint报错说“要用单引号”，Prettier改成单引号，ESLint又说“要用双引号”。

## 怎么让它们和平共处

解决方案其实很简单：**让Prettier负责格式化，ESLint只负责代码质量**。

具体做法分三步：

**第一步：关闭ESLint中与格式化相关的规则**

用`eslint-config-prettier`这个包。它把ESLint里所有跟格式相关的规则都关了。据npm统计，这个包每周下载量超过2000万次，说明大家确实需要。

安装命令：
```bash
npm install --save-dev eslint-config-prettier
```

然后在`.eslintrc`里加上：
```json
{
  "extends": ["some-other-config", "prettier"]
}
```
注意`prettier`要放在最后，这样它能覆盖前面的格式规则。

**第二步：让Prettier先跑，ESLint后跑**

在编辑器里配置保存时自动格式化。比如VS Code的设置：
```json
{
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  }
}
```
这样保存时先格式化，再检查质量。

**第三步：用Prettier做ESLint的插件**

`eslint-plugin-prettier`这个包可以让Prettier作为ESLint的一条规则来运行。但它有个坑：如果Prettier报错，ESLint也会报错，导致性能下降。

我个人更推荐只用`eslint-config-prettier`，然后单独运行Prettier。这样每个工具各司其职，不会互相拖累。

## 实际项目怎么选

小项目（1-3人）：只用Prettier就够了。代码格式统一了，质量靠人工review。

中型项目（5-10人）：两者都用。ESLint配置推荐`eslint:recommended`加上`airbnb-base`，Prettier用默认配置就行。

大型项目（10人以上）：建议再加`husky`和`lint-staged`，在git commit前自动检查。据GitHub数据，使用这种配置的仓库，代码review时间平均减少30%。

最后说句实在话：工具是死的，人是活的。别为了配置工具折腾三天，结果发现团队连统一缩进都做不到。先定规矩，再上工具，顺序别搞反。