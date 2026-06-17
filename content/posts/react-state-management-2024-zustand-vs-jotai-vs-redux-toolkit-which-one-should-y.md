---
title: "React State Management 2024: Zustand vs Jotai vs Redux Toolkit – Which One Should You Use?"
date: 2026-06-17T14:03:36+08:00
draft: false
tags:

---

# React状态管理2024：Zustand、Jotai、Redux Toolkit，到底该选谁？

2024年，React开发者面临一个幸福的烦恼：状态管理工具太多了。GitHub上，Zustand的Star数已突破4万，Jotai接近2万，而Redux Toolkit的下载量每周超过500万次。三足鼎立的局面下，选错可能意味着多写1000行无意义的样板代码。

## 为什么会有三个选择？

传统Redux太啰嗦。2019年以前，每个状态变更都要写action类型、action creator、reducer，一个简单的计数器需要3个文件。开发者受够了。

Zustand和Jotai应运而生。它们都属于“原子化”或“轻量级”方案，但设计哲学截然不同。Redux Toolkit则是官方对Redux的“抢救”——保留核心思想，砍掉样板代码。

## Zustand：小而美的全局状态

Zustand的思路很直接：一个全局store，用hooks读取和修改。代码量少得惊人。

```javascript
import { create } from 'zustand'

const useStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
}))
```

适合场景：中小型项目，全局状态不多（比如用户信息、主题设置）。Zustand的订阅粒度很细——只有用到的状态变化才会触发重渲染。据官方benchmark，1000个组件同时订阅不同片段，性能比Redux好30%。

缺点：没有内置的异步处理。需要自己写逻辑，或者加中间件。对于复杂的状态派生（比如根据用户ID计算订单列表），Zustand不够优雅。

## Jotai：原子化的细粒度控制

Jotai把状态拆成一个个“原子”（atom）。每个原子可以依赖其他原子。

```javascript
import { atom, useAtom } from 'jotai'

const countAtom = atom(0)
const doubledAtom = atom((get) => get(countAtom) * 2)
```

这解决了Zustand的派生问题。而且Jotai的订阅粒度更细——只有用到doubledAtom的组件才会重渲染，哪怕countAtom变了。

适合场景：需要大量派生状态的项目。比如一个表单，字段之间互相依赖（A字段的值决定B字段是否显示）。Jotai的原子间依赖关系天然适合这种场景。

缺点：概念比Zustand多。新手容易搞混“原子”和“派生原子”。调试时，原子之间的依赖链可能变得复杂。

## Redux Toolkit：大项目的稳定选择

Redux Toolkit（RTK）把Redux的样板代码砍掉了80%。用createSlice替代手写reducer，用configureStore简化配置。

```javascript
import { createSlice, configureStore } from '@reduxjs/toolkit'

const counterSlice = createSlice({
  name: 'counter',
  initialState: 0,
  reducers: {
    increment: (state) => state + 1,
  },
})
```

RTK内置了immer（不可变数据更新）、redux-thunk（异步逻辑）、devtools支持。生态最成熟——有Redux Persist、Redux Query等配套工具。

适合场景：大型项目，多人协作，需要严格的状态管理规范。比如一个电商后台，涉及购物车、用户、订单、商品等多个模块。RTK的中间件机制和调试工具能帮大忙。

缺点：即使简化了，概念仍然比Zustand和Jotai多。学习曲线最陡。对于小项目，RTK显得臃肿。

## 实际选择建议

**选Zustand，如果：**
- 项目规模小（少于20个页面）
- 全局状态不超过5个
- 团队成员习惯写函数式组件

**选Jotai，如果：**
- 状态之间有复杂依赖关系
- 需要频繁更新局部状态（比如实时数据流）
- 团队对React hooks熟悉

**选Redux Toolkit，如果：**
- 项目超过50个页面
- 需要严格的团队规范
- 依赖Redux生态（如RTK Query做数据缓存）
- 团队成员有Redux经验

## 一个反直觉的事实

很多人以为Zustand和Jotai会取代Redux。但据2024年State of JS调查，Redux Toolkit的使用率仍在上升，达到45%，而Zustand是25%，Jotai是12%。原因很简单：大公司不敢轻易换框架。

Redux Toolkit的稳定性、文档完善度、第三方工具链，是Zustand和Jotai短期内追不上的。但中小项目里，Zustand和Jotai确实让代码更清爽。

最后说一句：别纠结。先选一个上手，写着不对再换。React状态管理工具之间迁移成本很低——无非是把useStore换成useAtom，或者反过来。真正浪费时间的，是花两周对比工具，而不是动手写代码。