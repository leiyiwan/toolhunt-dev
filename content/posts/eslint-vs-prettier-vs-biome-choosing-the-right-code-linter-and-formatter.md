---
title: "ESLint vs. Prettier vs. Biome: Choosing the Right Code Linter and Formatter"
date: 2026-09-06T18:02:18+08:00
draft: false
tags:

---

# ESLint vs. Prettier vs. Biome: Choosing the Right Code Linter and Formatter

In 2024, the JavaScript ecosystem hit a significant milestone: the JavaScript tooling landscape, long dominated by a patchwork of separate utilities, began consolidating. According to the State of JS 2023 survey, over 88% of developers use ESLint, making it the de facto standard for linting. However, a new generation of tools—spearheaded by Biome—is challenging the status quo by promising to replace both ESLint and Prettier with a single, blazing-fast binary.

If you are setting up a new project or considering a migration, the choice between these tools isn't just about syntax highlighting. It impacts your CI pipeline speed, developer experience, and even the architectural decisions of your codebase. This guide breaks down the technical differences, performance metrics, and use cases to help you choose the right stack.

## The Current Standard: ESLint and Prettier

For the better part of a decade, the "gold standard" workflow has involved using two distinct tools that do different jobs:

- **ESLint** focuses on *code quality* and *correctness*. It catches unused variables, detects anti-patterns, and enforces stylistic rules that can prevent bugs (like `no-await-in-loop`).
- **Prettier** focuses exclusively on *code formatting*. It strips away your original formatting and reprints the code in a consistent style, ending the "tabs vs. spaces" debate forever.

The division of labor is clear, but it creates friction. Running two tools requires two configuration files (`.eslintrc` and `.prettierrc`), two separate sets of ignore rules, and an integration layer (like `eslint-config-prettier`) to disable stylistic rules in ESLint that conflict with Prettier. This "glue" code is a common source of frustration and config drift.

### Why Prettier Won the Formatting War

Prettier’s genius lies in its "opinionated" nature. Unlike earlier formatters (like JSCS or JSBeautify), Prettier offers very few options. This is a feature, not a bug. By limiting configuration to things like tab width and semicolons, Prettier ensures that code looks identical across every team and project. It effectively removed formatting decisions from code reviews, allowing developers to focus on logic.

However, Prettier has a critical limitation: **it does not check for errors**. A file with a syntax error or an undefined variable will still be "prettified" successfully. This means you cannot drop ESLint entirely if you rely on Prettier for formatting alone.

## The Contender: Biome (formerly Rome)

Biome entered the scene with a bold promise: "A toolchain for the web." Born from the ashes of Rome (which was shut down in 2023), Biome is a rewrite in Rust. It aims to unify linting, formatting, and even bundling into a single executable.

The performance difference is stark. In independent benchmarks published by the Biome team and verified by the community, Biome runs **~97% faster** than ESLint and **~90% faster** than Prettier on large codebases. On a typical monorepo with 10,000 files, ESLint might take 30 seconds to run, while Biome finishes in under 2 seconds.

### Native Language Implementation

The primary reason for this speed is the language choice. ESLint and Prettier are written in JavaScript and run on Node.js. They parse the Abstract Syntax Tree (AST) using JavaScript objects, which are memory-intensive and slow to traverse. Biome, written in Rust, uses a flat, contiguous memory layout for its AST. This allows for parallel processing and cache-friendly access patterns that are impossible in a garbage-collected runtime.

### Feature Parity and Gaps

As of Biome v1.8, the project boasts over 200 lint rules. While this is fewer than ESLint’s 300+ core rules (plus hundreds of plugins), Biome covers the most impactful rules:

- **Correctness:** `noUnusedVariables`, `noConstantCondition`
- **Suspicious:** `noDoubleEquals`, `noDebugger`
- **Style:** `useConst`, `noVar`

The biggest gap remains **plugin support**. ESLint has a massive ecosystem of plugins (React, TypeScript, Tailwind, etc.). Biome currently ships with built-in support for JSX and TypeScript syntax, but it does not support custom plugins. If you rely on a niche plugin like `eslint-plugin-jsx-a11y` for accessibility, you cannot use Biome yet.

## Configuration and DX Comparison

The developer experience differs significantly between the two stacks.

### ESLint: Powerful but Verbose

ESLint 9 introduced the new flat config system (`.eslint.config.js`), which replaced the legacy `.eslintrc`. While this modernizes the system, it is still verbose. A basic setup with TypeScript requires installing `typescript-eslint`, merging configs, and handling parser options. Here is a minimal example:

