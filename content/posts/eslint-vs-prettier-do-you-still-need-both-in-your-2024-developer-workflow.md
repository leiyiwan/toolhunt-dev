---
title: "ESLint vs Prettier: Do You Still Need Both in Your 2024 Developer Workflow?"
date: 2026-08-18T18:05:26+08:00
draft: false
tags:

---

# ESLint vs Prettier: Do You Still Need Both in Your 2024 Developer Workflow?

If you've written JavaScript in the last five years, you've almost certainly encountered the great formatting debate. On one side, ESLint catches bugs and enforces code quality rules. On the other, Prettier formats your code so it looks like a machine wrote it—consistently and without argument. For years, the standard advice was simple: use both. ESLint for logic and best practices, Prettier for formatting, and `eslint-config-prettier` to stop them from fighting.

But in 2024, the landscape has shifted. ESLint released a major overhaul with its flat config system, and TypeScript's tooling has matured significantly. A growing number of developers are asking a legitimate question: *Do I really need two tools doing overlapping jobs?* The short answer is: it depends. The longer answer requires a look at what each tool actually does, where they overlap, and what the modern alternatives offer.

## The Traditional Divide: What Each Tool Does

To understand whether you can drop one, you need to understand their core philosophies.

**Prettier** is an opinionated code formatter. It ignores your stylistic preferences—or rather, it has exactly one preference: its own. It handles line wrapping, indentation, quotes, semicolons, and trailing commas. The key word here is *formatting*. Prettier parses your code into an abstract syntax tree (AST) and prints it back out in a standardized way. It doesn't care if your function has a bug; it only cares if it looks neat.

**ESLint**, on the other hand, is a linter. Historically, it did two things: it found potential errors (like using a variable before defining it) and it enforced stylistic conventions (like requiring semicolons). The problem is that ESLint's stylistic rules were always weaker than Prettier's formatting engine. They were manual, inconsistent, and often conflicted with each other. This led to the now-common practice of turning off all stylistic rules in ESLint and letting Prettier handle the visual layout.

In this model, ESLint becomes purely a *code quality* tool. It catches unused variables, flags `console.log` statements in production code, and enforces rules like `no-await-in-loop` or `eqeqeq`. This division of labor works well, but it's worth noting that ESLint's own documentation now explicitly recommends using a formatter for style rules.

## The 2024 Shift: ESLint's Flat Config and TypeScript's Rise

The biggest change to ESLint in years landed in 2023 and stabilized through 2024: the **flat config** system (ESLint 9.x). This replaced the old `.eslintrc` JSON structure with a more programmatic `eslint.config.js` file. It's faster, more predictable, and easier to extend. Crucially, it also made it simpler to compose multiple rule sets—including turning off formatting rules entirely.

Meanwhile, TypeScript has become the default for most serious JavaScript projects. TypeScript's compiler itself catches a huge category of errors that ESLint used to handle—undefined variables, implicit `any` types, and unreachable code. This reduces the need for ESLint's core rules. Many teams now run TypeScript's `tsc --noEmit` as their primary type check, and use ESLint only for rules that TypeScript doesn't cover, like React hooks dependencies or import ordering.

But here's where the friction appears. TypeScript doesn't format your code. Prettier does. And if you're using a framework like Next.js or Remix, the default scaffolding often includes both ESLint and Prettier, configured to work together. So the default experience still leans on both tools.

## The Case for Dropping Prettier

A vocal minority of developers have started ditching Prettier entirely. Their reasoning is straightforward: modern language servers and editors are already good enough to handle formatting.

If you use VS Code with the built-in TypeScript formatter, or if you rely on the formatting that comes with frameworks like Svelte or Vue's tooling, you might not need Prettier's opinionated output. Additionally, Prettier's rigid line-width (default 80 characters) can produce awkward wrapping in complex expressions. Some developers find that hand-formatting certain code—like long ternary chains—produces more readable results than Prettier's forced wrapping.

There's also the performance argument. Running Prettier on every save adds a small but measurable delay. In a monorepo with thousands of files, that delay compounds. And if you're using `eslint --fix` to auto-fix issues, you might already be applying formatting-like changes. For small projects or solo developers, the overhead of maintaining a `.prettierrc` file, a `.prettierignore`, and a CI check might not be worth it.

