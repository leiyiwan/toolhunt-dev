---
title: "ESLint vs Biome: Which Linter and Formatter Should You Adopt in 2024"
date: 2026-08-28T14:04:36+08:00
draft: false
tags:

---

# ESLint vs Biome: Which Linter and Formatter Should You Adopt in 2024

JavaScript tooling has always been a moving target, but the past 18 months have seen a seismic shift in how developers approach code quality. For nearly a decade, ESLint has been the undisputed champion of JavaScript linting, with Prettier handling formatting. But in 2023, Biome emerged from the ashes of the Rome project, promising to combine both tools into a single, blazing-fast binary written in Rust. By mid-2024, Biome has reached version 1.8, and the question is no longer hypothetical: Is it time to switch, or should you double down on the ESLint ecosystem?

The short answer: It depends on your project size, your team's tolerance for configuration overhead, and whether you need the long tail of custom rules. Let's break down the real differences, performance benchmarks, and migration paths to help you make an informed decision.

## The Current State of Both Tools

ESLint remains the default choice for most JavaScript projects. It's installed over 30 million times per week on npm, and its plugin ecosystem is unmatched. With ESLint 9 released in April 2024, the project introduced a new flat config system (now the default), which simplified configuration but also caused migration headaches for many teams.

Biome, on the other hand, is a direct competitor that combines a linter, formatter, and (as of v1.7) a import sorting tool into one executable. It's written in Rust, which gives it a massive performance advantage over Node.js-based tools. The project reports 100% compatibility with ESLint's core rules and aims to support the most popular plugins over time.

## Performance: The Rust Advantage

Let's talk numbers, because this is where Biome makes its strongest case. In the Biome team's own benchmarks on a large monorepo with ~10,000 files:

- **Biome**: ~200ms to lint and format the entire codebase
- **ESLint + Prettier**: ~8-10 seconds for the same task

That's a 40-50x speed difference. Even in smaller projects, the difference is noticeable. On a typical 500-file codebase, ESLint takes about 1.5-2 seconds to run, while Biome completes in under 100ms.

Why does this matter? In a world of pre-commit hooks and CI pipelines, every second counts. Faster tooling means faster feedback loops, which means developers are more likely to run checks locally rather than discovering issues after pushing to CI. For large monorepos, the difference can save minutes per developer per day, which adds up to hours per week across a team.

The performance gap comes down to architecture. ESLint runs on Node.js, which requires starting a JavaScript runtime, parsing files with a JS-based parser (though it now uses a faster one by default), and executing rules as JavaScript functions. Biome compiles to native machine code and uses parallel processing by default, leveraging all available CPU cores.

## Configuration: Simplicity vs. Flexibility

This is where the two tools diverge philosophically.

### ESLint's Flat Config

ESLint 9's flat config (eslint.config.js) replaced the older .eslintrc format. It's more predictable and easier to reason about, but it still requires understanding the concept of "config objects" and how they merge. A typical modern ESLint setup looks like this:

```javascript
import js from '@eslint/js';
import react from 'eslint-plugin-react';

export default [
  js.configs.recommended,
  {
    files: ['**/*.{js,jsx}'],
    plugins: { react },
    rules: {
      'react/jsx-uses-react': 'error',
      'no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    },
  },
];
```

It's powerful, but there's a learning curve. You also need to install and configure Prettier separately, plus eslint-config-prettier to disable conflicting rules.

### Biome's Minimal Approach

Biome's configuration is driven by a single `biome.json` file. The default setup is intentionally minimal:

```json
{
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  }
}
```

That's it. No plugin installation, no rule conflicts, no separate formatter config. The "recommended" ruleset covers the most common issues, and you can override individual rules as needed. For teams that want reasonable defaults without spending hours configuring tooling, this is a huge win.

The trade-off: Biome's rule set is smaller. While it covers all of ESLint's core rules, it doesn't have the long tail of community plugins. For example, if you rely on `eslint-plugin-import` for import ordering or `eslint-plugin-react-hooks` for React hook rules, you'll need to wait for Biome to implement those (or use workarounds).

## Rule Coverage: Core Parity, Plugin Gap

Biome has achieved 100% coverage of ESLint's core rules, meaning anything you can do with ESLint's built-in rules, you can do with Biome. The recommended rule sets are also well-curated and align with modern best practices.

However, the plugin ecosystem is where ESLint still dominates. As of mid-2024:

