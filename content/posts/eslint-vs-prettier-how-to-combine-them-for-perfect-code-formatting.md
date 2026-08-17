---
title: "ESLint vs Prettier: How to Combine Them for Perfect Code Formatting"
date: 2026-08-17T18:04:58+08:00
draft: false
tags:

---

# ESLint vs Prettier: How to Combine Them for Perfect Code Formatting

If you've written JavaScript for more than a week, you've likely had a disagreement with your code. Maybe it was a missing semicolon, a tab where a space should be, or a string that should've been single-quoted but was double-quoted. These arguments are a waste of time—but they're also incredibly common. According to the 2023 State of JS survey, over 70% of JavaScript developers use ESLint, and Prettier adoption has grown to roughly 40% of the ecosystem.

The problem? Many developers treat them as interchangeable. They're not. ESLint and Prettier solve different problems, and when you understand the difference—and how to make them work together—you can eliminate entire categories of code review comments and merge conflicts.

Here's how to set them up correctly, avoid the infamous "conflict" issues, and get your codebase to a place where formatting is a non-issue.

## The Core Difference: Linting vs. Formatting

Let's start with the fundamental distinction.

**ESLint** is a linter. It analyzes your code for *logic* and *style* issues. It catches things like:
- Undefined variables
- Unused imports
- `console.log` left in production code
- Potential bugs like `==` instead of `===`

ESLint cares about *quality* and *correctness*. It asks: "Is this code written well?"

**Prettier** is a formatter. It doesn't care about logic at all. It only cares about *how the code looks*. It enforces consistent rules like:
- Line width (default: 80 characters)
- Indentation style (spaces vs. tabs)
- Semicolon presence
- Quote style
- Trailing commas

Prettier asks: "Does this code look consistent?"

One way to think about it: ESLint checks your grammar, Prettier checks your handwriting.

## Why You Need Both

If you only use ESLint, you'll end up writing style rules in your ESLint config. That's possible, but ESLint's formatting rules are slow and limited compared to Prettier. Plus, you'll spend hours debating whether to use `indent: [2, 4]` or `indent: [2, 2]`.

If you only use Prettier, your code will look beautiful—but it might still be broken. Prettier won't catch that you're using a deprecated API or that you've shadowed a variable name.

The industry-standard approach is:
- **ESLint for code quality** (rules about bugs, best practices, and potential errors)
- **Prettier for formatting** (rules about spacing, quotes, and line breaks)

This separation is the key. When you mix them, you get conflicts.

## The Classic Conflict: Why They Fight

Here's a scenario that happens to nearly every developer at some point:

1. You write code that violates Prettier's formatting rules.
2. You run ESLint with a rule like `quotes: ["error", "single"]`.
3. ESLint flags your double quotes.
4. You run Prettier, which changes the quotes to single.
5. ESLint runs again and passes.

That works. But what if Prettier's default settings *conflict* with your ESLint rules? For example, Prettier defaults to double quotes in some configurations, while ESLint might enforce single quotes. Or Prettier insists on semicolons, but your ESLint rule says `semi: ["error", "never"]`.

This is the "war" you've heard about. It's not that the tools hate each other—it's that they're both trying to control the same output, and their default opinions differ.

## The Solution: Disable ESLint's Formatting Rules

The modern, accepted solution is simple: **turn off all formatting rules in ESLint and let Prettier handle them.**

The `eslint-config-prettier` package does exactly this. It's a shareable config that disables all ESLint rules that conflict with Prettier. Here's how to set it up:

```bash
npm install --save-dev eslint-config-prettier
```

