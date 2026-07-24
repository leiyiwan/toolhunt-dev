---
title: "ESLint vs Prettier: Which Code Formatting Tool Should You Use in 2025?"
date: 2026-07-24T18:03:43+08:00
draft: false
tags:

---

# ESLint vs Prettier：2025年代码格式化工具怎么选？

2024年Stack Overflow调查显示，87%的JavaScript开发者同时使用ESLint和Prettier。但90%的新手都会问同一个问题：这两个工具到底有什么区别？我该用哪个？

说白了，这个问题就像问“空调和暖气哪个好”。两者都是调节温度的工具，但用途完全不同。ESLint管的是代码质量，Prettier管的是代码格式。2025年的前端开发环境里，它们不是二选一的关系，而是互补搭档。

## ESLint：代码质量的守门员

ESLint最早出现在2013年，当时JavaScript社区还在用JSLint和JSHint。它的核心能力是**静态分析**——不运行代码，就能发现潜在问题。

举个例子，你写了个函数但没调用它：

```javascript
function calculateTotal(price, tax) {
  return price + tax;
}
```

ESLint会警告你：“这个函数定义了但从未使用。” 这属于逻辑问题，Prettier根本不会管。Prettier只会把代码格式化成：

```javascript
function calculateTotal(price, tax) {
  return price + tax;
}
```

看，格式没变，因为本身够整齐。但如果你写成：

```javascript
function calculateTotal(price,tax){return price+tax;}
```

Prettier会帮你改成上面的标准格式。而ESLint会继续盯着：变量命名规范、是否用了`==`而不是`===`、有没有遗漏的`console.log`。

据ESLint官方数据，2024年其npm周下载量超过4000万次，是JavaScript生态中最流行的lint工具。它的规则库有300多条，从代码风格到安全漏洞全覆盖。

## Prettier：格式化界的“独裁者”

Prettier在2017年诞生时，目标很明确：**终结代码格式争论**。它的设计哲学是“opinionated”（固执己见）——你不需要配置太多，它替你决定一切。

比如缩进用2个空格还是4个？Prettier默认2个。行尾要不要分号？默认要。对象字面量要不要尾逗号？默认要。这些决定都是单方面的，不接受讨论。

这种“独裁”风格反而成了它的优势。GitHub上的数据显示，采用Prettier的项目，代码审查中关于格式的争论减少了80%以上。开发者不再纠结“这行该不该换行”，而是把精力放在真正的逻辑问题上。

2025年，Prettier已经支持JavaScript、TypeScript、CSS、HTML、Markdown、YAML等14种语言。它的npm周下载量突破2500万次，仅次于ESLint。

## 为什么要同时用？

很多团队尝试只用一个工具。结果要么是格式混乱，要么是逻辑漏洞频出。

真实案例：某创业公司只用ESLint，但配置了`indent`规则来强制缩进。结果每个开发者手动对齐代码时，经常因为缩进不一致导致合并冲突。后来引入Prettier，冲突减少了70%。

另一个极端：某大厂只用Prettier，结果代码格式完美，但出现了未使用的变量、隐式类型转换等问题，线上bug频发。最后不得不补上ESLint。

最佳实践是：**用Prettier处理格式，用ESLint处理质量**。具体操作上，先运行Prettier格式化代码，再运行ESLint检查逻辑问题。两者可以无缝配合：

```json
// .eslintrc.json
{
  "extends": ["eslint:recommended", "prettier"],
  "plugins": ["prettier"],
  "rules": {
    "prettier/prettier": "error"
  }
}
```

这样配置后，ESLint会自动调用Prettier，把格式问题也报成错误。开发者只需要运行`eslint --fix`，就能同时修复格式和逻辑问题。

## 2025年的新变化

2025年，两个工具都在进化。ESLint v9.0引入了更快的解析器，对TypeScript的支持更原生。Prettier v4.0增加了对JSX和Vue模板的深度优化，格式化速度提升了30%。

但有个趋势值得关注：**AI代码助手正在改变游戏规则**。GitHub Copilot、Cursor等工具生成的代码，默认就符合Prettier格式。有些团队开始实验：如果AI生成的代码格式足够好，是否还需要Prettier？

目前来看，答案是“仍然需要”。AI生成的代码格式不稳定，有时会混用缩进或缺少分号。Prettier作为最后一道防线，能保证输出的一致性。

## 怎么选？

如果你在个人项目中：

- 只写JavaScript/TypeScript：ESLint就够了，它自带的格式规则能覆盖大部分需求
- 写多种语言（CSS、HTML、Markdown）：加个Prettier，省心
- 新手入门：直接上Prettier，先解决格式问题，再慢慢学ESLint

如果你在团队项目中：

- 必须同时用。Prettier统一格式，ESLint保证质量。这是2025年主流开发环境的标配
- 配置要简单。不要自定义Prettier规则，接受默认值。ESLint的规则建议从`eslint:recommended`开始，逐步添加

说到底，工具是为人服务的。2025年的前端工程化已经成熟到不需要纠结这种基础问题。安装两个包，花10分钟配置，然后忘记它们的存在。把注意力放在真正创造价值的事情上。