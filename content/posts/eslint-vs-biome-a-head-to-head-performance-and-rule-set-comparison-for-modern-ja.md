---
title: "ESLint vs Biome: A Head-to-Head Performance and Rule-Set Comparison for Modern JavaScript Projects"
date: 2026-09-07T18:02:42+08:00
draft: false
tags:

---

# ESLint vs Biome: A Head-to-Head Performance and Rule-Set Comparison for Modern JavaScript Projects

If you’ve spent more than five minutes in a modern JavaScript repository, you’ve likely felt the sting of waiting for a lint run to finish. A typical mid-sized monorepo running ESLint can take anywhere from 10 to 30 seconds on a cold cache. Multiply that by every developer on your team, every pre-commit hook, and every CI pipeline, and you’re burning serious engineering hours.

Enter Biome. Formerly known as Rome, this toolchain rebranded in 2023 with a singular promise: drop-in JavaScript linting and formatting at Rust speed. But speed alone doesn’t win over a community that has spent a decade building ESLint’s plugin ecosystem. This article compares the two tools across performance benchmarks, rule coverage, extensibility, and real-world usability to help you decide which belongs in your stack.

## The Performance Gap: Benchmarks That Actually Matter

Let’s address the elephant in the room. Biome is fast—not "faster" in the marketing sense, but orders of magnitude faster. In the official Biome benchmark suite, the tool lints a codebase of roughly 20,000 files in about 0.3 seconds. ESLint, configured with the popular `eslint:recommended` set and TypeScript parser, takes approximately 7.5 seconds on the same machine for the same task. That’s a 25x difference.

But raw speed only tells part of the story. The more relevant metric for daily development is *incremental* performance—how long does it take to re-lint a single file after you’ve made a change? ESLint’s caching mechanism (`--cache` flag) helps, but it still needs to parse the file and traverse its AST. Biome, written in Rust and using a parallel architecture, can re-analyze a single file in under 5 milliseconds. For most developers, this means linting becomes effectively instant, which changes your workflow. You stop running lint as a separate step and start relying on it as a live feedback loop in your editor.

One caveat: Biome’s speed advantage narrows when you rely heavily on TypeScript type-aware linting. ESLint with `parserOptions.project` performs type checking, which is inherently slower but catches a class of bugs that pure syntax analysis cannot. Biome does not yet perform full type checking for lint rules. So the performance comparison is not entirely apples-to-apples—it’s more like comparing a sports car to a pickup truck. The sports car is faster, but the truck can carry more cargo.

## Rule Coverage: Where the Ecosystem Still Wins

ESLint’s greatest asset is not its core—it’s the massive plugin ecosystem. As of early 2025, there are over 3,000 community plugins available on npm. The most essential ones for modern JavaScript projects include:

- **typescript-eslint**: Provides type-aware rules like `no-unsafe-member-access` and `no-floating-promises`
- **eslint-plugin-react**: Covers JSX-specific patterns, prop-types, and hooks rules
- **eslint-plugin-import**: Enforces import ordering, no-cycle detection, and path validation
- **eslint-config-next**: Next.js’s opinionated defaults tailored to App Router and Server Components

Biome, by contrast, ships with approximately 200 built-in rules. That number is growing, but the coverage is still heavily weighted toward stylistic and correctness rules. For example, Biome supports `noUnusedVariables`, `noConstantCondition`, and `useExhaustiveDependencies` (the React hooks equivalent). However, it does not yet offer deep integration with framework-specific concerns like Next.js’s `next/image` optimization rules or Vue’s template compiler linting.

The practical implication is this: if your project is a vanilla TypeScript library or a React app with standard patterns, Biome’s rule set covers 80-90% of what you need. If you’re working with a complex monorepo, custom ESLint plugins, or framework-specific conventions, you’ll likely hit a wall where Biome simply doesn’t have an equivalent rule—and you’ll be forced to either disable the check or write a custom rule in Rust (which is a steep learning curve compared to writing a JavaScript ESLint plugin).

## Configuration and DX: A Tale of Two Philosophies

ESLint’s configuration has historically been a source of frustration. The shift from `.eslintrc` (JSON/YAML) to the flat config system (introduced in ESLint v9) was a major overhaul, but it still requires you to understand concepts like `plugins`, `extends`, `parserOptions`, and `settings`. A typical modern ESLint config for a TypeScript React project can easily exceed 80 lines.