| Plugin | ESLint | Biome |
|--------|--------|-------|
| TypeScript (typescript-eslint) | ✅ Full | ✅ Partial (via built-in TS support) |
| React hooks | ✅ Full | ❌ Not yet (planned) |
| Import sorting | ✅ Via plugin | ✅ Built-in (since v1.7) |
| JSX accessibility | ✅ Full | ✅ Partial |
| Custom rules | ✅ Full | ⚠️ Limited (JS-based, but fewer APIs) |

The TypeScript story is particularly interesting. Biome has native TypeScript parsing, so it doesn't need a separate parser like `@typescript-eslint/parser`. This eliminates a whole category of version mismatch issues. However, if you rely on type-aware linting rules (like `no-unsafe-any` or `no-floating-promises` from typescript-eslint), Biome doesn't support those yet because they require type information.

## Migration Path: How Hard Is It Really?

If you're considering switching, the migration path is surprisingly smooth. Biome provides a `biome migrate` command that can convert your existing ESLint and Prettier configurations into a `biome.json` file. It handles the most common rules and formatting options automatically.

For a typical project, the migration process looks like:

1. Install Biome and run `biome migrate`
2. Review the generated `biome.json` and adjust any unsupported rules
3. Remove ESLint and Prettier from your dev dependencies
4. Update your pre-commit hooks and CI scripts
5. Run `biome check .` and fix any remaining issues

Most teams report that 80-90% of their existing ESLint rules have direct Biome equivalents. The remaining 10-20% usually fall into the "nice to have" category—rules that were catching rare edge cases or enforcing team-specific conventions.

The bigger friction point is CI/CD integration. If you have complex GitHub Actions or Jenkins pipelines that reference ESLint and Prettier, you'll need to update those. Also, if you use editor extensions, you'll need to switch to the Biome VS Code extension and disable the ESLint and Prettier extensions to avoid conflicts.

## When to Stick with ESLint

There are still compelling reasons to stay with ESLint, particularly for larger organizations:

- **Custom rules**: If your team has written internal ESLint rules (a common practice at scale), Biome's custom rule API is less mature. You can write JavaScript rules for Biome, but the API is more limited than ESLint's.
- **Plugin depth**: If you depend on niche plugins like `eslint-plugin-security` or `eslint-plugin-jest-dom`, you'll likely find gaps in Biome's coverage.
- **Type-aware linting**: If you're using typescript-eslint's type-checked rules to catch real bugs (like unsafe type assertions), Biome can't replace that yet.
- **Legacy codebases**: If you have thousands of files with existing ESLint disable comments and rule configurations, the migration effort might not be worth the performance gain.

## When to Switch to Biome

On the flip side, Biome makes sense for:

- **New projects**: Starting fresh with Biome means no migration baggage. You get fast tooling from day one.
- **Performance-sensitive teams**: If linting is a bottleneck in your CI pipeline or pre-commit hooks, the speed difference is immediately noticeable.
- **Small to medium codebases**: If you have under 5,000 files and don't use exotic plugins, the rule coverage gap is unlikely to matter.
- **Simplified tooling**: If you're tired of managing ESLint + Prettier + eslint-config-prettier + various plugins, Biome's single-binary approach is refreshing.

## The Verdict: A Pragmatic Approach for 2024

Neither tool is objectively "better" across the board. Here's a practical recommendation:

**For new projects**: Start with Biome. It's faster, simpler, and covers the vast majority of use cases. The tooling ecosystem will only improve over time.

**For existing projects**: Evaluate your rule coverage. Run `biome migrate` in a branch and see how many rules map over. If you're using standard rules and no custom plugins, the migration is low-risk. If you have deep plugin dependencies, stay with ESLint for now but keep an eye on Biome's plugin roadmap.

**For monorepos**: The performance difference becomes critical. If you're spending more than 30 seconds on linting across your workspace, the switch is worth serious consideration.

**For teams with custom rules**: Stick with ESLint until Biome's custom rule API matures. Writing and maintaining custom rules is a significant investment, and you don't want to rewrite them twice.

The broader trend is clear: Rust-based tooling is the future of JavaScript development. We've seen it with SWC, Turbopack, and now Biome. The question isn't whether Biome will become the standard—it's when. For now, the pragmatic choice is to evaluate your specific needs and migrate when the benefits outweigh the costs.

One final note: Don't forget that you can use both tools in parallel during a transition period. Keep ESLint running in CI while you get used to Biome locally. Once you're confident in the parity, make the full switch. The tooling is mature enough that this isn't a risky experiment—it's a measured upgrade.