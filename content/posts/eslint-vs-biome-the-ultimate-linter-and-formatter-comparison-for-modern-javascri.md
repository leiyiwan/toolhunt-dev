---
title: "ESLint vs Biome: The Ultimate Linter and Formatter Comparison for Modern JavaScript"
date: 2026-08-12T18:02:40+08:00
draft: false
tags:

---

# ESLint vs Biome: The Ultimate Linter and Formatter Comparison for Modern JavaScript

In 2024, the JavaScript tooling landscape witnessed a seismic shift. Biome, a relative newcomer, announced it had been downloaded over 1 million times per week, while ESLint—the long-standing champion—was downloaded over 40 million times weekly. These numbers tell a story of both stability and disruption. For developers, the choice between these two tools is no longer hypothetical; it’s a daily decision that impacts build times, developer experience, and code quality.

If you’ve ever waited 30 seconds for ESLint to process a monorepo or wrestled with configuring 15 different plugins, you’ve likely wondered if there’s a better way. This comparison digs into the technical realities, performance benchmarks, and ecosystem trade-offs to help you decide which tool belongs in your stack.

## The Core Difference: Architecture and Philosophy

The fundamental distinction between ESLint and Biome isn't just speed—it's their entire architectural approach.

**ESLint** is a modular, plugin-based linter. It parses your code into an Abstract Syntax Tree (AST), then runs a series of rules against that tree. This design allows for incredible flexibility: you can lint everything from standard JavaScript to Vue templates to GraphQL schemas. However, this flexibility comes at a cost. Each plugin, parser, and rule adds overhead, and the AST traversal is repeated for each rule, making performance a secondary concern to extensibility.

**Biome**, on the other hand, is a "toolchain" written entirely in Rust. It combines a linter, formatter, and eventually a bundler into a single binary. Instead of an AST, Biome uses a concrete syntax tree (CST) that preserves all comments and formatting details. This allows it to perform linting and formatting in a single pass. The Rust compilation to native machine code means there’s no JIT warm-up time, no Node.js process spawn overhead, and no garbage collection pauses.

This isn't just a minor optimization. When you run Biome, you're executing a compiled binary that starts in milliseconds. When you run ESLint, you're spinning up a Node.js process, loading the CLI, resolving plugins, and then parsing code—a process that can take several seconds even on fast hardware.

## Performance: The Benchmark Reality

Let’s talk numbers. In the official Biome benchmarks, the tool consistently demonstrates 10x to 100x speed improvements over ESLint. But what does that look like in practice?

On a typical project with 1,000 JavaScript files:
- **ESLint** (with `eslint-config-airbnb` and TypeScript parser): 45-90 seconds for a full run
- **Biome**: 1.5-3 seconds for a full check

This isn't just about CI pipeline time. For local development, the difference is transformative. With Biome, you can run linting on every save without noticing any lag. With ESLint, most developers disable the linter in their IDE or run it only on commit because the feedback loop is too slow.

The performance gap becomes even more pronounced in monorepos. When you have 50 packages with shared configurations, ESLint's resolution algorithm becomes a bottleneck. Biome's single-binary approach sidesteps this entirely.

## Configuration: Simplicity vs. Flexibility

### ESLint's Configuration Complexity

ESLint 9 introduced a flat config system (`eslint.config.js`) to replace the older `.eslintrc` format. While this was a step forward, it remains verbose. A typical modern config looks like this:

```javascript
import js from '@eslint/js';
import tseslint from 'typescript-eslint';
import reactHooks from 'eslint-plugin-react-hooks';

export default [
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    plugins: { 'react-hooks': reactHooks },
    rules: {
      'react-hooks/rules-of-hooks': 'error',
      'react-hooks/exhaustive-deps': 'warn',
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    },
  },
];
```

This is manageable. But when you add Prettier for formatting, you now have two configuration files, two processes, and potential conflicts between the two tools.

### Biome's Zero-Config Approach

Biome's philosophy is "sensible defaults out of the box." A basic configuration can be as simple as:

```json
{
  "formatter": {
    "indentStyle": "space",
    "indentWidth": 2
  }
}
```

That's it. Biome ships with a recommended rule set that covers common pitfalls, and its formatter is opinionated—it doesn't offer 50 different options for quote style or trailing commas. This is a deliberate design choice. Biome aims to eliminate bikeshedding by providing one excellent default style, similar to how `gofmt` and `rustfmt` operate in other languages.

## Ecosystem and Plugin Support

This is where ESLint still holds a decisive advantage.

ESLint's plugin ecosystem is vast. Need to lint Tailwind CSS class ordering? There's a plugin. Need to enforce import sorting for your specific monorepo structure? There's a plugin. Need to catch React hooks violations, Vue template errors, or Svelte accessibility issues? ESLint has you covered.

