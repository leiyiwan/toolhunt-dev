---
title: "ESLint vs Prettier: Do You Need Both or Can One Tool Rule Them All?"
date: 2026-08-30T14:05:33+08:00
draft: false
tags:

---

# ESLint vs Prettier: Do You Need Both or Can One Tool Rule Them All?

If you’ve ever opened a pull request only to see a comment like *“Please run Prettier”* right next to *“ESLint is failing on line 47,”* you’ve felt the confusion firsthand. For years, the JavaScript ecosystem has treated these two tools as inseparable siblings. But as modern frameworks like Next.js and Vite ship with zero-config setups, a growing number of developers are asking a pragmatic question: **Do I actually need both?**

The short answer is: yes, but for reasons that are often misunderstood. The longer answer involves a deep dive into what each tool actually does, where their responsibilities overlap, and how the rise of type-aware linting and formatters built into editors is changing the calculus.

## What Each Tool Actually Does

Before we can debate whether you need both, we need to strip away the marketing hype and look at their core functions.

### ESLint: The Rule Enforcer

ESLint is a **linter**. Its job is to analyze your code for problematic patterns, potential bugs, and stylistic violations based on a configurable set of rules. It operates on the **Abstract Syntax Tree (AST)** of your code, meaning it understands the structure of your JavaScript, TypeScript, and even JSX.

ESLint’s power lies in its ability to catch *logical* issues. For example:

- `no-unused-vars` — flags variables you declared but never used.
- `no-constant-condition` — catches loops or if-statements with conditions that never change.
- `@typescript-eslint/no-floating-promises` — ensures you handle async errors properly.

ESLint is **opinionated but configurable**. You can turn rules off, change their severity, or adopt a shared config like Airbnb’s or Standard’s. But crucially, ESLint *can* fix issues automatically with `--fix`, which blurs the line between linting and formatting.

### Prettier: The Opinionated Formatter

Prettier is a **formatter**. It ignores the logic of your code entirely and focuses solely on **style**: line breaks, indentation, quotes, semicolons, and trailing commas. It takes your code, parses it, and reprints it according to a strict, deterministic algorithm.

Prettier’s core philosophy is **“It works by just accepting the defaults.”** There are very few options (about 20, compared to ESLint’s hundreds of rules), and the tool actively discourages heavy customization. The goal is to end the “formatting wars” by making every codebase look identical, regardless of who wrote it.

The key distinction: **ESLint catches mistakes; Prettier makes things pretty.** But here’s where it gets messy.

## The Overlap: Stylistic Rules in ESLint

Historically, ESLint included a large set of stylistic rules like `quotes`, `semi`, `indent`, and `comma-dangle`. This created a problem: if you used both ESLint and Prettier, they would often fight over the same code.

For example:

- ESLint’s `quotes` rule might say “use single quotes.”
- Prettier might also default to single quotes.
- But if you changed Prettier’s `singleQuote` option to `false`, you’d get a conflict.

The industry solution was the **`eslint-config-prettier`** plugin, which simply turns off all ESLint rules that overlap with Prettier’s formatting. This effectively created a clear division of labor:

- **Prettier** handles formatting (spacing, quotes, semicolons).
- **ESLint** handles logic and code quality.

This setup works, but it requires configuration. And configuration fatigue is a real problem in the JavaScript ecosystem.

## The Case for Using Only ESLint

There is a vocal minority in the developer community arguing that you can ditch Prettier entirely and rely on ESLint alone. Their reasoning is straightforward:

1. **ESLint’s `--fix` can handle most formatting.**
2. **Modern ESLint rules (like `@stylistic/eslint-plugin`) have caught up to Prettier’s capabilities.**
3. **One tool means one config file, one install, one CI step.**

If you adopt the `@stylistic` plugin (which is the official migration path for ESLint’s deprecated formatting rules), you can enforce consistent indentation, quotes, and line length directly through ESLint. For simple projects, this genuinely works.

However, there’s a critical flaw: **ESLint is not a fully deterministic formatter.** Consider this example:

