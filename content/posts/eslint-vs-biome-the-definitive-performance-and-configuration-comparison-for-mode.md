---
title: "ESLint vs Biome: The Definitive Performance and Configuration Comparison for Modern JavaScript Projects"
date: 2026-08-26T18:04:11+08:00
draft: false
tags:

---

# ESLint vs Biome: The Definitive Performance and Configuration Comparison for Modern JavaScript Projects

JavaScript tooling has undergone a quiet revolution. For nearly a decade, ESLint has been the undisputed standard for linting, with Prettier dominating formatting. But in 2023, Biome emerged from the ashes of Rome Tools with a bold promise: a single tool that lints, formats, and refactors at speeds previously thought impossible. By mid-2024, Biome had been downloaded over 3 million times per week, and its GitHub stars had eclipsed 10,000.

The question is no longer *whether* Biome is faster—benchmarks consistently show it is. The real question is whether speed alone justifies migrating your project, your CI pipeline, and your team's muscle memory. This article breaks down the performance metrics, configuration philosophies, and practical trade-offs to help you decide what fits your stack.

## The Performance Gap: Numbers That Actually Matter

Let's get the headline out of the way. Biome is dramatically faster than ESLint. In the official Biome benchmark on a codebase with 500 files and roughly 200,000 lines of code, Biome completed linting in **0.05 seconds** versus ESLint's **2.5 seconds**—a 50x difference. Formatting shows a similar gap: Biome formats the same codebase in **0.02 seconds** versus Prettier's **0.8 seconds**.

But raw speed on a local machine is only part of the story. Consider the CI pipeline where ESLint's `--cache` flag helps but doesn't eliminate cold starts. In a typical GitHub Actions environment, ESLint on a medium-sized monorepo (10,000 files) can take **60-90 seconds** without caching. Biome does the same job in **under 5 seconds**. Over a 10-minute CI run, that's a reduction from 15% of your build time to less than 1%.

There is one caveat worth noting: ESLint's architecture is plugin-based and extensible, which inherently adds overhead. Biome's performance comes from being a compiled binary (written in Rust) with a fixed set of rules. You cannot add a custom rule in Biome without writing Rust code and forking the project. That trade-off is central to everything that follows.

## Configuration: Declarative vs. Imperative

### ESLint's Flexible (and Verbose) Approach

ESLint's configuration is JavaScript-based, which means it's Turing-complete. You can write functions, conditionals, and imports inside your `.eslintrc.cjs` or `eslint.config.js`. This flexibility is powerful but often leads to configuration sprawl. A typical modern ESLint setup involves:

- `eslint` core
- `@typescript-eslint/parser` and `@typescript-eslint/eslint-plugin`
- `eslint-plugin-react`, `eslint-plugin-react-hooks`
- `eslint-plugin-import`
- `eslint-config-prettier` (to disable conflicting rules)
- `eslint-plugin-tailwindcss` or similar framework-specific plugins

That's six-plus dependencies, each with their own versioning, peer dependencies, and potential breaking changes. A common complaint in the community is "ESLint config debt"—the time spent updating plugins when you upgrade your framework or TypeScript version.

Here's what a modern flat config looks like:

```javascript
// eslint.config.js
import js from '@eslint/js';
import tseslint from 'typescript-eslint';
import react from 'eslint-plugin-react';

export default [
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    files: ['**/*.{ts,tsx}'],
    plugins: { react },
    rules: {
      'react/react-in-jsx-scope': 'off',
      '@typescript-eslint/no-explicit-any': 'warn'
    }
  }
];
```

This is clean enough, but it's the *end result* of significant setup time. For a new project, you're looking at 30-60 minutes of configuration and debugging before your linter runs cleanly.

### Biome's Zero-Config Philosophy

Biome takes the opposite approach. It ships with a single `biome.json` file that has sensible defaults tuned for modern JavaScript and TypeScript. Here's the entire configuration for a React project:

```json
{
  "$schema": "https://biomejs.dev/schemas/1.8.0/schema.json",
  "files": { "includes": ["src/**/*.ts", "src/**/*.tsx"] },
  "linter": { "rules": { "recommended": true } },
  "formatter": { "indentStyle": "space", "indentWidth": 2 }
}
```

