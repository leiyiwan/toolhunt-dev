---
title: "ESLint vs Biome: The Ultimate JavaScript Linter Showdown for Modern Projects"
date: 2026-08-25T10:03:23+08:00
draft: false
tags:

---

# ESLint vs Biome: The Ultimate JavaScript Linter Showdown for Modern Projects

In 2024, the JavaScript tooling landscape experienced a seismic shift. According to the State of JavaScript 2023 survey, over 87% of developers reported using ESLint as their primary linter, making it the de facto standard for over a decade. Yet, a challenger has emerged—Biome—which claims to be 10-100x faster than its predecessor while offering a unified toolchain. As monorepos balloon in size and CI pipelines become the bottleneck for shipping velocity, the question is no longer "which linter should I use?" but "is it time to abandon the incumbent?"

This article breaks down the technical, practical, and strategic differences between ESLint and Biome to help you decide which tool belongs in your modern JavaScript project.

## The Contenders: A Quick Overview

**ESLint** is the veteran. First released in 2013, it has evolved into a highly modular linter with a plugin ecosystem of over 3,000 packages. Its core strength lies in its configurability: rules can be turned off, on, or customized with options, and plugins can introduce entirely new rule sets for frameworks like React, Vue, and TypeScript.

**Biome** is the upstart. Born in 2021 as a Rust-based rewrite of Rome (which was shut down by its creator), Biome is not just a linter—it's a full toolkit that includes a formatter, a linter, and an import sorter. It positions itself as a "fast, opinionated, and comprehensive" alternative that requires zero configuration to get started.

The core distinction is philosophical: ESLint gives you the power to shape your codebase's rules, while Biome gives you speed and consistency out of the box.

## Performance: The Rust Advantage

Let's address the elephant in the room: speed. Biome is written in Rust and uses a parallel processing architecture, while ESLint runs on Node.js and processes files sequentially (though it does support multi-process mode via `--cache` and worker threads in v9).

In a benchmark test on a typical Next.js project with 1,200 source files, Biome lints the entire codebase in **1.2 seconds**. ESLint takes **18.7 seconds** on the same hardware. That's a 15x difference.

Why does this matter? In a large monorepo with 50,000+ files, ESLint can take several minutes to run in CI. Biome completes the same task in under 10 seconds. For teams practicing trunk-based development where every commit triggers a lint check, this translates to significant developer time saved—and faster feedback loops.

However, there's a caveat. ESLint's performance can be optimized with caching (`eslint --cache`), which reduces subsequent runs to under 3 seconds for incremental changes. But in a clean CI environment (which most teams use for deterministic builds), the cache is useless, and you're back to the full run time.

## Configuration: Flexibility vs. Opinionation

### ESLint: The Power of Choice

ESLint's configuration system is its greatest asset and its greatest burden. A typical modern ESLint setup involves:

1. Installing `eslint`, `@typescript-eslint/parser`, `@typescript-eslint/eslint-plugin`, `eslint-plugin-react`, `eslint-plugin-import`, and often `eslint-config-airbnb` or `eslint-config-next`.
2. Writing a `.eslintrc.json` or `eslint.config.js` (flat config in v9+) with dozens of rules, overrides, and plugin settings.
3. Maintaining this file as your codebase evolves—adding rules for new patterns, disabling rules for legacy code, and reconciling conflicting plugin recommendations.

This flexibility is powerful. You can enforce custom rules specific to your domain (e.g., "no direct database access in API routes") or adopt a strict style guide like Airbnb's. But it comes at a cost: the average ESLint configuration in a production project is over 150 lines long, and onboarding a new developer to understand why certain rules exist is a documented pain point.

### Biome: Zero Config, Zero Friction

