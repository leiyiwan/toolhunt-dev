---
title: "ESLint vs Prettier: The Ultimate Guide to Code Formatting and Linting in 2025"
date: 2026-09-01T18:04:59+08:00
draft: false
tags:

---

# ESLint vs Prettier: The Ultimate Guide to Code Formatting and Linting in 2025

If you've ever opened a pull request only to find 47 comments about missing semicolons and inconsistent quote styles, you already know the pain. A 2024 survey by Stack Overflow found that code style disputes are among the top five most common sources of developer friction, costing teams an estimated 3-4 hours per developer per week in review cycles. That's roughly 150 hours a year—time that could be spent shipping features.

The solution isn't picking a side in the "tabs vs. spaces" war. It's understanding how the two dominant tools—ESLint and Prettier—fit together. While they are often mentioned in the same breath (and frequently confused), they solve fundamentally different problems. Here's everything you need to know in 2025.

## The Core Difference: Linting vs. Formatting

Before diving into configuration, it's crucial to understand what each tool actually does. The confusion here is the root of most misconfiguration.

**ESLint is a linter.** Its primary job is to analyze your code for *logical* issues. It catches unused variables, flags `console.log` left in production code, enforces best practices like `no-await-in-loop`, and prevents common bugs like using `==` instead of `===`. ESLint is about *code quality* and *correctness*.

**Prettier is a formatter.** It doesn't care about logic at all. Prettier's only job is to parse your code and re-print it based on a strict, opinionated set of rules. It enforces consistent line wrapping, indentation, spacing, and semicolons. Prettier is about *style consistency*.

Think of it this way: ESLint asks, "Will this code work correctly and follow best practices?" Prettier asks, "Does this code *look* the same as every other file in the project?"

## Why You Need Both (Not Either/Or)

A common misconception is that you can replace one with the other. You can't.

If you use **only ESLint**, you'll need to manually configure stylistic rules like `indent`, `quotes`, and `semi`. This is a maintenance nightmare. Every time your team debates a style choice, you're editing config files. Worse, ESLint's stylistic rules are notoriously slow and often conflict with each other.

If you use **only Prettier**, your code will look beautiful and uniform. But it won't catch a single bug. You'll still ship code with unused imports, undefined variables, and security anti-patterns.

The industry standard in 2025 is a **hybrid approach**: Use Prettier for formatting, and use ESLint *only* for code-quality rules. To make this work seamlessly, you need to turn off all ESLint rules that overlap with Prettier's territory.

## The 2025 Setup: A Step-by-Step Guide

Here is the modern, recommended configuration that most senior developers and major open-source projects use.

### Step 1: Install Dependencies

```bash
npm install --save-dev eslint prettier eslint-config-prettier
```

The `eslint-config-prettier` package is the magic sauce. It disables all ESLint rules that conflict with Prettier. Without it, you'll get annoying errors like "Expected indentation of 2 spaces but found 4" even though Prettier just formatted the file correctly.

### Step 2: Configure ESLint

Create an `eslint.config.js` file (ESLint 9+ uses the flat config format by default):

```javascript
import js from '@eslint/js';
import prettierConfig from 'eslint-config-prettier';

export default [
  js.configs.recommended,
  prettierConfig,
  {
    rules: {
      // Your custom code-quality rules here
      'no-unused-vars': 'warn',
      'no-console': 'warn',
    },
  },
];
```

**Critical:** The `prettierConfig` must be the *last* entry in the array. This ensures it overrides any conflicting stylistic rules from the recommended set.

### Step 3: Configure Prettier

Prettier works out of the box with zero configuration. However, most teams add a `.prettierrc` file to set team-specific preferences:

```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5"
}
```

These are the defaults for most modern JavaScript projects. The key is to set these *once* and never argue about them again.

### Step 4: Automate with Git Hooks

Manual formatting is a thing of the past. Use **lint-staged** and **Husky** to run Prettier and ESLint automatically before every commit:

```bash
npm install --save-dev husky lint-staged
```

In `package.json`:

```json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "prettier --write",
      "eslint --fix"
    ]
  }
}
```

This ensures that no unformatted or broken code ever makes it into your repository. No more "fix the lint errors" comments in code review.

## The `--fix` Flag: What It Can and Can't Do

Both tools have a `--fix` flag, but they operate differently.

**Prettier's `--write`** rewrites the entire file. It will reformat 100% of the code that doesn't match its rules. It's deterministic—if you run it twice, you get the same output.

**ESLint's `--fix`** is more conservative. It only fixes issues that are *safe* to fix automatically. For example, it can auto-fix missing semicolons or convert double quotes to single quotes. But it will *not* fix a complex issue like `no-unused-vars` because doing so might break your code (e.g., if the variable is used in a side-effectful way).

In 2025, the workflow is simple: Run Prettier first to format, then run ESLint to catch quality issues. The `lint-staged` config above handles this order automatically.

## Common Pitfalls and How to Avoid Them

Even with the perfect setup, developers still run into issues. Here are the most common ones I see in 2025:

### The "Conflicting Rules" Trap
If you see errors like "Delete `␍`" or "Replace `'` with `"`", it means you haven't properly disabled ESLint's stylistic rules. Double-check that `eslint-config-prettier` is loaded and is the last item in your config array.

### The "Format on Save" Mismatch
Your IDE should be configured to format on save using Prettier, not ESLint. In VS Code, set Prettier as the default formatter:

```json
{
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true
}
```

Many developers mistakenly set ESLint as the formatter, which leads to weird behavior and slow performance.

### Ignoring Files
You need to tell both tools to ignore generated files, `node_modules`, and build outputs. Create a `.prettierignore` file:

```
node_modules
dist
build
package-lock.json
```

And add similar entries to ESLint's `ignores` config. This prevents your tools from wasting time on files that shouldn't be touched.

## The TypeScript and React Factor

If you're using TypeScript (and you should be), the setup changes slightly. You'll need `@typescript-eslint/parser` and `@typescript-eslint/eslint-plugin` for ESLint to understand TypeScript syntax. Prettier, however, handles TypeScript out of the box—it just strips the types and formats the code.

For React projects, add `eslint-plugin-react-hooks` and `eslint-plugin-react-refresh` to catch common React-specific issues like missing dependencies in `useEffect`. Prettier doesn't care about JSX specifics—it just formats them consistently.

## The Verdict for 2025

The debate isn't "ESLint vs. Prettier." It's "ESLint *and* Prettier." They are complementary tools that solve different problems. Trying to use one without the other leaves you with either messy code or buggy code.

The industry has largely settled on this architecture: **Prettier owns the formatting, ESLint owns the logic.** Tools like Biome are emerging as faster, all-in-one alternatives, but as of 2025, they haven't yet achieved the ecosystem maturity and plugin support that ESLint and Prettier offer together.

If you're starting a new project today, set up the hybrid approach from day one. It will save you thousands of hours of review time, eliminate style arguments, and make your codebase significantly easier to maintain. The 15 minutes it takes to configure these tools correctly is the highest-ROI investment you'll make in your project's developer experience.