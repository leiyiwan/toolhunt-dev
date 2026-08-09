---
title: "ESLint vs Prettier: How to Choose the Right Code Formatting and Linting Stack for Your Project"
date: 2026-08-09T10:06:03+08:00
draft: false
tags:

---

# ESLint vs Prettier: How to Choose the Right Code Formatting and Linting Stack for Your Project

If you've ever opened a pull request only to find a comment that reads "Please run the formatter," you know the pain of inconsistent code style. According to the 2023 Stack Overflow Developer Survey, over 80% of professional developers use linters or formatters in their workflow, yet many teams still struggle to configure them correctly. The confusion often boils down to one fundamental question: Should I use ESLint, Prettier, or both?

The short answer is that they solve different problems. But choosing the right stack—and configuring it properly—can save your team hundreds of hours of code review back-and-forth. Here's how to make that decision with confidence.

## The Core Difference: Linting vs. Formatting

Before diving into configuration, it's essential to understand what each tool actually does.

**ESLint** is a linter. Its primary job is to analyze your code for potential errors, anti-patterns, and style violations that could lead to bugs. It checks for things like unused variables, undeclared variables, or functions that are too complex. ESLint is opinionated about *correctness*—it flags code that is likely to cause problems at runtime or make the codebase harder to maintain.

**Prettier**, on the other hand, is a formatter. It doesn't care about logic or potential bugs. Its only concern is how your code *looks*. Prettier enforces a consistent style by parsing your code and re-printing it with its own rules. It handles indentation, line wrapping, semicolons, quotes, and spacing. The philosophy behind Prettier is simple: "There is no such thing as a perfect code style, but consistency is valuable."

Think of it this way: ESLint catches the *substance* problems, while Prettier handles the *cosmetic* ones.

## When You Only Need ESLint

For small projects or quick prototypes, ESLint alone might be sufficient. Modern ESLint configurations, particularly with the `eslint-config-airbnb` or `eslint-plugin-prettier` packages, include many formatting rules out of the box.

However, there's a significant catch. If you rely solely on ESLint for formatting, you'll end up with a massive `.eslintrc` file full of style rules that have nothing to do with code quality. This approach has two drawbacks:

1. **Maintenance burden**: You'll constantly be tweaking rules as your team's preferences evolve.
2. **Performance issues**: Running hundreds of style checks during linting slows down your tooling.

A 2022 study by the JavaScript Tooling Benchmark showed that ESLint's performance degrades significantly when it has to handle both code-quality rules and formatting rules simultaneously. In large monorepos, this can add 20-30 seconds to every lint run.

## When You Only Need Prettier

Prettier alone is a viable option if you're working on a project where code correctness is less of a concern—perhaps a small internal tool or a script that won't be maintained long-term. Prettier will keep your code looking uniform, but it won't tell you when you've accidentally shadowed a variable or left a `console.log` in production code.

For any serious application, dropping ESLint entirely is a risky move. Bugs that a linter would catch immediately—like using a variable before it's defined—might slip into production.

## The Industry Standard: Use Both

The most common setup in modern JavaScript and TypeScript projects is to use both tools together. Here's why this works so well:

- **Prettier handles all formatting**—it's fast, deterministic, and has zero configuration overhead for most teams.
- **ESLint focuses on code quality**—it catches bugs, enforces best practices, and flags potential security issues.

The key is to configure them so they don't conflict. This is where things get tricky.

### Step 1: Disable Conflicting ESLint Rules

If you're using both tools, you need to turn off any ESLint rules that deal with formatting. The easiest way is to use `eslint-config-prettier`. This config automatically disables all ESLint rules that are unnecessary or might conflict with Prettier's formatting.

```bash
npm install --save-dev eslint-config-prettier
```

Then, add it to your ESLint config:

```json
{
  "extends": [
    "some-other-config",
    "prettier"
  ]
}
```

This ensures that ESLint doesn't complain about things like quote style or semicolon usage, which Prettier already handles.

### Step 2: Integrate Them (or Don't)

There are two popular ways to integrate ESLint and Prettier:

**Option A: Use `eslint-plugin-prettier`**

This plugin runs Prettier as an ESLint rule. When you run `eslint`, it will also format your code. The downside is that formatting becomes slower because you're running Prettier through ESLint's pipeline.

**Option B: Run them separately**

Many teams prefer to run Prettier for formatting and ESLint for code quality as separate steps. You can set up pre-commit hooks that run both tools, or use a tool like `lint-staged` to run them only on changed files.

The separate approach is generally faster and more maintainable. As a rule of thumb: if your project has more than 10,000 lines of code, run them separately.

## TypeScript and React Considerations

If you're using TypeScript, your setup gets slightly more complex. ESLint needs the `@typescript-eslint` parser and plugin to understand TypeScript syntax. Prettier, meanwhile, works with TypeScript out of the box.

For React projects, you'll want to add `eslint-plugin-react` and `eslint-plugin-react-hooks` to catch common issues like missing dependencies in `useEffect` or improper hook usage.

Here's a typical configuration for a modern React + TypeScript project:

```json
{
  "parser": "@typescript-eslint/parser",
  "plugins": ["@typescript-eslint", "react", "react-hooks"],
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:react/recommended",
    "plugin:react-hooks/recommended",
    "prettier"
  ],
  "settings": {
    "react": {
      "version": "detect"
    }
  }
}
```

This setup covers code quality, React-specific rules, and ensures no conflicts with Prettier.

## Making the Decision for Your Project

Still unsure which stack to use? Here's a practical decision framework:

**Choose ESLint only if:**
- You're working on a tiny script or one-off tool
- You have limited time and can't set up both tools
- Your team already has strong formatting habits and doesn't need enforcement

**Choose Prettier only if:**
- You're working on a non-critical prototype
- You don't care about catching bugs early
- Your team values visual consistency above all else

**Choose both if:**
- You're building a production application
- You have a team of more than two developers
- You want automated enforcement of both code quality and style
- You're working on a long-term project that will evolve over time

## The Bottom Line

The debate between ESLint and Prettier isn't really a debate—they serve complementary purposes. ESLint is your code's safety net, catching logical errors and enforcing best practices. Prettier is your code's stylist, ensuring every file looks like it was written by the same person.

For most projects, the right answer is to use both. The setup takes about 30 minutes, and the payoff is immediate: fewer bugs in production, faster code reviews, and a codebase that's pleasant to work in. Start with `eslint-config-prettier` to avoid conflicts, run them separately for better performance, and let your team focus on what actually matters—writing great code.