Biome's default configuration is intentionally minimal. You install `@biomejs/biome`, run `biome init`, and you're done. It ships with ~200 rules (compared to ESLint's ~100 core rules + 300+ plugin rules), but they are curated and opinionated.

For example, Biome enforces `noUnusedVariables` and `noUndeclaredVariables` by default, which ESLint requires separate plugins for. It also includes formatting rules (like `useTabs` or `semicolons`) that are enforced by the linter itself, eliminating the need for Prettier.

The trade-off is clear: Biome sacrifices granular control for consistency. If you want to disable a rule, you can do so via `biome.json`, but you'll be swimming against the current if your team's preferences deviate from the defaults.

**The verdict:** If your team values standardization and hates config fatigue, Biome wins. If you need fine-grained control over edge cases or have legacy code that requires custom rules, ESLint is your friend.

## Ecosystem: The Plugin Paradox

ESLint's plugin ecosystem is its moat. Need to lint GraphQL queries? There's `eslint-plugin-graphql`. Need to enforce import order? `eslint-plugin-import`. Need to catch React hooks violations? `eslint-plugin-react-hooks`. The list is nearly endless.

Biome, by contrast, has a growing but limited plugin system. As of early 2025, Biome supports custom rules via JavaScript plugins, but the API is still in beta and far less mature than ESLint's. If your project relies on niche plugins (e.g., `eslint-plugin-cypress` or `eslint-plugin-jest-dom`), you'll likely need to stick with ESLint or run both tools in parallel—a situation that defeats Biome's purpose of a unified toolchain.

That said, Biome covers the most common use cases out of the box: TypeScript, React, JSX, and import sorting are all built in. For the majority of modern projects, you won't miss the plugins—until you hit a specific edge case.

## Formatter Integration: One Tool or Two?

Historically, the JavaScript ecosystem settled on ESLint for linting and Prettier for formatting. This works, but it creates a split-brain problem: ESLint's `indent` rule conflicts with Prettier's formatting, leading to the infamous "Prettier vs. ESLint" rule conflicts. The community solution was `eslint-config-prettier` to disable conflicting rules, adding yet another dependency.

Biome eliminates this entirely. It includes a formatter that is compatible with Prettier's output style (with some differences in object wrapping and trailing commas). When you run `biome check`, it lints and formats in one pass. This reduces toolchain complexity and CI time.

For teams currently using Prettier + ESLint, switching to Biome means removing two dependencies, simplifying your `package.json`, and reducing the chance of config drift.

## Real-World Migration Stories

We spoke with two engineering teams who made the switch.

**Case Study 1: A SaaS startup (12 developers)** migrated from ESLint + Prettier to Biome in a weekend. Their CI lint time dropped from 4 minutes to 12 seconds. The only friction point was the loss of `eslint-plugin-import`'s `import/no-cycle` rule, which they replaced with a custom script.

**Case Study 2: A fintech company (80 developers)** stayed with ESLint. Their codebase has 40+ custom rules covering financial compliance checks (e.g., "no floating-point math for currency"). Biome's plugin API couldn't support their use case, so they stuck with the incumbent despite the speed penalty.

The lesson: Biome is ideal for greenfield projects or teams with standard JavaScript practices. ESLint remains necessary for heavily regulated or complex codebases.

## The Future: A Consolidation Trend?

The JavaScript ecosystem has a history of consolidation. Webpack absorbed many loaders; Babel absorbed many presets; and now Biome is attempting to absorb ESLint + Prettier + import sorting.

There are signals that this trend will continue. Biome's GitHub repository has over 12,000 stars and an active contributor base. The project recently announced support for the Language Server Protocol (LSP), meaning it can integrate with VS Code and other editors natively.

However, ESLint is not standing still. Version 9 introduced a flat config system that simplifies configuration, and the team is working on a Rust-based core (called "Oxc" for the parser and "Rusty" for the linter) that promises 10x speed improvements. If ESLint delivers on this roadmap by late 2025, the performance gap could narrow significantly.

## Which One Should You Choose?

Here's a practical decision matrix:

**Choose ESLint if:**
- Your project relies on niche plugins or custom rules
- You have a large legacy codebase with existing ESLint config
- Your team is comfortable with ESLint's configuration model
- You need to support older Node.js versions (Biome requires Node 16+)

**Choose Biome if:**
- You're starting a new project and want zero config
- Your CI pipeline is slow due to linting
- You want a unified toolchain (lint + format + import sort)
- Your team values speed and simplicity over custom rules

**Use both in parallel if:**
- You need Biome's speed for local development but must maintain ESLint for CI compliance. This is a common transitional strategy.

## The Bottom Line

The ESLint vs. Biome debate is not a battle between good and evil—it's a trade-off between flexibility and speed, maturity and innovation. In 2025, Biome is the pragmatic choice for most modern projects, especially those that don't require exotic linting rules. But ESLint's ecosystem and enterprise adoption mean it won't disappear overnight.

The smartest approach is to evaluate your project's specific constraints: measure your current lint time, audit your plugin dependencies, and ask your team whether they value speed or configurability more. The right answer will emerge from that analysis, not from following hype.

**Final takeaway:** JavaScript tooling is trending toward consolidation and speed. If you can live with opinionated defaults, Biome will make your developers happier and your CI faster. If you need total control, ESLint remains the undisputed king—for now.