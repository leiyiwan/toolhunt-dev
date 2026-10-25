---
title: "Biome vs ESLint and Prettier: Is It Time to Replace Your JavaScript Linting Stack?"
date: 2026-10-25T14:02:22+08:00
draft: false
tags:

---

# Biome vs ESLint and Prettier: Is It Time to Replace Your JavaScript Linting Stack?

A typical React project in 2024 ships with ESLint, Prettier, and somewhere between five and fifteen plugins to keep them from fighting each other. `eslint-config-prettier`, `eslint-plugin-prettier`, `@typescript-eslint/parser`, `@typescript-eslint/eslint-plugin`—the list grows every time a new framework or file type enters the codebase. On a mid-sized monorepo, a full lint pass can take 30 to 90 seconds, and the configuration files alone can run past 200 lines.

Biome enters this picture with a blunt pitch: one binary, written in Rust, that handles both formatting and linting, runs in a fraction of the time, and replaces most of that dependency tree. It's a compelling sales pitch. Whether it holds up depends heavily on what your project actually needs. Here's a practical breakdown.

## What Biome Actually Is

Biome began in 2023 as a fork of Rome Tools, the ambitious but ultimately abandoned all-in-one JavaScript toolchain. The Biome team picked up the codebase, rewrote large portions, and shipped a stable 1.0 release in August 2023. As of early 2025, it's at version 1.9.x with a 2.0 release in development.

The tool combines two jobs that JavaScript developers have traditionally split between ESLint and Prettier:

- **A formatter** with near-parity to Prettier's output (Biome claims over 97% compatibility on Prettier's own test suite)
- **A linter** with roughly 200+ rules covering correctness, suspicious patterns, style, and some accessibility checks

It ships as a single binary distributed via npm, Homebrew, or direct download. There's no Node.js runtime dependency for the core tool, no plugin resolution, and no parser configuration. That architectural difference is where most of Biome's performance advantage comes from.

## The Performance Gap Is Real

Benchmarks published by Biome show formatting and linting large codebases in roughly 1–2% of the time ESLint and Prettier take, depending on project size and rule configuration. Independent tests have produced more modest but still significant numbers—often 10x to 25x faster on real projects.

The reason isn't just Rust. ESLint's performance is dominated by Node.js startup, plugin loading, and the overhead of running each rule as a separate JavaScript function over the AST. Biome compiles rules into a single pass and avoids the plugin resolution layer entirely. On a 5,000-file codebase, that difference turns a 60-second pre-commit hook into a 2-second one.

For CI pipelines running lint on every pull request, this translates directly into cost and developer patience. Teams that previously ran ESLint only on changed files (via `lint-staged` or similar) can often afford to lint everything on every run with Biome.

## Where Biome Wins

**Configuration simplicity.** A `biome.json` file replaces `.eslintrc.js`, `.prettierrc`, `.eslintignore`, `.prettierignore`, and the plugin dependency chain. A typical config is 20–40 lines. There's no equivalent of the `eslint-config-prettier` dance because formatting and linting are designed to coexist.

**Formatting and linting in one pass.** Running `biome check --write` formats and fixes in a single command. With ESLint and Prettier, you typically run Prettier first, then ESLint with `--fix`, and hope the two don't disagree.

**Zero-config defaults that are actually good.** Biome's recommended rule set catches real bugs—unused variables, unreachable code, suspicious `any` usage in TypeScript—without the noise that ESLint's default config produces.

**Monorepo support.** Biome handles nested configs and workspace-relative paths more gracefully than ESLint's cascading config system, which has been a persistent source of confusion.

## Where ESLint Still Has the Edge

**Plugin ecosystem.** This is the big one. ESLint has thousands of plugins, and many are load-bearing for real projects:

- `eslint-plugin-react-hooks` catches rules-of-hooks violations that Biome's React rules don't fully replicate
- `eslint-plugin-jsx-a11y` has far deeper accessibility coverage than Biome's current offering
- Framework-specific plugins for Next.js, Vue, Svelte, and Angular often encode rules that Biome simply doesn't have
- Custom rules written in-house for domain-specific patterns have no Biome equivalent

If your team relies on any of these, migrating to Biome means either losing those checks or running ESLint alongside Biome—which defeats much of the point.

**Type-aware linting.** ESLint's `@typescript-eslint` type-aware rules (like `no-floating-promises` and `no-misused-promises`) use the TypeScript compiler's type information to catch bugs that syntax-only linting misses. Biome's type inference is improving but doesn't yet match this capability. The Biome team has flagged type-aware linting as a long-term goal, not a near-term one.

**Customization depth.** ESLint rules can be written in JavaScript by anyone on the team. Biome rules require writing Rust, and the plugin API for custom rules is still in development. For teams with bespoke linting needs, this is a real constraint.

## Prettier Compatibility: Good, Not Perfect

Biome's formatter aims for Prettier compatibility, and for most code it achieves it. But "most" isn't "all." Edge cases in JSX formatting, complex ternary expressions, and certain comment placements can produce different output. If your team has strong opinions about formatting (or a large existing codebase formatted by Prettier), the migration will produce a one-time diff that can be thousands of lines.

That's not a dealbreaker—you only pay it once—but it does mean the migration isn't a drop-in swap. Plan for a dedicated formatting commit that's excluded from blame.

## A Practical Migration Path

Teams considering Biome don't have to go all-in. A staged approach works well:

1. **Start with the formatter.** Replace Prettier with `biome format` first. This is the lowest-risk change and immediately validates the compatibility claim on your codebase.
2. **Add the linter in parallel.** Run `biome lint` alongside ESLint for a few weeks, comparing output. You'll quickly see which ESLint rules Biome covers and which you'd lose.
3. **Keep ESLint for what Biome can't do.** If you depend on type-aware rules or specific plugins, run ESLint with just those rules and let Biome handle everything else. The performance hit is much smaller than running full ESLint.
4. **Drop ESLint only when you're confident.** For projects without heavy plugin dependencies, full replacement is realistic. For projects with complex React, accessibility, or framework-specific requirements, hybrid setups are the pragmatic answer.

## The Bottom Line

Biome is not a drop-in replacement for every ESLint setup, and the marketing around "replace your entire linting stack" oversells what it can do today. But for a large and growing share of JavaScript and TypeScript projects—especially those without deep plugin dependencies or type-aware linting needs—it's a genuinely better tool. The speed alone changes how teams work: linting on every save, in every CI run, without the usual "I'll just skip the pre-commit hook this once" temptation.

The honest answer to "is it time to replace your stack?" is: it depends on what's in your stack. Audit your ESLint config, count how many plugins you actually depend on, and check whether any of them are doing work Biome can't replicate. If the answer is "not many," Biome is worth a serious trial. If you're deep in type-aware rules and framework plugins, the hybrid approach—Biome for formatting and fast linting, ESLint for the specialized checks—is probably where you'll land. Either way, the monolithic ESLint-plus-Prettier-plus-plugins setup is no longer the only sensible default.