That's it. No plugins, no parsers, no cross-tool compatibility layers. Biome's rules are organized into groups like `correctness`, `suspicious`, `style`, and `performance`, and the `recommended` set covers most best practices out of the box.

The trade-off is clear: you trade flexibility for simplicity. If you need a rule that doesn't exist in Biome's catalog (for example, a custom rule for your internal API patterns), you're stuck. ESLint lets you write that rule in JavaScript in 20 minutes. Biome requires you to contribute to the Rust codebase.

## Ecosystem and Integration: The Hidden Costs

### ESLint's Mature Plugin Ecosystem

ESLint's biggest advantage is its ecosystem. As of 2024, the ESLint marketplace has over **1,000 plugins** covering everything from GraphQL schema validation to security scanning for AWS CDK. This maturity matters in enterprise environments where linting is a compliance gate, not just a developer convenience.

Consider accessibility. Tools like `eslint-plugin-jsx-a11y` are widely adopted and battle-tested. Biome has some accessibility rules, but they're a fraction of what the ESLint plugin offers. If you're building a public-facing application with strict WCAG requirements, ESLint may be the safer choice.

### Biome's All-in-One Approach

Biome bundles linting and formatting into one binary. This eliminates the ESLint + Prettier + `eslint-config-prettier` dance where you have to ensure Prettier's formatting rules don't conflict with ESLint's stylistic rules. Biome also includes a **refactoring engine** (similar to ESLint's `--fix` but more aggressive) and an **import sorter** that handles `import` statement organization automatically.

For monorepos, Biome offers workspace support where you can have a single `biome.json` at the root and override rules per package. ESLint's flat config also supports this, but it requires more manual wiring.

One practical integration note: Biome has a **VS Code extension** that works well, but ESLint's extension has been around longer and has more refined error reporting and quick-fix suggestions. In my experience, ESLint's inline errors are more actionable for junior developers because they include links to rule documentation.

## Migration Path: Is It Worth the Switch?

If you're starting a greenfield project today, Biome is a compelling choice. The setup time is nearly zero, the performance is transformative for large codebases, and the tool's opinionated defaults will keep your codebase consistent without constant configuration maintenance.

For existing projects, the migration path depends on your current setup:

- **Small to medium projects (under 50 files)**: Biome's import from ESLint and Prettier configs is decent, but you'll likely need to manually review rule differences. Plan for 1-2 hours of cleanup.
- **Large projects with custom rules**: If you have more than 10 custom ESLint rules, stay with ESLint. The migration effort isn't worth the speed gain unless your CI is severely bottlenecked.
- **Projects using framework-specific plugins**: Check if Biome supports your framework's patterns. For example, Biome handles React Hooks rules, but if you rely on `eslint-plugin-react-refresh` or `eslint-plugin-storybook`, you'll lose that coverage.

A pragmatic middle ground: use Biome for formatting and import sorting (where it's a drop-in replacement for Prettier) while keeping ESLint for linting. This gives you most of the performance win without sacrificing your linting rules.

## The Verdict: Not a Replacement, but a Revolution

As of late 2024, Biome is not a drop-in replacement for ESLint in every scenario. The plugin ecosystem gap is real, and the inability to write custom rules in JavaScript is a hard blocker for some teams. However, Biome's performance advantage is not incremental—it's a step change. When you're running linting in CI on every pull request, a 50x speedup translates to faster feedback loops and less developer frustration.

My recommendation: if you're starting fresh, choose Biome and don't look back. If you're on an existing ESLint setup, evaluate your custom rules first. If you have fewer than five and no exotic plugins, migrate. If you're in a large enterprise with deep ESLint investment, wait. The tooling landscape is moving fast, and Biome's team is actively adding new rules with every release.

The bottom line is that the JavaScript ecosystem has been overdue for a performance overhaul. Biome isn't just a faster linter—it's a signal that the era of slow, plugin-heavy tooling is ending. Whether you adopt it today or in a year, the direction is clear: speed and simplicity are winning.