Then, in your `.eslintrc.json` (or `eslint.config.js` if you're using the flat config):

```json
{
  "extends": [
    "eslint:recommended",
    "plugin:react/recommended",
    "prettier"
  ]
}
```

The `"prettier"` entry **must be last**. This ensures it overrides any conflicting rules from the other configs.

With this setup, ESLint stops complaining about formatting. It focuses on logic, bugs, and best practices. Prettier handles the visual consistency.

## The Practical Workflow

Once you've configured both tools, the workflow becomes:

1. **Write code** (however you want—messy is fine).
2. **Run Prettier** to format it.
3. **Run ESLint** to catch logic issues.
4. **Fix any ESLint errors** (which are now only about code quality).

You can run them in sequence:

```bash
npx prettier --write .
npx eslint . --fix
```

Or, if you want to be more efficient, you can use `lint-staged` to run both only on files that are staged for commit. This keeps your pre-commit hooks fast.

Here's a sample `.pre-commit` config using `lint-staged` and `husky`:

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

This runs Prettier first, then ESLint. The `--fix` flag on ESLint will auto-fix any remaining issues that Prettier didn't handle.

## Setting Up a New Project: A Complete Guide

If you're starting from scratch, here's the complete setup for a modern JavaScript project:

### Step 1: Install Both Tools

```bash
npm install --save-dev eslint prettier eslint-config-prettier
```

### Step 2: Create ESLint Config

For ESLint 9+ (flat config), create `eslint.config.js`:

```js
import js from '@eslint/js';
import prettier from 'eslint-config-prettier';

export default [
  js.configs.recommended,
  prettier,
  {
    rules: {
      // Your custom rules here
      'no-console': 'warn',
      'no-unused-vars': 'error'
    }
  }
];
```

For older versions, use `.eslintrc.json`:

```json
{
  "env": {
    "browser": true,
    "es2022": true
  },
  "extends": ["eslint:recommended", "prettier"],
  "parserOptions": {
    "ecmaVersion": "latest",
    "sourceType": "module"
  }
}
```

### Step 3: Create Prettier Config

Create a `.prettierrc` file:

```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 80
}
```

These are sensible defaults. Adjust to your team's taste—but once you set them, stop debating.

### Step 4: Add a `.prettierignore` File

Just like `.gitignore`, you want to exclude certain files:

```
node_modules
dist
build
package-lock.json
```

### Step 5: Add Scripts to `package.json`

```json
{
  "scripts": {
    "format": "prettier --write .",
    "lint": "eslint .",
    "check": "prettier --check . && eslint ."
  }
}
```

The `check` script is great for CI. It fails if any file isn't formatted correctly or has lint errors.

## Common Pitfalls and How to Avoid Them

Even with the right setup, developers run into issues. Here are the most common ones and how to fix them:

### Pitfall 1: ESLint Rules That Override Prettier

If you have `eslint-config-prettier` in your `extends`, but you *also* manually define a formatting rule like `"quotes": ["error", "single"]`, you'll get conflicts again. The solution: **never manually define formatting rules in ESLint**. If you find yourself writing rules about indentation, quotes, or semicolons in ESLint, stop. Move those to Prettier.

### Pitfall 2: Formatting That Changes Code Behavior

Prettier is generally safe, but there are edge cases. For example:

```js
const a = (1 + 2) * 3;
```

Prettier might reformat this to:

```js
const a = 1 + 2 * 3;
```

Which changes the result from 9 to 7. To avoid this, always run your tests after formatting. In practice, Prettier is very conservative about this, but it's a good habit.

### Pitfall 3: Prettier Slowing Down Your Editor

If you're using VS Code, install the Prettier extension and set it as the default formatter:

```json
{
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true
}
```

For ESLint, use the ESLint extension. You can also enable "format on save" for ESLint's `--fix`:

```json
{
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  }
}
```

This way, both tools run automatically every time you save. You never have to think about formatting again.

## The TypeScript Question

If you're using TypeScript, the setup is similar but with a few extra packages:

```bash
npm install --save-dev @typescript-eslint/parser @typescript-eslint/eslint-plugin
```

Your ESLint flat config becomes:

```js
import tseslint from '@typescript-eslint/eslint-plugin';
import tsParser from '@typescript-eslint/parser';
import prettier from 'eslint-config-prettier';

export default [
  {
    files: ['**/*.ts', '**/*.tsx'],
    languageOptions: {
      parser: tsParser
    },
    plugins: {
      '@typescript-eslint': tseslint
    },
    rules: {
      ...tseslint.configs.recommended.rules,
      ...prettier.rules
    }
  }
];
```

Prettier handles TypeScript formatting natively, so no extra config is needed there.

## The Bottom Line

The "ESLint vs Prettier" debate is a false dichotomy. They're not competitors; they're complementary tools that serve different purposes. ESLint ensures your code is *correct*; Prettier ensures it's *consistent*.

The winning setup is straightforward:
1. Use ESLint for code quality rules.
2. Use Prettier for formatting rules.
3. Use `eslint-config-prettier` to disable any formatting rules in ESLint.
4. Run Prettier first, then ESLint, in your pre-commit hooks and CI pipeline.

Once you have this configured, you can stop arguing about semicolons and start arguing about what actually matters: architecture, performance, and user experience.

Your future self—and your code reviewers—will thank you.