```js
const foo = { a: 1, b: 2, c: 3 }
```

Prettier will decide whether to break this into multiple lines based on the configured `printWidth` (default 80). ESLint’s `--fix` will only fix what the rules explicitly tell it to. If you haven’t written a rule for “object property line wrapping,” ESLint will leave it alone. Prettier, by contrast, handles this automatically.

In practice, this means **ESLint-only setups require you to write more custom rules** to approximate Prettier’s behavior. You end up reinventing the wheel, poorly.

## The Case for Using Only Prettier

What about the reverse? Can Prettier replace ESLint?

**No. Not even close.** Prettier does not check for:

- Undefined variables
- Unreachable code
- Async error handling
- React hook dependencies

Prettier is intentionally “dumb” about your code’s semantics. It won’t catch `console.log` left in production, nor will it flag a missing `key` prop in a React list. If you use Prettier alone, you’re essentially saying, “I don’t care about code quality, only consistency.”

That’s a dangerous trade-off for any serious project. The only scenario where Prettier-only makes sense is if you’re writing throwaway scripts or prototyping, and even then, you’re better off with at least a basic ESLint config.

## The Modern Reality: TypeScript and Editor Integration

The conversation shifts significantly when you introduce TypeScript. With `tsc` (the TypeScript compiler) already catching type errors, some developers argue that ESLint is redundant. However, **ESLint and TypeScript serve different purposes**:

- `tsc` catches type errors (e.g., passing a `string` where a `number` is expected).
- ESLint catches code-quality issues (e.g., using `any`, forgetting to handle a promise).

The `typescript-eslint` project even provides type-aware linting rules that go *beyond* what `tsc` offers, like `no-unsafe-argument` or `no-unnecessary-type-assertion`.

Meanwhile, editors like VS Code have made both tools nearly invisible. With the ESLint and Prettier extensions installed, your code is auto-formatted on save and lint errors are highlighted in real time. This has led to a “set it and forget it” mentality. But that convenience masks the underlying complexity.

## The Verdict: You Need Both (With One Caveat)

After weighing the evidence, the industry consensus remains: **Yes, you need both.** But you should configure them to be strictly complementary, not overlapping.

Here’s the winning combination:

1. **Install `eslint-config-prettier`** to disable all conflicting ESLint rules.
2. **Let Prettier handle formatting** (quotes, semicolons, line breaks).
3. **Let ESLint handle logic** (no-unused-vars, no-constant-condition, react-hooks/rules-of-hooks).
4. **Use `eslint-plugin-prettier`** (optional) to run Prettier as an ESLint rule. This ensures that if a developer runs `eslint --fix`, Prettier runs too, keeping CI simple.

In your `package.json`, you’d typically have:

```json
{
  "scripts": {
    "lint": "eslint . --ext .js,.jsx,.ts,.tsx",
    "format": "prettier --write .",
    "check": "npm run lint && npx prettier --check ."
  }
}
```

This gives you a clear separation of concerns. CI can run `npm run check` to verify both, and developers can run `npm run format` to fix everything at once.

## The Only Exception: Single-Person Projects

If you’re a solo developer working on a personal project with no team collaboration, you *can* get away with just ESLint + `@stylistic`. You’ll have consistent code because you’re the only one writing it. But the moment you add a second person, or you open-source the project, you’ll wish you had Prettier’s determinism.

## Conclusion: Two Tools, One Pipeline

The idea that one tool can “rule them all” is appealing, but it’s a false economy. ESLint and Prettier solve different problems, and conflating them leads to either fragile formatting rules (ESLint-only) or a complete lack of code-quality checks (Prettier-only).

The pragmatic approach is to embrace both, but configure them to respect each other’s boundaries. Use Prettier for the aesthetics and ESLint for the logic. Set up your editor to run both on save, add a single CI check that runs both, and move on to more interesting problems.

In the end, the tools aren’t rivals—they’re teammates. And like any good team, they work best when each player knows their role.