---
title: "ESLint vs Biome: Is Biome Ready to Replace Your Entire JavaScript Linting and Formatting Setup?"
date: 2026-09-06T10:02:01+08:00
draft: false
tags:

---

# ESLint vs Biome: Is Biome Ready to Replace Your Entire JavaScript Linting and Formatting Setup?

In 2024, the JavaScript tooling landscape experienced a seismic shift. According to the State of JavaScript 2023 survey, developer satisfaction with build tools and linters hit an all-time low, with configuration complexity cited as a top pain point. Enter Biome—a toolchain written in Rust that promises to unify linting, formatting, and more in a single binary, boasting speeds that are often 10x to 100x faster than existing solutions. The pitch is seductive: ditch the fragile ecosystem of ESLint plugins, Prettier configs, and Babel transforms for one fast, opinionated tool.

But the JavaScript ecosystem is notoriously sticky. ESLint has been the standard for over a decade, with a plugin ecosystem numbering in the thousands. Prettier, despite its own controversies, is ubiquitous. So, the question isn't just "Is Biome fast?"—it's "Is Biome fast *enough* to justify abandoning the tools you already know?" This article breaks down the technical realities, migration pain points, and ecosystem maturity to help you decide if Biome is ready for your production stack.

## The Core Difference: Architecture and Philosophy

The fundamental divergence between ESLint and Biome lies in their execution models. ESLint is a Node.js application that operates on an Abstract Syntax Tree (AST) built by Espree. It’s rule-based, pluggable, and mutable. Every plugin you add (TypeScript, React, import sorting) introduces a new parser or a new set of rules that must be loaded, parsed, and executed at runtime. While ESLint 9 introduced a faster engine, it still operates within the single-threaded, JIT-compiled constraints of the V8 engine.

Biome, on the other hand, is written in Rust and compiled to native code. It parses JavaScript, TypeScript, and JSX directly into its own lossless AST—meaning it can preserve formatting details during transformations. This allows Biome to offer a formatter and a linter that share the same underlying representation. The result is a tool that starts in milliseconds, not seconds, and uses a fraction of the memory. In benchmarks run by the Biome team, it lints files roughly 20x faster than ESLint on a typical codebase. For developers working on monorepos with thousands of files, this difference is not a nicety; it’s a daily productivity boost that eliminates the "wait for the linter" dead time.

## Formatting: Prettier Parity vs. Prettier Supremacy

Let’s address the elephant in the room: Prettier. For years, the "standard" setup has been ESLint for logic and Prettier for style. Biome aims to kill this dual-tool setup by offering a formatter that is, in its own words, "compatible with Prettier." The Biome team has invested heavily in matching Prettier’s output style. As of version 1.8, Biome passes over 95% of Prettier’s test suite. This is an impressive feat, but the remaining 5% is where friction lives.

Prettier’s philosophy is "no options." Biome initially adopted this, but has since introduced a few configuration options (like `semicolons` and `quoteStyle`) that Prettier famously refuses to add. This is a double-edged sword. On one hand, it provides flexibility that Prettier users have begged for. On the other hand, it breaks the "just works" promise. If you migrate a large codebase formatted with Prettier 3.x, you will likely find edge cases where Biome formats differently—usually involving nested ternaries, long chains, or specific JSX whitespace handling. It’s not that Biome is wrong; it’s that it’s *different*. For teams with strict formatting standards, this means a one-time, potentially massive diff to your repository that isn't purely cosmetic—it's a change in tooling philosophy.

## Linting: The Plugin Gap is the Real Dealbreaker

If formatting is a 95% match, linting is where the migration story gets complicated. ESLint’s true power is its plugin ecosystem. Need to enforce React Hooks rules? There’s a plugin. Need to catch security vulnerabilities in Express? There’s a plugin. Need custom rules specific to your startup’s code style? You write a plugin in JavaScript.