Here’s a minimal example of ESLint flat config:

```js
import js from '@eslint/js';
import tseslint from 'typescript-eslint';
import reactHooks from 'eslint-plugin-react-hooks';

export default [
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    files: ['**/*.{ts,tsx}'],
    plugins: { 'react-hooks': reactHooks },
    rules: {
      'react-hooks/rules-of-hooks': 'error',
      'react-hooks/exhaustive-deps': 'warn'
    }
  }
];
```

Biome’s configuration is deliberately minimal. A `biome.json` file with sensible defaults looks like this:

```json
{
  "formatter": {
    "indentStyle": "space",
    "indentWidth": 2
  },
  "linter": {
    "rules": {
      "recommended": true
    }
  }
}
```

That’s it. Biome’s philosophy is "convention over configuration." The defaults are opinionated but reasonable, and you only add overrides when you have a specific reason. For teams that suffer from configuration fatigue, Biome feels like a breath of fresh air. However, for teams that rely on heavily customized rule sets (e.g., enforcing specific import order or banning certain patterns across a monorepo), Biome’s limited configuration surface can feel restrictive.

## Migration Realities: What You’ll Lose and Gain

If you’re considering switching, the migration story is more nuanced than running `npx @biomejs/biome migrate`. The tool does a decent job of translating common ESLint rules to Biome equivalents, but it won’t catch everything. Here’s what you’ll likely lose in the move:

1. **Type-aware rules**: `no-unsafe-argument`, `no-implied-eval`, and `strict-boolean-expressions` are all dependent on TypeScript’s type checker. Biome doesn’t support these yet. You’ll need to rely on your IDE’s TypeScript diagnostics for some of these checks.

2. **Custom plugin rules**: If you’ve written an in-house ESLint plugin (common in large orgs), you can’t just port it. Biome’s custom rule API requires writing Rust code and compiling a native plugin. This is a significant barrier for most teams.

3. **Prettier integration**: Biome includes a formatter that is largely compatible with Prettier’s output, but not 100% identical. If you have a large codebase formatted with Prettier, you’ll see a one-time diff when you switch. Biome provides a `--write` flag to auto-format, but that initial commit can be noisy.

What you gain is equally clear:

- **Unified tooling**: Biome replaces ESLint, Prettier, and (partially) `lint-staged`. One binary, one config file, one execution path.
- **Editor responsiveness**: The VS Code extension for Biome updates diagnostics in near real-time, even on very large files.
- **Simplified CI**: No more npm install of 200+ transitive dependencies required just for linting. Biome is a single binary that installs in under a second.

## The Verdict: Not a Question of "Better," but of "Fit"

The decision between ESLint and Biome ultimately comes down to project complexity and team tolerance for configuration overhead.

**Choose ESLint if:**
- You rely on type-aware linting rules for TypeScript correctness.
- You use framework-specific plugins (Next.js, Vue, Angular, Svelte) that have no Biome equivalent.
- You maintain a custom plugin or need to enforce org-specific patterns.
- Your codebase already has a mature, battle-tested ESLint setup and linting speed is not a bottleneck.

**Choose Biome if:**
- You’re starting a new project and want a zero-config setup that "just works."
- You’re tired of the ESLint + Prettier + plugins configuration sprawl.
- Your lint runs are slow enough to disrupt your workflow (e.g., >10 seconds on pre-commit).
- You’re working on a standard TypeScript/React project that doesn’t need exotic rules.

One pragmatic path is a hybrid approach: keep ESLint for CI and pre-commit hooks where type-aware rules matter, but use Biome’s formatter and fast linting in your editor for immediate feedback. This gives you the best of both worlds, though it does mean maintaining two configs.

The JavaScript ecosystem is trending toward speed and simplicity. Biome’s momentum is real—it’s already adopted by companies like Vercel and is gaining traction in the open-source community. But ESLint’s plugin ecosystem is a moat that won’t disappear overnight. The smart move is to evaluate your own pain points honestly. If linting speed is causing friction, Biome is worth a serious trial. If you need deep type safety and framework-specific rules, ESLint remains the industry standard for good reason.