## The Case for Keeping Both

Despite these arguments, the majority of professional teams still use both—and for good reason.

First, **consistency across a team** is Prettier's killer feature. When you have ten developers with different editor setups, Prettier eliminates all formatting debates. No one argues about tabs vs. spaces or semicolons vs. no semicolons. Code reviews focus on logic, not style. This is a massive productivity win that individual developers often underestimate.

Second, **Prettier supports languages that ESLint doesn't**. ESLint primarily handles JavaScript and TypeScript. Prettier formats JSON, CSS, Markdown, YAML, GraphQL, and even HTML. In a modern full-stack project, you'll likely need formatting for more than just your `.ts` files. Prettier gives you a single tool for all of them.

Third, **the overlap is manageable**. The `eslint-config-prettier` plugin disables all ESLint rules that conflict with Prettier. You set up the config once, and the two tools coexist peacefully. The setup is a few lines in your `eslint.config.js`:

```js
import eslintConfigPrettier from "eslint-config-prettier";

export default [
  // ... other configs
  eslintConfigPrettier,
];
```

That's it. ESLint stops caring about formatting, Prettier stops caring about logic, and both work in tandem.

## What About the New Alternatives?

In 2024, two new tools are worth mentioning: **Biome** and **dprint**.

**Biome** (formerly Rome) is a JavaScript-native toolchain that combines linting, formatting, and bundling into a single binary. It's written in Rust, which makes it significantly faster than ESLint and Prettier. Biome can replace both tools entirely. Its formatter is Prettier-compatible by default, and its linter covers many of the same rules as ESLint's recommended set. As of late 2024, Biome is still missing some ESLint plugins (especially for React), but it's rapidly gaining ground.

**dprint** is another Rust-based formatter, but it takes a different approach. It's a pluggable platform that can format JavaScript, TypeScript, JSON, Markdown, and more. It's designed to be a drop-in replacement for Prettier in many cases, with better performance. However, it doesn't include linting, so you'd still need ESLint or TypeScript for quality checks.

The appeal of these tools is simplicity. One binary, one config file, one command. For new projects, they're extremely attractive. For existing projects, migrating from Prettier's ecosystem to Biome requires effort—especially if you rely on Prettier plugins for things like sorting imports or formatting Tailwind CSS classes.

## The Pragmatic Verdict for 2024

So, do you still need both? Here's a practical decision framework:

- **If you're starting a new project**: Use Biome if your stack is vanilla JavaScript or TypeScript with no exotic plugins. It's faster, simpler, and good enough. If you need React-specific rules or a mature plugin ecosystem, stick with ESLint + Prettier—it's still the safest bet.

- **If you're on an existing project**: Don't rip out Prettier unless formatting is actively causing pain. The migration cost isn't worth it. Instead, ensure you're using `eslint-config-prettier` and that your CI runs both tools. The setup is stable and well-documented.

- **If you're a solo developer**: Use whatever makes you fastest. If you prefer hand-formatting and rely on your editor's built-in formatter, drop Prettier. If you want zero thought about style, keep it.

- **If you're on a team**: Keep both. The consistency benefit outweighs the tooling overhead. Code review time is expensive; Prettier saves more than it costs.

## Conclusion

The ESLint vs. Prettier debate in 2024 isn't really about which tool wins—it's about whether the industry still needs two separate tools for code quality and code style. The answer is slowly shifting. ESLint's flat config has made integration cleaner, TypeScript has absorbed some of ESLint's error-checking role, and new all-in-one tools like Biome are proving that a single tool can handle both jobs efficiently.

For now, the pragmatic choice for most teams remains ESLint + Prettier. The setup is mature, the ecosystem is vast, and the mental overhead is low once configured. But the writing is on the wall: the era of separate formatters and linters is ending. Within the next few years, we'll likely see a single tool dominate—one that formats, lints, and type-checks in a single pass. Until then, keep both tools, configure them to play nice, and focus your energy on writing code that matters.