```js
// eslint.config.js
import tseslint from 'typescript-eslint';

export default tseslint.config(
  ...tseslint.configs.recommended,
  {
    rules: {
      '@typescript-eslint/no-unused-vars': 'error',
    },
  }
);
```

### Biome: Zero Config to Start

Biome follows the "batteries included" philosophy. A single command initializes a config file:

```bash
bunx @biomejs/biome init
```

This generates a `biome.json` file with sensible defaults. The configuration schema is much flatter and easier to read than ESLint’s. For example, to enforce using `const` where possible, you simply add:

```json
{
  "linter": {
    "rules": {
      "style": {
        "useConst": "error"
      }
    }
  }
}
```

Biome’s config file also unifies formatter and linter settings in one place, eliminating the need for a separate `.prettierrc`.

## Integration with Editors and CI

### Editor Experience

All three tools offer VS Code extensions. The key difference lies in **"format on save"** behavior.

- **Prettier** is the default formatter for many editors. You set it as the default and it runs on save.
- **ESLint** has a `--fix` flag that can format code on save, but it is slower and often conflicts with Prettier if both are enabled.
- **Biome** acts as both a linter and formatter. In VS Code, you can set Biome as the default formatter and enable `editor.formatOnSave`. It also supports `biome check --write` which applies both safe fixes and formatting in one command.

One significant DX advantage of Biome is the **error recovery** in its parser. If you are typing code and have a syntax error, ESLint often crashes or shows a red screen, refusing to lint the rest of the file. Biome’s parser is designed to recover from syntax errors, allowing it to continue providing linting feedback on the parts of the file that are syntactically valid. This makes the feedback loop much smoother.

### CI/CD Pipeline Speed

In a CI environment, speed translates directly to cost. If you use GitHub Actions, every second of compute time counts toward your monthly quota. A typical CI job might run:

1. `npm run lint` (ESLint)
2. `npm run format:check` (Prettier)

With Biome, this is a single command: `biome ci`. This command runs the formatter check and the linter simultaneously, failing the build if any issues are found. Because Biome is a compiled binary, you don't need to install `node_modules` to run it—you can use `bunx` or download the binary directly, saving significant install time in CI.

## Migration Strategy: Should You Switch?

If you are starting a new project today, **Biome is a compelling choice**. The speed alone justifies the switch, and the configuration simplicity lowers the barrier to entry for new developers. The lack of plugins is a non-issue if you stick to standard linting rules.

For existing projects, the migration path depends on your rule usage:

1. **The 80/20 Rule:** Run `biome migrate eslint` to automatically convert your ESLint config to Biome’s format. The tool will map equivalent rules and leave comments for rules that don't have a direct equivalent.
2. **Audit Your Plugins:** If you use React-specific rules (like `react-hooks/rules-of-hooks`), check if Biome’s `nursery` rules cover them. As of mid-2024, Biome supports React hooks rules but not all accessibility rules.
3. **Run in Parallel:** Do not delete your ESLint config immediately. Run both tools in CI for a sprint. Use `biome check --write` to format the codebase, then compare the diff. If the diff is small, you can safely switch your formatter to Biome and keep ESLint for linting only.

### The Hybrid Approach

A pragmatic middle-ground strategy is to use **Biome for formatting** and **ESLint for linting**. This gives you the speed of a Rust-based formatter while retaining the plugin ecosystem of ESLint. To do this, you disable formatting rules in Biome (or use it solely as a formatter) and disable stylistic rules in ESLint. This hybrid reduces the cognitive load of maintaining two formatters.

## The Verdict

The JavaScript tooling ecosystem is no longer a two-horse race. Here is a practical breakdown:

- **Choose ESLint + Prettier** if you have a large, established codebase with heavy reliance on custom ESLint plugins, or if your team values the massive community ecosystem and extensive documentation.
- **Choose Biome** if you are starting fresh, working in a monorepo where CI speed is critical, or if you are tired of maintaining multiple config files and dependency trees.
- **Choose Biome (Formatter) + ESLint (Linter)** if you want incremental speed gains without abandoning your existing ESLint investment.

The future is clear: Rust-based tooling is the direction of the ecosystem. Just as esbuild and SWC revolutionized bundling, Biome is set to do the same for linting and formatting. The only question is whether your team is ready to make the leap now or wait for the plugin ecosystem to catch up. In either case, the era of waiting 10 seconds for a linter to run is coming to an end.