Biome’s architecture does not support plugins. This is a conscious design choice—plugins are what slow ESLint down and create versioning conflicts. Instead, Biome ships with a curated set of ~200 built-in rules (compared to ESLint’s core ~300, which doesn't include the thousands from plugins). While Biome covers the "recommended" sets for TypeScript, React, and basic correctness, it does not have the long-tail coverage of the community.

Consider the specific rules your team relies on:
- `@typescript-eslint/consistent-type-imports` (Biome has a version)
- `eslint-plugin-import/no-cycle` (Biome does not have cycle detection)
- `eslint-plugin-jsx-a11y` (Biome only covers a fraction of accessibility rules)
- `eslint-plugin-tailwindcss` (Biome has zero Tailwind-specific class ordering or conflict detection)

If your codebase relies on these, Biome is not a drop-in replacement. You would be losing safety nets. The Biome team is rapidly adding rules, but they are building a vertical slice, not horizontal compatibility. For a greenfield project with modern TypeScript, Biome’s default rules are actually quite robust. For a legacy enterprise codebase with 20 plugins, Biome is a downgrade in safety, regardless of speed.

## Configuration and DX: The Uncanny Valley

ESLint’s configuration system is notoriously verbose. The shift to flat config (`eslint.config.js`) in ESLint v9 was an attempt to simplify, but it still requires a deep understanding of `defineConfig`, `plugins`, and `languageOptions`. Biome offers a single `biome.json` file that is remarkably clean. You can enable a recommended preset with three lines of JSON. The CLI is intuitive: `biome check .` runs linting and formatting together, with a `--write` flag for auto-fixing.

However, Biome’s DX has a catch: its error messages, while fast, are sometimes cryptic. ESLint errors often come with lengthy explanations and links to documentation. Biome provides concise messages, but for less common rules, the documentation is sparse. Furthermore, the "fix all" behavior in Biome is more aggressive than ESLint’s. Because it combines formatting and linting, running `biome check --write` might reformat code you didn't intend to touch if your previous Prettier config had custom settings that Biome doesn't recognize.

## Migration Strategy: The "Chicken-and-Egg" Problem

The biggest challenge for Biome adoption isn't technical; it's social. Your team knows ESLint. Your CI pipeline is built around it. Your IDE extensions are configured for it. Migrating to Biome requires a "Big Bang" moment where you accept a large diff and a period of adjustment.

A safer path is a hybrid approach:
1. **Phase 1 (Formatting):** Run Biome as a *formatter only* in CI, comparing its output against Prettier. Keep ESLint running for logic. This lets you identify formatting discrepancies without losing linting safety.
2. **Phase 2 (Linting):** Enable Biome’s linter with the `recommended` preset, but set the rules to "warn" instead of "error." Run it alongside ESLint to see which violations it catches that ESLint misses, and vice versa.
3. **Phase 3 (Switch):** Once the warning count is near zero and you’ve confirmed Biome covers your critical plugin rules, disable ESLint and Prettier.

This gradual approach mitigates risk. As of late 2024, we are seeing major open-source projects like Next.js and React Native exploring Biome for their internal tooling, but they haven't fully replaced ESLint yet—they are using it for specific performance-critical paths.

## Performance in the Real World

Let’s talk numbers. On a repository with 10,000 files, a cold ESLint run can take 60-90 seconds. A Biome run takes 2-3 seconds. In watch mode (via `biome watch`), the difference is imperceptible. For pre-commit hooks using `lint-staged`, ESLint might take 10 seconds to check 50 files; Biome takes 100 milliseconds.

This speed isn't just about patience—it enables new workflows. You can run Biome on every keystroke in your editor without lag. You can lint the entire codebase on every CI push without hitting timeouts. This immediacy encourages developers to actually run the linter, rather than relying on the CI to catch issues at the end of a pull request. That shift alone can improve code quality more than the specific rules you enable.

## The Verdict: Ready for Primetime (with Caveats)

So, is Biome ready to replace your entire setup? The answer depends on your context:

- **For a new project (Greenfield):** Yes. If you are starting fresh with TypeScript and modern React or plain JavaScript, Biome provides a superior developer experience. The speed is transformative, the config is clean, and the bundled rules are sufficient for high-quality code. You will miss some niche plugins, but you won't miss the configuration overhead.

- **For an existing project (Brownfield):** Not yet—unless you have a very simple setup. The lack of plugin support is a hard blocker for any codebase using `eslint-plugin-import`, `eslint-plugin-jsx-a11y`, or framework-specific rules. The formatting differences, while minor, will create noisy diffs that require team buy-in to manage.

- **For the future:** Biome is the most compelling candidate to unseat the ESLint/Prettier duopoly. Its architecture is superior, its speed is undeniable, and its team is executing with remarkable velocity. The roadmap indicates plugin support is not coming soon, but the rule count is growing every month.

**The takeaway:** Don't view this as a binary choice. View Biome as a high-performance engine that is currently missing a few luxury features. If you value speed and simplicity above absolute rule coverage, switch today. If you rely on the long tail of the ESLint ecosystem, monitor Biome’s releases—the gap is closing faster than any tool migration we've seen in the JavaScript ecosystem to date. Your future self will likely be running Biome, but your current self needs to weigh the cost of the migration against the benefit of the speed.