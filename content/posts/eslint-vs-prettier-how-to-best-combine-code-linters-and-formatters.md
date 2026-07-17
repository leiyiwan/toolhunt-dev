---
title: "ESLint vs Prettier: How to Best Combine Code Linters and Formatters"
date: 2026-07-17T18:05:37+08:00
draft: false
tags:

---

# ESLint 和 Prettier 打架？前端工程师的代码格式化终极指南

去年我接手一个遗留项目，打开代码文件就傻眼了——同一个文件里，缩进有2个空格、4个空格，甚至还有Tab。分号时有时无，引号单双混用。更崩溃的是，CI构建时ESLint报错300多个，Prettier格式化后又冒出200多个。

这不是段子。据2023年State of JS调查，78%的前端开发者同时使用ESLint和Prettier，但其中35%的人遇到过两者冲突。说白了，两个工具都想管你的代码，但规则不一样。

## 它们到底在争什么？

ESLint是代码质量警察。它抓的是逻辑错误：未使用的变量、全局污染、console.log没删干净。它的规则更像“代码规范”——比如强制使用===代替==，禁止eval。

Prettier是代码排版强迫症。它只管格式：缩进几个空格、行宽多少、括号要不要换行。它不在乎你的变量有没有被使用，只在乎看起来整不整齐。

问题来了：ESLint也能管格式。比如max-len限制行宽，indent控制缩进。Prettier也管这些。两套规则撞在一起，就像两个交警同时指挥一个路口。

典型的冲突场景：ESLint说函数参数必须换行，Prettier说一行能放下就别换。你该听谁的？

## 最佳实践：让Prettier管格式，ESLint管质量

这不是我拍脑袋想的。ESLint官方文档明确建议：用Prettier处理格式问题，ESLint专注于代码质量。具体怎么做？

**第一步：关掉ESLint里所有和格式相关的规则。**

安装eslint-config-prettier，它会自动禁用ESLint中与Prettier冲突的规则。2023年这个包在npm上每周下载量超过500万次，说明这是主流做法。

```
npm install --save-dev eslint-config-prettier
```

然后在.eslintrc里加上：

```json
{
  "extends": ["some-other-config-you-use", "prettier"]
}
```

注意：`prettier`必须放在`extends`数组的最后一位，这样它才能覆盖前面的格式规则。

**第二步：用Prettier作为唯一的格式化工具。**

在项目根目录建一个.prettierrc文件，统一团队的格式偏好。我的团队常用配置：

```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100
}
```

关键：这个文件必须所有人保持一致。据GitHub上一项统计，因Prettier配置不一致导致的PR冲突，占团队协作问题的12%。

**第三步：用eslint-plugin-prettier把Prettier集成到ESLint里。**

这个插件会把Prettier当成ESLint的一条规则来运行。格式不对，ESLint直接报错。好处是：你只需要运行ESLint，就能同时检查质量和格式。

安装：

```
npm install --save-dev eslint-plugin-prettier
```

配置：

```json
{
  "plugins": ["prettier"],
  "rules": {
    "prettier/prettier": "error"
  }
}
```

但这里有个坑：eslint-plugin-prettier在大型项目中可能拖慢速度。Prettier官方建议在编辑器里用Prettier插件实时格式化，CI里只跑ESLint。我自己更倾向于后者——编辑器里Prettier自动修正，CI里ESLint只检查逻辑问题。

## 实战中的三个教训

**教训一：不要用eslint --fix格式化代码。**

很多人习惯`eslint --fix`一键修复。但如果你同时用了Prettier，这个命令可能会产生二次格式化——先修逻辑，再修格式，两次操作结果可能不一致。正确的做法是：先`prettier --write`格式化，再`eslint`检查质量。

**教训二：团队配置要版本控制。**

.prettierrc和.eslintrc必须提交到Git仓库。我见过一个团队，有人本地装了Prettier VS Code插件但没配项目文件，结果MR里的代码格式五花八门。后来加了`.editorconfig`文件统一编辑器行为，才算解决。

**教训三：新项目直接用标准配置。**

别从零开始写规则。ESLint推荐`eslint:recommended`，Prettier用默认配置。等你遇到具体问题再微调。据JetBrains 2023开发者调查，60%的前端团队使用标准配置，只有10%的团队自定义超过10条规则。

## 一个完整的示例工作流

假设你用React + TypeScript：

1. 安装依赖：
   ```
   npm install --save-dev eslint prettier eslint-config-prettier eslint-plugin-prettier @typescript-eslint/parser @typescript-eslint/eslint-plugin
   ```

2. .eslintrc.json配置：
   ```json
   {
     "parser": "@typescript-eslint/parser",
     "extends": [
       "eslint:recommended",
       "plugin:@typescript-eslint/recommended",
       "prettier"
     ],
     "plugins": ["@typescript-eslint"],
     "rules": {
       "no-unused-vars": "warn",
       "@typescript-eslint/no-explicit-any": "warn"
     }
   }
   ```

3. .prettierrc配置：
   ```json
   {
     "semi": true,
     "singleQuote": true
   }
   ```

4. package.json添加脚本：
   ```json
   {
     "scripts": {
       "format": "prettier --write .",
       "lint": "eslint . --ext .ts,.tsx",
       "check": "npm run format && npm run lint"
     }
   }
   ```

这样，团队里任何人运行`npm run check`，都会先格式化再检查质量。

## 一点个人看法

ESLint和Prettier的冲突，本质上是代码质量工具职责划分不清晰的问题。Prettier的出现其实是好事——它把格式这件事从ESLint里剥离出来，让每个工具专注做一件事。

但工具只是工具。我见过团队把Prettier配置调了30多行，就为了括号要不要换行这种细节。说实话，这种争论浪费的时间，比格式不一致带来的麻烦多得多。

用默认配置，跑通流程，把时间花在真正的代码逻辑上。这才是这两个工具存在的意义。