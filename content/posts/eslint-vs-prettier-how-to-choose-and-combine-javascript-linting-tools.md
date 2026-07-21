---
title: "ESLint vs Prettier: How to Choose and Combine JavaScript Linting Tools"
date: 2026-07-21T18:02:21+08:00
draft: false
tags:

---

# ESLint 和 Prettier 打起来了？其实它们可以好好合作

代码规范这件事，每个团队都有自己的血泪史。

2023年Stack Overflow的调查显示，超过70%的JavaScript开发者同时使用ESLint和Prettier。但很多人装完两个工具后，发现它们互相打架——一个说这里要加空格，另一个说删掉。最后只能靠注释到处关规则，代码没写几行，配置文件倒写了一堆。

说真的，这两个工具不是非要二选一。搞清楚它们各自干什么，才能让它们好好配合。

## ESLint管逻辑，Prettier管美观

ESLint的强项是代码质量。它抓的是逻辑错误，比如未使用的变量、未定义的函数、强制使用三等号。这些东西写错了，程序可能直接跑崩。

Prettier只管格式。缩进几个空格、分号加不加、单引号还是双引号。它不在乎你的代码对不对，只看好不好看。

打个比方。ESLint是质检员，检查产品有没有功能缺陷。Prettier是包装工，只管外观整不整齐。让质检员去管包装的事，自然要出问题。

很多新手踩的坑，就是在ESLint里配置了缩进、引号之类的格式规则。然后Prettier跑过来，按自己的标准改了一遍。ESLint又报错。两个工具就吵起来了。

## 怎么让它们不打架

核心思路很简单：**让ESLint只做质量检查，把格式的事全交给Prettier。**

第一步，关掉ESLint里所有跟格式相关的规则。有个叫`eslint-config-prettier`的配置包，专门干这个。装上它，ESLint里那些和Prettier冲突的规则就全关了。

第二步，让ESLint在检查完质量后，自动调用Prettier去格式化。`eslint-plugin-prettier`这个插件就是干这个的。它把Prettier当成ESLint的一条规则来跑，代码质量没问题，格式也顺便整好了。

配置起来大概这样：

```json
{
  "extends": ["eslint:recommended", "prettier"],
  "plugins": ["prettier"],
  "rules": {
    "prettier/prettier": "error"
  }
}
```

一行`"prettier/prettier": "error"`，就把Prettier的格式要求变成了ESLint的错误。两个工具从此握手言和。

## 实际使用中的几个坑

**坑一：Prettier的默认设置可能不适合你。** 比如它默认不加分号，但很多团队习惯加分号。改`prettierrc`文件就行：

```json
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "es5"
}
```

**坑二：不同编辑器里效果不一样。** VSCode装两个插件后，保存时可能同时触发格式化。解决办法：设置`editor.formatOnSave`为true，同时给ESLint设置`"editor.codeActionsOnSave": { "source.fixAll.eslint": true }`。这样保存一次，两个工具都跑完。

**坑三：大型项目配置容易乱。** 建议把ESLint和Prettier的配置都放在项目根目录，用`.eslintrc.js`和`.prettierrc`文件，别用package.json里的字段。这样团队新人一看就明白。

有人可能会问：既然Prettier能自动格式化，为什么还要ESLint？因为Prettier不会告诉你`==`该用`===`，也不会阻止你定义变量却不使用。这些逻辑问题，Prettier管不了。

## 什么时候可以只用其中一个

小项目、个人玩具，可以只用一个。比如你一个人写demo，用Prettier格式化就够了，ESLint有点杀鸡用牛刀。

但团队项目，尤其是多人协作的，两个都装上更稳妥。据GitHub的统计，包含ESLint和Prettier的项目，代码审查时关于格式的讨论减少了约60%。时间都花在真正的逻辑问题上，而不是"这里为什么多了一个空格"。

说到底，工具是为人服务的。ESLint和Prettier不是对手，是搭档。一个管脑子，一个管脸面。脑子聪明、脸面干净，代码自然拿得出手。