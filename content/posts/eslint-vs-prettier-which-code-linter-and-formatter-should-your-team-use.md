---
title: "ESLint vs Prettier: Which Code Linter and Formatter Should Your Team Use?"
date: 2026-06-28T14:03:20+08:00
draft: false
tags:

---

# ESLint vs Prettier：别争了，两个都要

凌晨两点，GitHub上又炸了。一位开发者提交的PR被同事打回，理由只有一行字：“代码风格不一致。”两人在评论区吵了40条，一个说“空格缩进才是正统”，另一个坚持“Tab键就是真理”。最后项目组长出来和稀泥：“你们用ESLint还是Prettier？”

这个问题，每个前端团队都绕不过去。

## 它们不是同一种东西

很多人把ESLint和Prettier混为一谈，觉得都是管代码格式的。说真的，这俩货的定位完全不一样。

**ESLint是警察，Prettier是美容师。**

ESLint的核心是“找茬”。它能检查出你代码里潜在的错误——比如变量定义了没用、函数里漏了return、用了==而不是===。据ESLint官方统计，它的规则总数超过280条，覆盖从语法错误到代码质量的方方面面。你写一句`console.log(a)`，它都能告诉你“a还没定义”。

Prettier不管这些。它只关心你的代码好不好看。一行超过80个字符？它自动换行。双引号和单引号混用？它统一成一种。对象最后一个属性后面有没有逗号？它也管。Prettier的作者有个执念：代码应该像诗一样整齐，不需要人手动调整格式。

说白了，ESLint帮你避免Bug，Prettier帮你避免吵架。

## 冲突不可避免

问题来了：ESLint也管格式。

ESLint里有大量关于缩进、引号、分号的规则。Prettier也管这些。当你同时用两者时，就像给一个文件派了两个警察——一个说“这里必须用双引号”，另一个说“我改成单引号了”。结果就是保存文件时，两个工具来回改，代码闪个不停，最后报错。

我见过一个团队因为这个吵了三天。最后发现是ESLint的`indent`规则和Prettier的缩进设置冲突了。解决方案其实很简单：**让ESLint只管逻辑错误，格式问题全交给Prettier。**

具体做法是：在ESLint配置里关掉所有与格式相关的规则。ESLint官方提供了一个插件叫`eslint-config-prettier`，装上去一键禁用冲突规则。据npm统计，这个插件周下载量超过1500万次，说明大家都踩过这个坑。

## 实际项目怎么搭

别想复杂了，三步走完。

第一步，装包。`npm install eslint prettier eslint-config-prettier eslint-plugin-prettier -D`。最后那个`eslint-plugin-prettier`的作用是让ESLint把Prettier当成一条规则来跑——这样你运行ESLint时，它会自动调用Prettier检查格式。

第二步，配`.eslintrc.json`。在`extends`数组里把`prettier`放到最后。像这样：
```json
{
  "extends": ["eslint:recommended", "prettier"]
}
```
顺序很重要。Prettier必须在最后，这样才能覆盖掉前面ESLint的格式规则。

第三步，配`.prettierrc`。这个文件里写你团队的格式偏好。比如：
```json
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "all",
  "printWidth": 100
}
```
注意`printWidth`别设太短。很多人跟风设80，结果代码全是换行，反而难读。据Google的代码风格指南，100字符是更合理的折中。

## 谁适合只用其中一个

小项目或单人开发，可以只选一个。

如果你只想要代码没错误，不关心格式美不美，单用ESLint就够了。Vue和React的官方脚手架都默认只带ESLint。Prettier是可选插件。

如果你只想要格式统一，不在乎逻辑检查，单用Prettier也行。不过这种情况很少——大多数项目至少需要ESLint的`no-unused-vars`规则，不然代码里一堆死变量没人管。

一个例外是TypeScript项目。TS本身已经做了很多类型检查，ESLint的作用被削弱了。有些团队在TS项目里只用Prettier，ESLint只开最基础的几条规则。据TypeScript官方文档，从5.0版本开始，他们推荐用`@typescript-eslint`插件配合ESLint，而不是完全抛弃。

## 别让工具绑架团队

最后说点实在的。

我见过最离谱的团队，为了“代码格式100%一致”，在CI里设置了严格规则：只要Prettier检查出一个空格问题，整个构建就失败。结果新人入职第一天，花了两小时研究怎么配置编辑器自动格式化。

工具是为了让人更省心，不是让人更焦虑。

一个简单做法：在`package.json`的`scripts`里加一条`"lint": "eslint . --fix && prettier --write ."`。每次提交前跑一下，自动修好所有问题。配合husky和lint-staged，只在暂存的文件上运行，几秒钟搞定。

据GitHub 2023年的开发者调查，超过60%的前端项目同时使用ESLint和Prettier。这不是巧合——它们分工明确，配合得当的话，能让团队把精力从“这行该不该加空格”转移到真正的业务逻辑上。

说到底，代码是给人读的。格式统一是为了减少沟通成本，不是为了制造新的吵架素材。