Biome, despite its speed, has a limited plugin API. As of late 2024, Biome does not support third-party plugins. The official roadmap includes plugin support, but it's not yet available. This means if you rely on niche or framework-specific rules, Biome may not be able to replicate your current setup.

However, Biome does include built-in support for:
- TypeScript and TSX
- JavaScript and JSX
- JSON and JSONC
- CSS (as of version 1.8)

For the most common use cases—catching unused variables, enforcing consistent imports, preventing debugger statements—Biome's built-in rules are sufficient.

## Formatter: Prettier vs. Biome

The formatting battle is where Biome makes its strongest case. Biome's formatter is not just fast; it's designed to be compatible with Prettier's output for the majority of cases. This was a strategic decision—the Biome team recognized that developers were reluctant to switch formatters due to the massive diffs it would create in existing codebases.

In practice, Biome's formatter produces output that is visually indistinguishable from Prettier for about 95% of code. The remaining 5% involves edge cases around line wrapping and nested ternaries, where Biome's opinions differ slightly.

The key advantage here is unification. With Biome, you have one tool that handles both linting and formatting. You no longer need to worry about ESLint's `--fix` conflicting with Prettier's formatting, a common source of frustration that required the `eslint-config-prettier` plugin to resolve.

## IDE Integration and Developer Experience

Both tools offer VS Code extensions, but the experience differs significantly.

ESLint's extension is mature but can feel sluggish on large files. The extension communicates with the Node.js ESLint server, and every keystroke triggers a re-lint of the current file. On files over 500 lines, you'll notice the yellow squiggles lag behind your typing.

Biome's VS Code extension, by contrast, feels instant. Because the core is a Rust binary, the extension can process files in under 10 milliseconds. The extension also integrates formatting and linting into a single action, so you can "Organize Imports" and "Format Document" in one keyboard shortcut.

Both tools support:
- On-save formatting
- Inline error diagnostics
- Quick fixes for auto-fixable rules
- Command-line interfaces for CI integration

## Migration Path: Moving from ESLint to Biome

If you're considering switching, the migration is more straightforward than you might expect.

1. **Run Biome's migration tool**: `npx @biomejs/biome migrate eslint` automatically converts your ESLint config to Biome's format, mapping equivalent rules.
2. **Test in CI**: Run Biome alongside ESLint for a few weeks to identify any rules you're missing.
3. **Address gaps**: For critical ESLint rules without Biome equivalents, you can run both tools in parallel (Biome for speed, ESLint for coverage) or wait for Biome's plugin system.
4. **Switch your formatter**: Run Biome's formatter on your codebase and review the diff. It should be minimal if you were using Prettier.

One common pitfall: Biome's rule names differ from ESLint's. For example, `no-unused-vars` in ESLint becomes `noUnusedVariables` in Biome. The migration tool handles this mapping, but you should review the output carefully.

## When to Choose ESLint

ESLint remains the right choice if:

- You rely on framework-specific plugins (e.g., `eslint-plugin-react`, `eslint-plugin-vue`, `eslint-plugin-svelte`)
- You need custom rules for your organization's specific coding standards
- You work in a large enterprise environment with strict compliance requirements and need the audit trail of a well-established tool
- Your team has invested years in a complex ESLint configuration that would be hard to replicate

ESLint's 40 million weekly downloads aren't just inertia. For many teams, it's the only tool that meets their specific needs.

## When to Choose Biome

Biome is the better choice if:

- You're starting a new project with no legacy configuration
- You're frustrated with the speed of your current linting setup
- You want a single tool for both linting and formatting
- You're working on a large monorepo where build time matters
- You value simplicity and opinionated defaults over endless configuration options

Biome's trajectory is also worth considering. The project has received significant funding and is actively developed. The roadmap includes plugin support, a bundler, and test runner, which would make it a true all-in-one toolchain.

## The Verdict

The JavaScript ecosystem is moving toward speed and simplicity. Biome represents this shift—it's a modern tool built with modern technology (Rust) that solves the pain points of the previous generation. But ESLint isn't standing still; its flat config system and performance improvements in version 9 show that it's adapting.

For teams making a decision today, consider this: if you can achieve your code quality goals with Biome's built-in rules, the performance gains are too significant to ignore. If you need the deep ecosystem that ESLint provides, stick with it—but consider running a faster formatter alongside.

The ideal future might be a hybrid: Biome for speed-critical operations and ESLint for deep analysis. But as Biome matures, that future may become unnecessary.

**The takeaway**: Don't choose based on hype or fear of missing out. Benchmark both tools on your actual codebase. Measure the linting time, the configuration complexity, and the developer satisfaction. The right choice is the one that your team will actually use—and enjoy using—every day.