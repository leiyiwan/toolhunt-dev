---
title: "ESLint vs Biome: The Ultimate JavaScript Linter Performance and Configuration Comparison"
date: 2026-08-30T18:05:42+08:00
draft: false
tags:

---

# ESLint vs Biome: The Ultimate JavaScript Linter Performance and Configuration Comparison

In 2024, the JavaScript tooling ecosystem witnessed a seismic shift. Biome, a Rust-based toolkit, emerged from the ashes of Rome Tools with a bold promise: to deliver linting and formatting at speeds that make ESLint feel like dial-up internet. Meanwhile, ESLint—the long-standing champion—quietly released v9 with a new flat config system, proving it has no intention of ceding its throne.

The numbers are staggering. In independent benchmarks, Biome consistently completes linting tasks **10x to 100x faster** than ESLint on large codebases. For a monorepo with 10,000 files, ESLint might take 60 seconds; Biome does it in under 3. But speed is only half the story. The real battleground is configuration complexity, ecosystem maturity, and rule coverage.

If you're evaluating these tools for a new project or considering a migration, here is the definitive breakdown.

## The Performance War: Rust vs JavaScript

Let's address the elephant in the room: performance. Biome is written in Rust and compiled to native machine code. ESLint runs on Node.js, which means every file it processes is parsed, traversed, and linted by JavaScript's event loop. This architectural difference is the root cause of the performance gap.

### Cold Start and File Processing

When you run ESLint on a fresh checkout, it must:
1. Load the Node.js runtime
2. Parse your `.eslintrc` or `eslint.config.js`
3. Resolve all plugins and shareable configs
4. Build an abstract syntax tree (AST) for every file

Biome does all of this in a single binary with zero external dependencies. In a benchmark on the TypeScript compiler's codebase (roughly 1,500 files), Biome linted everything in **0.7 seconds**. ESLint took **18 seconds**. That's a 25x difference.

### Watch Mode and CI Bottlenecks

The gap widens in watch mode. ESLint's incremental rebuilds still require Node.js to re-parse configuration and re-apply rules. Biome's incremental cache is memory-mapped, making subsequent runs nearly instant. In CI environments where you lint on every commit, this can cut your pipeline time from 5 minutes to 30 seconds.

**The trade-off:** Biome's speed comes from doing fewer things. It doesn't support custom rule plugins (yet), and its rule set is a curated subset of what ESLint offers. You're trading flexibility for velocity.

## Configuration: The Flat Config Revolution vs A Single File

ESLint has historically been criticized for its configuration complexity. The old `.eslintrc` system required juggling `extends`, `plugins`, `rules`, and `parserOptions` across multiple files. The new flat config (`eslint.config.js`) simplifies this, but it's still JavaScript—which means it's programmable and infinitely flexible.

### ESLint's Flat Config in Action

Here's a minimal flat config:

```javascript
export default [
  { ignores: ["dist/**"] },
  {
    files: ["**/*.{js,ts}"],
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
    },
    plugins: { "@typescript-eslint": tsPlugin },
    rules: {
      "@typescript-eslint/no-explicit-any": "error",
    },
  },
];
```

This is powerful. You can write conditional logic, import configs from npm packages, and compose rules dynamically. But it's also a double-edged sword: the more you can do, the more you *need* to do. A typical production ESLint config is 100-200 lines, and that's before you add framework-specific plugins like `eslint-plugin-react` or `eslint-plugin-vue`.

### Biome's Zero-Config Approach

Biome ships with sensible defaults out of the box. A `biome.json` file with 20 lines covers most projects:

```json
{
  "$schema": "https://biomejs.dev/schemas/1.9.0/schema.json",
  "formatter": { "enabled": true },
  "linter": {
    "enabled": true,
    "rules": { "recommended": true }
  }
}
```

No plugins to install. No parser configuration. No `env` declarations. Biome automatically detects TypeScript, JSX, and modern ECMAScript features. For teams that want to move fast, this is a godsend.

**The trade-off:** Biome's configuration is declarative, not programmatic. You can't write a function that conditionally disables a rule based on environment variables. If you need that level of control, ESLint wins.

## Rule Coverage and Ecosystem Depth

ESLint has been around since 2013. Over a decade, the community has built **over 1,000 plugins** covering everything from React hooks to security vulnerabilities to CSS-in-JS. The official `eslint:recommended` set has ~60 rules, but the real power lies in third-party plugins.

Biome, as of version 1.9, offers **around 200 lint rules** in its core linter. It covers the essentials: no-unused-vars, no-undef, no-constant-condition, plus a solid set of correctness and style rules. It also includes a formatter (like Prettier) and a bundler-agnostic import sorter.

### Where Biome Falls Short

- **React-specific rules:** Biome has basic JSX support but lacks the depth of `eslint-plugin-react-hooks` (e.g., `exhaustive-deps`).
- **Accessibility:** `eslint-plugin-jsx-a11y` has 30+ rules for ARIA and keyboard navigation. Biome has ~5.
- **Custom rules:** ESLint allows you to write custom rules in JavaScript or TypeScript. Biome requires Rust knowledge to extend.

### Where Biome Excels

- **Consistency:** Because Biome handles formatting and linting together, there's no conflict between Prettier and ESLint rules.
- **Performance under scale:** For large monorepos, Biome's memory efficiency (it uses a single AST for both formatting and linting) is a game-changer.

## Migration: What to Expect

If you're considering switching, the migration path is smoother than you might think. Biome includes a `biome migrate eslint` command that reads your existing ESLint config and translates it to `biome.json`. It won't cover every rule, but it handles the common ones.

However, be prepared to:
1. **Lose custom rules:** Any rules you wrote yourself will need rewriting in Rust (or dropping).
2. **Adjust rule names:** Biome uses different naming conventions (e.g., `noExplicitAny` instead of `@typescript-eslint/no-explicit-any`).
3. **Test your CI:** The speed increase might expose hidden race conditions in your build scripts.

## The Verdict: Which Should You Choose?

**Choose ESLint if:**
- You rely heavily on React, Vue, or Angular ecosystem plugins.
- You need custom rules for internal code standards.
- You're on a legacy codebase with deep ESLint configuration.
- You value the safety of a mature ecosystem with extensive documentation.

**Choose Biome if:**
- You're starting a new project and want minimal setup.
- Performance is critical (large monorepos, tight CI budgets).
- You're tired of managing Prettier + ESLint + plugins as separate concerns.
- Your team values simplicity over configurability.

## The Future: A Converging Landscape

The JavaScript tooling world is not standing still. ESLint is exploring native performance improvements via `@eslint/js` and experimental Rust-based parsers. Biome is adding a plugin API (scheduled for v2.0) that will let developers write custom rules in JavaScript.

The smart play is to **evaluate both with your actual codebase**. Run ESLint's `--max-warnings=0` and Biome's `biome ci` on your CI and compare not just time, but the *actionable* warnings produced. In many cases, you'll find that Biome's 200 rules catch 80% of the issues ESLint's 1,000+ rules do—at 1/20th of the cost.

Tooling decisions are never permanent. The best engineers choose tools that solve today's problems without painting them into tomorrow's corner. Whichever you pick, the important thing is to keep linting—your future self will thank you.