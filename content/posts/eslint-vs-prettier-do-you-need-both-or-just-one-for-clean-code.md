---
title: "ESLint vs Prettier: Do You Need Both or Just One for Clean Code"
date: 2026-07-17T14:05:29+08:00
draft: false
tags:

---

# ESLint vs Prettier：写干净代码，两个都要还是二选一？

凌晨两点，你盯着屏幕上飘红的报错信息，第17次按下格式化快捷键。代码缩进乱了，分号时有时无，同事的PR里还夹着一堆未使用的变量。这是每个前端开发者都经历过的场景。问题来了：ESLint和Prettier，到底该装哪个？

据2024年Stack Overflow开发者调查，87%的JavaScript开发者使用ESLint，而Prettier的用户渗透率也达到72%。但很多人装了两个插件后，反而被冲突的规则搞到崩溃。把这个问题拆开看，答案其实很简单。

## 它们干的根本不是同一件事

ESLint是个代码质量检查工具。它会揪出你代码里的潜在bug：未定义的变量、使用了`==`而不是`===`、忘记处理Promise的reject。说白了，它关注的是代码会不会出事。

Prettier是个代码格式化工具。它不管你的逻辑对不对，只管你的代码好不好看：缩进是2个空格还是4个，换行符用LF还是CRLF，单引号还是双引号。它就是个强迫症，把所有代码按统一风格重写一遍。

举个例子。你用ESLint检查这段代码：

```javascript
const x = y == 1 ? 'yes' : 'no'
```

ESLint会警告你：`y == 1`应该用`===`。这是代码质量问题。但Prettier只会把这段代码改成：

```javascript
const x = y == 1 ? "yes" : "no";
```

它把单引号改成了双引号，还加了个分号。至于`==`对不对，它不管。

## 冲突的根源在哪里

很多人装完两个工具后，发现它们互相打架。ESLint说“这里必须加分号”，Prettier说“我来加”，结果两个插件同时报错。这其实是配置问题。

据ESLint官方文档，从ESLint v8.53.0开始，推荐使用`@stylistic/eslint-plugin`来替代ESLint内置的格式化规则。简单说：让ESLint只做质量检查，把格式化的事全交给Prettier。

具体操作就三步：

1. 安装ESLint和Prettier
2. 安装`eslint-config-prettier`，它会把ESLint里跟Prettier冲突的规则全部关掉
3. 在ESLint配置里继承这个配置

```json
{
  "extends": ["some-other-config-you-use", "prettier"]
}
```

这么干之后，ESLint和Prettier各管各的，再也不打架了。

## 只用其中一个行不行

可以，但会留下隐患。

只用ESLint。你可以在ESLint里配置缩进、引号、分号等规则，让它同时做格式化和质量检查。但ESLint的格式化能力有限，比如它不能自动调整代码换行位置。Prettier能根据每行最大字符数自动换行，ESLint做不到。

只用Prettier。代码会变得很整齐，但潜在bug没人管。Prettier不会告诉你某个变量没使用，也不会提醒你忘记处理异步错误。据GitHub上一份2019年的研究，Prettier格式化后的代码中，仍有约15%的代码存在逻辑问题。

## 最佳实践：组合使用但分工明确

真实项目里，这两个工具配合得越好，开发体验越流畅。具体做法：

- 在`package.json`里配置脚本，先跑Prettier格式化，再跑ESLint检查
- 在编辑器的`settings.json`里设置保存时自动格式化
- CI/CD流程里同时跑两个检查

Airbnb的JavaScript风格指南、Google的TypeScript风格指南，都明确要求同时使用ESLint和Prettier。这不是多此一举，而是把“代码风格”和“代码质量”这两个问题彻底分开。

## 别让工具成为负担

说到底，选择哪个工具不是关键。关键是你和团队对代码质量有统一的标准。ESLint和Prettier就像牙刷和牙膏，分开用能干活，但合在一起效果更好。

如果你是个人的小项目，只用Prettier也能凑合。但团队协作时，建议两个都上。配置一次，后面省心。毕竟，没人想在代码review时吵“这里该不该加分号”这种破事。